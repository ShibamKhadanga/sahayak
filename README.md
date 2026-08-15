<div align="center">

# 🤖 Sahayak v2.0 — AI Co-Pilot for CSC Operators

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.0-black?logo=flask)](https://flask.palletsprojects.com)
[![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-yellow?logo=googlechrome)](https://developer.chrome.com/docs/extensions/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Hackathon](https://img.shields.io/badge/CHIPS%20AIML%20Hackathon-IIIT%20Nava%20Raipur%202025-orange)](https://www.iiitnr.ac.in/)

> **Built at CHIPS AIML Hackathon** · IIIT Nava Raipur · 13–15 March 2025  
> **Team:** GramMatrix

**Sahayak** (Hindi: सहायक, meaning *"Helper"*) is a real-time AI-powered platform that helps Common Service Centre (CSC) operators search, retrieve, and auto-fill government forms — powered by live internet scraping, OCR, and machine learning.

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

Sahayak v2.0 is a **three-part platform** — Chrome Extension + Operator Dashboard + WhatsApp Bot — all powered by a unified Python backend:

- 🌐 **Searches the internet in real-time** — no static database, always current
- 📄 **Extracts data from uploaded documents** via Tesseract OCR
- 🧠 **Learns from corrections** using a scikit-learn ML model
- 🎯 **Predicts eligible government schemes** using an AI rules engine
- 🎤 **Supports voice input** in English, Hindi, and Chhattisgarhi
- 💬 **WhatsApp bot + Dashboard** stay in sync via a shared session store

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

```
User corrects: age 55 → 65 for pension form
Next time:     Sahayak auto-suggests 65 ✅
```

### 🎯 4. AI Eligibility Engine
Input age + income → Get predicted eligible schemes with confidence scores:

| Scheme | Confidence |
|--------|-----------|
| Old Age Pension | 95% |
| Senior Citizen Health Card | 90% |
| BPL Card | 95% |
| Subsidized Ration | 90% |
| Free Bus Pass | 85% |

### 🎤 5. Multilingual Voice Assistant
Speak your query in **English**, **Hindi**, or **Chhattisgarhi** using the browser's built-in Speech API.

### 💬 6. Persistent Chat
Chat history persists across page loads, per-tab — operators can refer to form requirements while filling.

### 🧾 7. Forms Platform — Dashboard + WhatsApp, Always in Sync

A `webapp/` operator dashboard and a WhatsApp bot both sit on top of the same backend session store:

- **On WhatsApp**, a citizen picks a form from a numbered menu, sends the required documents one at a time (each auto-filled via OCR), then answers whatever fields weren't found on a document.
- **On the dashboard**, an operator sees every session in a live-updating register, can start a session directly, upload documents, and edit any field — including sessions that were started on WhatsApp.

Because both channels read and write the same `session_store.py`, a document sent on WhatsApp shows up on the dashboard within seconds (and vice versa) with no manual syncing step.

A built-in WhatsApp simulator on the dashboard lets you try the whole flow without a Twilio account — see [`docs/WHATSAPP_INTEGRATION.md`](docs/WHATSAPP_INTEGRATION.md).

---

## 🏗️ Architecture

```
┌───────────────────────────────────────────────┐
│              Client Layer                      │
├──────────────┬────────────────┬────────────────┤
│    Chrome    │   Operator     │   WhatsApp     │
│  Extension   │  Dashboard     │     Bot        │
│  (content.js)│  (webapp/)     │(Twilio Webhook)│
└──────┬───────┴───────┬────────┴───────┬────────┘
       │               │                │
       │    HTTP (localhost:5000)        │
       ▼               ▼                ▼
┌───────────────────────────────────────────────┐
│         Flask REST API  (app.py)               │
├──────────────┬────────────────┬────────────────┤
│  Web Scraper │  OCR Processor │  Form Engine   │
│ (DuckDuckGo) │  (Tesseract)   │ (session_store)│
├──────────────┴────────────────┴────────────────┤
│  scikit-learn ML Model · Eligibility Engine    │
│  AI Chatbot · Forms Catalog                    │
└────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Browser Extension | Vanilla JavaScript, Chrome Extension API (Manifest V3), Web Speech API |
| Operator Dashboard | HTML, CSS, JavaScript (vanilla) |
| WhatsApp Bot | Twilio Webhook, built-in simulator |
| Backend Framework | Python 3.8+, Flask, Flask-CORS |
| Web Scraping | BeautifulSoup4, Requests, lxml |
| OCR | Tesseract, pytesseract, Pillow, pdf2image |
| Machine Learning | scikit-learn, NumPy |
| Document Parsing | PyPDF2, python-docx |

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Install |
|---|---|
| **Python 3.8+** | [python.org](https://python.org) — check "Add to PATH" during install |
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
# Windows (CMD):
venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Start the Flask server
python backend/app.py
```

The backend will start at `http://localhost:5000`. You should see:
```
 * Running on http://127.0.0.1:5000
```

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

### ✅ Test It

1. Make sure the backend is running (`python backend/app.py`)
2. Open any website in Chrome
3. Click the Sahayak extension icon
4. Type: **"I want to apply for Learner's License"**
5. Watch it search the internet and return live requirements!

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
| `POST` | `/whatsapp/webhook` | Twilio inbound WhatsApp webhook |
| `POST` | `/api/whatsapp/simulate` | Built-in WhatsApp simulator |

---

## 📁 Project Structure

```
sahayak/
│
├── 📁 backend/                      # Python AI/ML Backend
│   ├── app.py                       # Flask API server (all routes)
│   ├── ai_chatbot.py                # Chatbot response engine
│   ├── eligibility_engine.py        # Government scheme eligibility predictor
│   ├── form_engine.py               # State machine: docs → fields → done
│   ├── forms_catalog.py             # Form definitions, required docs/fields
│   ├── ml_model.py                  # scikit-learn ML model
│   ├── ocr_processor.py             # Tesseract OCR + smart field extraction
│   ├── session_store.py             # Shared session state (dashboard + WhatsApp)
│   ├── web_scraper.py               # DuckDuckGo search & gov portal scraping
│   ├── whatsapp_bot.py              # WhatsApp conversation logic
│   ├── requirements.txt             # Python dependencies
│   ├── data/                        # Session data (gitignored — contains PII)
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
├── 📁 webapp/                       # Operator Dashboard
│   ├── index.html                   # Session register + case-file panel
│   ├── app.js                       # Polls backend, renders sessions
│   └── styles.css                   # Dashboard styling
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
| Forms | ❌ Hardcoded 50 forms | ✅ Live web search, unlimited |
| Data | ❌ Static database | ✅ Real-time scraping |
| AI | ❌ No real AI | ✅ ML model + eligibility engine |
| Dashboard | ❌ None | ✅ Full operator dashboard |
| WhatsApp | ❌ None | ✅ WhatsApp bot with shared sessions |
| OCR | ❌ Basic | ✅ Multi-file smart field extraction |

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
