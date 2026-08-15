"""
Sahayak AI Chatbot - Complete Local Knowledge Base
Works 100% offline - no API key needed
Full information about Indian government documents, schemes, and certificates
"""

import logging

logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════════════════════
# COMPLETE KNOWLEDGE DATABASE
# ══════════════════════════════════════════════════════════════════════════════

KNOWLEDGE_BASE = {

    "aadhaar": {
        "name": "Aadhaar Card",
        "emoji": "🪪",
        "keywords": ["aadhaar", "aadhar", "adhaar", "adhar", "aadhaaar", "uid", "biometric id", "uidai", "unique id", "aadhaar ke liye", "adhaar banana", "aadhaar card banana"],
        "official_link": "https://uidai.gov.in",
        "online_portal": "https://myaadhaar.uidai.gov.in",
        "appointment": "https://appointments.uidai.gov.in",
        "eligibility": [
            "Any Indian resident (citizen or non-citizen)",
            "Children of any age (Baal Aadhaar blue card for under 5)",
            "No income limit"
        ],
        "documents": {
            "Identity Proof (any ONE)": [
                "Passport", "Voter ID (EPIC)", "PAN Card",
                "Driving Licence", "Government employee photo ID"
            ],
            "Address Proof (any ONE)": [
                "Passport", "Bank / Post Office Passbook with photo", "Voter ID",
                "Ration Card", "Electricity / Water / Gas Bill (last 3 months)"
            ],
            "Date of Birth Proof (any ONE)": [
                "Birth Certificate", "SSLC / Matriculation Certificate",
                "Passport", "PAN Card"
            ]
        },
        "steps": [
            "Visit nearest Aadhaar Enrolment Centre (find at appointments.uidai.gov.in)",
            "Fill Aadhaar Enrolment Form (available at centre)",
            "Submit original documents for verification",
            "Biometric capture — fingerprints, iris scan, and photograph",
            "Receive acknowledgement slip with Enrolment ID",
            "Aadhaar delivered by post in 90 days",
            "Download e-Aadhaar anytime at myaadhaar.uidai.gov.in"
        ],
        "fee": "Free of cost",
        "time": "90 days for physical card | Instant e-Aadhaar download",
        "extra_info": "Aadhaar is mandatory for most government schemes, banking, and SIM cards. Update address/mobile online at myaadhaar.uidai.gov.in"
    },

    "pan": {
        "name": "PAN Card",
        "emoji": "💳",
        "keywords": ["pan", "pan card", "permanent account number", "income tax card"],
        "official_link": "https://www.onlineservices.nsdl.com/paam/endUserRegisterContact.html",
        "online_portal": "https://www.utiitsl.com",
        "eligibility": [
            "Indian citizens and NRIs",
            "Companies, firms, and other entities",
            "No age limit (minors can apply with guardian)"
        ],
        "documents": {
            "Identity Proof (any ONE)": [
                "Aadhaar Card", "Voter ID", "Passport", "Driving Licence"
            ],
            "Address Proof (any ONE)": [
                "Aadhaar Card", "Voter ID", "Passport",
                "Bank Statement (last 3 months)", "Electricity Bill"
            ],
            "Date of Birth Proof (any ONE)": [
                "Birth Certificate", "Matriculation Certificate", "Passport", "Aadhaar Card"
            ]
        },
        "steps": [
            "Visit NSDL: onlineservices.nsdl.com OR UTIITSL: utiitsl.com",
            "Fill Form 49A (Indian citizens) or 49AA (foreign citizens)",
            "Upload scanned documents and passport photo",
            "Pay fee online (Rs 107 for Indian address)",
            "Submit — get acknowledgement number",
            "PAN delivered by post in 15-20 working days",
            "Download instant e-PAN after approval (free)"
        ],
        "fee": "Rs 107 (Indian address) | Rs 1,017 (foreign address)",
        "time": "15-20 working days | Instant e-PAN available",
        "extra_info": "Mandatory for income tax filing, bank accounts above Rs 50,000, and property purchase"
    },

    "driving_licence": {
        "name": "Driving Licence",
        "emoji": "🚗",
        "keywords": ["driving licence", "driving license", "dl", "learner", "ll", "parivahan"],
        "official_link": "https://parivahan.gov.in/parivahan",
        "online_portal": "https://sarathi.parivahan.gov.in",
        "eligibility": [
            "Age 18+ for motor vehicles (car, bike with gear)",
            "Age 16+ for gearless 2-wheelers (with parent consent)",
            "Valid medical fitness certificate required",
            "Must pass written test for Learner Licence"
        ],
        "documents": {
            "Age and Identity Proof (any ONE)": [
                "Aadhaar Card", "Birth Certificate", "Matriculation Certificate",
                "Passport", "Voter ID"
            ],
            "Address Proof (any ONE)": [
                "Aadhaar Card", "Voter ID", "Passport", "Utility Bill (last 3 months)"
            ],
            "Additional Required": [
                "Form 1 — Medical self-declaration",
                "2 passport-size photographs",
                "Learner Licence (required before applying for permanent DL)"
            ]
        },
        "steps": [
            "STEP 1 — Learner Licence: Register at sarathi.parivahan.gov.in",
            "Fill Form 1 + pay Rs 150 fee + book RTO slot",
            "Appear for written test (traffic rules and signs)",
            "Get Learner Licence (valid 6 months)",
            "STEP 2 — Permanent DL: Apply after 30 days of LL",
            "Book driving test at RTO",
            "Pass practical driving test → DL issued in 7 days"
        ],
        "fee": "Learner Licence: Rs 150 | Permanent DL: Rs 200",
        "time": "Learner Licence: Same day | Permanent DL: 7-30 days",
        "extra_info": "Smart Card DL valid for 20 years. Renewal required before expiry."
    },

    "ration_card": {
        "name": "Ration Card",
        "emoji": "🍚",
        "keywords": ["ration", "ration card", "food card", "nfsa", "bpl card", "aay", "antyodaya", "rashan card", "rashan", "rashan ke liye"],
        "official_link": "https://nfsa.gov.in",
        "online_portal": "https://nfsa.gov.in",
        "eligibility": [
            "APL (Above Poverty Line) — annual income above poverty line",
            "BPL (Below Poverty Line) — annual income below Rs 1,00,000",
            "AAY (Antyodaya Anna Yojana) — poorest of poor, no regular income",
            "Indian citizen and resident of the state",
            "One ration card per family"
        ],
        "documents": {
            "Family Head": [
                "Aadhaar Card (mandatory)", "Passport-size photograph"
            ],
            "All Family Members": [
                "Aadhaar Card of each member", "Passport-size photo of each member"
            ],
            "Address Proof (any ONE)": [
                "Electricity Bill", "Gas Connection Bill", "Registered Rent Agreement"
            ],
            "Income Proof (for BPL/AAY)": [
                "Income Certificate from Tehsildar", "BPL survey data"
            ]
        },
        "steps": [
            "Visit state food department portal or nearest ration office",
            "Fill application form (available online or at office)",
            "Attach all documents — submit to Food Supply Officer",
            "Inspector visits for field verification",
            "Ration Card issued in 30-45 days",
            "Link Aadhaar to ration card at nearest PDS shop"
        ],
        "fee": "Free (nominal Rs 5-10 in some states)",
        "time": "30-45 days",
        "extra_info": "Ration Card is also valid as address proof and identity document"
    },

    "voter_id": {
        "name": "Voter ID Card (EPIC)",
        "emoji": "🗳️",
        "keywords": ["voter id", "voter card", "epic", "election card", "voter registration"],
        "official_link": "https://voters.eci.gov.in",
        "online_portal": "https://voters.eci.gov.in",
        "eligibility": [
            "Indian citizen, age 18 years or above",
            "Ordinary resident of the constituency",
            "Not disqualified under any law"
        ],
        "documents": {
            "Age and Identity Proof (any ONE)": [
                "Birth Certificate", "Aadhaar Card", "PAN Card",
                "Passport", "Matriculation Certificate"
            ],
            "Address Proof (any ONE)": [
                "Aadhaar Card", "Passport", "Bank Passbook",
                "Electricity / Gas Bill", "Registered Rent Agreement"
            ],
            "Photo": ["1 recent passport-size photograph"]
        },
        "steps": [
            "Visit voters.eci.gov.in or download Voter Helpline App",
            "Click New Voter Registration → Fill Form 6",
            "Upload documents and photograph",
            "Submit online — get application reference number",
            "Booth Level Officer (BLO) verifies details",
            "Name added to electoral roll in 30-45 days",
            "Download e-EPIC or receive physical Voter ID card"
        ],
        "fee": "Free of cost",
        "time": "30-45 days",
        "extra_info": "Voter ID also accepted as identity proof for bank KYC, Aadhaar, etc."
    },

    "passport": {
        "name": "Passport",
        "emoji": "🛂",
        "keywords": ["passport", "travel document", "psk", "tatkal"],
        "official_link": "https://passportindia.gov.in",
        "online_portal": "https://passportindia.gov.in",
        "eligibility": [
            "Indian citizen of any age",
            "Minors need parent/guardian consent",
            "Police verification required (background check)"
        ],
        "documents": {
            "Address Proof (any ONE)": [
                "Aadhaar Card", "Voter ID",
                "Electricity / Water / Gas Bill (last 3 months)",
                "Bank Statement (last 3 months)", "Registered Rent Agreement"
            ],
            "Date of Birth Proof (any ONE)": [
                "Birth Certificate", "Matriculation Certificate with DOB", "Aadhaar Card"
            ],
            "Identity Proof": ["Aadhaar Card", "Voter ID", "PAN Card"],
            "For Minors (additional)": [
                "Parent passport copies",
                "Annexure H — declaration by parents",
                "School bonafide certificate"
            ]
        },
        "steps": [
            "Register at passportindia.gov.in",
            "Fill online application form",
            "Pay fee — Rs 1,500 (Normal) or Rs 3,500 (Tatkal)",
            "Book appointment at nearest PSK / POPSK / Post Office Passport Seva",
            "Attend appointment with ORIGINAL documents",
            "Document verification + photo + biometrics at PSK",
            "Police verification (home visit)",
            "Passport dispatched by Speed Post in 7-30 days"
        ],
        "fee": "Normal: Rs 1,500 | Tatkal: Rs 3,500 | Senior Citizen: Rs 1,000",
        "time": "Normal: 30-45 days | Tatkal: 7-14 days",
        "extra_info": "Police verification is the main delay. Keep address updated on Aadhaar before applying."
    },

    "birth_certificate": {
        "name": "Birth Certificate",
        "emoji": "👶",
        "keywords": ["birth certificate", "birth proof", "janm praman patra"],
        "official_link": "https://crsorgi.gov.in",
        "online_portal": "https://crsorgi.gov.in",
        "eligibility": [
            "All births on Indian soil must be registered",
            "Free registration within 21 days of birth",
            "Late registration fee applies after 21 days"
        ],
        "documents": {
            "Hospital Birth (within 21 days)": [
                "Hospital discharge summary / birth proof from hospital",
                "Father Aadhaar Card", "Mother Aadhaar Card",
                "Parents marriage certificate"
            ],
            "Home Birth": [
                "Declaration from parents",
                "Two witnesses with ID proof",
                "Address proof of parents"
            ]
        },
        "steps": [
            "For hospital birth: Hospital registers automatically within 21 days",
            "Collect from hospital registration desk OR",
            "Visit local Municipal Corporation / Gram Panchayat office",
            "Fill birth registration form with required documents",
            "Certificate issued in 3-7 days",
            "Download digitally at crsorgi.gov.in (available in many states)"
        ],
        "fee": "Free within 21 days | Rs 2-10 after 21 days",
        "time": "3-7 working days",
        "extra_info": "Mandatory for school admission, passport for children, and Aadhaar enrollment of minors"
    },

    "income_certificate": {
        "name": "Income Certificate",
        "emoji": "💰",
        "keywords": ["income certificate", "income proof", "aay praman patra", "salary certificate"],
        "official_link": "https://serviceonline.gov.in",
        "online_portal": "https://serviceonline.gov.in",
        "eligibility": [
            "Any Indian citizen needing to prove annual income",
            "Required for scholarships, BPL schemes, government jobs, fee waivers",
            "Valid for 6 months to 1 year (varies by state)"
        ],
        "documents": {
            "Mandatory": [
                "Aadhaar Card",
                "Address Proof (Voter ID / Utility Bill / Bank Passbook)"
            ],
            "Income Proof (as applicable)": [
                "Salary slips (last 3 months) — for salaried employees",
                "Bank statements (last 6 months)",
                "Income Tax Return (if filed)",
                "Land records / Khasra-Khatauni — for farmers",
                "Self-declaration affidavit for informal workers"
            ],
            "Additional": [
                "Ration Card", "Passport-size photograph", "Application form"
            ]
        },
        "steps": [
            "Visit serviceonline.gov.in or state e-district portal",
            "Select Income Certificate under Revenue services",
            "Fill application with income details",
            "Upload required documents and pay Rs 10-50 fee",
            "Application sent to Tehsildar for verification",
            "Certificate issued in 7-15 days"
        ],
        "fee": "Rs 10-50 (varies by state)",
        "time": "7-15 working days",
        "extra_info": "Required for scholarships, BPL ration card, fee concessions, pension, OBC NCL certificates"
    },

    "caste_certificate": {
        "name": "Caste Certificate (SC/ST/OBC)",
        "emoji": "📜",
        "keywords": ["caste certificate", "sc certificate", "st certificate", "obc certificate", "jati praman patra"],
        "official_link": "https://serviceonline.gov.in",
        "online_portal": "https://serviceonline.gov.in",
        "eligibility": [
            "SC (Scheduled Caste) — as per Presidential Order",
            "ST (Scheduled Tribe) — as per Presidential Order",
            "OBC (Other Backward Classes) — as per state/central list",
            "Must belong to the caste by birth"
        ],
        "documents": {
            "Mandatory": [
                "Aadhaar Card",
                "Address Proof (Voter ID / Utility Bill)"
            ],
            "Caste Proof (any ONE)": [
                "Father's / Mother's caste certificate",
                "School certificate / Transfer certificate mentioning caste",
                "Old government document mentioning caste"
            ],
            "Additional": [
                "Ration Card", "2 passport-size photographs",
                "Self-declaration affidavit on stamp paper"
            ]
        },
        "steps": [
            "Visit serviceonline.gov.in or state e-district portal or SDM office",
            "Fill caste certificate application form",
            "Attach all documents — submit to SDM / Tehsildar",
            "Field verification by revenue official",
            "Certificate issued in 15-30 days"
        ],
        "fee": "Rs 10-50 (varies by state)",
        "time": "15-30 working days",
        "extra_info": "Essential for government job reservations, educational admissions, scholarships, and fee waivers"
    },

    "domicile_certificate": {
        "name": "Domicile / Residence Certificate",
        "emoji": "🏠",
        "keywords": ["domicile", "residence certificate", "niwas praman patra", "mool niwas"],
        "official_link": "https://serviceonline.gov.in",
        "online_portal": "https://serviceonline.gov.in",
        "eligibility": [
            "Minimum 15 years residence in state (varies: some states require 3-5 years)",
            "OR born in the state / parents born in state",
            "Valid for 3 years (varies by state)"
        ],
        "documents": {
            "Mandatory": [
                "Aadhaar Card", "Voter ID (showing state address)"
            ],
            "Residence Proof (showing years of stay)": [
                "School / College Certificates from state institutions",
                "Utility bills for multiple years",
                "Ration Card issued by state",
                "Property ownership documents",
                "Registered Rent Agreements for multiple years"
            ],
            "Additional": [
                "Passport-size photograph",
                "Affidavit declaring years of residence"
            ]
        },
        "steps": [
            "Visit state e-district portal or Tehsildar office",
            "Fill domicile certificate application",
            "Attach proof of residence for required years",
            "Submit with affidavit",
            "Tehsildar / SDM verifies the application",
            "Certificate issued in 15-30 days"
        ],
        "fee": "Rs 10-50 (varies by state)",
        "time": "15-30 working days",
        "extra_info": "Required for state government jobs, state quota in colleges, and state-specific schemes"
    },

    "old_age_pension": {
        "name": "Old Age Pension (IGNOAPS / NSAP)",
        "emoji": "👴",
        "keywords": ["pension", "old age pension", "vridha pension", "nsap", "ignoaps", "budhapa pension", "senior citizen pension", "old age", "budhapa", "vridha", "bujurg", "vriddhavasta", "pension ke liye", "pension chahiye"],
        "official_link": "https://nsap.nic.in",
        "online_portal": "https://nsap.nic.in",
        "eligibility": [
            "Age: 60 years or above",
            "Annual income: Below Rs 1,00,000",
            "BPL (Below Poverty Line) household preferred",
            "Indian citizen and state resident",
            "Bank account linked to Aadhaar mandatory (for DBT)"
        ],
        "documents": {
            "Mandatory": [
                "Aadhaar Card (mandatory for Direct Benefit Transfer)",
                "Bank passbook copy (Aadhaar-linked account)",
                "2 passport-size photographs"
            ],
            "Age Proof (any ONE)": [
                "Birth Certificate", "Voter ID with date of birth",
                "School / Matriculation Certificate", "Passport",
                "Medical age certificate from government hospital"
            ],
            "Income and BPL Proof": [
                "Income Certificate from Tehsildar (below Rs 1,00,000)",
                "BPL Ration Card (preferred)",
                "Address proof (Voter ID / Utility Bill)"
            ]
        },
        "steps": [
            "Visit state social welfare department office or Block/Gram Panchayat office",
            "Collect pension application form (also at nsap.nic.in)",
            "Fill form and attach all documents",
            "Submit to concerned officer — get acknowledgement",
            "Field verification by social welfare inspector",
            "Application sent to District Collector for approval",
            "Pension starts after approval — directly in bank account via DBT",
            "Annual Life Certificate required every November"
        ],
        "fee": "Free of cost",
        "time": "30-90 days (varies by state)",
        "pension_amount": "Central: Rs 200-500/month + State top-up (total Rs 500-3,500/month depending on state)",
        "extra_info": "Aadhaar-bank linking is MANDATORY. Annual Life Certificate (Jeevan Pramaan) needed every November to continue pension."
    },

    "widow_pension": {
        "name": "Widow Pension (IGNWPS)",
        "emoji": "👩",
        "keywords": ["widow pension", "vidhwa pension", "ignwps", "widow scheme"],
        "official_link": "https://nsap.nic.in",
        "online_portal": "https://nsap.nic.in",
        "eligibility": [
            "Widowed woman, age 40-79 years (central scheme)",
            "Annual income below Rs 1,00,000",
            "BPL household",
            "Bank account linked to Aadhaar"
        ],
        "documents": {
            "Mandatory": [
                "Aadhaar Card",
                "Husband Death Certificate",
                "Bank passbook (Aadhaar linked)",
                "2 passport-size photographs"
            ],
            "Age and Income Proof": [
                "Age proof (Voter ID / Birth Certificate)",
                "Income Certificate from Tehsildar"
            ],
            "Residence and BPL Proof": [
                "BPL Ration Card", "Address proof"
            ]
        },
        "steps": [
            "Visit state social welfare / district office",
            "Fill widow pension application form",
            "Attach all required documents",
            "Submit and get acknowledgement",
            "Verification by field inspector",
            "Pension approved — credited monthly to bank account"
        ],
        "fee": "Free of cost",
        "time": "30-60 days",
        "extra_info": "State governments add additional top-up. Check state social welfare website for state-specific amount."
    },

    "scholarship": {
        "name": "Government Scholarships",
        "emoji": "🎓",
        "keywords": ["scholarship", "chatravritti", "student scheme", "nsp", "national scholarship", "education scheme", "chhatravritti", "padhai", "scholarship chahiye", "scholarship ke liye"],
        "official_link": "https://scholarships.gov.in",
        "online_portal": "https://scholarships.gov.in",
        "eligibility": [
            "Indian students enrolled in recognized schools/colleges",
            "Family income below Rs 2,50,000/year (most schemes)",
            "Category: SC/ST/OBC/Minority/General EWS",
            "Minimum 50% marks in previous year (most schemes)"
        ],
        "documents": {
            "Mandatory": [
                "Aadhaar Card",
                "Bank account linked to Aadhaar (for DBT)",
                "Mobile number linked to Aadhaar"
            ],
            "Academic Documents": [
                "Previous year marksheet / result",
                "Current year bonafide / enrollment certificate",
                "School/college fee receipt"
            ],
            "Income and Category": [
                "Income Certificate (family annual income)",
                "Caste Certificate (for SC/ST/OBC schemes)",
                "EWS Certificate (for General EWS)"
            ],
            "Photo": ["Recent passport-size photograph"]
        },
        "steps": [
            "Register at scholarships.gov.in using Aadhaar + mobile",
            "Select appropriate scholarship scheme",
            "Fill application with academic and family details",
            "Upload all required documents",
            "Submit before deadline (usually October-November)",
            "Institute verifies and forwards the application",
            "Amount directly credited to bank account after approval"
        ],
        "fee": "Free to apply",
        "time": "Results in 3-6 months | Amount credited January-February",
        "extra_info": "Application window: July to November. Renewal required every year. Keep bank account active."
    },

    "ayushman_bharat": {
        "name": "Ayushman Bharat PMJAY Health Card",
        "emoji": "🏥",
        "keywords": ["ayushman bharat", "pmjay", "health card", "golden card", "health insurance", "ayushman card"],
        "official_link": "https://pmjay.gov.in",
        "online_portal": "https://beneficiary.nha.gov.in",
        "eligibility": [
            "Based on SECC 2011 data — BPL and vulnerable families",
            "Check eligibility at pmjay.gov.in by mobile/ration card number",
            "No upper age limit — entire family covered",
            "No premium — fully government funded"
        ],
        "documents": {
            "Mandatory": [
                "Aadhaar Card",
                "Ration Card / BPL Card",
                "Mobile number"
            ]
        },
        "steps": [
            "Check eligibility at pmjay.gov.in or call 14555",
            "Visit nearest Ayushman Mitra at empanelled hospital or CSC centre",
            "Carry Aadhaar and Ration Card",
            "Ayushman Mitra verifies and generates Ayushman Card on same day",
            "Use card at any empanelled hospital for cashless treatment"
        ],
        "fee": "Free of cost — fully government funded",
        "time": "Card generated same day at Ayushman Mitra counter",
        "benefit": "Rs 5 lakh per year health insurance per family | Covers 1,949 medical procedures | Pre-existing conditions covered from day 1",
        "extra_info": "Find empanelled hospitals at pmjay.gov.in. Covers hospitalization, surgery, medicines, and diagnostics."
    },

    "pm_kisan": {
        "name": "PM Kisan Samman Nidhi",
        "emoji": "🌾",
        "keywords": ["pm kisan", "kisan", "farmer scheme", "pmkisan", "kisan samman"],
        "official_link": "https://pmkisan.gov.in",
        "online_portal": "https://pmkisan.gov.in",
        "eligibility": [
            "Small and marginal farmers with land up to 2 hectares",
            "Indian citizen",
            "NOT eligible: Government employees, income tax payers, pension holders above Rs 10,000/month"
        ],
        "documents": {
            "Mandatory": [
                "Aadhaar Card (mandatory for DBT)",
                "Bank account linked to Aadhaar",
                "Mobile number linked to Aadhaar"
            ],
            "Land Documents": [
                "Land ownership documents (Khasra / Khatauni / 7-12 Extract)",
                "Land records from Patwari / Tehsildar"
            ]
        },
        "steps": [
            "Visit pmkisan.gov.in",
            "Click Farmer Corner → New Farmer Registration",
            "Enter Aadhaar number + mobile + state",
            "Fill land and bank details",
            "State government verifies land records",
            "Rs 2,000 installments transferred to bank every 4 months"
        ],
        "fee": "Free of cost",
        "time": "Verification 30-60 days | First installment after approval",
        "benefit": "Rs 6,000 per year in 3 installments of Rs 2,000 each",
        "extra_info": "Check status at pmkisan.gov.in/Beneficiary_Status using Aadhaar number"
    },

    "digilocker": {
        "name": "DigiLocker",
        "emoji": "📱",
        "keywords": ["digilocker", "digital locker", "e document", "digital document", "digi locker"],
        "official_link": "https://digilocker.gov.in",
        "online_portal": "https://digilocker.gov.in",
        "app": "DigiLocker App (Android and iOS)",
        "eligibility": [
            "Any Indian citizen with Aadhaar and mobile number",
            "Completely free service from Government of India"
        ],
        "documents": {
            "To Register": [
                "Aadhaar Card number",
                "Mobile number linked to Aadhaar (for OTP verification)"
            ]
        },
        "available_documents": [
            "Aadhaar Card", "PAN Card", "Driving Licence", "Vehicle RC",
            "Class 10 and 12 Marksheets (CBSE, State Boards)", "Degree Certificates",
            "Insurance Policy documents", "Land Records (some states)"
        ],
        "steps": [
            "Visit digilocker.gov.in or download DigiLocker App",
            "Sign up with mobile number + Aadhaar OTP",
            "Set 6-digit security PIN",
            "Access Issued Documents to get official digital docs",
            "Share documents digitally — legally valid under IT Act 2000"
        ],
        "fee": "Completely free",
        "extra_info": "DigiLocker documents are legally valid. No need to carry physical documents for government work."
    },


    "death_certificate": {
        "name": "Death Certificate",
        "emoji": "📋",
        "keywords": ["death certificate", "mrityu praman patra", "death proof", "mrityu", "death card"],
        "official_link": "https://crsorgi.gov.in",
        "online_portal": "https://crsorgi.gov.in",
        "eligibility": [
            "Mandatory for all deaths on Indian soil",
            "Free registration within 21 days of death",
            "Fee applies after 21 days",
            "Family member or eyewitness can apply"
        ],
        "documents": {
            "Mandatory Documents": [
                "Medical Certificate of Cause of Death (Form 4A — from hospital/doctor)",
                "Deceased person Aadhaar Card / Voter ID / any ID proof",
                "Applicant Aadhaar Card (person applying)",
                "Proof of relationship with deceased (Ration Card / Family Register)"
            ],
            "Address and Registration": [
                "Address proof of deceased (utility bill / Aadhaar)",
                "Completed registration form (Form 2 — from Municipal office)"
            ]
        },
        "steps": [
            "For hospital death: Hospital submits death report to registrar automatically",
            "Collect Form 4A (cause of death certificate) from hospital",
            "Visit local Municipal Corporation / Gram Panchayat office",
            "Fill Form 2 (Death Registration Form) within 21 days",
            "Submit with required documents",
            "Death Certificate issued in 3-7 days",
            "Download digitally at crsorgi.gov.in (in many states)"
        ],
        "fee": "Free within 21 days | Rs 10-50 after 21 days (varies by state)",
        "time": "3-7 working days",
        "extra_info": "Required for: insurance claims, pension cancellation, property transfer, bank account closure, widow pension application"
    },

    "pension_card": {
        "name": "Pension Card / Pensioner Identity Card",
        "emoji": "🪪",
        "keywords": ["pension card", "pensioner card", "pension identity", "pensioner id", "jeevan pramaan", "life certificate", "pension book"],
        "official_link": "https://nsap.nic.in",
        "online_portal": "https://jeevanpramaan.gov.in",
        "eligibility": [
            "Already approved pension beneficiary (Old Age / Widow / Disability)",
            "Must have active pension account",
            "Aadhaar linked to bank account mandatory"
        ],
        "documents": {
            "For Pension Card / Identity Card": [
                "Aadhaar Card",
                "Pension sanction order / approval letter",
                "Bank passbook (Aadhaar linked)",
                "Passport-size photograph (2 copies)",
                "Old Age / Widow / Disability certificate"
            ],
            "For Annual Life Certificate (Jeevan Pramaan)": [
                "Aadhaar Card",
                "Mobile number linked to Aadhaar",
                "Pension Payment Order (PPO) number",
                "Bank account number"
            ]
        },
        "steps": [
            "For Pension Card: Visit state social welfare / district office",
            "Carry pension sanction order + Aadhaar + photo",
            "Pension card issued after identity verification",
            "FOR ANNUAL LIFE CERTIFICATE (every November):",
            "  -> Visit nearest bank branch / CSC centre / post office",
            "  -> Or use Jeevan Pramaan App (jeevanpramaan.gov.in)",
            "  -> Biometric verification using Aadhaar",
            "  -> Certificate generated instantly — pension continues"
        ],
        "fee": "Free of cost",
        "time": "Same day (Life Certificate) | 7-15 days (Pension Card)",
        "extra_info": "Life Certificate (Jeevan Pramaan) must be submitted every November to continue receiving pension. Can be done at any bank, CSC, post office, or doorstep service."
    },

    "widow_card": {
        "name": "Widow Card / Vidhwa Praman Patra",
        "emoji": "📄",
        "keywords": ["widow card", "vidhwa card", "widow certificate", "vidhwa praman patra", "widow identity", "vidhwa"],
        "official_link": "https://nsap.nic.in",
        "online_portal": "https://serviceonline.gov.in",
        "eligibility": [
            "Woman whose husband has died",
            "Indian citizen",
            "Required for: widow pension, government scheme benefits, legal matters"
        ],
        "documents": {
            "Mandatory Documents": [
                "Aadhaar Card of the widow",
                "Husband Death Certificate (mandatory)",
                "Marriage Certificate OR any proof of marriage (joint ration card / family register)",
                "Passport-size photograph (2 copies)"
            ],
            "Additional Documents": [
                "Address proof (Voter ID / Utility Bill / Ration Card)",
                "Income Certificate (for BPL/pension schemes)",
                "Bank account details (for widow pension)"
            ]
        },
        "steps": [
            "Visit Tehsildar office or state e-district portal",
            "Fill Widow Certificate application form",
            "Attach Husband Death Certificate + Marriage proof + Aadhaar",
            "Submit to SDM / Tehsildar office",
            "Verification by revenue official",
            "Widow Certificate issued in 15-30 days",
            "Use certificate to apply for widow pension at nsap.nic.in"
        ],
        "fee": "Rs 10-50 (varies by state)",
        "time": "15-30 working days",
        "extra_info": "Widow Certificate is needed to apply for Widow Pension (IGNWPS), free ration, housing schemes, and other government benefits"
    },

    "marriage_certificate": {
        "name": "Marriage Certificate",
        "emoji": "💍",
        "keywords": ["marriage certificate", "vivah praman patra", "marriage proof", "marriage registration", "nikah", "wedding certificate"],
        "official_link": "https://igrsup.gov.in",
        "online_portal": "https://serviceonline.gov.in",
        "eligibility": [
            "Hindu Marriage Act 1955 — for Hindus, Buddhists, Jains, Sikhs",
            "Special Marriage Act 1954 — for inter-religion marriages",
            "Both parties must be of legal age: Bride 18+, Groom 21+",
            "Must not have living spouse"
        ],
        "documents": {
            "Both Bride and Groom": [
                "Aadhaar Card",
                "Age Proof: Birth Certificate / Passport / Matriculation Certificate",
                "Address Proof: Voter ID / Passport / Utility Bill",
                "Passport-size photographs (4 each)"
            ],
            "Marriage Proof": [
                "Wedding invitation card OR",
                "Temple / Church / Gurudwara certificate OR",
                "Joint photograph at wedding"
            ],
            "Witnesses": [
                "2 witnesses with Aadhaar and photograph each"
            ]
        },
        "steps": [
            "Visit local Sub-Registrar office OR state portal (serviceonline.gov.in)",
            "Fill marriage registration application",
            "Submit documents for both bride and groom + 2 witnesses",
            "Pay registration fee",
            "Both parties and witnesses appear for verification",
            "Marriage Certificate issued in 7-30 days",
            "Certificate also available on DigiLocker after registration"
        ],
        "fee": "Rs 100-500 (varies by state and act)",
        "time": "Same day to 30 days (varies by state)",
        "extra_info": "Marriage Certificate required for: passport (spouse visa), bank joint account, property transfer, insurance nomination, visa applications"
    },

    "character_certificate": {
        "name": "Character Certificate / Police Clearance Certificate",
        "emoji": "✅",
        "keywords": ["character certificate", "charitra praman patra", "police clearance", "pcc", "good conduct certificate", "character proof"],
        "official_link": "https://serviceonline.gov.in",
        "online_portal": "https://serviceonline.gov.in",
        "eligibility": [
            "Any Indian citizen",
            "Required for: government jobs, passport, visa, foreign employment, educational admissions",
            "Police verification required"
        ],
        "documents": {
            "Mandatory Documents": [
                "Aadhaar Card",
                "Address Proof (Voter ID / Passport / Utility Bill)",
                "Passport-size photographs (2 copies)",
                "Purpose of certificate (job offer letter / admission letter / visa documents)"
            ],
            "Additional for PCC (Passport)": [
                "Passport copy (all pages)",
                "Proof of foreign travel / visa application"
            ]
        },
        "steps": [
            "Visit nearest police station or state e-district portal",
            "Fill application form mentioning purpose",
            "Submit documents and pay fee",
            "Police verification at your address",
            "Certificate issued in 7-15 days",
            "FOR PASSPORT PCC: Apply through passportindia.gov.in"
        ],
        "fee": "Rs 50-500 (varies by state and purpose)",
        "time": "7-15 working days",
        "extra_info": "Different from police NOC. PCC for passport/visa is done through Passport Seva portal."
    },

    "obc_certificate": {
        "name": "OBC Non-Creamy Layer Certificate",
        "emoji": "📜",
        "keywords": ["obc certificate", "obc ncl", "non creamy layer", "other backward class", "obc ncl certificate"],
        "official_link": "https://serviceonline.gov.in",
        "online_portal": "https://serviceonline.gov.in",
        "eligibility": [
            "Belongs to OBC caste as per central/state list",
            "Family annual income below Rs 8,00,000 (for central NCL)",
            "Parents not in Class I/II central government positions",
            "Valid for 1 year (must be renewed annually)"
        ],
        "documents": {
            "Mandatory": [
                "Aadhaar Card",
                "Income Certificate (family income below Rs 8 lakh)",
                "OBC Caste Certificate",
                "Address Proof (Voter ID / Utility Bill)"
            ],
            "Additional": [
                "Father occupation proof (salary slip / employment certificate)",
                "Ration Card",
                "Passport-size photographs (2 copies)"
            ]
        },
        "steps": [
            "Visit serviceonline.gov.in or state e-district portal or SDM office",
            "Fill OBC NCL Certificate application",
            "Attach income + caste + Aadhaar documents",
            "Submit to Tehsildar / SDM",
            "Verification and income check",
            "Certificate issued in 15-30 days"
        ],
        "fee": "Rs 10-50 (varies by state)",
        "time": "15-30 working days",
        "extra_info": "Required every year for college admissions, NEET/JEE reservations, government job applications under OBC quota"
    },

    "ews_certificate": {
        "name": "EWS Certificate (Economically Weaker Section)",
        "emoji": "📋",
        "keywords": ["ews certificate", "economically weaker section", "ews", "general ews", "10 percent reservation"],
        "official_link": "https://serviceonline.gov.in",
        "online_portal": "https://serviceonline.gov.in",
        "eligibility": [
            "General category (not SC/ST/OBC)",
            "Family annual income below Rs 8,00,000",
            "Family does not own more than 5 acres of agricultural land",
            "Residential plot less than 1000 sq ft in notified municipalities",
            "10% reservation in government jobs and education"
        ],
        "documents": {
            "Mandatory": [
                "Aadhaar Card",
                "Income Certificate (below Rs 8 lakh per year)",
                "Self-declaration about caste (General category)",
                "Address Proof (Voter ID / Utility Bill)"
            ],
            "Property Documents": [
                "Land records / property documents (to verify no large assets)",
                "Ration Card"
            ],
            "Additional": [
                "Passport-size photographs (2 copies)",
                "PAN Card (if available)"
            ]
        },
        "steps": [
            "Visit Tehsildar office or state e-district portal",
            "Fill EWS Certificate application form",
            "Attach income + identity + property documents",
            "Submit to Tehsildar / SDM",
            "Income and asset verification",
            "Certificate issued in 15-30 days"
        ],
        "fee": "Rs 10-50 (varies by state)",
        "time": "15-30 working days",
        "extra_info": "EWS Certificate valid for 1 year. Required for NEET/JEE/UPSC and central government jobs under 10% EWS quota."
    },

    "land_records": {
        "name": "Land Records / Khasra Khatauni / Jamabandi",
        "emoji": "🏞️",
        "keywords": ["land record", "khasra", "khatauni", "jamabandi", "land ownership", "plot records", "bhu naksha", "bhulekh"],
        "official_link": "https://bhulekh.gov.in",
        "online_portal": "https://bhulekh.gov.in",
        "eligibility": [
            "Land owner or their legal heir",
            "Available online in most states for free viewing",
            "Certified copy needed for official purposes"
        ],
        "documents": {
            "To Get Certified Copy": [
                "Aadhaar Card",
                "Land survey number / Khasra number",
                "Village / Tehsil / District information",
                "Application form"
            ]
        },
        "steps": [
            "ONLINE (free viewing): Visit state Bhulekh portal",
            "  -> UP: upbhulekh.gov.in | MP: mpbhulekh.gov.in",
            "  -> Maharashtra: bhulekh.mahabhumi.gov.in",
            "  -> Enter district, tehsil, village, survey number",
            "  -> View and download Khasra / Khatauni",
            "FOR CERTIFIED COPY: Visit Tehsildar office",
            "Submit application with survey details",
            "Pay nominal fee — certified copy in 3-7 days"
        ],
        "fee": "Free online viewing | Rs 10-50 for certified copy",
        "time": "Instant online | 3-7 days for certified copy",
        "extra_info": "Required for: PM Kisan, bank loans, property sale/purchase, domicile certificate, inheritance claims"
    },

    "handicap_certificate": {
        "name": "Disability Certificate / PH Certificate",
        "emoji": "♿",
        "keywords": ["handicap certificate", "disability certificate", "ph certificate", "divyang certificate", "viklang certificate", "udid", "disabled"],
        "official_link": "https://www.udid.co.in",
        "online_portal": "https://www.udid.co.in",
        "eligibility": [
            "Person with disability as per RPWD Act 2016",
            "21 types of disabilities covered",
            "Minimum 40% disability for most government benefits",
            "Medical Board assessment required"
        ],
        "documents": {
            "Mandatory": [
                "Aadhaar Card",
                "Passport-size photograph (4 copies)",
                "Medical records / hospital reports related to disability"
            ],
            "Medical Evidence": [
                "Hospital discharge summary",
                "Specialist doctor certificate mentioning disability type",
                "Relevant test reports: X-Ray, MRI, audiometry, vision test as applicable"
            ]
        },
        "steps": [
            "Register at udid.co.in (Unique Disability ID portal)",
            "Fill online application with disability details",
            "Upload Aadhaar, photo, and medical documents",
            "Get appointment at nearest government hospital",
            "Medical Board assesses disability percentage",
            "UDID Card with Unique Disability ID issued in 30-60 days",
            "Download e-UDID card from udid.co.in"
        ],
        "fee": "Free of cost",
        "time": "30-60 days",
        "benefit": "Travel concessions | Reservation in jobs and education | Tax benefits | Disha Scheme | Assistive devices",
        "extra_info": "UDID Card is accepted nationwide. Replace all old disability certificates — single card for all benefits."
    },

    "senior_citizen_card": {
        "name": "Senior Citizen Card",
        "emoji": "👴",
        "keywords": ["senior citizen card", "senior card", "vrishtha nagrik", "old age card", "senior citizen certificate"],
        "official_link": "https://socialjustice.gov.in",
        "online_portal": "https://serviceonline.gov.in",
        "eligibility": [
            "Age 60 years or above",
            "Indian citizen",
            "Valid for various discounts and government benefits"
        ],
        "documents": {
            "Mandatory": [
                "Aadhaar Card",
                "Age Proof showing 60+ years (Voter ID / Birth Certificate / Passport)",
                "Address Proof",
                "Passport-size photograph (2 copies)"
            ]
        },
        "steps": [
            "Visit District Social Welfare Office or state portal",
            "Fill Senior Citizen Card application form",
            "Attach age proof + Aadhaar + address proof",
            "Submit and get acknowledgement",
            "Card issued in 15-30 days"
        ],
        "fee": "Free or nominal Rs 10-20",
        "time": "15-30 working days",
        "benefit": "Railway / Air travel discounts (up to 50%) | Priority in queues | Bank interest benefits | Medical discounts",
        "extra_info": "Railway concession: 40% for men, 50% for women. Air travel: various airlines give discounts. Income tax benefits under section 80TTB."
    },

    "bpl_card": {
        "name": "BPL Card (Below Poverty Line)",
        "emoji": "📗",
        "keywords": ["bpl card", "bpl certificate", "below poverty line", "garib card", "poverty card", "bpl"],
        "official_link": "https://nfsa.gov.in",
        "online_portal": "https://nfsa.gov.in",
        "eligibility": [
            "Annual household income below state-defined poverty line",
            "Usually Rs 27,000/year rural | Rs 33,000/year urban (varies by state)",
            "Based on SECC 2011 data and state surveys",
            "No regular government employment in the family"
        ],
        "documents": {
            "Mandatory": [
                "Aadhaar Cards of all family members",
                "Income proof / self-declaration of income",
                "Address Proof",
                "Passport-size photographs of all family members"
            ],
            "Supporting Documents": [
                "Land records (if farmer, should be small/marginal farmer)",
                "Details of occupation / livelihood",
                "Existing ration card (if any)"
            ]
        },
        "steps": [
            "Visit Block Development Office (BDO) or Gram Panchayat office",
            "Fill BPL survey / application form",
            "Social survey by government officials",
            "Name added to BPL list after verification",
            "BPL Ration Card issued by Food Department",
            "OR check if your name is in SECC 2011 BPL list at nfsa.gov.in"
        ],
        "fee": "Free of cost",
        "time": "1-3 months (depends on state survey cycle)",
        "benefit": "Subsidized food grains | Free/subsidized LPG | Ayushman Bharat health card | Scholarship priority | Pension schemes | Free legal aid",
        "extra_info": "BPL status opens access to MOST government schemes. Check your name in SECC 2011 data at nfsa.gov.in."
    },

    "pm_awas": {
        "name": "PM Awas Yojana (Housing Scheme)",
        "emoji": "🏠",
        "keywords": ["pm awas", "pmay", "housing scheme", "free house", "awas yojana", "gramin awas", "pradhan mantri awas"],
        "official_link": "https://pmaymis.gov.in",
        "online_portal": "https://pmaymis.gov.in",
        "eligibility": [
            "EWS: Annual income up to Rs 3,00,000",
            "LIG: Annual income Rs 3,00,001 to Rs 6,00,000",
            "MIG I: Annual income Rs 6,00,001 to Rs 12,00,000",
            "MIG II: Annual income Rs 12,00,001 to Rs 18,00,000",
            "Should not own a pucca house anywhere in India",
            "Woman ownership preferred (beneficiary or co-owner)"
        ],
        "documents": {
            "Mandatory": [
                "Aadhaar Card of all family members",
                "Income Certificate",
                "Bank account details (Aadhaar linked)",
                "Address Proof"
            ],
            "Property and Identity": [
                "Self-declaration of no pucca house",
                "Land ownership documents (for PMAY-G rural scheme)",
                "Ration Card / BPL Card",
                "Caste Certificate (if SC/ST/OBC)"
            ]
        },
        "steps": [
            "Check eligibility at pmaymis.gov.in",
            "Urban (PMAY-U): Apply at Urban Local Body (Municipal Corporation)",
            "Rural (PMAY-G): Apply at Gram Panchayat or Block office",
            "Submit application with documents",
            "Social survey and verification",
            "If approved, subsidy credited directly to bank account",
            "Construction to be completed within specified time"
        ],
        "fee": "Free to apply",
        "time": "3-6 months for approval",
        "benefit": "Subsidy Rs 1.5 lakh to Rs 2.67 lakh on home loan (varies by income category)",
        "extra_info": "PM Awas Yojana Gramin (rural) and Urban (cities) are separate schemes. Apply through your local body."
    },

    "e_shram": {
        "name": "e-Shram Card (Unorganised Workers)",
        "emoji": "👷",
        "keywords": ["e shram", "eshram", "labour card", "worker card", "shram card", "unorganized worker"],
        "official_link": "https://eshram.gov.in",
        "online_portal": "https://eshram.gov.in",
        "eligibility": [
            "Unorganised sector workers (construction, domestic, agriculture, etc.)",
            "Age 16-59 years",
            "Not covered under ESIC or EPFO",
            "Indian citizen"
        ],
        "documents": {
            "Mandatory": [
                "Aadhaar Card",
                "Mobile number linked to Aadhaar",
                "Bank account details"
            ]
        },
        "steps": [
            "Visit eshram.gov.in",
            "Click Register on e-Shram",
            "Enter Aadhaar number + OTP on mobile",
            "Fill occupation and bank details",
            "Download e-Shram Card (UAN number generated instantly)"
        ],
        "fee": "Free of cost",
        "benefit": "Rs 2 lakh accident insurance | Access to all future government schemes",
        "extra_info": "UAN (Universal Account Number) gives single-point access to all unorganised worker schemes."
    }
}




# ══════════════════════════════════════════════════════════════════════════════
# HINDI KEYWORDS MAP — maps Hindi speech-to-text output to service keys
# These are exactly what Google Voice Recognition returns for Hindi speech
# ══════════════════════════════════════════════════════════════════════════════

HINDI_KEYWORDS = {
    "aadhaar": [
        "आधार", "आधार कार्ड", "आधार कार्ड के लिए", "आधार बनवाना",
        "आधार नंबर", "आधार बनाना", "आधार कैसे बनाएं", "आधार अपडेट",
        "युआईडी", "यूआईडीएआई",
    ],
    "pan": [
        "पैन", "पैन कार्ड", "पेन कार्ड", "पैन कार्ड के लिए",
        "पैन कार्ड बनवाना", "परमानेंट अकाउंट नंबर", "आयकर कार्ड",
    ],
    "driving_licence": [
        "ड्राइविंग लाइसेंस", "ड्राइविंग लाईसेंस", "ड्राइविंग लाइसेन्स",
        "ड्राइविंग", "लाइसेंस", "डीएल", "लर्नर लाइसेंस",
        "वाहन लाइसेंस", "गाड़ी चलाने का लाइसेंस",
    ],
    "ration_card": [
        "राशन कार्ड", "राशन", "राशन कार्ड बनवाना", "खाद्य कार्ड",
        "बीपीएल कार्ड", "राशन कार्ड के लिए", "अन्त्योदय",
    ],
    "voter_id": [
        "वोटर आईडी", "वोटर कार्ड", "मतदाता पहचान पत्र",
        "मतदाता कार्ड", "चुनाव कार्ड", "मतदाता पंजीकरण",
    ],
    "passport": [
        "पासपोर्ट", "पासपोर्ट के लिए", "पासपोर्ट बनवाना",
        "यात्रा दस्तावेज", "विदेश यात्रा", "तत्काल पासपोर्ट",
    ],
    "birth_certificate": [
        "जन्म प्रमाण पत्र", "जन्म प्रमाणपत्र", "जन्म सर्टिफिकेट",
        "जन्म का प्रमाण", "बर्थ सर्टिफिकेट", "जन्म रजिस्ट्रेशन",
    ],
    "death_certificate": [
        "मृत्यु प्रमाण पत्र", "मृत्यु प्रमाणपत्र", "मृत्यु सर्टिफिकेट",
        "डेथ सर्टिफिकेट", "मृत्यु का प्रमाण", "मृत्यु रजिस्ट्रेशन",
    ],
    "income_certificate": [
        "आय प्रमाण पत्र", "आय प्रमाणपत्र", "आय सर्टिफिकेट",
        "आय का प्रमाण", "इनकम सर्टिफिकेट", "आमदनी प्रमाण",
    ],
    "caste_certificate": [
        "जाति प्रमाण पत्र", "जाति प्रमाणपत्र", "जाति सर्टिफिकेट",
        "जाति का प्रमाण", "एससी सर्टिफिकेट", "एसटी सर्टिफिकेट",
        "ओबीसी सर्टिफिकेट", "जाति",
    ],
    "domicile_certificate": [
        "निवास प्रमाण पत्र", "निवास प्रमाणपत्र", "मूल निवास",
        "डोमिसाइल", "निवास सर्टिफिकेट", "स्थायी निवास",
    ],
    "old_age_pension": [
        "पेंशन", "वृद्धावस्था पेंशन", "बुढ़ापा पेंशन",
        "वृद्धा पेंशन", "बुजुर्ग पेंशन", "पेंशन योजना",
        "पेंशन के लिए", "पेंशन कैसे मिलेगी",
    ],
    "widow_pension": [
        "विधवा पेंशन", "विधवा पेंशन के लिए",
    ],
    "widow_card": [
        "विधवा कार्ड", "विधवा प्रमाण पत्र", "विधवा प्रमाणपत्र",
        "विधवा सर्टिफिकेट", "विधवा",
    ],
    "pension_card": [
        "पेंशन कार्ड", "पेंशनर कार्ड", "जीवन प्रमाण",
        "लाइफ सर्टिफिकेट", "जीवन प्रमाण पत्र",
    ],
    "scholarship": [
        "छात्रवृत्ति", "स्कॉलरशिप", "छात्रवृत्ति के लिए",
        "पढ़ाई की मदद", "एजुकेशन स्कॉलरशिप", "एनएसपी",
    ],
    "ayushman_bharat": [
        "आयुष्मान भारत", "आयुष्मान कार्ड", "गोल्डन कार्ड",
        "हेल्थ कार्ड", "पीएमजेएवाई", "स्वास्थ्य कार्ड",
        "आयुष्मान", "मुफ्त इलाज",
    ],
    "pm_kisan": [
        "पीएम किसान", "किसान सम्मान निधि", "किसान योजना",
        "किसान पंजीकरण", "किसान",
    ],
    "digilocker": [
        "डिजिलॉकर", "डिजिटल लॉकर", "डिजी लॉकर",
        "ई दस्तावेज", "डिजिटल दस्तावेज",
    ],
    "marriage_certificate": [
        "विवाह प्रमाण पत्र", "विवाह प्रमाणपत्र", "शादी प्रमाण पत्र",
        "मैरिज सर्टिफिकेट", "विवाह रजिस्ट्रेशन",
    ],
    "character_certificate": [
        "चरित्र प्रमाण पत्र", "पुलिस क्लीयरेंस", "पीसीसी",
        "आचरण प्रमाण पत्र", "कैरेक्टर सर्टिफिकेट",
    ],
    "obc_certificate": [
        "ओबीसी सर्टिफिकेट", "ओबीसी एनसीएल", "नॉन क्रीमी लेयर",
        "ओबीसी प्रमाण पत्र", "अन्य पिछड़ा वर्ग",
    ],
    "ews_certificate": [
        "ईडब्ल्यूएस सर्टिफिकेट", "ईडब्ल्यूएस", "आर्थिक कमजोर वर्ग",
        "10 प्रतिशत आरक्षण",
    ],
    "land_records": [
        "खसरा", "खतौनी", "भूलेख", "जमाबंदी", "भू नक्शा",
        "जमीन के कागज", "जमीन का रिकॉर्ड", "खसरा खतौनी",
    ],
    "handicap_certificate": [
        "विकलांग प्रमाण पत्र", "दिव्यांग सर्टिफिकेट", "यूडीआईडी",
        "विकलांगता प्रमाण पत्र", "दिव्यांग कार्ड", "विकलांग",
    ],
    "senior_citizen_card": [
        "वरिष्ठ नागरिक कार्ड", "सीनियर सिटीजन कार्ड", "बुजुर्ग कार्ड",
    ],
    "bpl_card": [
        "बीपीएल कार्ड", "गरीबी रेखा कार्ड", "बीपीएल सर्टिफिकेट",
        "गरीब कार्ड", "बीपीएल",
    ],
    "pm_awas": [
        "पीएम आवास", "प्रधानमंत्री आवास", "आवास योजना",
        "मकान योजना", "पीएमएवाई", "मुफ्त मकान",
    ],
    "e_shram": [
        "ई श्रम", "ई-श्रम", "श्रम कार्ड", "मजदूर कार्ड",
        "श्रमिक कार्ड",
    ],
}

# ══════════════════════════════════════════════════════════════════════════════
# SMART RESPONSE ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def find_service(query):
    """Find best matching service — supports English + Hindi"""
    q = query.lower().strip()

    best = None
    best_score = 0

    for key, service in KNOWLEDGE_BASE.items():
        score = 0

        # ── English keywords ──────────────────────────────────
        for kw in service.get("keywords", []):
            if kw in q:
                score += len(kw) * 2

        # English service name words
        for word in service["name"].lower().split():
            if len(word) > 3 and word in q:
                score += len(word)

        # ── Hindi keywords ────────────────────────────────────
        hindi_kws = HINDI_KEYWORDS.get(key, [])
        for kw in hindi_kws:
            if kw in query:          # Use original query (preserves Unicode)
                score += len(kw) * 3  # Hindi match weighted higher (more specific)

        if score > best_score:
            best_score = score
            best = (key, service)

    if best and best_score > 0:
        return best
    return None, None


def detect_intent(message):
    """Detect what user is asking for — supports English + Hindi"""
    import re
    msg = message.lower()
    words = set(re.findall(r'[a-z]+', msg))  # English words only

    greet_en = {"hello", "hi", "namaste", "hey", "hlo", "hii", "namaskar"}
    link_words_en  = ["link", "website", "portal", "url", "site", "online"]
    elig_words_en  = ["eligible", "qualify", "criteria", "condition", "age limit", "requirement"]
    help_words_en  = ["help", "guide", "commands"]

    # Hindi intent phrases (from voice recognition)
    greet_hi  = ["नमस्ते", "हेलो", "हाय", "नमस्कार"]
    link_hi   = ["वेबसाइट", "लिंक", "पोर्टल", "साइट"]
    elig_hi   = ["योग्यता", "पात्रता", "उम्र", "आयु", "शर्त", "क्राइटेरिया"]
    help_hi   = ["मदद", "सहायता", "क्या कर सकते", "क्या-क्या"]
    docs_hi   = ["दस्तावेज", "कागज", "क्या चाहिए", "कौन से कागज",
                 "के बारे में", "बताइए", "बताओ", "जानना है",
                 "जानकारी", "कैसे बनाएं", "कैसे मिलेगा", "कैसे मिलेगी",
                 "बनवाना है", "चाहिए", "के लिए", "अप्लाई"]

    # Greeting check
    if words & greet_en and len(msg.split()) <= 3:
        return "greeting"
    for w in greet_hi:
        if w in message and len(message.split()) <= 4:
            return "greeting"

    # Help
    for w in help_words_en:
        if w in words:
            return "help"
    for w in help_hi:
        if w in message:
            return "help"

    # Link
    for w in link_words_en:
        if w in msg:
            return "link"
    for w in link_hi:
        if w in message:
            return "link"

    # Eligibility
    for w in elig_words_en:
        if w in msg:
            return "eligibility"
    for w in elig_hi:
        if w in message:
            return "eligibility"

    # Hindi docs/full info — most voice queries fall here
    for w in docs_hi:
        if w in message:
            return "full"

    return "full"


def format_full_response(service, is_hindi=False):
    """Format complete service info — bilingual English/Hindi labels"""
    L = {
        "eligibility": "पात्रता (Eligibility):" if is_hindi else "Eligibility:",
        "docs":        "जरूरी दस्तावेज:"        if is_hindi else "Documents Required:",
        "fee":         "शुल्क:"                  if is_hindi else "Fee:",
        "time":        "समय:"                    if is_hindi else "Processing Time:",
        "benefit":     "लाभ:"                    if is_hindi else "Benefit:",
        "pension":     "पेंशन राशि:"            if is_hindi else "Pension Amount:",
        "how":         "आवेदन कैसे करें:"       if is_hindi else "How to Apply:",
        "links":       "आधिकारिक लिंक:"         if is_hindi else "Official Links:",
        "note":        "नोट:"                    if is_hindi else "Note:",
        "appt":        "अपॉइंटमेंट:"            if is_hindi else "Book Appointment:",
    }
    lines = [service["emoji"] + " " + service["name"], ""]
    lines.append(L["eligibility"])
    for e in service.get("eligibility", []):
        lines.append("  * " + e)
    lines.append("")
    lines.append(L["docs"])
    for cat, docs in service.get("documents", {}).items():
        lines.append("  " + cat + ":")
        for i, d in enumerate(docs, 1):
            lines.append("    " + str(i) + ". " + d)
    lines.append("")
    if "fee" in service:
        lines.append(L["fee"] + " " + service["fee"])
    if "time" in service:
        lines.append(L["time"] + " " + service["time"])
    if "benefit" in service:
        lines.append(L["benefit"] + " " + service["benefit"])
    if "pension_amount" in service:
        lines.append(L["pension"] + " " + service["pension_amount"])
    lines.append("")
    lines.append(L["how"])
    for i, s in enumerate(service.get("steps", []), 1):
        if s.startswith("STEP") or s.startswith("  "):
            lines.append(s)
        else:
            lines.append(str(i) + ". " + s)
    lines.append("")
    lines.append(L["links"])
    lines.append("  -> " + service["official_link"])
    if "online_portal" in service and service["online_portal"] != service["official_link"]:
        lines.append("  -> " + service["online_portal"])
    if "appointment" in service:
        lines.append("  -> " + L["appt"] + " " + service["appointment"])
    if "extra_info" in service:
        lines.append("")
        lines.append(L["note"] + " " + service["extra_info"])
    return "\n".join(lines)


def get_ai_response(message, context=None, history=None):
    """
    Main function — pure local knowledge base, no API needed
    """
    context = context or {}
    msg = message.lower().strip()

    service_key, service = find_service(message)
    intent = detect_intent(message)

    # Detect if query is Hindi
    is_hindi = any(ord(c) >= 0x0900 and ord(c) <= 0x097F for c in message)

    # Greeting
    if intent == "greeting":
        if is_hindi:
            return ("नमस्ते! मैं सहायक AI हूँ। 🙏\n\n"
                    "मैं इन सेवाओं की पूरी जानकारी दे सकता हूँ:\n\n"
                    "आधार कार्ड | पैन कार्ड | ड्राइविंग लाइसेंस | राशन कार्ड\n"
                    "वोटर आईडी | पासपोर्ट | जन्म प्रमाण पत्र | मृत्यु प्रमाण पत्र\n"
                    "आय प्रमाण पत्र | जाति प्रमाण पत्र | निवास प्रमाण पत्र\n"
                    "पेंशन | विधवा पेंशन | छात्रवृत्ति | आयुष्मान भारत | पीएम किसान\n\n"
                    "बोलिए: \'आधार कार्ड के लिए दस्तावेज\' या \'पेंशन कैसे मिलेगी\'")
        return ("Namaste! I am Sahayak AI.\n\n"
                "I can give you complete information about:\n\n"
                "Aadhaar | PAN Card | Driving Licence | Ration Card | Voter ID | Passport\n"
                "Birth Certificate | Death Certificate | Income / Caste / Domicile Certificate\n"
                "Old Age Pension | Widow Pension | Scholarship | Ayushman Bharat | PM Kisan\n"
                "DigiLocker | e-Shram Card | BPL Card | EWS | OBC NCL | PM Awas\n\n"
                "Just ask: \'documents for aadhaar\' or \'how to apply for pension\'")

    # Help
    if intent == "help":
        services = " | ".join([v["emoji"] + " " + v["name"] for v in KNOWLEDGE_BASE.values()])
        if is_hindi:
            return ("मैं इन सेवाओं में मदद कर सकता हूँ:\n\n" + services +
                    "\n\nऐसे पूछें:\n"
                    "-> 'आधार कार्ड के लिए दस्तावेज'\n"
                    "-> 'पेंशन कैसे मिलेगी'\n"
                    "-> 'राशन कार्ड बनवाना है'\n"
                    "-> 'छात्रवृत्ति के लिए क्या चाहिए'")
        return ("I have complete information about:\n\n" + services +
                "\n\nAsk me:\n"
                "-> 'documents for aadhaar'\n"
                "-> 'how to apply for old age pension'\n"
                "-> 'link for scholarship'\n"
                "-> 'eligibility for PM Kisan'")

    # Service found
    if service:
        if intent == "link":
            lines = [service["emoji"] + " " + service["name"] + " — Official Links:", ""]
            if is_hindi:
                lines = [service["emoji"] + " " + service["name"] + " — आधिकारिक लिंक:", ""]
            lines.append("Main Portal: " + service["official_link"])
            if "online_portal" in service and service["online_portal"] != service["official_link"]:
                lines.append("Online Services: " + service["online_portal"])
            if "appointment" in service:
                lines.append("Book Appointment: " + service["appointment"])
            return "\n".join(lines)

        if intent == "eligibility":
            if is_hindi:
                lines = [service["emoji"] + " " + service["name"] + " — पात्रता (Eligibility):", ""]
            else:
                lines = [service["emoji"] + " " + service["name"] + " — Eligibility:", ""]
            for e in service.get("eligibility", []):
                lines.append("* " + e)
            if "fee" in service:
                label = "\nशुल्क (Fee): " if is_hindi else "\nFee: "
                lines.append(label + service["fee"])
            label = "\nआवेदन करें: " if is_hindi else "\nApply at: "
            lines.append(label + service["official_link"])
            return "\n".join(lines)

        return format_full_response(service, is_hindi)

    # Score query
    if any(w in msg for w in ["score", "fields", "filled", "status"]):
        filled = context.get("filled", 0)
        total = context.get("total", 0)
        form_label = context.get("formLabel", "this form")
        if total > 0:
            return "Your score: " + str(filled) + "/" + str(total) + " fields filled on " + str(form_label) + "."
        return "No form fields detected yet."

    # List all services
    if any(w in msg for w in ["all", "list", "services", "kya", "what services"]):
        return ("Complete list of services I can help with:\n\n" +
                "\n".join([v["emoji"] + " " + v["name"] for v in KNOWLEDGE_BASE.values()]) +
                "\n\nAsk about any one for full documents + link!")

    # Default — bilingual
    names = " | ".join([v["name"] for v in list(KNOWLEDGE_BASE.values())[:6]])
    if is_hindi:
        return ("मैं इन सेवाओं में मदद कर सकता हूँ:\n" + names + " और भी...\n\n"
                "ऐसे पूछें: 'आधार कार्ड के लिए दस्तावेज' या 'पेंशन कैसे मिलेगी'\n"
                "'मदद' टाइप करें सभी सेवाएं देखने के लिए।")
    return ("I can help with: " + names + " and more.\n\n"
            "Try asking: 'documents for aadhaar' or 'how to apply for pension'\n"
            "Type 'help' to see all available services.")


# ══════════════════════════════════════════════════════════════════════════════
# Legacy class — kept for compatibility with app.py
# ══════════════════════════════════════════════════════════════════════════════

class AdvancedAIChatbot:
    def __init__(self):
        self.conversation_history = []
        self.context = {}

    def get_response(self, user_message, context=None, history=None):
        if context:
            self.context.update(context)
        return get_ai_response(user_message, self.context, history)

    def train_from_conversations(self, conversations):
        return {"status": "ok", "conversations": len(conversations)}


chatbot = AdvancedAIChatbot()


def train_model(training_data):
    return chatbot.train_from_conversations(training_data)