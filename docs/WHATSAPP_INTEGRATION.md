# WhatsApp Integration Guide

Sahayak's WhatsApp bot and the operator dashboard (`webapp/`) are two
front doors onto **the same backend**. Every message, document, or typed
field goes through `backend/session_store.py` and `backend/form_engine.py`
— there's exactly one copy of each session's data, so whichever channel a
person used, the other channel sees it on its next read.

```
Citizen on WhatsApp ──┐
                       ├──► session_store.py (backend/data/sessions.json)
Operator on dashboard ─┘         ▲
                                  │
                    Both read/write through
                    form_engine.py + forms_catalog.py
```

## Option A — Try it instantly with the built-in simulator (no Twilio needed)

1. Start the backend: `cd backend && python app.py`
2. Open `webapp/index.html` in a browser (or serve the folder with
   `python -m http.server 8080` from inside `webapp/`)
3. Click the **"Test WhatsApp"** button in the bottom-right corner
4. Type `hi`, pick a form by number, then attach documents with the 📎
   button — the simulator hits the exact same `whatsapp_bot.py` logic
   Twilio would trigger, and the sessions it creates appear in the
   register table on the left, live.

This is the fastest way to demo the whole flow and is enough for local
development — you only need Option B when you want a real WhatsApp
number.

## Option B — Connect a real WhatsApp number with Twilio

Twilio's WhatsApp Sandbox is free and takes a few minutes to set up.

### 1. Get a Twilio account and join the sandbox
- Sign up at twilio.com, open **Messaging → Try it out → Send a WhatsApp message**
- Follow the on-screen instructions to join the sandbox from your own phone
  (you'll send a "join &lt;code&gt;" message to Twilio's sandbox number)

### 2. Expose your local backend to the internet
Twilio needs to reach your Flask server, so tunnel it (e.g. with ngrok):
```bash
ngrok http 5000
```
Copy the `https://...ngrok-free.app` URL it prints.

### 3. Point the sandbox at your webhook
In the Twilio console, under the sandbox settings, set
**"When a message comes in"** to:
```
https://<your-ngrok-url>/whatsapp/webhook
```
Method: `HTTP POST`.

### 4. (Optional) Set credentials for media downloads
Photos and PDFs sent on WhatsApp are fetched from Twilio's media URLs,
which require your account credentials:
```bash
export TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export TWILIO_AUTH_TOKEN=your_auth_token
```
Without these set, text-only conversations still work, but uploaded
documents won't download (you'll see a warning in the backend log).

### 5. Test it
Message your sandbox number "hi" from WhatsApp. You should get the forms
menu back, and the session will show up in the dashboard's register table
within a few seconds (it polls every 4 seconds).

## How the conversation flows

1. **Pick a form** — the bot lists every form in `forms_catalog.py` and
   waits for a number reply.
2. **Send documents one at a time** — the bot asks for each document the
   form needs (`forms_catalog.py` → `documents`), in order. Each upload is
   OCR'd by `ocr_processor.extract_smart_data()` (the same function the
   web dashboard's document upload uses), and any recognised fields
   (name, DOB, address, Aadhaar number, etc.) are filled in automatically.
3. **Answer whatever's still missing** — once every document is in, the
   bot asks one-by-one for any required field that wasn't found on a
   document (e.g. income, or a field no document mentioned).
4. **Done** — the bot sends a summary, and the case is marked *Complete*
   on the dashboard, ready for an operator to review and submit.

At any point, typing **menu** restarts the current session's form choice,
and **status** shows progress without restarting anything.

## Production notes

- `backend/data/sessions.json` is a simple file store — fine for a CSC's
  scale of concurrent sessions, but swap `session_store.py` for a real
  database if you outgrow it; nothing else needs to change since every
  other module only calls its functions.
- Session data contains personal information (names, Aadhaar numbers,
  etc.) — keep `backend/data/` out of version control (already in
  `.gitignore`) and restrict access to the server it runs on.
- This bot answers with WhatsApp's plain-text formatting (`*bold*`,
  line breaks). If you want quick-reply buttons or list menus, that's a
  Twilio Content API / WhatsApp Business API upgrade on top of the same
  `whatsapp_bot.handle_incoming()` function — the conversation logic
  itself wouldn't need to change.
