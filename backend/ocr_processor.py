"""
OCR Processor Module
Processes uploaded documents (images, PDFs) and extracts text
Uses Tesseract OCR and PIL
"""

import pytesseract
from PIL import Image
import io
import re
import logging
import time
# from pdf2image import convert_from_bytes  # Disabled - install Poppler if needed
PDF_SUPPORT = False

def process_pdf(pdf_bytes):
    return "PDF not supported. Please convert to image (JPG/PNG) and upload."

logger = logging.getLogger(__name__)

# Configure Tesseract path. On Windows the binary usually isn't on PATH, so
# point pytesseract at the default install location if it exists there.
# On Linux/Mac, `tesseract` is normally already on PATH after installation,
# so we leave pytesseract's default alone (hardcoding the Windows path
# unconditionally used to break OCR on every non-Windows machine).
import platform as _platform
if _platform.system() == 'Windows':
    import os as _os
    _WIN_TESSERACT_PATHS = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    ]
    for _p in _WIN_TESSERACT_PATHS:
        if _os.path.exists(_p):
            pytesseract.pytesseract.tesseract_cmd = _p
            break

def process_document(file):
    """
    Process uploaded document with OCR
    
    Args:
        file: FileStorage object from Flask request.files
    
    Returns:
        Dictionary with extracted data and confidence
    """
    start_time = time.time()
    
    try:
        file_bytes = file.read()
        filename = file.filename.lower()
        
        # Determine file type
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            text = process_image(file_bytes)
        elif filename.endswith('.pdf'):
            text = process_pdf(file_bytes)
        elif filename.endswith('.txt'):
            text = file_bytes.decode('utf-8', errors='ignore')
        else:
            raise ValueError(f"Unsupported file type: {filename}")
        
        # Extract structured data from text
        extracted_data = extract_data_from_text(text)
        
        # Calculate confidence (simple heuristic)
        confidence = calculate_confidence(extracted_data, text)
        
        processing_time = round(time.time() - start_time, 2)
        
        return {
            'data': extracted_data,
            'confidence': confidence,
            'raw_text': text[:500],  # First 500 chars
            'processing_time': processing_time
        }
        
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        raise

def process_image(image_bytes):
    """
    Extract text from image using OCR
    """
    try:
        # Open image from bytes
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Preprocess image for better OCR
        # (Could add: resize, denoise, threshold, etc.)
        
        # Run OCR
        text = pytesseract.image_to_string(image, lang='eng+hin')
        
        return text
        
    except Exception as e:
        logger.error(f"Error in OCR processing: {e}")
        raise

def process_pdf(pdf_bytes):
    """
    Extract text from PDF
    PDF processing disabled - install Poppler and pdf2image to enable
    """
    return "PDF processing not available. Please install Poppler and pdf2image.\nFor now, please convert PDF to image and upload the image instead."

def extract_data_from_text(text):
    """
    Extract structured data from OCR text
    Uses regex patterns to find: Aadhar, PAN, phone, email, etc.
    """
    data = {}
    
    # Aadhar number (12 digits, may have spaces)
    aadhar_pattern = r'\b\d{4}\s?\d{4}\s?\d{4}\b'
    aadhar_match = re.search(aadhar_pattern, text)
    if aadhar_match:
        data['aadhar'] = aadhar_match.group().replace(' ', '')
    
    # PAN card (ABCDE1234F format)
    pan_pattern = r'\b[A-Z]{5}\d{4}[A-Z]\b'
    pan_match = re.search(pan_pattern, text)
    if pan_match:
        data['pan'] = pan_match.group()
    
    # Mobile number (10 digits starting with 6-9)
    mobile_pattern = r'\b[6-9]\d{9}\b'
    mobile_match = re.search(mobile_pattern, text)
    if mobile_match:
        data['mobile'] = mobile_match.group()
    
    # Email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, text)
    if email_match:
        data['email'] = email_match.group()
    
    # Name (look for "Name:" keyword)
    name_patterns = [
        r'Name\s*:?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
        r'(?:Full Name|Name of Applicant)\s*:?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)'
    ]
    for pattern in name_patterns:
        name_match = re.search(pattern, text, re.IGNORECASE)
        if name_match:
            data['name'] = name_match.group(1).strip()
            break
    
    # Date of Birth
    dob_patterns = [
        r'(?:DOB|Date of Birth|D\.O\.B\.?)\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{4})\b'
    ]
    for pattern in dob_patterns:
        dob_match = re.search(pattern, text, re.IGNORECASE)
        if dob_match:
            data['dob'] = dob_match.group(1)
            # Calculate age
            try:
                from datetime import datetime
                dob_parts = re.split(r'[/-]', data['dob'])
                year = int(dob_parts[2]) if len(dob_parts[2]) == 4 else int('19' + dob_parts[2])
                age = datetime.now().year - year
                data['age'] = str(age)
            except:
                pass
            break
    
    # Age (direct mention)
    if 'age' not in data:
        age_pattern = r'Age\s*:?\s*(\d{1,3})'
        age_match = re.search(age_pattern, text, re.IGNORECASE)
        if age_match:
            data['age'] = age_match.group(1)
    
    # Gender
    gender_pattern = r'(?:Gender|Sex)\s*:?\s*(Male|Female|Other|M|F)'
    gender_match = re.search(gender_pattern, text, re.IGNORECASE)
    if gender_match:
        gender = gender_match.group(1).lower()
        if gender.startswith('m'):
            data['gender'] = 'male'
        elif gender.startswith('f'):
            data['gender'] = 'female'
        else:
            data['gender'] = 'other'
    
    # Address
    address_pattern = r'(?:Address|Permanent Address)\s*:?\s*([^.;]{20,150})'
    address_match = re.search(address_pattern, text, re.IGNORECASE | re.DOTALL)
    if address_match:
        data['address'] = address_match.group(1).strip()
    
    # Income
    income_pattern = r'(?:Income|Annual Income)\s*:?\s*₹?\s*([\d,]+)'
    income_match = re.search(income_pattern, text, re.IGNORECASE)
    if income_match:
        data['income'] = income_match.group(1).replace(',', '')
    
    # Bank account
    account_pattern = r'(?:Account|A/c|Account Number)\s*:?\s*(\d{9,18})'
    account_match = re.search(account_pattern, text, re.IGNORECASE)
    if account_match:
        data['account_number'] = account_match.group(1)
    
    # IFSC code
    ifsc_pattern = r'\b([A-Z]{4}0[A-Z0-9]{6})\b'
    ifsc_match = re.search(ifsc_pattern, text)
    if ifsc_match:
        data['ifsc'] = ifsc_match.group(1)
    
    return data

def calculate_confidence(extracted_data, original_text):
    """
    Calculate confidence score based on:
    - Number of fields extracted
    - Pattern match quality
    - Text clarity
    """
    # Base confidence
    confidence = 0.5
    
    # Add points for each extracted field
    field_count = len(extracted_data)
    confidence += min(field_count * 0.05, 0.3)
    
    # Check for high-confidence patterns
    if 'aadhar' in extracted_data:
        confidence += 0.1
    if 'pan' in extracted_data:
        confidence += 0.1
    
    # Check text length (longer text usually means better scan)
    if len(original_text) > 200:
        confidence += 0.1
    
    # Cap at 1.0
    return min(confidence, 1.0)

def extract_document_type(text):
    """
    Identify what type of document this is
    """
    text_lower = text.lower()
    
    if 'aadhar' in text_lower or 'uidai' in text_lower:
        return 'aadhar_card'
    elif 'pan' in text_lower and 'income tax' in text_lower:
        return 'pan_card'
    elif 'driving' in text_lower and 'license' in text_lower:
        return 'driving_license'
    elif 'voter' in text_lower and ('id' in text_lower or 'identity' in text_lower):
        return 'voter_id'
    elif 'birth' in text_lower and 'certificate' in text_lower:
        return 'birth_certificate'
    elif 'income' in text_lower and 'certificate' in text_lower:
        return 'income_certificate'
    else:
        return 'unknown'


def normalize_field_key(key):
    """Normalize OCR field keys — handles spelling variants, typos, abbreviations."""
    import re
    k = (key or '').lower().strip()
    # Phone / Mobile
    k = re.sub(r'\bph\.?\s*no\.?\b',              'mobile number', k)
    k = re.sub(r'\bph\.?\s*num(ber)?\b',           'mobile number', k)
    k = re.sub(r'\bphn\.?\b',                      'mobile number', k)
    k = re.sub(r'\bph[ao]ne?\b',                   'phone', k)
    k = re.sub(r'\bphono\b',                       'phone', k)
    k = re.sub(r'\bmob\.?\s*no\.?\b',              'mobile number', k)
    k = re.sub(r'\bmob\.?\s*num(ber)?\b',          'mobile number', k)
    k = re.sub(r'\bm[ou]b[iy]l[ae]?\b',            'mobile', k)
    k = re.sub(r'\bcontact\s*(no\.?|num(ber)?)?\b','mobile number', k)
    k = re.sub(r'\bcell\s*(no\.?|num(ber)?)?\b',   'mobile number', k)
    k = re.sub(r'\bwhatsapp\s*(no\.?|num(ber)?)?\b','mobile number', k)
    k = re.sub(r'\btel\.?\s*(no\.?|num(ber)?)?\b', 'phone number', k)
    k = re.sub(r'\bteleph[ao]ne?\b',               'phone', k)
    # Aadhaar
    k = re.sub(r'\baadh?[aeu]{1,2}r\b',  'aadhaar', k)
    k = re.sub(r'\badh[aeu]{1,2}r\b',    'aadhaar', k)
    k = re.sub(r'\baadhar\b',            'aadhaar', k)
    k = re.sub(r'\badhar\b',             'aadhaar', k)
    k = re.sub(r'\baadh\b',             'aadhaar', k)
    k = re.sub(r'\buid[ai]?\s*(no\.?|num(ber)?)?\b','aadhaar number', k)
    # PAN
    k = re.sub(r'\bpan\s*c[ae]rd\b',             'pan card', k)
    k = re.sub(r'\bpan\s*(no\.?|num(ber)?)\b',   'pan number', k)
    k = re.sub(r'\bperman[ae]nt\s*acc[ao]unt\s*(num(ber)?)?\b', 'pan number', k)
    # IFSC
    k = re.sub(r'\bif[sc]{2}\b',   'ifsc', k)
    k = re.sub(r'\bifcs\b',        'ifsc', k)
    k = re.sub(r'\bisfc\b',        'ifsc', k)
    k = re.sub(r'\bbank\s*c[ao]de\b', 'ifsc code', k)
    k = re.sub(r'\brtgs\s*c[ao]de\b', 'ifsc code', k)
    # Account
    k = re.sub(r'\bacc[ao]unt\b',                  'account', k)
    k = re.sub(r'\bacct?\.?\b',                    'account', k)
    k = re.sub(r'\bacc\.?\s*(no\.?|num(ber)?)\b',  'account number', k)
    k = re.sub(r'\bbank\s*acc(ount)?\b',            'account', k)
    # Email
    k = re.sub(r'\be[-\s]?m[ae][iy]l\b', 'email', k)
    k = re.sub(r'\bemeil\b',             'email', k)
    k = re.sub(r'\bemail\s*[iy]d\b',     'email', k)
    # DOB
    k = re.sub(r'\bdate\s*of\s*br[iy]th\b', 'date of birth', k)
    k = re.sub(r'\bdate\s*of\s*birt?h?\b',  'date of birth', k)
    k = re.sub(r'\bd\.?o\.?b\.?\b',         'date of birth', k)
    k = re.sub(r'\bbirth\s*d[ae]te\b',      'date of birth', k)
    k = re.sub(r'\bbirthd[ae]y\b',          'date of birth', k)
    k = re.sub(r'\bjanm\s*(tithi|date)?\b', 'date of birth', k)
    # Names
    k = re.sub(r"\bfather[\s']*s?\s*n[ae]m[ae]\b", "father's name", k)
    k = re.sub(r"\bmother[\s']*s?\s*n[ae]m[ae]\b", "mother's name", k)
    k = re.sub(r'\bf[au]ll\s*n[ae]m[ae]\b',        'full name', k)
    k = re.sub(r'\bpita\s*(ka\s*)?n[ae]am?\b',     "father's name", k)
    k = re.sub(r'\bmata\s*(ka\s*)?n[ae]am?\b',     "mother's name", k)
    k = re.sub(r'\bn[ae]am?\b',                    'name', k)
    # Address
    k = re.sub(r'\bperm[ae]n[ae]nt\s*addr[ae]s{1,2}\b', 'permanent address', k)
    k = re.sub(r'\bpres[ae]nt\s*addr[ae]s{1,2}\b',      'present address', k)
    k = re.sub(r'\baddr[ae]s{1,2}\b', 'address', k)
    k = re.sub(r'\bpata\b',           'address', k)
    # Pincode
    k = re.sub(r'\bpin\s*c[ao]de\b',        'pin code', k)
    k = re.sub(r'\bpinc[ao]de\b',           'pin code', k)
    k = re.sub(r'\bpost[ae]l\s*(c[ao]de)?\b','pin code', k)
    k = re.sub(r'\bzip\s*(c[ao]de)?\b',     'pin code', k)
    # Other
    k = re.sub(r'\bs[ae]x\b',              'gender', k)
    k = re.sub(r'\bc[ae]t[ae]g[ao]ry\b',  'category', k)
    k = re.sub(r'\bjati\b',               'caste', k)
    k = re.sub(r'\b[ae]nn?u[ae]l\s*[iy]nc[ao]me\b', 'annual income', k)
    k = re.sub(r'\bb[ae]nk\s*n[ae]m[ae]\b', 'bank name', k)
    k = re.sub(r'\bjila\b',               'district', k)
    return k


def extract_smart_data(text):
    import re
    from datetime import datetime
    data = {}

    def is_english(line):
        s = line.strip()
        if not s: return False
        return sum(1 for c in s if ord(c) < 128) / len(s) > 0.55

    eng_lines = [l.strip() for l in text.split('\n') if is_english(l)]
    t = '\n'.join(eng_lines)
    full = text

    # ── Detect document type ──────────────────────────────────────────
    is_passbook = bool(re.search(r'Account\s*(?:No|Number|Particulars)|IFSC|MICR|Mode of Operation|खाता', full, re.IGNORECASE))
    is_pan      = bool(re.search(r'PAN\s*CARD|Pan\s*Number|Permanent\s*Account', full, re.IGNORECASE))
    is_aadhaar  = bool(re.search(r'Aadhaar|UIDAI|Unique Identification|आधार|Enrollment No|Your.*No\.\s*:\s*\d{4}', full, re.IGNORECASE))

    # ── GENERIC KEY-VALUE PARSER (handles WhatsApp/typed text) ───────────
    # Matches: "Name : Mata Rani", "Father's name : Ram Prasad" etc.
    KV_MAP = [
        ('name',           [r'(?:full\s*)?name', r'naam', r'नाम']),
        ('father_name',    [r'father[\'s]*\s*name', r'father[\'s]*\s*naam', r'पिता']),
        ('mother_name',    [r'mother[\'s]*\s*name', r'mother[\'s]*\s*naam', r'माता']),
        ('email',          [r'e?-?mail(?:\s*id)?(?:\s*address)?']),
        ('mobile',         [r'mobile(?:\s*no\.?|\s*number)?(?:\s*no\.?)?'
                            , r'phone(?:\s*no\.?|\s*number)?'
                            , r'contact(?:\s*no\.?|\s*number)?'
                            , r'mob(?:\s*no\.?)?', r'मोबाइल']),
        ('address',        [r'(?:permanent\s*)?address', r'(?:present\s*)?address', r'पता']),
        ('account_number', [r'account\s*no\.?', r'account\s*number', r'acc\s*no\.?', r'खाता\s*(?:संख्या)?']),
        ('ifsc',           [r'ifsc(?:\s*code)?', r'bank\s*code']),
        ('pan',            [r'pan(?:\s*(?:no|number|card))?']),
        ('aadhar',         [r'aadh?aar?(?:\s*(?:no\.?|number))?', r'adhaar(?:\s*(?:no\.?|number))?', r'uid(?:\s*number)?']),
        ('dob',            [r'd\.?o\.?b\.?', r'date\s*of\s*birth', r'birth\s*date', r'date\s*of\s*brith', r'जन्म\s*तिथि']),
        ('father_name',    [r's/o', r'c/o']),
        ('bank_name',      [r'bank(?:\s*name)?']),
        ('pincode',        [r'pin(?:\s*code)?', r'postal(?:\s*code)?']),
        ('state',          [r'state']),
        ('district',       [r'district']),
        ('gender',         [r'gender', r'sex']),
        ('caste',          [r'caste', r'category']),
        ('income',         [r'(?:annual\s*)?income']),
        ('occupation',     [r'occupation', r'profession']),
    ]

    for line in eng_lines:
        # Match "Key : Value" or "Key - Value" or "Key = Value"
        m = re.match(r'^(.{2,35})\s*[:\-=]\s*(.+)$', line.strip())
        if not m: continue
        key_raw = normalize_field_key(m.group(1).strip())
        val_raw = m.group(2).strip()
        if not val_raw or len(val_raw) < 1: continue

        for field, patterns in KV_MAP:
            if field in data: continue  # already found
            for pat in patterns:
                if re.fullmatch(pat, key_raw, re.IGNORECASE):
                    # Validate value type
                    if field in ('mobile',):
                        clean = re.sub(r'[^\d]', '', val_raw)
                        if not re.match(r'[6-9]\d{9}$', clean):
                            continue
                        val_raw = clean
                    if field == 'email' and '@' not in val_raw:
                        continue
                    if field == 'account_number' and not re.match(r'\d{6,18}$', val_raw.replace(' ','')):
                        continue
                    if field == 'aadhar':
                        val_clean = re.sub(r'[\s-]', '', val_raw)
                        if re.match(r'^\d{12}$', val_clean):
                            data[field] = val_clean
                        # Strictly reject anything not exactly 12 digits — do NOT store partial
                        continue
                    if field == 'dob' and re.search(r'\d', val_raw):
                        data[field] = val_raw
                        try:
                            parts = re.split(r'[/\-\.]', val_raw.strip())
                            if len(parts) == 3:
                                # Handle D/M/YYYY or M/D/YYYY
                                yr = int(parts[2]) if len(parts[2]) == 4 else int(parts[0]) if len(parts[0]) == 4 else None
                                if yr and 1900 < yr < 2100:
                                    age = datetime.now().year - yr
                                    # Adjust if birthday hasn't occurred this year
                                    data['age'] = str(max(0, age))
                            elif len(parts) == 1:
                                yr = int(parts[0])
                                if 1900 < yr < 2100:
                                    data['age'] = str(datetime.now().year - yr)
                        except: pass
                        continue
                    if field == 'gender':
                        g = val_raw.lower()
                        data[field] = 'male' if 'male' in g or 'm' == g else 'female' if 'female' in g else val_raw.lower()
                        continue
                    # Clean junk chars (©, emoji, watermarks) from value
                    val_clean = re.sub(r'[©®™✓•·|\\\\]', '', val_raw).strip()
                    val_clean = re.sub(r'\s+', ' ', val_clean).strip()
                    data[field] = val_clean.title() if field in ('name','father_name','mother_name','address','bank_name','state','district','occupation','caste') else val_clean
                    break

    # ── Post-process: fix mobile/account confusion ──────────────────────
    if data.get('mobile') and data.get('account_number'):
        if data['mobile'] == data['account_number']:
            del data['mobile']  # remove wrong mobile

    # ── PAN Number (any doc) ──────────────────────────────────────────
    if 'pan' not in data:
        m = re.search(r'\b([A-Z]{5}\d{4}[A-Z])\b', t)
        if m: data['pan'] = m.group(1)

    # ── Email (any doc) ───────────────────────────────────────────────
    if 'email' not in data:
        m = re.search(r'\b([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})\b', t)
        if m: data['email'] = m.group(1)

    # ── Mobile (any doc) ─────────────────────────────────────────────
    if 'mobile' not in data:
        m = re.search(r'\b([6-9]\d{9})\b', full)
        if m: data['mobile'] = m.group(1)

    # ════════════════════════════════════════════════════════════════
    # PAN CARD
    # ════════════════════════════════════════════════════════════════
    if is_pan:
        if 'name' not in data:
            m = re.search(r'Name\s*[:/]\s*([A-Za-z ]+?)(?:\n|$)', t, re.IGNORECASE|re.MULTILINE)
            if m:
                raw = m.group(1).strip()
                skip = ['CARD','NUMBER','GENDER','DOB','PERMANENT','ACCOUNT','DIGILOCKER']
                if not any(s in raw.upper() for s in skip) and len(raw) > 3:
                    data['name'] = raw.title()
        if 'dob' not in data:
            m = re.search(r'DOB\s*[:/]\s*(\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4})', t, re.IGNORECASE)
            if m:
                data['dob'] = m.group(1)
                try:
                    parts = re.split(r'[-/\.]', data['dob'])
                    yr = int(parts[2]) if len(parts[2]) == 4 else int('19' + parts[2])
                    data['age'] = str(datetime.now().year - yr)
                except: pass
        if 'gender' not in data:
            m = re.search(r'Gender\s*[:/]\s*(MALE|FEMALE|Male|Female)', t, re.IGNORECASE)
            if m: data['gender'] = m.group(1).lower()
        if 'father_name' not in data:
            m = re.search(r"Father'?s?\s*Name\s*[:/]\s*([A-Za-z\s]{2,35})", t, re.IGNORECASE)
            if m: data['father_name'] = m.group(1).strip().title()

    # ════════════════════════════════════════════════════════════════
    # PASSBOOK
    # ════════════════════════════════════════════════════════════════
    if is_passbook:
        if 'account_number' not in data:
            m = re.search(r'[Aa]ccount\s*No[^\n]{0,10}(\d{9,18})', full, re.IGNORECASE)
            if m:
                num = m.group(1)
                if not re.match(r'^[6-9]\d{9}$', num):
                    data['account_number'] = num
        if 'ifsc' not in data:
            m = re.search(r'IFSC[^\n]{0,20}([A-Z]{4}0[A-Z0-9]{6})', full, re.IGNORECASE)
            if m: data['ifsc'] = m.group(1)
        if 'micr' not in data:
            m = re.search(r'MICR\s*(?:Code)?\s*[:/]?\s*(\d{9})', full, re.IGNORECASE)
            if m: data['micr'] = m.group(1)
        banks = [
            ('Punjab National Bank', r'Punjab.National.Bank|PNB\b|PUNB'),
            ('State Bank of India', r'State.Bank.of.India|SBI\b|SBIN'),
            ('Bank of Baroda', r'Bank.of.Baroda|BARB'),
            ('Canara Bank', r'Canara.Bank|CNRB'),
            ('Union Bank of India', r'Union.Bank|UBIN'),
            ('HDFC Bank', r'HDFC.Bank|HDFC\b'),
            ('ICICI Bank', r'ICICI.Bank|ICIC\b'),
            ('Axis Bank', r'Axis.Bank|UTIB'),
            ('Bank of India', r'Bank.of.India|BKID'),
            ('Indian Bank', r'Indian.Bank|IDIB'),
            ('UCO Bank', r'UCO.Bank|UCBA'),
            ('Central Bank of India', r'Central.Bank|CBIN'),
        ]
        if 'bank_name' not in data:
            for bname, pat in banks:
                if re.search(pat, full, re.IGNORECASE):
                    data['bank_name'] = bname
                    break
        if 'name' not in data:
            for pat in [
                r'(?:SHRI|SMT|KUM|MR|MRS|MS)\.?\s+([A-Z][A-Z\s]{3,35})',
                r'[Aa]ccount\s*No[^\n]*\n\s*([A-Z][A-Z\s]{3,35})\n',
            ]:
                m = re.search(pat, full, re.IGNORECASE)
                if m:
                    raw = m.group(1).strip()
                    skip = ['SELF','INDIA','BANK','ACCOUNT','BRANCH','IFSC',
                            'MICR','MODE','OPERATION','CUSTOMER','NOMINATION']
                    if len(raw) > 4 and not any(s in raw.upper() for s in skip):
                        data['name'] = raw.title()
                        break
        if 'mobile' not in data:
            for m in re.finditer(r'\b([6-9]\d{9})\b', full):
                if m.group(1) != data.get('account_number',''):
                    data['mobile'] = m.group(1)
                    break
        if 'pincode' not in data:
            m = re.search(r'Pin\s*[:/]?\s*(\d{6})', full, re.IGNORECASE)
            if not m: m = re.search(r'\b(\d{6})\b', full)
            if m: data['pincode'] = m.group(1)
        if 'state' not in data:
            states = ['Odisha','Orissa','Chhattisgarh','Maharashtra','Delhi',
                      'Uttar Pradesh','Madhya Pradesh','Bihar','Rajasthan',
                      'Gujarat','Karnataka','Tamil Nadu','West Bengal',
                      'Andhra Pradesh','Telangana','Kerala','Punjab',
                      'Haryana','Jharkhand','Assam','Uttarakhand','Goa']
            for state in states:
                if state.lower() in full.lower():
                    data['state'] = state
                    break

    # ════════════════════════════════════════════════════════════════
    # AADHAAR
    # ════════════════════════════════════════════════════════════════
    if is_aadhaar or (not is_passbook and not is_pan):
        if 'aadhar' not in data:
            for m in re.finditer(r'\b(\d{4}\s?\d{4}\s?\d{4})\b', full):
                num = m.group(1).replace(' ', '')
                if not re.match(r'^[6-9]\d{9}$', num):
                    data['aadhar'] = num
                    break
        to_m = re.search(r'(?:^|\n)To\s*\n((?:[ \t]*[^\n]*\n){2,15})', t, re.IGNORECASE)
        if to_m:
            block_lines = [l.strip() for l in to_m.group(1).split('\n') if l.strip()]
            addr_skip = ['government','authority','india','unique','identification',
                         'enrollment','aadhaar','aadhar','signature','valid']
            addr_lines = []
            name_done = 'name' in data
            father_done = False  # always scan for name even if father already found via KV
            for line in block_lines:
                so = re.match(r'^(?:S/O|C/O|D/O)\s*[:/]?\s*(.+)$', line, re.IGNORECASE)
                if so:
                    if 'father_name' not in data:
                        data['father_name'] = so.group(1).strip().title()
                    father_done = True
                    continue
                if not name_done and not father_done:
                    # A valid name: 2-4 Title Case words, only letters and spaces
                    # Must have at least 2 words (first + last name)
                    # Reject: single words, ALL CAPS garbage, OCR noise with digits/symbols
                    is_valid_name = bool(re.match(
                        r'^[A-Z][a-z]{1,20}(\s[A-Z][a-z]{1,20}){1,3}$', line
                    ))
                    has_garbage = bool(re.search(r'[^A-Za-z\s]', line))  # digits/symbols
                    is_all_caps_short = bool(re.match(r'^[A-Z0-9\s]{1,15}$', line) and len(line.replace(' ','')) < 10)
                    is_single_word = len(line.split()) == 1

                    if is_valid_name and not has_garbage and not any(kw in line.lower() for kw in addr_skip):
                        data['name'] = line
                        name_done = True
                        continue
                    # Skip garbage/noise lines — don't add to address either
                    if has_garbage or is_all_caps_short or is_single_word:
                        continue
                if father_done:
                    # Stop address at phone, pincode, DOB, aadhaar number, gender keywords
                    if re.match(r'^[6-9]\d{9}$', line): break
                    if re.match(r'^\d{4}\s?\d{4}\s?\d{4}$', line): break  # aadhaar number
                    if re.match(r'^\d{12}$', line): break
                    if re.match(r'^(MALE|FEMALE)$', line, re.IGNORECASE): break
                    if re.match(r'^\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}$', line): break  # DOB line
                    if re.search(r'DOB|Date of Birth', line, re.IGNORECASE): break
                    if re.match(r'^\d{6}$', line):
                        data['pincode'] = line
                        break
                    # Stop if line has 6-digit pin embedded
                    pin_m = re.search(r'\b(\d{6})\b', line)
                    if pin_m:
                        data['pincode'] = pin_m.group(1)
                        # Still add this line to address (it has city info)
                        if not any(kw in line.lower() for kw in addr_skip):
                            addr_lines.append(line)
                        break
                    if not any(kw in line.lower() for kw in addr_skip):
                        addr_lines.append(line)
            if addr_lines and 'address' not in data:
                data['address'] = ', '.join(addr_lines)
        if 'father_name' not in data:
            for pat in [
                r'S/O\s*[:/]?\s*([A-Z][a-z]{2,15}(?:\s[A-Z][a-z]{2,15}){1,3})',
                r'Father\s*[:/]\s*([A-Z][A-Z\s]{4,40})',
            ]:
                m = re.search(pat, t, re.IGNORECASE)
                if m:
                    c = m.group(1).strip().title()
                    if c != data.get('name', ''): 
                        data['father_name'] = c
                        break
        if 'mother_name' not in data:
            m = re.search(r"(?:Mother'?s?\s*Name|W/O|माता)\s*[:/]?\s*([A-Z][a-z]{2,15}(?:\s[A-Z][a-z]{2,15}){1,3})", t, re.IGNORECASE)
            if m:
                c = m.group(1).strip().title()
                if c != data.get('name', ''): data['mother_name'] = c
        if 'gender' not in data:
            if re.search(r'\bMALE\b', full): data['gender'] = 'male'
            elif re.search(r'\bFEMALE\b', full): data['gender'] = 'female'
        if 'pincode' not in data:
            m = re.search(r'\b(\d{6})\b', full)
            if m: data['pincode'] = m.group(1)
        if 'state' not in data:
            states = ['Chhattisgarh','Maharashtra','Delhi','Uttar Pradesh',
                      'Madhya Pradesh','Bihar','Rajasthan','Gujarat','Karnataka',
                      'Tamil Nadu','West Bengal','Andhra Pradesh','Telangana',
                      'Kerala','Punjab','Haryana','Odisha','Jharkhand','Assam',
                      'Uttarakhand','Himachal Pradesh','Goa']
            for state in states:
                if state.lower() in full.lower():
                    data['state'] = state
                    break

    # ── DOB / Age ─────────────────────────────────────────────────────────
    if 'dob' not in data:
        dob_text = re.sub(r'(?:Account\s*Open\s*Date|Issue\s*Date|Date\s*of\s*Issue)[^\n]*', '', full, flags=re.IGNORECASE)
        for pat in [
            r'(?:DOB|Date of Birth|D\.O\.B)\s*[:/]?\s*(\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4})',
            r'\b(\d{2}/\d{2}/\d{4})\b',
        ]:
            m = re.search(pat, dob_text, re.IGNORECASE)
            if m:
                data['dob'] = m.group(1)
                try:
                    parts = re.split(r'[-/\.]', data['dob'])
                    yr = int(parts[2]) if len(parts[2]) == 4 else int('19' + parts[2])
                    data['age'] = str(datetime.now().year - yr)
                except: pass
                break

    # ── Final cleanup: remove mobile if same as account number ──────────
    if data.get('mobile') and data.get('account_number'):
        if data['mobile'] == data['account_number']:
            del data['mobile']

    # ── Blood Group ───────────────────────────────────────────────────────
    m = re.search(r'\b(A|B|AB|O)[+-]\b', full)
    if m: data['blood_group'] = m.group(0)

    # ── Caste ─────────────────────────────────────────────────────────────
    if 'caste' not in data:
        m = re.search(r'(?:Category|Caste)\s*[:/]?\s*(General|OBC|SC|ST|EWS)', t, re.IGNORECASE)
        if m: data['caste'] = m.group(1).upper()

    # ── Marks ─────────────────────────────────────────────────────────────
    m = re.search(r'(?:10th|SSC|Matriculation).*?(?:Marks|%)\s*[:/]?\s*(\d{2,3})', t, re.IGNORECASE)
    if m: data['marks_10th'] = m.group(1)
    m = re.search(r'(?:12th|XII|HSC|Intermediate).*?(?:Marks|%)\s*[:/]?\s*(\d{2,3})', t, re.IGNORECASE)
    if m: data['marks_12th'] = m.group(1)

    # ── Income ────────────────────────────────────────────────────────────
    if 'income' not in data:
        m = re.search(r'(?:Annual Income|Income|आय)\s*[:/]?\s*(?:Rs\.?|₹)?\s*([\d,]+)', t, re.IGNORECASE)
        if m: data['income'] = m.group(1).replace(',', '')

    return data


# ─────────────────────────────────────────────────────────────────────────
# Shared multi-format extraction (used by /api/smart-ocr, the web dashboard
# document upload, and the WhatsApp bot). One pipeline so every channel
# produces identical results.
# ─────────────────────────────────────────────────────────────────────────

def extract_text_from_bytes(filename, file_bytes):
    """
    Run OCR / text extraction on raw file bytes, regardless of source
    (browser upload in the web dashboard, or a WhatsApp media download).
    Returns plain extracted text (may be an empty string on failure).
    """
    import io as _io
    fname = (filename or '').lower()
    text = ''
    try:
        if fname.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')) or not fname:
            img = Image.open(_io.BytesIO(file_bytes)).convert('RGB')
            img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
            try:
                text = pytesseract.image_to_string(img, lang='eng+hin')
            except Exception:
                text = pytesseract.image_to_string(img, lang='eng')

        elif fname.endswith('.pdf'):
            try:
                from pdf2image import convert_from_bytes
                import os
                poppler_candidates = [
                    r'C:\poppler-25.12.0\Library\bin',
                    r'C:\poppler\Library\bin',
                    r'C:\poppler\bin',
                    r'C:\Program Files\poppler\Library\bin',
                ]
                poppler_path = next((p for p in poppler_candidates if os.path.exists(p)), None)
                pages = convert_from_bytes(file_bytes, dpi=200, first_page=1, last_page=6, poppler_path=poppler_path)
                chunks = []
                for page in pages:
                    page = page.resize((page.width * 2, page.height * 2), Image.LANCZOS)
                    try:
                        chunks.append(pytesseract.image_to_string(page, lang='eng+hin'))
                    except Exception:
                        chunks.append(pytesseract.image_to_string(page, lang='eng'))
                text = "\n".join(chunks)
            except Exception:
                try:
                    import PyPDF2
                    reader = PyPDF2.PdfReader(_io.BytesIO(file_bytes))
                    text = "\n".join(p.extract_text() or '' for p in reader.pages[:6])
                except Exception as e2:
                    logger.warning(f'PDF text extraction failed: {e2}')

        elif fname.endswith(('.doc', '.docx')):
            try:
                import docx
                doc_obj = docx.Document(_io.BytesIO(file_bytes))
                text = "\n".join(p.text for p in doc_obj.paragraphs if p.text.strip())
            except Exception as e:
                logger.warning(f'DOCX extraction failed: {e}')

        elif fname.endswith('.txt'):
            text = file_bytes.decode('utf-8', errors='ignore')

        else:
            # Unknown extension — best-effort as image. WhatsApp media often
            # arrives without a real filename/extension.
            try:
                img = Image.open(_io.BytesIO(file_bytes)).convert('RGB')
                text = pytesseract.image_to_string(img, lang='eng')
            except Exception:
                pass
    except Exception as e:
        logger.warning(f'extract_text_from_bytes failed for {filename}: {e}')

    return text

if __name__ == '__main__':
    # Test OCR with a sample image
    print("OCR Processor ready")
    print("To test, upload a document through the API endpoint")
