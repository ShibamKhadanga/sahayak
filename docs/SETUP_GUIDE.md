# 🚀 Sahayak Complete Setup Guide

## 📁 Project Structure

```
sahayak-final/
├── backend/                    ← Python AI/ML Server
│   ├── app.py                 # Main Flask API
│   ├── web_scraper.py         # Web search & scraping
│   ├── ocr_processor.py       # Document OCR
│   ├── ml_model.py            # Machine Learning
│   ├── eligibility_engine.py  # AI predictions
│   ├── requirements.txt       # Dependencies
│   └── models/                # Saved ML models
│
├── extension/                  ← Browser Extension
│   ├── manifest.json
│   ├── content.js
│   ├── background.js
│   ├── popup.html
│   ├── popup.js
│   ├── styles.css
│   └── icons/
│
└── docs/                       ← Documentation
    └── SETUP_GUIDE.md         # This file
```

---

## ⚡ Quick Setup (30 Minutes)

### Step 1: Install Python (5 minutes)

**Windows:**
1. Download Python 3.8+ from https://python.org
2. Run installer
3. ✅ CHECK "Add Python to PATH"
4. Click Install

**Mac:**
```bash
brew install python3
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

**Verify:**
```bash
python --version
# Should show: Python 3.8 or higher
```

---

### Step 2: Install System Dependencies (10 minutes)

**Tesseract OCR** (for document processing):

**Windows:**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer
3. Note installation path (usually `C:\Program Files\Tesseract-OCR`)
4. Add to PATH or update `ocr_processor.py` line 18

**Mac:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-hin  # Hindi support
```

**Poppler** (for PDF processing):

**Windows:**
1. Download from: https://blog.alivate.com.au/poppler-windows/
2. Extract to `C:\Program Files\poppler`
3. Add `bin` folder to PATH

**Mac:**
```bash
brew install poppler
```

**Linux:**
```bash
sudo apt-get install poppler-utils
```

---

### Step 3: Setup Backend (10 minutes)

**1. Navigate to backend folder:**
```bash
cd sahayak-final/backend
```

**2. Install Python packages:**
```bash
pip install -r requirements.txt
```

If you get errors, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt --user
```

**3. Test the backend:**
```bash
python app.py
```

You should see:
```
Starting Sahayak Backend Server...
Server will run on http://localhost:5000
 * Running on http://0.0.0.0:5000
```

**4. Test in browser:**
Open: http://localhost:5000

You should see:
```json
{
  "status": "running",
  "service": "Sahayak AI Backend",
  "version": "2.0"
}
```

✅ **Backend is ready!**

Keep this terminal open (server must run).

---

### Step 4: Setup Extension (5 minutes)

**1. Open Chrome/Edge**

**2. Go to Extensions:**
- Chrome: `chrome://extensions/`
- Edge: `edge://extensions/`

**3. Enable Developer Mode:**
- Toggle switch in top-right corner

**4. Load Extension:**
- Click "Load unpacked"
- Navigate to `sahayak-final/extension/`
- Click "Select Folder"

**5. Create Icons** (if not done):
- You need 3 PNG files: icon16.png, icon48.png, icon128.png
- Use any online tool to create simple icons
- Or skip - extension will work without them

✅ **Extension loaded!**

---

### Step 5: Test Everything (5 minutes)

**Test 1: Basic Connection**

1. Open any webpage
2. Look for purple Sahayak button (bottom-right)
3. Click it
4. Panel should open

**Test 2: Form Search (Internet Search)**

1. In chat, type: **"I want to apply for LL"**
2. Wait 2-3 seconds
3. Should see:
   - Learning License form link
   - Requirements list
   - All from live internet search!

**Test 3: Document Upload (OCR)**

1. Click "📄 Upload Document"
2. Select any text file or image
3. Wait for processing
4. Should see extracted data

**Test 4: Eligibility AI**

1. Fill some form fields (age, income)
2. Complete form (score 80%+)
3. Should see eligible schemes suggested

✅ **All features working!**

---

## 🔧 Troubleshooting

### Backend Issues

**Problem: "ModuleNotFoundError: No module named 'flask'"**

**Solution:**
```bash
pip install Flask
# Or install all at once:
pip install -r requirements.txt
```

---

**Problem: "Tesseract not found"**

**Solution:**

Windows - Edit `ocr_processor.py` line 18:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

Linux/Mac:
```bash
which tesseract
# Use that path if needed
```

---

**Problem: "Port 5000 already in use"**

**Solution:**

Change port in `app.py` (last line):
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

Also update in `content.js` (search for `localhost:5000`):
```javascript
const API_URL = 'http://localhost:5001';
```

---

### Extension Issues

**Problem: "Failed to load extension"**

**Solution:**
- Make sure `manifest.json` is in the root of selected folder
- Check browser console (F12) for specific errors

---

**Problem: "Sahayak button doesn't appear"**

**Solution:**
1. Refresh webpage (Ctrl+R)
2. Check extension is enabled in chrome://extensions/
3. Look in browser console for errors (F12)

---

**Problem: "Can't connect to backend"**

**Solution:**
1. Make sure backend is running (check terminal)
2. Visit http://localhost:5000 - should see JSON
3. Check CORS - should see no errors in browser console
4. Try restarting backend

---

**Problem: "Web search not working"**

**Solution:**
- Internet connection required
- DuckDuckGo might be blocked - try VPN
- Fallback to common portals should work

---

## 🎓 How to Use

### Feature 1: Web Search for Forms

**Instead of database, searches real internet!**

**Try:**
- "I want to apply for LL"
- "pension application"
- "how to get ration card"
- "scholarship form chhattisgarh"

**What happens:**
1. Extension calls backend API
2. Backend searches DuckDuckGo
3. Scrapes form pages for requirements
4. Returns live, up-to-date information!

---

### Feature 2: Document OCR

**Upload any document, get data extracted:**

**Supported:**
- Images (JPG, PNG)
- PDFs
- Text files

**Try:**
1. Create a text file:
```
Name: Ramesh Kumar
Aadhar: 1234 5678 9012
Mobile: 9876543210
Age: 65
Income: 30000
```

2. Upload it
3. Watch form auto-fill!

---

### Feature 3: Machine Learning

**Learns from corrections:**

**Try:**
1. Enter age: 55 (wrong)
2. Get error
3. Correct to: 65
4. Close and reopen extension
5. Enter 55 again
6. ML suggests: "Did you mean 65?"

---

### Feature 4: AI Eligibility

**Real AI predictions:**

**Try:**
1. Fill form with:
   - Age: 65
   - Income: 30000
2. Get score 80%+
3. See: "You may be eligible for:"
   - Old Age Pension
   - Senior Citizen Health Card
   - BPL Card
   - Subsidized Ration
   - Free Bus Pass

---

## 🌐 Architecture

```
Browser Extension
      ↓
  User Interaction
      ↓
┌─────────────────────┐
│   Content.js        │
│   • Form validation │
│   • Voice UI        │
│   • Local storage   │
└─────────────────────┘
      ↓
  Needs AI/Search?
      ↓
┌─────────────────────┐
│  Flask Backend API  │
│  localhost:5000     │
└─────────────────────┘
      ↓
┌─────────────────────────────────┐
│  • Web Scraper → Internet       │
│  • OCR → Tesseract              │
│  • ML Model → Scikit-learn      │
│  • Eligibility → Rule Engine    │
└─────────────────────────────────┘
      ↓
  Returns Results
      ↓
  Display to User
```

---

## 📊 API Endpoints

**Your backend provides:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Health check |
| `/api/search-form` | POST | Search for forms (internet) |
| `/api/process-document` | POST | OCR on uploaded docs |
| `/api/predict-eligibility` | POST | AI predictions |
| `/api/learn` | POST | ML training |
| `/api/suggest` | POST | ML suggestions |

**Test with curl:**

```bash
# Search for forms
curl -X POST http://localhost:5000/api/search-form \
  -H "Content-Type: application/json" \
  -d '{"query": "learning license", "state": "india"}'

# Predict eligibility
curl -X POST http://localhost:5000/api/predict-eligibility \
  -H "Content-Type: application/json" \
  -d '{"age": 65, "income": 30000, "state": "chhattisgarh"}'
```

---

## 🎯 Key Differences from Old Version

| Feature | Old (v1) | New (v2) |
|---------|----------|----------|
| Form Database | ✅ Hardcoded 50 forms | ❌ None |
| Web Search | ❌ No | ✅ Real-time DuckDuckGo |
| Form Info | ❌ Static | ✅ Live scraping |
| AI/ML | ❌ Fake | ✅ Real Python ML |
| OCR | ❌ Pattern matching | ✅ Tesseract OCR |
| Updates | ❌ Manual | ✅ Always current |

---

## 🚀 Next Steps

### For Hackathon Demo:

1. ✅ **Practice**: Search 5 different forms
2. ✅ **Upload**: Test with Aadhar image
3. ✅ **Eligibility**: Show AI predictions
4. ✅ **ML**: Demonstrate learning

### For Production:

1. **Google Custom Search API**:
   - Get free API key
   - Replace DuckDuckGo scraping
   - Better results

2. **Deploy Backend**:
   - Use Heroku/Railway/PythonAnywhere
   - Replace localhost with real URL

3. **Publish Extension**:
   - Chrome Web Store
   - Edge Add-ons

---

## 📞 Need Help?

**Common Questions:**

**Q: Do I need internet?**
A: Yes, for form search and AI features. Basic validation works offline.

**Q: Is my data safe?**
A: Yes! All processing happens locally. Nothing sent to external servers except web search queries.

**Q: Can I add more forms?**
A: No need! It searches the internet in real-time.

**Q: How accurate is OCR?**
A: 80-90% for clear images. Improve by using high-quality scans.

**Q: How to improve ML model?**
A: Use it more! Model gets smarter with each correction.

---

**You're all set! Start the backend, load the extension, and start searching! 🎉**
