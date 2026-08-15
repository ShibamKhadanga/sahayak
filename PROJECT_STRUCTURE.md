# 🏗️ Sahayak Complete Project Structure

```
sahayak-final/
│
├── 📁 extension/                    # Browser Extension Files
│   ├── manifest.json                # Extension configuration
│   ├── content.js                   # Main content script (web search, OCR)
│   ├── background.js                # Service worker
│   ├── popup.html                   # Extension popup
│   ├── popup.js                     # Popup logic
│   ├── styles.css                   # All styles
│   └── icons/                       # Extension icons
│       ├── icon16.png
│       ├── icon48.png
│       └── icon128.png
│
├── 📁 webapp/                       # Operator Dashboard ("the software")
│   ├── index.html                   # Session register + case-file panel
│   ├── app.js                       # Polls the same backend the bot uses
│   └── styles.css                   # Dashboard styling
│
├── 📁 backend/                      # Python AI/ML Backend
│   ├── app.py                       # Flask API server (all routes)
│   ├── forms_catalog.py             # Which forms exist, their docs/fields
│   ├── session_store.py             # Shared, file-backed session state
│   ├── form_engine.py               # State machine: docs → fields → done
│   ├── whatsapp_bot.py              # WhatsApp conversation logic
│   ├── ml_model.py                  # Machine Learning model
│   ├── ocr_processor.py             # Document OCR + smart field extraction
│   ├── web_scraper.py               # Web scraping for forms
│   ├── ai_chatbot.py                # General chatbot responses (extension)
│   ├── eligibility_engine.py        # Eligibility prediction
│   ├── requirements.txt             # Python dependencies
│   ├── data/                        # sessions.json (gitignored — has PII)
│   │   └── .gitkeep
│   └── models/                      # Saved ML models
│       └── .gitkeep
│
├── 📁 docs/                         # Documentation
│   ├── SETUP_GUIDE.md              # Complete setup instructions
│   └── WHATSAPP_INTEGRATION.md     # Twilio setup + built-in simulator
│
└── README.md                        # Main project README

```

## 🆕 Forms Platform (dashboard + WhatsApp, kept in sync)

Sahayak now goes beyond one browser extension. `forms_catalog.py` defines
every government form Sahayak knows how to fill — its required documents
and the fields it needs. A citizen can complete that form from **either**:

- **The WhatsApp bot** — pick a form by number, send documents one at a
  time (auto-filled by OCR), then answer whatever's still missing.
- **The operator dashboard** (`webapp/`) — start a session, upload
  documents, and edit fields directly, watching the same session update
  live if the citizen is also messaging on WhatsApp.

Both channels are just callers into `form_engine.py` and
`session_store.py` — there's one shared session per person, not two
separate systems that need reconciling. See
`docs/WHATSAPP_INTEGRATION.md` for setup, including a no-Twilio-required
simulator built into the dashboard itself.

## 🔄 How It Works

### Architecture Flow:

```
User Browser (Extension)
        ↓
    Content.js
        ↓
    ┌───────────────────────────────┐
    │  Local Processing:            │
    │  • Form validation            │
    │  • UI rendering               │
    │  • Voice recognition          │
    └───────────────────────────────┘
        ↓
    Needs AI/Web Search?
        ↓
    ┌───────────────────────────────┐
    │  Python Backend (Flask):      │
    │  • Web scraping (real-time)   │
    │  • ML predictions             │
    │  • OCR processing             │
    │  • Eligibility analysis       │
    └───────────────────────────────┘
        ↓
    Internet Search
    (Google, Gov Websites)
        ↓
    Returns Results
        ↓
    Display to User
```

## 🎯 Feature Implementation Map

| Feature | Frontend (JS) | Backend (Python) | Internet |
|---------|--------------|------------------|----------|
| Form Validation | ✅ | ❌ | ❌ |
| Voice Assistant | ✅ | ❌ | ❌ |
| Document Upload | ✅ | ✅ OCR | ❌ |
| Form Search | ✅ | ✅ Scrape | ✅ Google |
| Persistent Chat | ✅ | ❌ | ❌ |
| ML Learning | ✅ | ✅ Model | ❌ |
| Eligibility AI | ✅ | ✅ Predict | ✅ Web |

## 📦 Components

### Extension (JavaScript)
- Runs in browser
- Handles UI and user interaction
- Calls backend when needed
- Works offline for basic features

### Backend (Python)
- Flask REST API
- Real AI/ML processing
- Web scraping and search
- OCR for documents
- Runs on localhost or server

### Internet APIs
- Google Custom Search API (form search)
- Government websites (real-time scraping)
- No hardcoded database!

## 🚀 Quick Start

1. **Setup Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```

2. **Load Extension**:
   ```
   Chrome → Extensions → Load unpacked → Select 'extension' folder
   ```

3. **Test**:
   - Backend runs on: http://localhost:5000
   - Extension connects automatically
   - Try: "I want to apply for LL"

## 🔑 Key Differences from Old Version

### OLD (Database):
- ❌ Hardcoded 50 forms
- ❌ Static requirements
- ❌ No real AI

### NEW (Internet):
- ✅ Live web search
- ✅ Real-time scraping
- ✅ True ML model
- ✅ Always up-to-date
- ✅ Unlimited forms

## 📡 API Endpoints

**Extension / AI endpoints:**

1. `POST /api/search-form` - Search for government forms
2. `POST /api/process-document` - OCR on uploaded docs
3. `POST /api/smart-ocr` - Multi-file OCR + smart field extraction
4. `POST /api/predict-eligibility` - AI eligibility prediction
5. `POST /api/learn` / `POST /api/suggest` - ML model training/suggestions
6. `POST /api/ai-chat` - Chatbot responses
7. `GET /api/health` - Server health check

**Forms platform endpoints (dashboard + WhatsApp):**

8. `GET /api/forms` - List every form Sahayak can fill (catalog)
9. `GET /api/sessions` - List every session, for the dashboard register
10. `POST /api/session/start` - Start a new session from the web dashboard
11. `GET /api/session/<id>` - Full detail of one session
12. `POST /api/session/<id>/document` - Upload a document into a session
13. `POST /api/session/<id>/field` - Set/correct one field's value
14. `POST /api/session/<id>/reset` - Reset a session back to form selection
15. `POST /whatsapp/webhook` - Twilio inbound WhatsApp webhook
16. `POST /api/whatsapp/simulate` - Dashboard's no-Twilio WhatsApp tester

## 🎓 Technologies Used

**Frontend:**
- Vanilla JavaScript
- Web Speech API
- Chrome Extension APIs

**Backend:**
- Python 3.8+
- Flask (web server)
- Scikit-learn (ML)
- Tesseract (OCR)
- BeautifulSoup (web scraping)
- Google Custom Search API

**No Database Needed!**
- Everything is real-time
- Cache in browser localStorage
- ML model saves to file

---

**Next: I'll create all these files for you!** 🚀
