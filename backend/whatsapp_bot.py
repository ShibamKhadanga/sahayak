"""
WhatsApp Bot
============
Turns an inbound WhatsApp message (text and/or a document/photo) into a
reply, by driving the exact same form_engine + session_store used by the
web dashboard's API routes. There is no separate "WhatsApp database" —
handle_incoming() reads and writes the one shared session, which is the
whole mechanism behind "the WhatsApp chat and the software stay in sync".

This module is transport-agnostic: app.py's /whatsapp/webhook route calls
it with data decoded from Twilio's webhook payload, and the dashboard's
built-in simulator (/api/whatsapp/simulate) calls it directly with a
browser-uploaded file — both go through handle_incoming().
"""

import re

import forms_catalog
import form_engine
import session_store

GREETING_WORDS = {"hi", "hello", "hey", "start", "namaste", "menu"}
RESTART_WORDS = {"menu", "restart", "reset"}
STATUS_WORDS = {"status", "progress"}


def _forms_menu_text():
    lines = ["🙏 Welcome to *Sahayak*! Which form do you need help with today?", ""]
    for i, form in enumerate(forms_catalog.list_forms(), start=1):
        lines.append(f"{i}. {form['name']}")
    lines.append("")
    lines.append("Reply with the *number* of the form you want.")
    return "\n".join(lines)


def _documents_needed_text(form):
    lines = [f"Great, let's fill your *{form['name']}*.", "", "Please send these documents one at a time (as a photo or PDF):"]
    for i, doc_type in enumerate(form["documents"], start=1):
        lines.append(f"{i}. {forms_catalog.document_label(doc_type)}")
    lines.append("")
    lines.append("Send the first one whenever you're ready 📎")
    return "\n".join(lines)


def _ask_for_document_text(doc_type):
    return f"📎 Please send: *{forms_catalog.document_label(doc_type)}*"


def _ask_for_field_text(field_key):
    label, _source, _required = forms_catalog.field_meta(field_key)
    return f"✍️ What is the *{label}*?"


def _status_text(session):
    p = form_engine.progress(session)
    form = forms_catalog.get_form(session.get("form_id"))
    if not form:
        return "You haven't started a form yet. Type *menu* to see the list of forms."
    return (
        f"*{form['name']}*\n"
        f"Documents: {p['docs_done']}/{p['docs_total']}\n"
        f"Fields filled: {p['fields_done']}/{p['fields_total']}\n"
        f"Overall: {p['percent']}% complete"
    )


def _completion_text(session):
    summary = form_engine.session_summary(session)
    lines = [f"✅ All done! Here's your *{summary['form_name']}* summary:", ""]
    for row in summary["field_rows"]:
        if row["value"]:
            lines.append(f"• {row['label']}: {row['value']}")
    lines.append("")
    lines.append("An operator can review and submit this from the Sahayak dashboard.")
    lines.append("Type *menu* to fill another form.")
    return "\n".join(lines)


def handle_incoming(session_id, channel, phone, text, files):
    """
    files: list of (filename, bytes) tuples — empty list if no attachment.
    Returns the reply text (string). Mutates + persists the session.
    """
    session = session_store.get_or_create_session(session_id, channel, phone=phone)
    text = (text or "").strip()
    text_lower = text.lower()

    if text:
        session_store.add_history(session, "user", text)
    elif files:
        session_store.add_history(session, "user", f"[sent {len(files)} file(s)]")

    if text_lower in RESTART_WORDS:
        session = session_store.reset_session(session_id)
        reply = _forms_menu_text()
        session_store.add_history(session, "bot", reply)
        return reply

    if text_lower in STATUS_WORDS:
        reply = _status_text(session)
        session_store.add_history(session, "bot", reply)
        return reply

    state = session.get("state", "SELECT_FORM")

    # ── Picking a form ──────────────────────────────────────────────
    if state == "SELECT_FORM" or not session.get("form_id"):
        if text_lower in GREETING_WORDS or not text:
            reply = _forms_menu_text()
            session_store.add_history(session, "bot", reply)
            return reply

        m = re.match(r"^\s*(\d+)\s*$", text)
        forms = forms_catalog.list_forms()
        if m and 1 <= int(m.group(1)) <= len(forms):
            form = forms[int(m.group(1)) - 1]
            form_engine.start_form(session, form["id"])
            reply = _documents_needed_text(form)
        else:
            reply = "Sorry, I didn't catch that.\n\n" + _forms_menu_text()
        session_store.add_history(session, "bot", reply)
        return reply

    form = forms_catalog.get_form(session["form_id"])

    # ── Collecting documents ────────────────────────────────────────
    if state == "COLLECT_DOCS":
        if files:
            doc_type = form_engine.next_missing_document(session)
            if doc_type is None:
                # Shouldn't happen, but guard anyway.
                doc_type = form["documents"][-1]
            filename, file_bytes = files[0]
            newly_filled = form_engine.apply_document_bytes(session, doc_type, filename, file_bytes)

            lines = [f"✅ Received: {forms_catalog.document_label(doc_type)}"]
            if newly_filled:
                lines.append("Auto-filled from this document:")
                for key, value in newly_filled.items():
                    label, _s, _r = forms_catalog.field_meta(key)
                    lines.append(f"  • {label}: {value}")
            lines.append("")

            next_doc = form_engine.next_missing_document(session)
            if next_doc:
                lines.append(_ask_for_document_text(next_doc))
            else:
                next_field = form_engine.next_missing_field(session)
                if next_field:
                    lines.append("All documents received! Just a few more details:")
                    lines.append(_ask_for_field_text(next_field))
                else:
                    lines.append(_completion_text(session))
            reply = "\n".join(lines)
        else:
            next_doc = form_engine.next_missing_document(session)
            reply = "Please send that as a photo or PDF 📎\n\n" + _ask_for_document_text(next_doc)
        session_store.add_history(session, "bot", reply)
        return reply

    # ── Collecting remaining fields ─────────────────────────────────
    if state == "COLLECT_FIELDS":
        pending_field = session.get("pending_field") or form_engine.next_missing_field(session)
        if pending_field and text:
            form_engine.apply_field_answer(session, pending_field, text)
            next_field = form_engine.next_missing_field(session)
            if next_field:
                reply = _ask_for_field_text(next_field)
            else:
                reply = _completion_text(session)
        else:
            reply = _ask_for_field_text(pending_field) if pending_field else _completion_text(session)
        session_store.add_history(session, "bot", reply)
        return reply

    # ── Complete ─────────────────────────────────────────────────────
    reply = _completion_text(session) + "\n\nType *menu* to start another form."
    session_store.add_history(session, "bot", reply)
    return reply
