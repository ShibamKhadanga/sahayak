<div align="center">

# 🤖 Sahayak — AI Co-Pilot for CSC Operators

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.0-black?logo=flask)](https://flask.palletsprojects.com)
[![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-yellow?logo=googlechrome)](https://developer.chrome.com/docs/extensions/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Hackathon](https://img.shields.io/badge/CHIPS%20AIML%20Hackathon-IIIT%20Nava%20Raipur%202025-orange)](https://www.iiitnr.ac.in/)

> **Built at CHIPS AIML Hackathon** · IIIT Nava Raipur · 13–15 March 2025  
> **Team:** GramMatrix

**Sahayak** (Hindi: सहायक, meaning *"Helper"*) is a real-time AI-powered browser extension that helps Common Service Centre (CSC) operators search, retrieve, and auto-fill government forms — powered by live internet scraping, OCR, and machine learning.

No hardcoded database. Always current. Always intelligent.

---

![Architecture Diagram](docs/architecture.png)

</div>

---

## 📋 Table of Contents

- [The Problem](#-the-problem)
- [Our Solution](#-our-solution)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
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

Sahayak v2.0 is a Chrome Extension + Python backend that:

- 🌐 **Searches the internet in real-time** — no static database, always current
- 📄 **Extracts data from uploaded documents** via Tesseract OCR
- 🧠 **Learns from corrections** using a scikit-learn ML model
- 🎯 **Predicts eligible government schemes** using an AI rules engine
- 🎤 **Supports voice input** in English, Hindi, and Chhattisgarhi

**Result: 10 minutes → 3 minutes per form. 70% time saved.**

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

---

## 🏗️ Architecture

```
┌──────────────────────┐
│   Chrome Extension   │
│  (JavaScript / HTML) │
└──────────┬───────────┘
           │ HTTP (localhost:5000)
           ▼
┌──────────────────────┐
│   Flask REST API     │
│   Python Backend     │
└──────┬───────────────┘
       │
  ┌────┴────────────────┐
  ▼                     ▼
┌──────────┐     ┌──────────────┐
│  Web     │     │  Tesseract   │
│ Scraper  │     │   OCR        │
│(DuckDuck)│     │  Processor   │
└────┬─────┘     └──────┬───────┘
     │                  │
     └──────────┬────────┘
                ▼
     ┌───────────────────┐
     │  scikit-learn     │
     │   ML Model        │
     │ Eligibility Engine│
     └───────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Browser Extension | Vanilla JavaScript, Chrome Extension API, Web Speech API |
| Backend Framework | Python, Flask, Flask-CORS |
| Web Scraping | BeautifulSoup4, Requests, lxml |
| OCR | Tesseract, pytesseract, Pillow, pdf2image |
| Machine Learning | scikit-learn, NumPy |
| Document Parsing | PyPDF2, python-docx |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Google Chrome / Microsoft Edge
- Internet connection
- Tesseract OCR installed on your system

#### Install Tesseract

| OS | Command |
|----|---------|
| Ubuntu/Debian | `sudo apt-get install tesseract-ocr` |
| macOS | `brew install tesseract` |
| Windows | [Download installer](https://github.com/UB-Mannheim/tesseract/wiki) |

#### Install Poppler (for PDF support)

| OS | Command |
|----|---------|
| Ubuntu/Debian | `sudo apt-get install poppler-utils` |
| macOS | `brew install poppler` |
| Windows | [Download here](https://blog.alivate.com.au/poppler-windows/) |

---

### 🖥️ Backend Setup

```bash
# 1. Clone the repository
git clone https://github.com/ShibamKhadanga/sahayak.git
cd sahayak

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

# 3. Install Python dependencies
cd backend
pip install -r requirements.txt

# 4. Start the Flask server
python app.py
```

The backend will start at `http://localhost:5000`. You should see:
```
* Running on http://127.0.0.1:5000
```

---

### 🧩 Extension Setup

1. Open Chrome and go to `chrome://extensions/`
2. Enable **Developer Mode** (toggle in top-right corner)
3. Click **"Load unpacked"**
4. Select the `extension/` folder from this repository
5. The Sahayak icon will appear in your browser toolbar ✅

---

### ✅ Test It

1. Make sure the backend is running (`python app.py`)
2. Open any website in Chrome
3. Click the Sahayak extension icon
4. Type: **"I want to apply for Learner's License"**
5. Watch it search the internet and return live requirements!

---

## 📁 Project Structure

```
sahayak/
│
├── 📁 backend/
│   ├── app.py                   # Flask API server (entry point)
│   ├── web_scraper.py           # DuckDuckGo search & gov portal scraping
│   ├── ocr_processor.py         # Tesseract OCR for documents
│   ├── ml_model.py              # scikit-learn ML model (learns from corrections)
│   ├── ai_chatbot.py            # Chatbot response engine
│   ├── eligibility_engine.py    # Government scheme eligibility predictor
│   ├── requirements.txt         # Python dependencies
│   └── models/                  # Saved ML model files (auto-generated)
│
├── 📁 extension/
│   ├── manifest.json            # Chrome Extension manifest (v3)
│   ├── content.js               # Injected script — main extension logic
│   ├── background.js            # Service worker
│   ├── popup.html               # Extension popup UI
│   ├── popup.js                 # Popup interaction logic
│   ├── styles.css               # Extension styles
│   └── icons/                   # Extension icons (16, 48, 128px)
│
├── 📁 docs/
│   └── SETUP_GUIDE.md           # Detailed setup & troubleshooting guide
│
├── .gitignore
├── LICENSE
└── README.md                    # You are here
```

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
| *(Add teammates)* | — |

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**सहायक — Empowering CSC operators across rural India 🇮🇳**

⭐ Star this repo if you find it useful!

</div>
