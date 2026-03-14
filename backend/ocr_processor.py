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

# Configure Tesseract path (update based on your system)
# Windows: pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# WINDOWS: Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Linux/Mac: Usually works by default after installation

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

if __name__ == '__main__':
    # Test OCR with a sample image
    print("OCR Processor ready")
    print("To test, upload a document through the API endpoint")
