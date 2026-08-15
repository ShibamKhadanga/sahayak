"""
Forms Catalog
=============
The single source of truth for "which forms does Sahayak handle, what
documents does each one need, and what fields does it collect".

Both the web dashboard and the WhatsApp bot read this catalog through
form_engine.py, so adding a new form here automatically makes it available
on both channels — that's the "always in sync" requirement in practice.

Each field's `source` key is the key that ocr_processor.extract_smart_data()
produces when it recognises that value on an uploaded document. When a
document is uploaded, form_engine copies any matching `source` keys into
the session's collected fields automatically. Fields with no matching
extracted key (or where extraction failed) are asked as plain questions —
on WhatsApp as a one-by-one text prompt, on the dashboard as an editable
input.
"""

DOCUMENT_TYPES = {
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
}

# field key -> (label, source key from extract_smart_data, required?)
FIELD_LIBRARY = {
    "name":            ("Full name",               "name",           True),
    "father_name":     ("Father's name",            "father_name",    True),
    "mother_name":     ("Mother's name",            "mother_name",    False),
    "dob":             ("Date of birth (DD/MM/YYYY)","dob",           True),
    "age":             ("Age",                      "age",            False),
    "gender":          ("Gender",                   "gender",         True),
    "address":         ("Address",                  "address",        True),
    "mobile":          ("Mobile number",             "mobile",        True),
    "email":           ("Email address",             "email",         False),
    "aadhar":          ("Aadhaar number",             "aadhar",       True),
    "pan":             ("PAN number",                "pan",           False),
    "account_number":  ("Bank account number",       "account_number",True),
    "ifsc":            ("Bank IFSC code",             "ifsc",         True),
    "bank_name":       ("Bank name",                  "bank_name",    False),
    "pincode":         ("PIN code",                   "pincode",      False),
    "state":           ("State",                      "state",       True),
    "district":        ("District",                   "district",    False),
    "caste":           ("Caste / category",            "caste",      True),
    "income":          ("Annual family income (Rs.)",  "income",     True),
    "occupation":      ("Occupation",                   "occupation",False),
    "family_members":  ("Number of family members",     None,        False),
}

FORMS = [
    {
        "id": "aadhaar_update",
        "name": "Aadhaar Card — Update",
        "category": "Identity",
        "documents": ["aadhaar", "address_proof"],
        "fields": ["name", "dob", "gender", "address", "mobile", "aadhar"],
    },
    {
        "id": "pan_card",
        "name": "PAN Card — New Application",
        "category": "Identity",
        "documents": ["aadhaar", "photo"],
        "fields": ["name", "father_name", "dob", "gender", "address", "mobile", "email"],
    },
    {
        "id": "driving_license",
        "name": "Learner's / Driving License",
        "category": "Transport",
        "documents": ["aadhaar", "address_proof", "photo"],
        "fields": ["name", "dob", "gender", "address", "mobile"],
    },
    {
        "id": "income_certificate",
        "name": "Income Certificate",
        "category": "Revenue",
        "documents": ["aadhaar", "income_proof"],
        "fields": ["name", "father_name", "address", "income", "occupation", "district", "state"],
    },
    {
        "id": "ration_card",
        "name": "Ration Card — New Application",
        "category": "Food & Civil Supplies",
        "documents": ["aadhaar", "address_proof", "income_proof"],
        "fields": ["name", "father_name", "address", "income", "family_members", "caste"],
    },
    {
        "id": "old_age_pension",
        "name": "Old Age Pension",
        "category": "Social Welfare",
        "documents": ["aadhaar", "age_proof", "bank_passbook"],
        "fields": ["name", "dob", "age", "gender", "address", "account_number", "ifsc", "bank_name", "income"],
    },
    {
        "id": "voter_id",
        "name": "Voter ID Registration",
        "category": "Identity",
        "documents": ["aadhaar", "address_proof", "photo"],
        "fields": ["name", "father_name", "dob", "gender", "address"],
    },
    {
        "id": "birth_certificate",
        "name": "Birth Certificate",
        "category": "Civil Registration",
        "documents": ["hospital_discharge", "parent_id_proof"],
        "fields": ["name", "father_name", "mother_name", "dob", "address", "district", "state"],
    },
    {
        "id": "bank_account_opening",
        "name": "Bank Account Opening",
        "category": "Banking",
        "documents": ["aadhaar", "pan", "photo"],
        "fields": ["name", "father_name", "dob", "address", "mobile", "email", "pan", "occupation"],
    },
    {
        "id": "caste_certificate",
        "name": "Caste Certificate",
        "category": "Revenue",
        "documents": ["aadhaar", "address_proof", "caste_proof"],
        "fields": ["name", "father_name", "address", "caste", "district", "state"],
    },
]

FORMS_BY_ID = {f["id"]: f for f in FORMS}


def get_form(form_id):
    return FORMS_BY_ID.get(form_id)


def list_forms():
    return FORMS


def field_meta(field_key):
    """Returns (label, source_key, required) for a field key."""
    return FIELD_LIBRARY.get(field_key, (field_key.replace("_", " ").title(), None, False))


def document_label(doc_type):
    return DOCUMENT_TYPES.get(doc_type, doc_type.replace("_", " ").title())
