# 🐞 Lazy QA Agent | AI-Powered Automated Bug Reporting

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![AI](https://img.shields.io/badge/Model-Gemini%201.5%20Flash-orange)

**Stop writing bug reports manually.** Lazy QA is an intelligent agent that watches screen recordings of software glitches and generates professional, engineering-grade JIRA tickets instantly.

## 🚀 Live Demo
[Insert Your Streamlit Link Here]

## ⚡ Key Features
- **Multimodal Analysis:** Uses Google Gemini 1.5 Flash to "see" the bug in the video.
- **Auto-Step Generation:** Converts visual actions (clicks, scrolls) into written "Steps to Reproduce."
- **Root Cause Prediction:** The agent analyzes error messages or UI behavior to guess if it's a Backend, Frontend, or Network issue.
- **Dark Mode UI:** Built with a custom Streamlit theme for a modern developer experience.

## 🛠️ Tech Stack
- **Orchestration:** Python & Streamlit
- **AI Engine:** Google Gemini 1.5 Flash (Vision + Text)
- **Deployment:** Streamlit Community Cloud

## 📦 Local Setup
1. Clone the repo
2. `pip install -r requirements.txt`
3. `streamlit run app.py`

---
*Built as a showcase of Agentic AI Workflows.*
