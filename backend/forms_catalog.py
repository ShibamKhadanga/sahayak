"""
Forms Catalog (PostgreSQL)
==========================
The single source of truth for "which forms does Sahayak handle, what
documents does each one need, and what fields does it collect".

This module reads from the PostgreSQL database (tables: forms,
document_types, field_library) instead of hardcoded Python dicts.
The default data is seeded by database.init_db() on first run.

All function signatures are preserved from the original version so that
form_engine.py, whatsapp_bot.py, and app.py work unchanged.
"""

import json
import database as db


# ---------------------------------------------------------------------------
# Read operations (same signatures as the original)
# ---------------------------------------------------------------------------

def get_form(form_id):
    """Returns a form dict or None."""
    row = db.fetch_one("SELECT * FROM forms WHERE id = %s", (form_id,))
    if not row:
        return None
    return _row_to_form(row)


def list_forms():
    """Returns all forms as a list of dicts."""
    rows = db.fetch_all("SELECT * FROM forms ORDER BY category, name")
    return [_row_to_form(r) for r in rows]


def field_meta(field_key):
    """Returns (label, source_key, required) for a field key."""
    row = db.fetch_one("SELECT * FROM field_library WHERE field_key = %s", (field_key,))
    if row:
        return (row["label"], row.get("source_key"), row.get("required", False))
    # Fallback for unknown fields
    return (field_key.replace("_", " ").title(), None, False)


def document_label(doc_type):
    """Returns the human-readable label for a document type."""
    row = db.fetch_one("SELECT label FROM document_types WHERE type_key = %s", (doc_type,))
    if row:
        return row["label"]
    return doc_type.replace("_", " ").title()


# ---------------------------------------------------------------------------
# CRUD operations (new — used by the admin panel)
# ---------------------------------------------------------------------------

def add_form(form_id, name, category, documents, fields):
    """Add a new form to the catalog."""
    db.execute(
        """INSERT INTO forms (id, name, category, documents, fields)
           VALUES (%s, %s, %s, %s, %s)""",
        (form_id, name, category, json.dumps(documents), json.dumps(fields)),
    )
    return get_form(form_id)


def update_form(form_id, name, category, documents, fields):
    """Update an existing form."""
    db.execute(
        """UPDATE forms SET name = %s, category = %s, documents = %s, fields = %s, updated_at = NOW()
           WHERE id = %s""",
        (name, category, json.dumps(documents), json.dumps(fields), form_id),
    )
    return get_form(form_id)


def delete_form(form_id):
    """Delete a form from the catalog."""
    db.execute("DELETE FROM forms WHERE id = %s", (form_id,))
    return True


# Document types CRUD
def list_document_types():
    rows = db.fetch_all("SELECT * FROM document_types ORDER BY type_key")
    return {r["type_key"]: r["label"] for r in rows}


def upsert_document_type(type_key, label):
    db.execute(
        """INSERT INTO document_types (type_key, label) VALUES (%s, %s)
           ON CONFLICT (type_key) DO UPDATE SET label = EXCLUDED.label""",
        (type_key, label),
    )


def delete_document_type(type_key):
    db.execute("DELETE FROM document_types WHERE type_key = %s", (type_key,))


# Field library CRUD
def list_field_library():
    rows = db.fetch_all("SELECT * FROM field_library ORDER BY field_key")
    return rows


def upsert_field(field_key, label, source_key=None, required=False):
    db.execute(
        """INSERT INTO field_library (field_key, label, source_key, required) VALUES (%s, %s, %s, %s)
           ON CONFLICT (field_key) DO UPDATE SET label = EXCLUDED.label, source_key = EXCLUDED.source_key, required = EXCLUDED.required""",
        (field_key, label, source_key, required),
    )


def delete_field(field_key):
    db.execute("DELETE FROM field_library WHERE field_key = %s", (field_key,))


# ---------------------------------------------------------------------------
# Internal
# ---------------------------------------------------------------------------

def _row_to_form(row):
    """Convert a DB row to the form dict format expected by form_engine."""
    return {
        "id": row["id"],
        "name": row["name"],
        "category": row["category"],
        "documents": row["documents"] if isinstance(row["documents"], list) else json.loads(row["documents"]),
        "fields": row["fields"] if isinstance(row["fields"], list) else json.loads(row["fields"]),
    }
