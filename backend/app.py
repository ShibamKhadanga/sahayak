"""
Sahayak Backend API Server
Flask-based REST API for AI/ML features
"""
import sys
import io

# Fix Windows console encoding — prevents 'charmap' codec errors when
# Flask logs strings that contain emojis (e.g. 🙏, 📎, ✅).
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from ai_chatbot import get_ai_response
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime

# Import our modules
from web_scraper import search_government_forms, scrape_form_details
from ocr_processor import process_document, extract_smart_data, extract_text_from_bytes, extract_document_type
from ml_model import MLModel
from eligibility_engine import predict_eligibility

# Forms platform: catalog + session engine + WhatsApp bot (shared by the
# web dashboard and the WhatsApp channel — see form_engine.py for why)
import forms_catalog
import form_engine
import session_store
import whatsapp_bot

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
    Accepts multiple files: PDF, images, Word docs.
    Extraction logic lives in ocr_processor.py and is shared with the web
    dashboard's per-session document upload and the WhatsApp bot, so all
    three channels parse documents identically.
    """
    try:
        from ocr_processor import extract_document_type, extract_text_from_bytes, extract_smart_data

        files = request.files.getlist('files[]')
        if not files or all(f.filename == '' for f in files):
            return jsonify({'success': False, 'error': 'No files uploaded'}), 400

        all_text = ""
        doc_summary = []

        for file in files:
            file_bytes = file.read()
            text = extract_text_from_bytes(file.filename, file_bytes)
            if text:
                all_text += "\n" + text
                doc_summary.append(file.filename)

        if not all_text.strip():
            return jsonify({'success': False, 'error': 'Could not extract any text from uploaded files'}), 400

        # Extract structured data using shared smart regex parser
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


# ═══════════════════════════════════════════════════════════════════════
# Forms Platform — form catalog, sessions, WhatsApp bot, web dashboard API
#
# One rule keeps everything in sync: the dashboard and the WhatsApp bot
# both read/write through session_store.py and form_engine.py, and never
# keep their own copy of a session. Whichever channel a citizen or
# operator is using, the other channel sees the same state on its next
# read/poll.
# ═══════════════════════════════════════════════════════════════════════

@app.route('/api/forms', methods=['GET'])
def api_list_forms():
    """Catalog of all forms Sahayak can help fill, with their documents/fields."""
    forms = []
    for form in forms_catalog.list_forms():
        forms.append({
            **form,
            "document_labels": [forms_catalog.document_label(d) for d in form["documents"]],
            "field_labels": [forms_catalog.field_meta(f)[0] for f in form["fields"]],
        })
    return jsonify({'success': True, 'forms': forms})


@app.route('/api/sessions', methods=['GET'])
def api_list_sessions():
    """All form sessions (from both WhatsApp and the web dashboard) for the operator console."""
    sessions = session_store.list_sessions()
    summaries = [form_engine.session_summary(s) for s in sessions]
    return jsonify({'success': True, 'sessions': summaries})


@app.route('/api/session/start', methods=['POST'])
def api_start_session():
    """Start a new session from the web dashboard (WhatsApp sessions start themselves on first message)."""
    try:
        data = request.json or {}
        form_id = data.get('form_id')
        if not forms_catalog.get_form(form_id):
            return jsonify({'success': False, 'error': 'Unknown form_id'}), 400

        session_id = session_store.new_web_session_id()
        session = session_store.create_session(session_id, channel='web')
        form_engine.start_form(session, form_id)
        session = session_store.get_session(session_id)

        return jsonify({'success': True, 'session': form_engine.session_summary(session)})
    except Exception as e:
        logger.error(f"Error in api_start_session: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/session/<session_id>', methods=['GET'])
def api_get_session(session_id):
    session = session_store.get_session(session_id)
    if not session:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    return jsonify({'success': True, 'session': form_engine.session_summary(session)})


@app.route('/api/session/<session_id>/document', methods=['POST'])
def api_upload_document(session_id):
    """Upload a document into an existing session (used by the dashboard's per-session upload)."""
    try:
        session = session_store.get_session(session_id)
        if not session:
            return jsonify({'success': False, 'error': 'Session not found'}), 404

        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        file = request.files['file']
        doc_type = request.form.get('doc_type')
        if not doc_type:
            doc_type = form_engine.next_missing_document(session)
        if not doc_type:
            return jsonify({'success': False, 'error': 'No document type specified or pending'}), 400

        newly_filled = form_engine.apply_document_bytes(session, doc_type, file.filename, file.read())
        session = session_store.get_session(session_id)

        return jsonify({
            'success': True,
            'newly_filled': newly_filled,
            'session': form_engine.session_summary(session),
        })
    except Exception as e:
        logger.error(f"Error in api_upload_document: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/session/<session_id>/field', methods=['POST'])
def api_set_field(session_id):
    """Manually set (or correct) one field's value — used by the dashboard's editable field rows."""
    try:
        session = session_store.get_session(session_id)
        if not session:
            return jsonify({'success': False, 'error': 'Session not found'}), 404

        data = request.json or {}
        field_key = data.get('field_key')
        value = data.get('value', '')
        if not field_key:
            return jsonify({'success': False, 'error': 'field_key is required'}), 400

        form_engine.apply_field_answer(session, field_key, value)
        session = session_store.get_session(session_id)

        return jsonify({'success': True, 'session': form_engine.session_summary(session)})
    except Exception as e:
        logger.error(f"Error in api_set_field: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/session/<session_id>/reset', methods=['POST'])
def api_reset_session(session_id):
    session = session_store.reset_session(session_id)
    if not session:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    return jsonify({'success': True, 'session': form_engine.session_summary(session)})


@app.route('/api/session/<session_id>/delete', methods=['POST', 'DELETE'])
def api_delete_session(session_id):
    """Permanently remove a session from the store."""
    deleted = session_store.delete_session(session_id)
    if not deleted:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    return jsonify({'success': True})


def _twiml(message_text):
    """Build a minimal TwiML <Response><Message> body — no twilio SDK dependency required."""
    from xml.sax.saxutils import escape
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        f'<Response><Message>{escape(message_text)}</Message></Response>'
    )


@app.route('/whatsapp/webhook', methods=['POST'])
def whatsapp_webhook():
    """
    Twilio WhatsApp webhook. Point your Twilio WhatsApp Sandbox / number's
    "when a message comes in" URL at <your-public-url>/whatsapp/webhook.
    See docs/WHATSAPP_INTEGRATION.md for setup (Twilio sandbox + ngrok).
    """
    import os
    import requests as _requests

    try:
        from_number = request.values.get('From', '')
        body = request.values.get('Body', '')
        num_media = int(request.values.get('NumMedia', 0) or 0)

        account_sid = os.environ.get('TWILIO_ACCOUNT_SID', 'REDACTED_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN', 'REDACTED_TOKEN')

        files = []
        for i in range(num_media):
            media_url = request.values.get(f'MediaUrl{i}')
            content_type = request.values.get(f'MediaContentType{i}', '')
            if not media_url:
                continue
            try:
                auth = (account_sid, auth_token) if account_sid and auth_token else None
                resp = _requests.get(media_url, auth=auth, timeout=20)
                resp.raise_for_status()
                ext = content_type.split('/')[-1] if '/' in content_type else 'jpg'
                files.append((f"whatsapp-media.{ext}", resp.content))
            except Exception as e:
                logger.warning(f"Could not download WhatsApp media {media_url}: {e}")

        session_id = session_store.whatsapp_session_id(from_number)
        reply_text = whatsapp_bot.handle_incoming(
            session_id=session_id, channel='whatsapp', phone=from_number,
            text=body, files=files,
        )

        from flask import Response
        return Response(_twiml(reply_text), mimetype='application/xml')
    except Exception as e:
        logger.error(f"Error in whatsapp_webhook: {e}", exc_info=True)
        from flask import Response
        return Response(_twiml("Sorry, something went wrong. Please try again in a moment."), mimetype='application/xml')


@app.route('/api/whatsapp/simulate', methods=['POST'])
def whatsapp_simulate():
    """
    Lets the dashboard's built-in 'Test WhatsApp' widget exercise the exact
    same bot logic as the real Twilio webhook, without needing a Twilio
    account — handy for demos and development.
    """
    try:
        sim_phone = request.form.get('phone') or 'whatsapp:+910000000000'
        text = request.form.get('text', '')

        files = []
        if 'file' in request.files:
            f = request.files['file']
            files.append((f.filename, f.read()))

        session_id = session_store.whatsapp_session_id(sim_phone)
        reply_text = whatsapp_bot.handle_incoming(
            session_id=session_id, channel='whatsapp', phone=sim_phone,
            text=text, files=files,
        )
        session = session_store.get_session(session_id)

        return jsonify({
            'success': True,
            'reply': reply_text,
            'session': form_engine.session_summary(session),
        })
    except Exception as e:
        logger.error(f"Error in whatsapp_simulate: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


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