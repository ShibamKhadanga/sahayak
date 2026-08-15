"""
Database Module
===============
Central PostgreSQL connection manager for Sahayak. Creates a connection
pool on import and provides helper functions for running queries.

Tables are created automatically on first call to init_db().
"""

import os
import json
import logging
from contextlib import contextmanager

import psycopg2
import psycopg2.pool
import psycopg2.extras

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Connection pool
# ---------------------------------------------------------------------------
_pool = None


def _get_pool():
    global _pool
    if _pool is None:
        database_url = os.environ.get(
            "DATABASE_URL",
            "postgresql://postgres:postgres@localhost:5432/sahayak",
        )
        try:
            _pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=10,
                dsn=database_url,
            )
            logger.info("PostgreSQL connection pool created")
        except psycopg2.OperationalError as e:
            logger.error(f"Could not connect to PostgreSQL: {e}")
            raise
    return _pool


@contextmanager
def get_conn():
    """Context manager that checks out a connection from the pool and
    returns it when done. Auto-commits on success, rolls back on error."""
    pool = _get_pool()
    conn = pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        pool.putconn(conn)


def execute(sql, params=None):
    """Run a query that doesn't return rows (INSERT/UPDATE/DELETE)."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)


def fetch_one(sql, params=None):
    """Run a query and return a single row as a dict, or None."""
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            row = cur.fetchone()
            return dict(row) if row else None


def fetch_all(sql, params=None):
    """Run a query and return all rows as a list of dicts."""
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            return [dict(r) for r in cur.fetchall()]


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------
_SCHEMA_SQL = """
-- Document type labels
CREATE TABLE IF NOT EXISTS document_types (
    type_key    VARCHAR(64) PRIMARY KEY,
    label       VARCHAR(256) NOT NULL
);

-- Field definitions
CREATE TABLE IF NOT EXISTS field_library (
    field_key   VARCHAR(64) PRIMARY KEY,
    label       VARCHAR(256) NOT NULL,
    source_key  VARCHAR(64),
    required    BOOLEAN DEFAULT FALSE
);

-- Forms catalog
CREATE TABLE IF NOT EXISTS forms (
    id          VARCHAR(64) PRIMARY KEY,
    name        VARCHAR(256) NOT NULL,
    category    VARCHAR(128) NOT NULL,
    documents   JSONB NOT NULL DEFAULT '[]',
    fields      JSONB NOT NULL DEFAULT '[]',
    created_at  TIMESTAMP DEFAULT NOW(),
    updated_at  TIMESTAMP DEFAULT NOW()
);

-- Sessions
CREATE TABLE IF NOT EXISTS sessions (
    id              VARCHAR(128) PRIMARY KEY,
    channel         VARCHAR(16) NOT NULL,
    phone           VARCHAR(32),
    form_id         VARCHAR(64),
    state           VARCHAR(32) NOT NULL DEFAULT 'SELECT_FORM',
    documents       JSONB NOT NULL DEFAULT '{}',
    fields          JSONB NOT NULL DEFAULT '{}',
    field_sources   JSONB NOT NULL DEFAULT '{}',
    pending_field   VARCHAR(64),
    history         JSONB NOT NULL DEFAULT '[]',
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
"""


def init_db():
    """Create all tables if they don't exist, then seed default data."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(_SCHEMA_SQL)
    logger.info("Database schema ensured")
    _seed_defaults()


# ---------------------------------------------------------------------------
# Seed default data (runs only when tables are empty)
# ---------------------------------------------------------------------------

_DEFAULT_DOCUMENT_TYPES = {
    "aadhaar": "Aadhaar Card",
    "pan": "PAN Card",
    "photo": "Passport-size photo",
    "address_proof": "Address proof (Aadhaar / electricity bill / rent agreement)",
    "bank_passbook": "Bank passbook (first page)",
    "income_proof": "Income proof / salary slip",
    "age_proof": "Age proof (Aadhaar / birth certificate / 10th marksheet)",
    "caste_proof": "Caste certificate, if already issued (or a self-declaration)",
    "hospital_discharge": "Hospital discharge slip or birth affidavit",
    "parent_id_proof": "Parent's ID proof (Aadhaar)",
    "marriage_proof": "Marriage certificate / affidavit",
    "death_proof": "Death certificate / hospital report",
    "property_docs": "Sale deed / property tax receipt",
    "disability_proof": "Disability certificate from medical board",
    "education_proof": "10th/12th marksheet / enrollment certificate",
    "passport_photo": "Recent passport-size photograph (white background)",
}

_DEFAULT_FIELD_LIBRARY = {
    "name":            ("Full name",                    "name",           True),
    "father_name":     ("Father's name",                "father_name",    True),
    "mother_name":     ("Mother's name",                "mother_name",    False),
    "spouse_name":     ("Spouse's name",                "spouse_name",    False),
    "dob":             ("Date of birth (DD/MM/YYYY)",   "dob",            True),
    "age":             ("Age",                          "age",            False),
    "gender":          ("Gender",                       "gender",         True),
    "address":         ("Address",                      "address",        True),
    "mobile":          ("Mobile number",                "mobile",         True),
    "email":           ("Email address",                "email",          False),
    "aadhar":          ("Aadhaar number",               "aadhar",         True),
    "pan":             ("PAN number",                   "pan",            False),
    "account_number":  ("Bank account number",          "account_number", True),
    "ifsc":            ("Bank IFSC code",               "ifsc",           True),
    "bank_name":       ("Bank name",                    "bank_name",      False),
    "pincode":         ("PIN code",                     "pincode",        False),
    "state":           ("State",                        "state",          True),
    "district":        ("District",                     "district",       False),
    "caste":           ("Caste / category",             "caste",          True),
    "income":          ("Annual family income (Rs.)",   "income",         True),
    "occupation":      ("Occupation",                   "occupation",     False),
    "family_members":  ("Number of family members",     None,             False),
    "nationality":     ("Nationality",                  "nationality",    False),
    "place_of_birth":  ("Place of birth",               "place_of_birth", False),
    "religion":        ("Religion",                     None,             False),
    "education":       ("Education qualification",      None,             False),
    "blood_group":     ("Blood group",                  None,             False),
    "disability_type": ("Type of disability",           None,             False),
    "disability_pct":  ("Disability percentage",        None,             False),
    "marriage_date":   ("Date of marriage",             None,             False),
    "death_date":      ("Date of death",                None,             False),
    "property_type":   ("Property type",                None,             False),
    "property_area":   ("Property area (sq. ft.)",      None,             False),
    "vehicle_type":    ("Vehicle type (2W/4W/other)",   None,             False),
    "vehicle_make":    ("Vehicle make & model",         None,             False),
    "course_name":     ("Course / programme name",      None,             False),
    "institution":     ("Institution / college name",   None,             False),
}

_DEFAULT_FORMS = [
    # ── Existing 10 forms ──
    {"id": "aadhaar_update",      "name": "Aadhaar Card — Update",              "category": "Identity",             "documents": ["aadhaar", "address_proof"],                        "fields": ["name", "dob", "gender", "address", "mobile", "aadhar"]},
    {"id": "pan_card",            "name": "PAN Card — New Application",         "category": "Identity",             "documents": ["aadhaar", "photo"],                               "fields": ["name", "father_name", "dob", "gender", "address", "mobile", "email"]},
    {"id": "driving_license",     "name": "Learner's / Driving License",        "category": "Transport",            "documents": ["aadhaar", "address_proof", "photo"],              "fields": ["name", "dob", "gender", "address", "mobile"]},
    {"id": "income_certificate",  "name": "Income Certificate",                 "category": "Revenue",              "documents": ["aadhaar", "income_proof"],                        "fields": ["name", "father_name", "address", "income", "occupation", "district", "state"]},
    {"id": "ration_card",         "name": "Ration Card — New Application",      "category": "Food & Civil Supplies","documents": ["aadhaar", "address_proof", "income_proof"],       "fields": ["name", "father_name", "address", "income", "family_members", "caste"]},
    {"id": "old_age_pension",     "name": "Old Age Pension",                    "category": "Social Welfare",       "documents": ["aadhaar", "age_proof", "bank_passbook"],          "fields": ["name", "dob", "age", "gender", "address", "account_number", "ifsc", "bank_name", "income"]},
    {"id": "voter_id",            "name": "Voter ID Registration",              "category": "Identity",             "documents": ["aadhaar", "address_proof", "photo"],              "fields": ["name", "father_name", "dob", "gender", "address"]},
    {"id": "birth_certificate",   "name": "Birth Certificate",                  "category": "Civil Registration",   "documents": ["hospital_discharge", "parent_id_proof"],          "fields": ["name", "father_name", "mother_name", "dob", "address", "district", "state"]},
    {"id": "bank_account_opening","name": "Bank Account Opening",               "category": "Banking",              "documents": ["aadhaar", "pan", "photo"],                        "fields": ["name", "father_name", "dob", "address", "mobile", "email", "pan", "occupation"]},
    {"id": "caste_certificate",   "name": "Caste Certificate",                  "category": "Revenue",              "documents": ["aadhaar", "address_proof", "caste_proof"],        "fields": ["name", "father_name", "address", "caste", "district", "state"]},
    # ── New 10 forms ──
    {"id": "passport_new",        "name": "Passport — New Application",         "category": "Identity",             "documents": ["aadhaar", "pan", "passport_photo", "address_proof"],"fields": ["name", "father_name", "mother_name", "dob", "gender", "address", "mobile", "email", "nationality", "place_of_birth"]},
    {"id": "passport_renewal",    "name": "Passport — Renewal",                 "category": "Identity",             "documents": ["aadhaar", "passport_photo", "address_proof"],     "fields": ["name", "dob", "gender", "address", "mobile", "email"]},
    {"id": "domicile_certificate","name": "Domicile Certificate",               "category": "Revenue",              "documents": ["aadhaar", "address_proof"],                       "fields": ["name", "father_name", "dob", "address", "district", "state", "pincode"]},
    {"id": "marriage_certificate","name": "Marriage Certificate",               "category": "Civil Registration",   "documents": ["aadhaar", "marriage_proof", "photo"],             "fields": ["name", "spouse_name", "dob", "marriage_date", "address", "district", "state"]},
    {"id": "death_certificate",   "name": "Death Certificate",                  "category": "Civil Registration",   "documents": ["death_proof", "parent_id_proof"],                 "fields": ["name", "death_date", "dob", "gender", "address", "district", "state"]},
    {"id": "property_registration","name": "Property Registration",             "category": "Revenue",              "documents": ["aadhaar", "property_docs", "address_proof"],      "fields": ["name", "father_name", "address", "property_type", "property_area", "district", "state"]},
    {"id": "vehicle_registration","name": "Vehicle Registration (RC)",           "category": "Transport",            "documents": ["aadhaar", "address_proof", "photo"],              "fields": ["name", "father_name", "address", "mobile", "vehicle_type", "vehicle_make"]},
    {"id": "disability_certificate","name": "Disability Certificate",           "category": "Social Welfare",       "documents": ["aadhaar", "disability_proof", "photo"],           "fields": ["name", "dob", "gender", "address", "disability_type", "disability_pct", "mobile"]},
    {"id": "widow_pension",       "name": "Widow Pension",                      "category": "Social Welfare",       "documents": ["aadhaar", "death_proof", "bank_passbook"],        "fields": ["name", "dob", "gender", "address", "account_number", "ifsc", "bank_name", "income"]},
    {"id": "scholarship",         "name": "Scholarship Application",            "category": "Education",            "documents": ["aadhaar", "income_proof", "education_proof"],     "fields": ["name", "father_name", "dob", "address", "income", "caste", "course_name", "institution"]},
]


def _seed_defaults():
    """Insert default document types, fields, and forms if the tables are empty."""

    # Seed document types
    count = fetch_one("SELECT COUNT(*) AS c FROM document_types")
    if count and count["c"] == 0:
        with get_conn() as conn:
            with conn.cursor() as cur:
                for type_key, label in _DEFAULT_DOCUMENT_TYPES.items():
                    cur.execute(
                        "INSERT INTO document_types (type_key, label) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                        (type_key, label),
                    )
        logger.info(f"Seeded {len(_DEFAULT_DOCUMENT_TYPES)} document types")

    # Seed field library
    count = fetch_one("SELECT COUNT(*) AS c FROM field_library")
    if count and count["c"] == 0:
        with get_conn() as conn:
            with conn.cursor() as cur:
                for field_key, (label, source_key, required) in _DEFAULT_FIELD_LIBRARY.items():
                    cur.execute(
                        "INSERT INTO field_library (field_key, label, source_key, required) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                        (field_key, label, source_key, required),
                    )
        logger.info(f"Seeded {len(_DEFAULT_FIELD_LIBRARY)} field definitions")

    # Seed forms
    count = fetch_one("SELECT COUNT(*) AS c FROM forms")
    if count and count["c"] == 0:
        with get_conn() as conn:
            with conn.cursor() as cur:
                for form in _DEFAULT_FORMS:
                    cur.execute(
                        """INSERT INTO forms (id, name, category, documents, fields)
                           VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING""",
                        (form["id"], form["name"], form["category"],
                         json.dumps(form["documents"]), json.dumps(form["fields"])),
                    )
        logger.info(f"Seeded {len(_DEFAULT_FORMS)} forms")
