"""
Session Store
=============
A single, file-backed store for "form sessions". A form session is one
citizen's journey through one government form — which documents they've
sent, what data has been extracted or typed in, and what's still missing.

Both the WhatsApp bot and the web dashboard's API routes read and write
through this module and nothing else, so a document sent on WhatsApp shows
up on the dashboard (and a field typed on the dashboard shows up in the
next WhatsApp reply) without any separate syncing step — there's only one
copy of the data.

Storage is a single JSON file (backend/data/sessions.json) guarded by a
lock. That's intentionally simple: CSC-scale usage (tens of concurrent
operators) doesn't need a database server, and it keeps the whole project
runnable with `python app.py` and nothing else installed. Swapping this
module for a real database later would not require touching app.py,
whatsapp_bot.py, or the dashboard — they only call the functions below.
"""

import json
import os
import threading
import uuid
from datetime import datetime

_LOCK = threading.RLock()
_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
_STORE_PATH = os.path.join(_DATA_DIR, "sessions.json")


def _ensure_store():
    os.makedirs(_DATA_DIR, exist_ok=True)
    if not os.path.exists(_STORE_PATH):
        with open(_STORE_PATH, "w") as f:
            json.dump({}, f)


def _load():
    _ensure_store()
    with open(_STORE_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def _save(data):
    tmp_path = _STORE_PATH + ".tmp"
    with open(tmp_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp_path, _STORE_PATH)


def new_web_session_id():
    return "web:" + uuid.uuid4().hex[:8]


def whatsapp_session_id(phone):
    """Normalise a WhatsApp phone number (e.g. 'whatsapp:+91987...') to a session id."""
    clean = phone.replace("whatsapp:", "").strip()
    return f"wa:{clean}"


def get_session(session_id):
    with _LOCK:
        return _load().get(session_id)


def list_sessions():
    with _LOCK:
        data = _load()
        sessions = list(data.values())
        sessions.sort(key=lambda s: s.get("updated_at", ""), reverse=True)
        return sessions


def create_session(session_id, channel, phone=None):
    with _LOCK:
        data = _load()
        now = datetime.now().isoformat()
        session = {
            "id": session_id,
            "channel": channel,           # 'whatsapp' or 'web'
            "phone": phone,
            "form_id": None,
            "state": "SELECT_FORM",       # SELECT_FORM | COLLECT_DOCS | COLLECT_FIELDS | COMPLETE
            "documents": {},              # doc_type -> {filename, received_at, extracted}
            "fields": {},                 # field_key -> value
            "field_sources": {},          # field_key -> 'document' | 'manual'
            "pending_field": None,
            "history": [],                # [{role, text, ts}] — for the dashboard transcript
            "created_at": now,
            "updated_at": now,
        }
        data[session_id] = session
        _save(data)
        return session


def get_or_create_session(session_id, channel, phone=None):
    session = get_session(session_id)
    if session:
        return session
    return create_session(session_id, channel, phone=phone)


def save_session(session):
    with _LOCK:
        data = _load()
        session["updated_at"] = datetime.now().isoformat()
        data[session["id"]] = session
        _save(data)
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
    with _LOCK:
        data = _load()
        history = session.get("history", [])
        channel = session.get("channel")
        phone = session.get("phone")
        now = datetime.now().isoformat()
        data[session_id] = {
            "id": session_id,
            "channel": channel,
            "phone": phone,
            "form_id": None,
            "state": "SELECT_FORM",
            "documents": {},
            "fields": {},
            "field_sources": {},
            "pending_field": None,
            "history": history,
            "created_at": session.get("created_at", now),
            "updated_at": now,
        }
        _save(data)
        return data[session_id]


def delete_session(session_id):
    with _LOCK:
        data = _load()
        if session_id in data:
            del data[session_id]
            _save(data)
            return True
        return False
