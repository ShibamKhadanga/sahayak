"""
Sahayak Backend API Server
Flask-based REST API for AI/ML features
"""
from ai_chatbot import get_ai_response
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime

# Import our modules
from web_scraper import search_government_forms, scrape_form_details
from ocr_processor import process_document
from ml_model import MLModel
from eligibility_engine import predict_eligibility

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow requests from browser extension

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize ML model
ml_model = MLModel()

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'service': 'Sahayak AI Backend',
        'version': '2.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Detailed health check"""
    return jsonify({
        'status': 'healthy',
        'ml_model_loaded': ml_model.is_loaded(),
        'endpoints': [
            '/api/search-form',
            '/api/process-document',
            '/api/predict-eligibility',
            '/api/learn'
        ]
    })

@app.route('/api/search-form', methods=['POST'])
def search_form():
    """
    Search for government forms on the internet
    
    Request:
    {
        "query": "learning license application",
        "state": "chhattisgarh",  # optional
        "max_results": 5           # optional
    }
    
    Response:
    {
        "success": true,
        "results": [
            {
                "title": "Learning License - Parivahan",
                "url": "https://sarathi.parivahan.gov.in/...",
                "snippet": "Apply for learning license online...",
                "requirements": ["Age 16+", "Address proof", ...],
                "source": "official"
            }
        ]
    }
    """
    try:
        data = request.json
        query = data.get('query', '')
        state = data.get('state', 'india')
        max_results = data.get('max_results', 5)
        
        if not query:
            return jsonify({'success': False, 'error': 'Query is required'}), 400
        
        logger.info(f"Searching for: {query} in {state}")
        
        # Search the web for government forms
        results = search_government_forms(query, state, max_results)
        
        # Scrape details from top results
        detailed_results = []
        for result in results[:3]:  # Get details for top 3
            try:
                details = scrape_form_details(result['url'])
                result.update(details)
            except Exception as e:
                logger.warning(f"Could not scrape details for {result['url']}: {e}")
            
            detailed_results.append(result)
        
        return jsonify({
            'success': True,
            'query': query,
            'count': len(detailed_results),
            'results': detailed_results
        })
        
    except Exception as e:
        logger.error(f"Error in search_form: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/process-document', methods=['POST'])
def process_doc():
    """
    Process uploaded document with OCR
    
    Request:
    Form-data with 'file' field
    
    Response:
    {
        "success": true,
        "extracted_data": {
            "aadhar": "1234 5678 9012",
            "name": "Ramesh Kumar",
            "dob": "01/01/1960",
            "address": "Raipur, Chhattisgarh"
        },
        "confidence": 0.95
    }
    """
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Empty filename'}), 400
        
        logger.info(f"Processing document: {file.filename}")
        
        # Process the document with OCR
        result = process_document(file)
        
        return jsonify({
            'success': True,
            'filename': file.filename,
            'extracted_data': result['data'],
            'confidence': result['confidence'],
            'processing_time': result['processing_time']
        })
        
    except Exception as e:
        logger.error(f"Error in process_document: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/predict-eligibility', methods=['POST'])
def predict_elig():
    """
    Predict user eligibility for government schemes
    
    Request:
    {
        "age": 65,
        "income": 30000,
        "gender": "male",
        "education": "graduate",
        "state": "chhattisgarh",
        "category": "general"
    }
    
    Response:
    {
        "success": true,
        "eligible_schemes": [
            {
                "name": "Old Age Pension",
                "confidence": 0.98,
                "reasons": ["Age > 60", "Income < 48000"],
                "form_url": "https://..."
            }
        ]
    }
    """
    try:
        data = request.json
        
        logger.info(f"Predicting eligibility for profile: {data}")
        
        # Use AI to predict eligibility
        predictions = predict_eligibility(data)
        
        # Search for application links for each scheme
        for scheme in predictions:
            try:
                search_results = search_government_forms(
                    f"{scheme['name']} application {data.get('state', 'india')}",
                    data.get('state', 'india'),
                    1
                )
                if search_results:
                    scheme['form_url'] = search_results[0]['url']
            except:
                scheme['form_url'] = None
        
        return jsonify({
            'success': True,
            'profile': data,
            'eligible_schemes': predictions,
            'count': len(predictions)
        })
        
    except Exception as e:
        logger.error(f"Error in predict_eligibility: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/learn', methods=['POST'])
def learn():
    """
    Train ML model from user corrections
    
    Request:
    {
        "field": "age",
        "wrong_value": "55",
        "correct_value": "65",
        "form_type": "pension"
    }
    
    Response:
    {
        "success": true,
        "model_updated": true
    }
    """
    try:
        data = request.json
        
        field = data.get('field')
        wrong_value = data.get('wrong_value')
        correct_value = data.get('correct_value')
        form_type = data.get('form_type', 'general')
        
        logger.info(f"Learning: {field} {wrong_value} -> {correct_value} ({form_type})")
        
        # Train the ML model
        ml_model.learn(field, wrong_value, correct_value, form_type)
        
        return jsonify({
            'success': True,
            'model_updated': True,
            'learning_count': ml_model.get_learning_count()
        })
        
    except Exception as e:
        logger.error(f"Error in learn: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/suggest', methods=['POST'])
def suggest():
    """
    Get ML-based suggestions for a field
    
    Request:
    {
        "field": "age",
        "value": "55",
        "form_type": "pension"
    }
    
    Response:
    {
        "success": true,
        "suggestion": "65",
        "confidence": 0.85
    }
    """
    try:
        data = request.json
        
        field = data.get('field')
        value = data.get('value')
        form_type = data.get('form_type', 'general')
        
        suggestion = ml_model.get_suggestion(field, value, form_type)
        
        return jsonify({
            'success': True,
            'field': field,
            'original_value': value,
            'suggestion': suggestion['value'] if suggestion else None,
            'confidence': suggestion['confidence'] if suggestion else 0
        })
        
    except Exception as e:
        logger.error(f"Error in suggest: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500



@app.route('/api/smart-ocr', methods=['POST'])
def smart_ocr():
    """
    Smart multi-document OCR using Tesseract (100% free, offline, no API key needed)
    Accepts multiple files: PDF, images, Word docs
    """
    try:
        import io, re
        from PIL import Image
        import pytesseract
        from ocr_processor import extract_document_type

        files = request.files.getlist('files[]')
        if not files or all(f.filename == '' for f in files):
            return jsonify({'success': False, 'error': 'No files uploaded'}), 400

        all_text = ""
        doc_summary = []

        for file in files:
            fname = file.filename.lower()
            file_bytes = file.read()

            # ── Images ──────────────────────────────────────────
            if fname.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')):
                img = Image.open(io.BytesIO(file_bytes)).convert('RGB')
                # Upscale for better OCR
                img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
                try:
                    text = pytesseract.image_to_string(img, lang='eng+hin')
                except Exception:
                    text = pytesseract.image_to_string(img, lang='eng')
                all_text += "\n" + text
                doc_summary.append(file.filename)

            # ── PDF ──────────────────────────────────────────────
            elif fname.endswith('.pdf'):
                try:
                    from pdf2image import convert_from_bytes
                    import os
                    POPPLER_PATHS = [
                        r'C:\poppler-25.12.0\Library\bin',
                        r'C:\poppler\Library\bin',
                        r'C:\poppler\bin',
                        r'C:\Program Files\poppler\Library\bin',
                        r'C:\Users\DELL\poppler\Library\bin',
                    ]
                    poppler_path = next((p for p in POPPLER_PATHS if os.path.exists(p)), None)
                    pages = convert_from_bytes(file_bytes, dpi=200, first_page=1, last_page=6, poppler_path=poppler_path)
                    for page in pages:
                        page = page.resize((page.width * 2, page.height * 2), Image.LANCZOS)
                        try:
                            text = pytesseract.image_to_string(page, lang='eng+hin')
                        except Exception:
                            text = pytesseract.image_to_string(page, lang='eng')
                        all_text += "\n" + text
                    doc_summary.append(f"{file.filename} ({len(pages)} pages)")
                except Exception:
                    # Fallback: PyPDF2 text extraction
                    try:
                        import PyPDF2
                        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
                        pdf_text = '\n'.join(p.extract_text() or '' for p in reader.pages[:6])
                        all_text += "\n" + pdf_text
                        doc_summary.append(f"{file.filename} (text PDF)")
                    except Exception as e2:
                        logger.warning(f"PDF failed: {e2}")

            # ── Word Doc ─────────────────────────────────────────
            elif fname.endswith(('.doc', '.docx')):
                try:
                    import docx
                    doc_obj = docx.Document(io.BytesIO(file_bytes))
                    doc_text = '\n'.join(p.text for p in doc_obj.paragraphs if p.text.strip())
                    all_text += "\n" + doc_text
                    doc_summary.append(f"{file.filename} (Word)")
                except Exception as e:
                    logger.warning(f"DOCX failed: {e}")

            # ── Plain Text ───────────────────────────────────────
            elif fname.endswith('.txt'):
                all_text += "\n" + file_bytes.decode('utf-8', errors='ignore')
                doc_summary.append(file.filename)

        if not all_text.strip():
            return jsonify({'success': False, 'error': 'Could not extract any text from uploaded files'}), 400

        # ── Extract structured data using smart regex ─────────────
        extracted = extract_smart_data(all_text)
        doc_type = extract_document_type(all_text)
        doc_types = [doc_type] if doc_type != 'unknown' else []

        fields_found = len([v for v in extracted.values() if v])
        logger.info(f"Smart OCR (Tesseract): {fields_found} fields from {len(files)} file(s)")

        return jsonify({
            'success': True,
            'extracted_data': extracted,
            'doc_types': doc_types,
            'fields_found': fields_found,
            'files_processed': len(files),
            'confidence': min(0.4 + fields_found * 0.06, 0.95)
        })

    except Exception as e:
        logger.error(f"Smart OCR failed: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


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



@app.route('/api/ai-chat', methods=['POST'])
def ai_chat():
    try:
        data = request.json
        message = data.get('message', '')
        context = data.get('context', {})
        history = data.get('history', [])

        logger.info(f"Chat request: '{message[:60]}' | history={len(history)} msgs")

        response = get_ai_response(message, context, history)

        logger.info(f"Chat response: '{response[:60]}...'")
        return jsonify({'success': True, 'response': response})

    except Exception as e:
        error_msg = str(e)
        logger.error(f"AI chat FAILED: {type(e).__name__}: {error_msg}", exc_info=True)
        # Return success:True with error text so extension SHOWS it instead of using local fallback
        return jsonify({
            'success': True,
            'response': f"⚠️ AI Error: {error_msg[:200]}\n\nPlease check the backend terminal for details."
        })

if __name__ == '__main__':
    logger.info("Starting Sahayak Backend Server...")
    logger.info("Server will run on http://localhost:5000")
    logger.info("Press Ctrl+C to stop")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True  # Set to False in production
    )