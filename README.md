ClassPulse 🎓

Hear the room. Not just the raised hands.

ClassPulse is an interactive, real-time classroom web-app prototype. A teacher posts a prompt; students join instantly via room code and submit anonymous, short responses. The teacher closes the round, runs machine-learning analyses to discover answer patterns and misconceptions, inspects evidence, records a review, and launches follow-up questions—all in real time.

📌 Table of Contents

Quick Start

Manual Installation

Analysis Modes

Key Features

Architecture & Tech Stack

Running Tests

Deployment

Render / Cloud Web Host

Docker

Privacy, Security & Limitations

Demo Walkthrough & Submission

Acknowledgements

⚡ Quick Start

Download Python: Install Python 3.13 or 3.14 from python.org.

Extract Archive: Unzip the project files into a normal folder (do not run directly inside the archive).

Launch Server:

Windows: Double-click START_WINDOWS.bat.

Mac: Open START_MAC.command (or run zsh START_MAC.command in Terminal).

Initial Configuration: On first launch, dependencies will install automatically. You will be prompted to set a private teacher password (input is masked—type password and hit Enter).

Open App: Visit http://localhost:8765 in your web browser. Keep the terminal active.

Teacher Studio / Demo: Log in to Teacher studio to launch a live room, or select Explore a sample class to inspect 8 pre-populated fictional responses.

Student Experience: Copy the student room link, open an incognito/private browser window, and submit a test response.

Analyze: Return to the teacher panel, close the round, and click Reveal patterns.

⚠️ Note: localhost is your local testing environment, not a public deployment URL.

🛠 Manual Installation

If you prefer to set up the Python environment manually:

=======
# ClassPulse 🎓

> **Hear the room. Not just the raised hands.**

ClassPulse is an interactive, real-time classroom web application prototype. Teachers can launch instant questions, aggregate anonymous short responses, run machine-learning models to surface common misconceptions, inspect evidence, record reviews, and open follow-up rounds.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Quick Start](#-quick-start)
- [Manual Setup](#-manual-setup)
- [Analysis Modes](#-analysis-modes)
  - [Local Machine Learning (Default)](#1-local-machine-learning-default)
  - [Gemini AI Semantic Analysis (Optional)](#2-gemini-ai-semantic-analysis-optional)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Testing](#-testing)
- [Deployment](#-deployment)
  - [Cloud Hosting (Render / Railway)](#cloud-hosting-render--railway)
  - [Docker Container](#docker-container)
- [Security & Privacy](#-security--privacy)
- [Demo Script & Submission](#-demo-script--submission)
- [Acknowledgements](#-acknowledgements)

---

## 🔎 Overview

ClassPulse solves the engagement gap in classroom settings by allowing friction-free, anonymous responses. Instead of relying only on students who raise their hands, teachers get a structured view of the whole room's understanding using built-in unsupervised machine learning and generative AI analysis.

---

## ⚡ Quick Start

1. **Download Python:** Install **Python 3.13 or 3.14** from [python.org](https://www.python.org/downloads/).
2. **Extract Archive:** Unzip the project folder (*do not run directly from inside a ZIP file*).
3. **Run the Script:**
   - **Windows:** Double-click `START_WINDOWS.bat`.
   - **Mac / Linux:** Run `START_MAC.command` (or execute `zsh START_MAC.command` in Terminal).
4. **Initial Configuration:** On first launch, required packages will auto-install and prompt for a private teacher password (*input is masked*).
5. **Launch Application:** Open [`http://localhost:8765`](http://localhost:8765) in your web browser.
6. **Try Sample Data:** Log in to **Teacher Studio** or select **Explore a Sample Class** to test with pre-loaded fictional responses.

> ⚠️ **Note:** `localhost` is for local testing only and is not accessible externally.

---

## 🛠 Manual Setup

If you prefer installing dependencies using standard terminal commands:

```bash
>>>>>>> 716e120 (Update README)
# Clone the repository
git clone https://github.com/your-username/classpulse.git
cd classpulse

<<<<<<< HEAD
# Create and activate a virtual environment
python -m venv .venv

# Mac/Linux:
source .venv/bin/activate

# Windows (Command Prompt):
# .venv\Scripts\activate.bat

# Install dependencies and initialize application
=======
# Create and activate virtual environment
python -m venv .venv

# On Mac/Linux:
source .venv/bin/activate

# On Windows (Command Prompt):
# .venv\Scripts\activate.bat

# Install dependencies and setup instance
>>>>>>> 716e120 (Update README)
python -m pip install -r requirements.txt
python setup.py
python app.py

<<<<<<< HEAD

Tip: If python is not recognized, try python3 or py -3. Always use the activated environment's Python binary going forward.

🧠 Analysis Modes

ClassPulse supports two distinct modes for clustering and evaluating student responses:

1. Local Machine Learning (No API Key Required)

Runs locally using scikit-learn TF-IDF term extraction paired with a K-Means clustering model fitted directly to submitted student responses.

Behavior: Clusters up to 3 groups based on vocabulary similarities. Validates exact response IDs and total counts.

Limitations: Clusters similar vocabulary, not semantic logic. Syntactically similar correct and incorrect answers may group together. Teachers must manually inspect and interpret the underlying evidence.

2. Optional Gemini AI Semantic Analysis

When configured, ClassPulse communicates with Google's Gemini REST API (generateContent) using strict JSON schemas to group answers semantically.

Setup: Set the GEMINI_API_KEY environment variable in your server environment and restart. Default model is gemini-3.8-flash (override via GEMINI_MODEL if needed).

Data Flow & Privacy: Only question prompts, teacher reference keys, response IDs, and answer text are sent. No user tokens or PII are transmitted.

Validation: Every response ID must be explicitly returned in the structured output; duplicate or omitted IDs trigger an explicit error display.

Docs: Google Gemini API Reference.

✨ Key Features

📱 Fully Responsive: Optimized UI for desktop, tablet, and mobile browsers—no native apps required.

🔐 Secure Access Separation: Isolated teacher authentication with public, frictionless student entry.

⚡ Persistent Multi-Session Data: Shared SQLite database manages real-time classroom state across sessions.

📊 Interactive Analytics: Supports up to 50 student submissions per round, 5 rounds per room.

🕵️ Original Evidence Inspection: Drill down into raw student inputs behind every identified cluster.

💪 Confidence & Correctness Tracking: Tracks self-reported student confidence metrics separately from response accuracy.

🖼️ Presentation Mode: One-click clean display for projector mirroring (Press Esc to exit).

📁 Data Export: Download room data and analytics as JSON, or wipe sessions cleanly.

🏗 Architecture & Tech Stack

   ┌─────────────────┐       ┌─────────────────┐
   │ Student Session │       │ Teacher Studio  │
   └────────┬────────┘       └────────┬────────┘
            │                         │
            └───────────┬─────────────┘
                        │ HTTP / JSON
                        v
     ┌──────────────────────────────────────┐
     │  Flask + Waitress Application Server │
     └──────────────────┬───────────────────┘
                        │
         ┌──────────────┼──────────────┐
         v              v              v
  ┌────────────┐ ┌────────────┐ ┌────────────┐
  │ SQLite DB  │ │  Local ML  │ │ Gemini API │
  │ (Data Store)││(scikit-learn)││ (Optional) │
  └────────────┘ └────────────┘ └────────────┘


Backend: Python 3.13+, Flask, Waitress WSGI Server

Database: SQLite3

Machine Learning: scikit-learn (TF-IDF + K-Means)

AI Integration: Google Gemini API (google-genai REST integration)

Note: The app relies on Flask + Waitress + SQLite for low-latency server-rendered flows, replacing earlier planning prototypes.

🧪 Running Tests

Execute the automated test suite covering authentication, CSRF validation, submission constraints, clustering logic, and API fail-safes:

# Install development and testing dependencies
=======
---

## 🧠 Analysis Modes

ClassPulse supports two modes for response aggregation and pattern detection:

### 1. Local Machine Learning (Default)
- **Engine:** `scikit-learn` TF-IDF term extraction paired with a K-Means clustering model.
- **Requirements:** None. Works offline without API keys.
- **How it works:** Groups responses into up to 3 clusters based on keyword frequencies.
- **Notes:** Local ML matches vocabulary patterns rather than underlying semantic logic. Teachers should inspect raw evidence before drawing conclusions.

### 2. Gemini AI Semantic Analysis (Optional)
- **Engine:** Google Gemini API (`generateContent`) with JSON schema enforcement.
- **Requirements:** Requires setting `GEMINI_API_KEY` in environment variables.
- **How it works:** Groups answers based on semantic understanding and underlying misconceptions.
- **Data Safety:** Sends only question prompts, reference answers, response IDs, and answer text. Never transmits browser tokens or PII.

---

## ✨ Key Features

- 📱 **Zero Installation for Students:** Fully responsive browser UI for desktop, tablet, and mobile.
- 🔒 **Separated Interfaces:** Private authenticated Teacher Studio vs. public instant-join Student view.
- 📊 **Real-time Analytics:** Up to 50 responses per round, supporting 5 sequential rounds per room.
- 💪 **Confidence Indicators:** Tracks self-reported confidence separately from answer correctness.
- 🖼️ **Projector Mode:** Clean, full-screen presentation layout (Press `Esc` to exit).
- 💾 **Export Options:** Export complete room reports and analytics as JSON data.

---

## 🏗 System Architecture

```text
   ┌──────────────────┐           ┌──────────────────┐
   │ Student Session  │           │  Teacher Studio  │
   └────────┬─────────┘           └────────┬─────────┘
            │                              │
            └──────────────┬───────────────┘
                           │ HTTP / JSON
                           v
     ┌──────────────────────────────────────────┐
     │   Flask + Waitress Application Server   │
     └────────────────────┬─────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          v               v               v
  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
  │  SQLite DB   │ │   Local ML   │ │  Gemini API  │
  │ (Data Store) │ │(scikit-learn)│ │  (Optional)  │
  └──────────────┘ └──────────────┘ └──────────────┘
```

---

## 🧪 Testing

Run the automated test suite covering authentication, CSRF protections, input validation, and clustering reliability:

```bash
>>>>>>> 716e120 (Update README)
python -m pip install -r requirements-dev.txt

# Run pytest suite
python -m pytest -q

<<<<<<< HEAD

Review past test logs in docs/TEST_RESULTS.txt.

🚀 Deployment

Render / Cloud Web Host

Push your sanitized codebase to a private/public GitHub repository (verify .venv, instance/, .env, and databases are in .gitignore).

Create a new Python Web Service on Render (or equivalent provider).

Build Command: pip install -r requirements.txt

Start Command: python app.py

Configure Environment Variables:

HOST=0.0.0.0
TEACHER_PASSWORD=YourSuperStrongPasswordHere
SECRET_KEY=YourRandomSecretSessionKey
COOKIE_SECURE=1
GEMINI_API_KEY=YourOptionalApiKey
GEMINI_MODEL=gemini-3.8-flash


Persistent Data: Mount a persistent disk volume to the path designated by CLASSPULSE_DATA so SQLite database records persist across deployments.

Verify setup by checking https://your-app-name.onrender.com/health.

Docker

# Build Docker image
docker build -t classpulse .

# Run container with environment variables and local volume
docker run --rm -p 8765:8765 \
  -e TEACHER_PASSWORD="YourPassword" \
  -e SECRET_KEY="YourSecretKey" \
  -v classpulse-data:/data \
  classpulse


🔒 Privacy, Security & Limitations

Single-Teacher Design: Designed for single-instructor deployment. Anyone possessing the global teacher password has administrative privileges on that instance.

Data Minimization: No usernames, emails, or student credentials are required or logged. Remind students not to enter PII in open answer fields.

Session Integrity: Duplicate prevention relies on browser cookies/sessions, which can be reset in incognito mode.

Security Controls: Session passwords use secure hashing algorithms; mutating requests require CSRF protection tokens; database access is fully parameterized to prevent SQL injection.

🎥 Demo Walkthrough & Submission

For a step-by-step 3–5 minute presentation script, refer to docs/DEMO_SCRIPT.md.

Submission Checklist:

[x] Public live web application URL

[x] Public GitHub repository with documentation

[x] Unlisted/Public video demonstration link

[x] Verified /health endpoint status

🤝 Acknowledgements

Built with ❤️ using Python, Flask, Waitress, scikit-learn, and the Google Gemini API.
=======
---

## 🚀 Deployment

### Cloud Hosting (Render / Railway)

1. Push your code to a GitHub repository (ensure `.venv`, `instance/`, and credentials are listed in `.gitignore`).
2. Create a new Python Web Service.
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
3. Configure Environment Variables:
   ```env
   HOST=0.0.0.0
   TEACHER_PASSWORD=YourSecurePassword
   SECRET_KEY=YourRandomSecretKey
   COOKIE_SECURE=1
   GEMINI_API_KEY=YourApiKeyHere
   ```
4. Attach a persistent volume mapped to `CLASSPULSE_DATA` to keep SQLite data intact across redeploys.

### Docker Container

```bash
# Build Image
docker build -t classpulse .

# Run Container
docker run --rm -p 8765:8765 \
  -e TEACHER_PASSWORD="YourPassword" \
  -e SECRET_KEY="YourSecretKey" \
  -v classpulse-data:/data \
  classpulse
```

---

## 🔒 Security & Privacy

- **Minimal Data Collection:** No names, emails, or personal identifiers are requested from students.
- **CSRF & Parameterized Queries:** Full protection against cross-site request forgery and SQL injection attacks.
- **Hashed Credentials:** Password strings are hashed prior to storage in local instances.

---

## 🎥 Demo Script & Submission

See [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md) for a complete 3–5 minute presentation transcript and testing walkthrough.

---

## 🤝 Acknowledgements

Developed with Python, Flask, Waitress, scikit-learn, and the Google Gemini API.
