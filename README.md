# The Lazy QA Agent 🤖
### *Autonomous AI Agent for Automated Bug Reporting via Vision LLMs*

**The Lazy QA Agent** is an intelligent workflow designed to streamline the software quality assurance process. By integrating **Vision models** and **LLMs**, the agent autonomously parses screen recordings of software defects and generates highly structured, engineering-grade bug reports. This eliminates the manual overhead of documenting reproduction steps and ensures consistency across engineering teams.

---

## 🚀 Key Engineering Highlights

* **Autonomous Media Parsing:** Leverages Vision LLMs to analyze video recordings, extracting logical reproduction steps and identifying actual vs. expected behaviors.
* **Asynchronous Processing:** Built with **FastAPI** using non-blocking I/O to handle concurrent video ingestion and heavy AI processing tasks without performance degradation.
* **Highly Structured Reporting:** Enforces strict Pydantic schemas to produce reports containing Title, Severity, Reproduction Steps, and Root Cause Hypothesis—ready for JIRA/Azure DevOps integration.
* **DevOps Integration:** Configured with **Azure DevOps CI/CD pipelines** and **Docker** to automate testing and streamline the deployment of the AI agent.

---

## 🛠️ Technical Stack

* **Language:** Python 3.10+
* **AI Engine:** Google Gemini (Vision & Pro)
* **Backend:** FastAPI (Asynchronous)
* **DevOps:** Azure Pipelines, Docker
* **Validation:** Pydantic, Pytest

---

## 📂 Project Structure

    ├── api/            # Asynchronous Endpoints & Pydantic Schemas
    ├── core/           # Vision Parser & Bug Report Generation Engine
    ├── tests/          # Automated Unit & Integration Test Suite
    ├── azure-pipelines.yml # CI/CD Pipeline Configuration
    ├── Dockerfile      # Containerization for Streamlined Deployment
    └── main.py         # Application Entry Point

---



## ⚙️ Installation & Setup

1. **Clone the repository:**
    ```bash
    git clone git@github.com:yourusername/The-Lazy-QA-Agent.git
    cd The-Lazy-QA-Agent
    ```

2. **Configure Environment:**
    Create a `.env` file:
    ```bash
    GEMINI_API_KEY=your_api_key
    MEDIA_UPLOAD_DIR=./temp_media
    ```

3. **Deploy with Docker:**
    ```bash
    docker build -t lazy-qa-agent .
    docker run -p 8000:8000 lazy-qa-agent
    ```

---

## 🧪 Automated Testing

This project maintains high code quality through automated testing integrated into the Azure DevOps pipeline.

**Run local tests:**
```bash
pytest -v