<div align="center">

# 🤖 Sahayak v2.0 — AI Co-Pilot for CSC Operators

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.0-black?logo=flask)](https://flask.palletsprojects.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-blue?logo=postgresql)](https://postgresql.org)
[![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-yellow?logo=googlechrome)](https://developer.chrome.com/docs/extensions/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Hackathon](https://img.shields.io/badge/CHIPS%20AIML%20Hackathon-IIIT%20Nava%20Raipur%202025-orange)](https://www.iiitnr.ac.in/)

> **Built at CHIPS AIML Hackathon** · IIIT Nava Raipur · 13–15 March 2025  
> **Team:** GramMatrix

**Sahayak** (Hindi: सहायक, meaning *"Helper"*) is a real-time AI-powered platform that helps Common Service Centre (CSC) operators search, retrieve, and auto-fill government forms — powered by live internet scraping, OCR, machine learning, and WhatsApp integration.

No hardcoded database. Always current. Always intelligent.

---

**Result: 10 minutes → 3 minutes per form. 70% time saved.**

</div>

---

## 📋 Table of Contents

- [The Problem](#-the-problem)
- [Our Solution](#-our-solution)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [API Endpoints](#-api-endpoints)
- [Project Structure](#-project-structure)
- [Team](#-team)
- [License](#-license)

---

## 🎯 The Problem

CSC (Common Service Centre) operators across rural India spend **10+ minutes per government form** because:

- 🗄️ Existing tools use hardcoded databases that go **out of date quickly**
- 🔍 Operators manually search across **dozens of government portals**
- 📄 Document details must be **manually typed** from physical papers
- ❓ Citizens often don't know **which schemes they're eligible for**

---

## 💡 Our Solution

Sahayak v2.0 is a **multi-channel platform** — Chrome Extension + Operator Dashboard + Admin Panel + WhatsApp Bot — all powered by a unified Python backend with PostgreSQL:

- 🌐 **Searches the internet in real-time** — no static database, always current
- 📄 **Extracts data from uploaded documents** via Tesseract OCR
- 🧠 **Learns from corrections** using a scikit-learn ML model
- 🎯 **Predicts eligible government schemes** using an AI rules engine
- 🎤 **Supports voice input** in English, Hindi, and Chhattisgarhi
- 💬 **WhatsApp bot + Dashboard** stay in sync via a shared PostgreSQL session store
- ⚙️ **Admin Panel** to dynamically add/edit/delete forms, document types, and fields — no code changes needed
- 🗄️ **PostgreSQL database** for production-grade data persistence

---

## ✨ Features

### 🌐 1. Live Internet Search
No database — searches government portals on the fly via DuckDuckGo.

```
User: "I want to apply for Learner's License"
Sahayak: → Searches web → Finds official RTO portal → Returns live requirements + links
```

### 📄 2. OCR Document Processing
Upload an Aadhaar card, PAN card, or income certificate. Tesseract OCR extracts name, DOB, address, Aadhaar number — and **auto-fills the form**.

### 🧠 3. Machine Learning from Corrections
Uses `scikit-learn` to learn from user corrections over time.

### 🎯 4. AI Eligibility Engine
Input age + income → Get predicted eligible schemes with confidence scores.

### 🎤 5. Multilingual Voice Assistant
Speak your query in **English**, **Hindi**, or **Chhattisgarhi** using the browser's built-in Speech API.

### 🧾 6. Forms Platform — Dashboard + WhatsApp, Always in Sync

A `webapp/` operator dashboard and a WhatsApp bot both sit on top of the same PostgreSQL session store:

- **On WhatsApp**, a citizen picks a form from a numbered menu, sends the required documents one at a time (each auto-filled via OCR), then answers whatever fields weren't found on a document.
- **On the dashboard**, an operator sees every session in a live-updating register, can start a session directly, upload documents, and edit any field — including sessions that were started on WhatsApp.

Because both channels read and write the same PostgreSQL database, a document sent on WhatsApp shows up on the dashboard within seconds (and vice versa) with no manual syncing step.

### ⚙️ 7. Admin Panel — Dynamic Form Management

The admin panel (`webapp/admin.html`) lets you manage the entire forms catalog without touching code:

- **Forms Catalog**: Add, edit, or delete government forms with their required documents and fields
- **Document Types**: Manage the document type library (Aadhaar, PAN, etc.)
- **Field Library**: Define field definitions with OCR source keys and required flags

**20 government forms** are pre-seeded across 8 categories: Identity, Revenue, Transport, Civil Registration, Social Welfare, Education, Banking, and Food & Civil Supplies.

### 💬 8. WhatsApp Integration via Twilio

Real WhatsApp messaging via Twilio Sandbox + ngrok. A built-in simulator on the dashboard lets you test the flow without a Twilio account.

---

## 🏗️ Architecture

```
┌───────────────────────────────────────────────────┐
│                Client Layer                        │
├──────────┬────────────┬──────────┬────────────────┤
│  Chrome  │  Operator  │  Admin   │   WhatsApp     │
│Extension │ Dashboard  │  Panel   │     Bot        │
│(content) │(index.html)│(admin)   │(Twilio Webhook)│
└────┬─────┴─────┬──────┴────┬─────┴───────┬────────┘
     │           │           │             │
     │      HTTP (localhost:5000)          │
     ▼           ▼           ▼             ▼
┌───────────────────────────────────────────────────┐
│          Flask REST API  (app.py)                  │
├──────────┬──────────┬──────────┬─────────────────┤
│  Web     │   OCR    │  Form    │  Admin API       │
│ Scraper  │Processor │  Engine  │ (CRUD routes)    │
├──────────┴──────────┴──────────┴─────────────────┤
│  scikit-learn ML · Eligibility · AI Chatbot       │
├──────────────────────────────────────────────────┤
│           PostgreSQL Database                     │
│  ┌────────┬───────────┬──────────┬──────────┐    │
│  │ forms  │doc_types  │field_lib │ sessions │    │
│  └────────┴───────────┴──────────┴──────────┘    │
└───────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Browser Extension | Vanilla JavaScript, Chrome Extension API (Manifest V3), Web Speech API |
| Operator Dashboard | HTML, CSS, JavaScript (vanilla) — professional light theme with dark sidebar |
| Admin Panel | HTML, CSS, JavaScript — modal editors, tab navigation |
| WhatsApp Bot | Twilio Webhook + built-in simulator |
| Backend Framework | Python 3.8+, Flask, Flask-CORS |
| Database | PostgreSQL 17/18 with psycopg2 connection pooling |
| Web Scraping | BeautifulSoup4, Requests, lxml |
| OCR | Tesseract, pytesseract, Pillow, pdf2image |
| Machine Learning | scikit-learn, NumPy |
| Document Parsing | PyPDF2, python-docx |
| Secrets Management | python-dotenv (.env files, gitignored) |

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Install |
|---|---|
| **Python 3.8+** | [python.org](https://python.org) — check "Add to PATH" during install |
| **PostgreSQL 17+** | [postgresql.org/download](https://www.postgresql.org/download/) |
| **Tesseract OCR** | [Windows installer](https://github.com/UB-Mannheim/tesseract/wiki) · Ubuntu: `sudo apt install tesseract-ocr` · macOS: `brew install tesseract` |
| **Poppler** (for PDFs) | [Windows download](https://blog.alivate.com.au/poppler-windows/) (add `bin/` to PATH) · Ubuntu: `sudo apt install poppler-utils` · macOS: `brew install poppler` |
| **Google Chrome** | For the browser extension |

---

### 🖥️ Backend Setup

```bash
# 1. Clone the repository
git clone https://github.com/ShibamKhadanga/sahayak.git
cd sahayak

# 2. Create a virtual environment
python -m venv venv

# Activate it:
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Set up environment variables
cp backend/.env.example backend/.env
# Edit backend/.env with your actual credentials:
#   TWILIO_ACCOUNT_SID=ACxxxxxx
#   TWILIO_AUTH_TOKEN=your_token
#   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/sahayak

# 5. Create the PostgreSQL database
psql -U postgres -c "CREATE DATABASE sahayak"

# 6. Start the Flask server (tables are auto-created on first run)
python backend/app.py
```

The backend will start at `http://localhost:5000`. On first run, it will:
- Create all database tables (`forms`, `sessions`, `document_types`, `field_library`)
- Seed 20 government forms, 16 document types, and 38 field definitions

> **Note (Windows PowerShell):** If activation fails with an execution policy error, run:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

---

### 🧩 Chrome Extension Setup

1. Open Chrome and go to `chrome://extensions/`
2. Enable **Developer Mode** (toggle in top-right corner)
3. Click **"Load unpacked"**
4. Select the `extension/` folder from this repository
5. The Sahayak icon will appear in your browser toolbar ✅

---

### 🌐 Operator Dashboard

Open `webapp/index.html` in your browser, or use VS Code's **Live Server** extension to serve it.

The dashboard connects to the same Flask backend — you'll see live session data, can upload documents, and try the built-in WhatsApp simulator.

---

### ⚙️ Admin Panel

Click **"Admin Panel"** in the dashboard sidebar, or open `webapp/admin.html` directly.

From here you can:
- Add new government forms to the catalog
- Define new document types and field definitions
- Edit or delete existing forms without touching any code

---

### 💬 WhatsApp Setup (Optional)

To receive real WhatsApp messages:

1. Sign up for a [Twilio account](https://www.twilio.com/try-twilio)
2. Set up the [WhatsApp Sandbox](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn)
3. Install [ngrok](https://ngrok.com/) and run: `ngrok http 5000`
4. In Twilio Sandbox Settings, set webhook URL to: `https://your-ngrok-url/whatsapp/webhook`
5. Send the join code from your phone to the Twilio WhatsApp number

---

### ✅ Test It

1. Make sure the backend is running (`python backend/app.py`)
2. Open `webapp/index.html` — verify "Backend connected" appears
3. Try the **WhatsApp Simulator** — click the green button, type "hi"
4. Open the **Admin Panel** and browse all 20 forms
5. Open the Chrome extension and type: **"I want to apply for Learner's License"**

---

## 📡 API Endpoints

### Extension / AI Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/search-form` | Search for government forms |
| `POST` | `/api/process-document` | OCR on uploaded documents |
| `POST` | `/api/smart-ocr` | Multi-file OCR + smart field extraction |
| `POST` | `/api/predict-eligibility` | AI eligibility prediction |
| `POST` | `/api/learn` | ML model training from corrections |
| `POST` | `/api/suggest` | Get ML model suggestions |
| `POST` | `/api/ai-chat` | Chatbot responses |
| `GET`  | `/api/health` | Server health check |

### Forms Platform Endpoints (Dashboard + WhatsApp)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/forms` | List all forms in the catalog |
| `GET`  | `/api/sessions` | List all sessions (dashboard register) |
| `POST` | `/api/session/start` | Start a new session |
| `GET`  | `/api/session/<id>` | Get full session detail |
| `POST` | `/api/session/<id>/document` | Upload a document into a session |
| `POST` | `/api/session/<id>/field` | Set/correct a field value |
| `POST` | `/api/session/<id>/reset` | Reset a session |
| `POST` | `/api/session/<id>/delete` | Delete a session |
| `POST` | `/whatsapp/webhook` | Twilio inbound WhatsApp webhook |
| `POST` | `/api/whatsapp/simulate` | Built-in WhatsApp simulator |

### Admin API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/admin/forms` | Create a new form |
| `PUT` | `/api/admin/forms/<id>` | Update a form |
| `DELETE` | `/api/admin/forms/<id>` | Delete a form |
| `GET` | `/api/admin/document-types` | List all document types |
| `POST` | `/api/admin/document-types` | Add/update a document type |
| `DELETE` | `/api/admin/document-types/<key>` | Delete a document type |
| `GET` | `/api/admin/fields` | List all field definitions |
| `POST` | `/api/admin/fields` | Add/update a field definition |
| `DELETE` | `/api/admin/fields/<key>` | Delete a field definition |

---

## 📁 Project Structure

```
sahayak/
│
├── 📁 backend/                      # Python AI/ML Backend
│   ├── app.py                       # Flask API server (all routes + admin API)
│   ├── database.py                  # PostgreSQL connection pool + schema + seeding
│   ├── ai_chatbot.py                # Chatbot response engine
│   ├── eligibility_engine.py        # Government scheme eligibility predictor
│   ├── form_engine.py               # State machine: docs → fields → done
│   ├── forms_catalog.py             # Form definitions (reads from PostgreSQL)
│   ├── ml_model.py                  # scikit-learn ML model
│   ├── ocr_processor.py             # Tesseract OCR + smart field extraction
│   ├── session_store.py             # Session CRUD (PostgreSQL-backed)
│   ├── web_scraper.py               # DuckDuckGo search & gov portal scraping
│   ├── whatsapp_bot.py              # WhatsApp conversation logic
│   ├── requirements.txt             # Python dependencies
│   ├── .env.example                 # Environment variable template
│   ├── data/                        # Legacy data folder
│   │   └── .gitkeep
│   └── models/                      # Saved ML model files (auto-generated)
│       └── .gitkeep
│
├── 📁 extension/                    # Chrome Extension (Manifest V3)
│   ├── manifest.json                # Extension configuration
│   ├── content.js                   # Main content script (search, OCR, chat)
│   ├── background.js                # Service worker
│   ├── popup.html                   # Extension popup UI
│   ├── popup.js                     # Popup interaction logic
│   ├── styles.css                   # Extension styles
│   └── icons/                       # Extension icons (16, 48, 128px)
│
├── 📁 webapp/                       # Operator Dashboard + Admin Panel
│   ├── index.html                   # Session register + case-file panel
│   ├── app.js                       # Dashboard logic (polls backend)
│   ├── styles.css                   # Professional light theme + dark sidebar
│   ├── admin.html                   # Admin panel (forms/docs/fields CRUD)
│   ├── admin.js                     # Admin CRUD logic
│   └── admin.css                    # Admin panel styles
│
├── 📁 docs/                         # Documentation
│   ├── SETUP_GUIDE.md               # Complete setup & troubleshooting
│   └── WHATSAPP_INTEGRATION.md      # Twilio setup + built-in simulator
│
├── .gitignore
├── LICENSE
├── PROJECT_STRUCTURE.md             # Detailed architecture & feature map
└── README.md                        # ← You are here
```

---

## 🔑 What's New in v2.0

| | v1.0 (Hackathon) | v2.0 (Current) |
|---|---|---|
| Forms | ❌ Hardcoded 50 forms | ✅ 20 seeded + dynamic via admin panel |
| Data | ❌ Static database | ✅ Real-time scraping + PostgreSQL |
| Storage | ❌ JSON file | ✅ PostgreSQL with connection pooling |
| AI | ❌ No real AI | ✅ ML model + eligibility engine |
| Dashboard | ❌ None | ✅ Professional dark-sidebar dashboard |
| Admin | ❌ None | ✅ Full admin panel (add/edit/delete forms) |
| WhatsApp | ❌ None | ✅ WhatsApp bot + simulator + Twilio |
| OCR | ❌ Basic | ✅ Multi-file smart field extraction |
| Secrets | ❌ Hardcoded | ✅ .env with dotenv (gitignored) |

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork this repository
2. Create your branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add: your feature description"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## 👥 Team — GramMatrix

Built with ❤️ at **CHIPS AIML Hackathon 2025**, IIIT Nava Raipur (13–15 March 2025)

| Name | GitHub |
|------|--------|
| Shibam Khadanga | [@ShibamKhadanga](https://github.com/ShibamKhadanga) |

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**सहायक — Empowering CSC operators across rural India 🇮🇳**

⭐ Star this repo if you find it useful!

</div>
