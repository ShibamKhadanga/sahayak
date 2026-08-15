# Sahayak — Git Setup, Run, & Push Guide

---

## Part 1 — Link Your Local Folder to Git & Push to GitHub

Open **VS Code's integrated terminal** (<kbd>Ctrl + `</kbd>) and make sure you're in:

```
f:\Programs\sahayak-final
```

Then run these commands **in order**:

### Step 1: Initialize a new Git repo

```powershell
git init
```

### Step 2: Set the default branch to `main`

```powershell
git branch -M main
```

### Step 3: Add the GitHub remote

```powershell
git remote add origin https://github.com/ShibamKhadanga/sahayak.git
```

### Step 4: Stage all files

```powershell
git add .
```

### Step 5: Create your first commit

```powershell
git commit -m "v2.0: Complete Sahayak rewrite with webapp, WhatsApp bot, OCR & ML upgrades"
```

### Step 6: Force-push to `main` (replaces old repo content)

```powershell
git push --force origin main
```

> [!CAUTION]
> `--force` will **overwrite** everything currently on the remote `main` branch. The old hackathon code will be gone from `main`. Make sure that's what you want.

> [!NOTE]
> If you get an authentication prompt, you'll need a **GitHub Personal Access Token (PAT)** — GitHub no longer accepts passwords for HTTPS.
> Generate one at: **GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)** → select `repo` scope.
> When prompted for a password, paste the token instead.

---

## Part 2 — Running the Project in VS Code

### Prerequisites

| Requirement | Install |
|---|---|
| **Python 3.8+** | [python.org](https://python.org) — make sure to check "Add to PATH" |
| **Tesseract OCR** | [Windows installer](https://github.com/UB-Mannheim/tesseract/wiki) |
| **Poppler** (for PDFs) | [Download](https://blog.alivate.com.au/poppler-windows/) — add `bin/` to your system PATH |
| **Google Chrome** | For the browser extension |

### Step 1: Open the project in VS Code

```powershell
code f:\Programs\sahayak-final
```

Or: **File → Open Folder → select `sahayak-final`**

### Step 2: Create a Python virtual environment

```powershell
python -m venv venv
```

### Step 3: Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

> [!TIP]
> If you get an execution policy error, run this first:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

### Step 4: Install Python dependencies

```powershell
pip install -r backend\requirements.txt
```

### Step 5: Start the Flask backend server

```powershell
python backend\app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### Step 6: Load the Chrome Extension

1. Open Chrome → go to `chrome://extensions/`
2. Enable **Developer Mode** (top-right toggle)
3. Click **"Load unpacked"**
4. Navigate to `f:\Programs\sahayak-final\extension\` and select it
5. The **Sahayak** icon appears in your toolbar ✅

### Step 7: Open the Webapp Dashboard

Open `f:\Programs\sahayak-final\webapp\index.html` in your browser (or serve it via VS Code's Live Server extension).

### Step 8: Test it

1. Make sure the Flask backend is running
2. Open any website in Chrome
3. Click the Sahayak extension icon
4. Type: **"I want to apply for Learner's License"**
5. Watch it search the internet and return live results!

---

## Part 3 — Ongoing: Push Future Changes from VS Code

After you make edits, use either the **terminal** or the **VS Code Source Control panel** (the branch icon on the left sidebar):

### Option A: Using the Terminal

```powershell
# 1. See what changed
git status

# 2. Stage all changes
git add .

# 3. Commit with a descriptive message
git commit -m "feat: add new feature X"

# 4. Push to GitHub
git push origin main
```

### Option B: Using VS Code GUI (Source Control Panel)

1. Click the **Source Control** icon in the sidebar (or <kbd>Ctrl + Shift + G</kbd>)
2. You'll see all changed files listed
3. Click the **`+`** icon next to each file (or next to "Changes" to stage all)
4. Type a commit message in the text box at the top
5. Click the **✓ checkmark** button (or <kbd>Ctrl + Enter</kbd>) to commit
6. Click **"Sync Changes"** or the **`↑`** push icon to push to GitHub

> [!TIP]
> Install the **GitLens** extension in VS Code for a much richer Git experience — inline blame, file history, branch comparison, etc.

---

## Quick Reference

| Action | Command |
|---|---|
| Check status | `git status` |
| Stage all | `git add .` |
| Stage specific file | `git add path/to/file` |
| Commit | `git commit -m "message"` |
| Push | `git push origin main` |
| Pull latest | `git pull origin main` |
| View log | `git log --oneline -10` |
| Undo last commit (keep files) | `git reset --soft HEAD~1` |
| Create new branch | `git checkout -b feature/name` |
