# ClassPulse

**Hear the room. Not just the raised hands.**

ClassPulse is an Education web-app prototype. A teacher opens a question; students join using a room code and submit short answers without entering names. The teacher closes the round, analyses patterns, inspects the original evidence, records a review, and opens a follow-up question.

## Start here

1. Install **Python 3.13 or 3.14** from https://www.python.org/downloads/.
2. Extract the complete ZIP into a normal folder. Do not run it from inside the ZIP.
3. **Windows:** double-click `START_WINDOWS.bat`. **Mac:** open `START_MAC.command` (if needed, run `zsh START_MAC.command` in Terminal from this folder).
4. First run downloads dependencies and asks you to choose a private teacher password. Password input is hidden: type it and press Enter.
5. Open **http://localhost:8765**. Keep the terminal window open.
6. Choose **Teacher studio**, sign in with your password, and create a room. Or choose **Explore a sample class** for eight clearly labelled fictional responses.
7. Copy the student link and open it in a private/incognito window to test a separate student session.
8. Submit an answer, return to the teacher view, close the round, and choose **Reveal patterns**.
9. Open the evidence, record a teacher review, and edit/open the follow-up question.

Localhost is a local test address, **not** the public competition submission URL.

## Manual installation

```sh
python -m venv .venv
# Mac/Linux:
source .venv/bin/activate
# Windows Command Prompt instead:
# .venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python setup.py
python app.py
```

Use `python3` or `py -3` to create the environment if `python` is not available. Use the activated environment's `python` thereafter.

## Real analysis modes

### Local ML (works without an API key)

Uses scikit-learn TF-IDF features and a K-means clustering model fitted to the actual submitted responses. It is real unsupervised machine learning, not hard-coded analysis. The number of clusters is capped at three. Exact response IDs and counts are validated.

**Limits:** it clusters similar words, not semantic truth. It can put correct and incorrect answers together if they use similar vocabulary. Pattern names are extracted terms. Teaching prompts in this mode are transparent templates. The teacher must interpret the evidence. Do not describe Local ML as an LLM or a proven misconception detector.

### Optional Gemini semantic analysis

Set `GEMINI_API_KEY` privately in the server environment, then restart. `GEMINI_MODEL` defaults to `gemini-3.8-flash`; select a model supported by your account if needed. The app uses Google's `generateContent` REST endpoint with JSON output. It sends the question, teacher reference, response IDs and answer text, never the browser tokens.

The dropdown enables Gemini only when a server key is configured. Every ID must appear exactly once in the returned groups. Unknown, duplicate or missing IDs cause a visible failure. Failed requests never silently become simulated Gemini results. **No live Gemini call has been verified without a real API key.** Quota and billing depend on your account.

Official API reference: https://ai.google.dev/api/generate-content

## Features

- Responsive desktop and phone interface; no Android installation required.
- Separate teacher password and public student routes.
- Shared SQLite response storage across browser sessions.
- Up to 50 responses per round and five rounds per room.
- One submission per browser session per round; this is not verified identity.
- Teacher-only original answers, reference, analysis and review.
- Original evidence behind every pattern; all counts computed by the app.
- Self-reported confidence, clearly separate from correctness.
- Follow-up rounds and side-by-side response/confidence snapshots.
- Presentation view; Escape exits.
- JSON export and room deletion.
- Explicit fictional sample class, separate from a new empty classroom.

## What changed from the earlier planning PDF

The delivered application uses **Flask + Waitress + SQLite**, not Streamlit. This supports a custom, polished interface and separate browser flows. Follow this README and `docs/START_HERE.html` for the actual app. The earlier planning PDF remains background reading, not the final installation guide. Only ClassPulse is included in this source package.

## Run tests

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Tests cover the two-round flow, authorisation, CSRF, anonymous student response visibility, input limits, duplicate/late submissions, empty analysis, sample labels, actual local clustering, invalid AI IDs and provider failure. See `docs/TEST_RESULTS.txt` for results actually run during packaging. No real classroom effectiveness study has been performed.

## Public deployment

The package includes `Dockerfile` and `render.yaml`. Hosting accounts and a public URL are not bundled into a source ZIP. Do not submit localhost.

### Render or a similar Python web host

1. Upload the clean source to your own public GitHub repository (exclude `.venv`, `instance`, `.env`, databases and credentials).
2. Create a Python web service from that repository. Build: `pip install -r requirements.txt`. Start: `python app.py`.
3. Set `HOST=0.0.0.0`, a strong `TEACHER_PASSWORD`, a random `SECRET_KEY`, and `COOKIE_SECURE=1` on an HTTPS host. The service supplies `PORT`.
4. Optionally set `GEMINI_API_KEY` and `GEMINI_MODEL` privately.
5. For durable storage, point `CLASSPULSE_DATA` at a persistent volume. Without one, data may disappear on restart/redeploy. Use only fictional data in a public judging demo.
6. Wait for `/health` to return `{"status":"ok"}`. Open the public link in incognito and test a student submission from a separate session.
7. Provide judges with appropriate access to an isolated demo teacher account, not a real staff password. Do not publish a production password in your README.

### Docker

```sh
docker build -t classpulse .
docker run --rm -p 8765:8765 -e TEACHER_PASSWORD -e SECRET_KEY -v classpulse-data:/data classpulse
```

Set those environment variables privately in your shell first. Docker is an alternative, not required for local use.

## Privacy, security and limits

This is a single-teacher-account prototype, not a multi-school service. Anyone with the teacher password can manage all rooms on this instance. Do not use real student records in a public demo. No names, roll numbers or emails are requested, but answer text can still contain personal information and hosting services may log technical metadata. Give students a clear notice before external AI processing.

Passwords are hashed; the session secret and local database are stored in `instance/`, excluded from source sharing. Mutating requests require a CSRF token; student input is escaped in the UI; database queries use parameters. Cookie secure mode should be enabled on HTTPS deployments. The public demo is not a substitute for production authentication, abuse prevention, retention controls or an institutional review.

Browser-session duplicate prevention can be bypassed by opening a new session. Displayed totals are submissions, not verified students. Confidence is self-reported. Different questions and participants make round comparisons descriptive, not proof of learning gains. AI suggestions are not official grades.

## Demo and submission

Use `docs/DEMO_SCRIPT.md` for a 3–5 minute walkthrough. The competition requires a public working app, public GitHub repository with README, a Google Drive video link accessible to anyone with the link, and the organiser's form submitted before the deadline. There must be no post-deadline code pushes. Hosting, repository creation, video upload and the submission form are separate actions; verify each before claiming completion.

## Acknowledgements

Built with Python, Flask, Waitress and scikit-learn; optional Gemini API. The local clustering approach is standard unsupervised ML, not a newly invented model. The product workflow and interface are a hackathon prototype and are not affiliated with an official institute system. Library licences remain with their respective authors.
