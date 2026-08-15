"""
Session Store (PostgreSQL)
==========================
A PostgreSQL-backed store for "form sessions". A form session is one
citizen's journey through one government form — which documents they've
sent, what data has been extracted or typed in, and what's still missing.

Both the WhatsApp bot and the web dashboard's API routes read and write
through this module and nothing else, so a document sent on WhatsApp shows
up on the dashboard (and a field typed on the dashboard shows up in the
next WhatsApp reply) without any separate syncing step.

All function signatures are preserved from the original JSON-file version
so that app.py, whatsapp_bot.py, and form_engine.py work unchanged.
"""

import json
import uuid
from datetime import datetime

import database as db


def new_web_session_id():
    return "web:" + uuid.uuid4().hex[:8]


def whatsapp_session_id(phone):
    """Normalise a WhatsApp phone number (e.g. 'whatsapp:+91987...') to a session id."""
    clean = phone.replace("whatsapp:", "").strip()
    return f"wa:{clean}"


def _row_to_session(row):
    """Convert a DB row (RealDictRow) to a session dict matching the old format."""
    if not row:
        return None
    return {
        "id": row["id"],
        "channel": row["channel"],
        "phone": row.get("phone"),
        "form_id": row.get("form_id"),
        "state": row["state"],
        "documents": row.get("documents") or {},
        "fields": row.get("fields") or {},
        "field_sources": row.get("field_sources") or {},
        "pending_field": row.get("pending_field"),
        "history": row.get("history") or [],
        "created_at": row["created_at"].isoformat() if row.get("created_at") else None,
        "updated_at": row["updated_at"].isoformat() if row.get("updated_at") else None,
    }


def get_session(session_id):
    row = db.fetch_one("SELECT * FROM sessions WHERE id = %s", (session_id,))
    return _row_to_session(row)


def list_sessions():
    rows = db.fetch_all("SELECT * FROM sessions ORDER BY updated_at DESC")
    return [_row_to_session(r) for r in rows]


def create_session(session_id, channel, phone=None):
    now = datetime.now()
    db.execute(
        """INSERT INTO sessions (id, channel, phone, form_id, state, documents, fields, field_sources, pending_field, history, created_at, updated_at)
           VALUES (%s, %s, %s, NULL, 'SELECT_FORM', '{}', '{}', '{}', NULL, '[]', %s, %s)
           ON CONFLICT (id) DO NOTHING""",
        (session_id, channel, phone, now, now),
    )
    return get_session(session_id)


def get_or_create_session(session_id, channel, phone=None):
    session = get_session(session_id)
    if session:
        return session
    return create_session(session_id, channel, phone=phone)


def save_session(session):
    now = datetime.now()
    session["updated_at"] = now.isoformat()
    db.execute(
        """UPDATE sessions SET
            channel = %s,
            phone = %s,
            form_id = %s,
            state = %s,
            documents = %s,
            fields = %s,
            field_sources = %s,
            pending_field = %s,
            history = %s,
            updated_at = %s
           WHERE id = %s""",
        (
            session["channel"],
            session.get("phone"),
            session.get("form_id"),
            session["state"],
            json.dumps(session.get("documents", {})),
            json.dumps(session.get("fields", {})),
            json.dumps(session.get("field_sources", {})),
            session.get("pending_field"),
            json.dumps(session.get("history", [])),
            now,
            session["id"],
        ),
    )
    return session


def add_history(session, role, text):
    """role: 'user' or 'bot'. Mutates and persists the session."""
    session.setdefault("history", []).append({
        "role": role,
        "text": text,
        "ts": datetime.now().isoformat(),
    })
    # Keep the transcript bounded
    session["history"] = session["history"][-100:]
    return save_session(session)


def reset_session(session_id):
    session = get_session(session_id)
    if not session:
        return None
    now = datetime.now()
    db.execute(
        """UPDATE sessions SET
            form_id = NULL,
            state = 'SELECT_FORM',
            documents = '{}',
            fields = '{}',
            field_sources = '{}',
            pending_field = NULL,
            updated_at = %s
           WHERE id = %s""",
        (now, session_id),
    )
    return get_session(session_id)


def delete_session(session_id):
    session = get_session(session_id)
    if not session:
        return False
    db.execute("DELETE FROM sessions WHERE id = %s", (session_id,))
    return True
