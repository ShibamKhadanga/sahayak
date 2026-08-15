"""
Form Engine
===========
The state machine that drives a form session from "pick a form" through
"upload documents" and "fill remaining fields" to "complete". This module
has no knowledge of WhatsApp or HTTP — whatsapp_bot.py and the dashboard's
routes in app.py both call these same functions, which is what keeps the
two channels behaved identically and in sync (they're driven by the same
code against the same session_store).
"""

from datetime import datetime

import forms_catalog
from ocr_processor import extract_smart_data, extract_text_from_bytes
import session_store


def start_form(session, form_id):
    form = forms_catalog.get_form(form_id)
    if not form:
        return False
    session["form_id"] = form_id
    session["state"] = "COLLECT_DOCS"
    session["documents"] = {}
    session["fields"] = {}
    session["field_sources"] = {}
    session_store.save_session(session)
    return True


def next_missing_document(session):
    form = forms_catalog.get_form(session.get("form_id"))
    if not form:
        return None
    for doc_type in form["documents"]:
        if doc_type not in session.get("documents", {}):
            return doc_type
    return None


def next_missing_field(session):
    form = forms_catalog.get_form(session.get("form_id"))
    if not form:
        return None
    for field_key in form["fields"]:
        label, _source, required = forms_catalog.field_meta(field_key)
        value = session.get("fields", {}).get(field_key)
        if required and not value:
            return field_key
    return None


def apply_document_bytes(session, doc_type, filename, file_bytes):
    """
    Run OCR on an uploaded document's raw bytes, merge any recognised
    fields into the session, and record the document as received.
    Returns the dict of newly-extracted field values.
    """
    text = extract_text_from_bytes(filename, file_bytes)
    extracted = extract_smart_data(text) if text else {}

    session.setdefault("documents", {})[doc_type] = {
        "filename": filename,
        "received_at": datetime.now().isoformat(),
        "extracted": extracted,
    }

    form = forms_catalog.get_form(session.get("form_id"))
    newly_filled = {}
    if form:
        # Only auto-fill fields this form actually asks for, and don't
        # overwrite a value the operator/citizen already typed manually.
        source_to_field = {}
        for field_key in form["fields"]:
            _label, source, _required = forms_catalog.field_meta(field_key)
            if source:
                source_to_field[source] = field_key
        for source_key, value in extracted.items():
            field_key = source_to_field.get(source_key)
            if field_key and value and not session.get("fields", {}).get(field_key):
                session.setdefault("fields", {})[field_key] = value
                session.setdefault("field_sources", {})[field_key] = "document"
                newly_filled[field_key] = value

    _advance_state(session)
    session_store.save_session(session)
    return newly_filled


def apply_field_answer(session, field_key, value):
    session.setdefault("fields", {})[field_key] = value
    session.setdefault("field_sources", {})[field_key] = "manual"
    _advance_state(session)
    session_store.save_session(session)


def _advance_state(session):
    if next_missing_document(session):
        session["state"] = "COLLECT_DOCS"
    elif next_missing_field(session):
        session["state"] = "COLLECT_FIELDS"
        session["pending_field"] = next_missing_field(session)
    else:
        session["state"] = "COMPLETE"
        session["pending_field"] = None


def progress(session):
    form = forms_catalog.get_form(session.get("form_id"))
    if not form:
        return {"docs_done": 0, "docs_total": 0, "fields_done": 0, "fields_total": 0, "percent": 0}

    docs_total = len(form["documents"])
    docs_done = len(session.get("documents", {}))

    field_keys = form["fields"]
    fields_total = len(field_keys)
    fields_done = sum(1 for k in field_keys if session.get("fields", {}).get(k))

    total_steps = docs_total + fields_total
    done_steps = docs_done + fields_done
    percent = round((done_steps / total_steps) * 100) if total_steps else 0

    return {
        "docs_done": docs_done,
        "docs_total": docs_total,
        "fields_done": fields_done,
        "fields_total": fields_total,
        "percent": percent,
    }


def session_summary(session):
    """A dashboard/WhatsApp-friendly view of the session, form details included."""
    form = forms_catalog.get_form(session.get("form_id"))
    field_rows = []
    if form:
        for field_key in form["fields"]:
            label, _source, required = forms_catalog.field_meta(field_key)
            field_rows.append({
                "key": field_key,
                "label": label,
                "required": required,
                "value": session.get("fields", {}).get(field_key, ""),
                "source": session.get("field_sources", {}).get(field_key),
            })
    doc_rows = []
    if form:
        for doc_type in form["documents"]:
            doc = session.get("documents", {}).get(doc_type)
            doc_rows.append({
                "type": doc_type,
                "label": forms_catalog.document_label(doc_type),
                "received": bool(doc),
                "filename": doc.get("filename") if doc else None,
            })
    return {
        **session,
        "form_name": form["name"] if form else None,
        "field_rows": field_rows,
        "doc_rows": doc_rows,
        "progress": progress(session),
    }
