# 🏛️ CivicPulse | THE_VANGUARD_HACKATHON_DITE

> **Turn unstructured community feedback into an actionable, real-time local problem map.**

CivicPulse is a smart civic-tech web application built for the hackathon that collects citizen complaints via text or voice, automatically classifies and structures the issue, groups duplicate reports spatially, and pins them onto an interactive local hotspot map.

---

## 🚀 The Real-World Problem

Local public complaints—such as water supply leakages, uncollected garbage, or failing streetlights—often remain scattered across informal WhatsApp messages, local Facebook groups, or ignored phone lines. Municipal authorities lack a single, structured view of real-time community needs, leading to slow response times and redundant work.

## 💡 The Solution

Rather than building another generic "complaint chatbot," **CivicPulse** transforms messy, unstructured feedback into a **dynamic municipal hotspot map**. 

* **Citizen-Facing:** Submit voice or text reports securely using CNIC verification.
* **Smart Deduplication Engine:** Automatically checks for duplicate complaints within a spatial radius and merges them into a single high-priority hotspot cluster.
* **Actionable Hotspots:** Authorities see clear cluster badges and severity indicators instead of endless individual support tickets.

---

## ✨ Key Features

- **🔒 CNIC & Password Authentication:** Secure login and registration backed by an SQLite database.
- **🎙️ Voice-to-Text Input:** Integrated Web Speech API for low-friction voice reporting.
- **🗺️ Dynamic Leaflet.js Mapping:** Interactive map markers displaying localized problem hotspots.
- **⚡ SQLite Data Persistence:** Full backend state management using Python, Flask, and SQLAlchemy.

---

## 🛠️ Tech Stack

* **Frontend:** HTML5, Tailwind CSS, JavaScript (Vanilla ES6), Leaflet.js, Web Speech API.
* **Backend:** Python 3, Flask, Flask-SQLAlchemy.
* **Database:** SQLite (`civicpulse.db`).

---

## 📦 Quick Start & Local Setup

### Prerequisites
Make sure you have **Python 3.8+** installed on your system.

### 1. Clone the Repository
```bash
git clone [https://github.com/khizarshaikh-ai/THE_VANGUARD_HACKATHON_DITE.git](https://github.com/khizarshaikh-ai/THE_VANGUARD_HACKATHON_DITE.git)
cd THE_VANGUARD_HACKATHON_DITE
