# 🛡️ AI SOC Analyst Agent
### An Agentic AI System for Automated Security Alert Triage and Investigation

An AI-powered Security Operations Center (SOC) assistant built with **LangChain, LangGraph, Groq LLMs, Retrieval-Augmented Generation (RAG), FAISS, FastAPI, and Streamlit**.

The system automates parts of the security alert investigation workflow by classifying alerts, retrieving relevant security knowledge, correlating related alerts, and generating structured AI-assisted investigation reports.

Designed as a cybersecurity automation project, it demonstrates how agentic workflows and LLM-powered reasoning can support security analysts while keeping critical incident-response decisions under human control.

> **Project focus:** Agentic AI · Generative AI · LLM Applications · RAG · Workflow Automation · Cybersecurity · API Development · Deployment

## 🚀 Key Features

- 🤖 **AI SOC Analyst Agent:** Uses an LLM to assist with alert investigation and produce structured security reports.
- 🔗 **LangChain Integration:** Connects the application to Groq-hosted LLMs and integrates retrieval components into the investigation workflow.
- 🔄 **LangGraph Orchestration:** Implements a stateful workflow with conditional routing for alert analysis, evidence collection, investigation, and skipped investigation.
- ⚙️ **Security Workflow Automation:** Automatically routes alerts based on preliminary severity and gathers supporting information for flagged alerts.
- 🧠 **Retrieval-Augmented Generation (RAG):** Retrieves relevant security guidance to provide contextual information to the LLM.
- 🔍 **Semantic Search:** Uses Sentence Transformers embeddings and FAISS similarity search to find relevant security knowledge.
- 🚨 **Automated Alert Triage:** Applies explainable rules to assign preliminary HIGH, MEDIUM, or LOW severity.
- 🔗 **Related Alert Correlation:** Searches for other sample alerts associated with the same source IP address.
- 📝 **AI Investigation Reports:** Generates reports covering observed evidence, potential explanations, additional evidence needed, and recommended investigation steps.
- 🌐 **FastAPI REST API:** Exposes endpoints for health checks and security alert analysis.
- 📊 **Interactive Streamlit Dashboard:** Provides an interface for viewing alerts and investigating their results.
- 🧪 **Automated Testing:** Includes tests for alert classification and LangGraph routing.
- 🔐 **Human-in-the-Loop Design:** AI outputs support analysts; they do not independently authorize incident-response actions.

## 🏗️ System Architecture

```text
                 Security Alert
                       |
                       v
              FastAPI REST API
                       |
                       v
              Rule-Based Triage
                       |
                       v
               LangGraph Workflow
                       |
                Conditional Router
                  /           \
                 /             \
         HIGH / MEDIUM          LOW
               |                 |
               v                 v
        Evidence Gathering   Skip LLM
               |
        +------+-------+
        |              |
        v              v
   Related Alerts   RAG Retrieval
                         |
                  Sentence Embeddings
                         |
                       FAISS
                         |
        +----------------+
        |
        v
   LangChain + Groq LLM
        |
        v
 AI-Assisted Investigation
        |
        v
 FastAPI Response / Streamlit UI
        |
        v
   Human Analyst Review
```

## 🧰 Technology Stack

| Technology | Role |
|---|---|
| Python | Core application development |
| LangChain | LLM integration and retrieval components |
| LangGraph | Stateful, conditional agent workflow orchestration |
| Groq API | Hosted LLM inference |
| Large Language Models | AI-assisted alert investigation and report generation |
| Hugging Face Sentence Transformers | Text embedding generation |
| FAISS | Vector similarity search |
| RAG | Context retrieval for investigation |
| FastAPI | REST API and request validation |
| Streamlit | Interactive SOC dashboard |
| Pydantic | API input validation |
| Pytest | Automated testing |
| Git and GitHub | Version control and source-code hosting |

## 🧠 Agentic AI and Automation

The project uses a LangGraph-orchestrated workflow to automate defined investigation steps.

### Workflow stages

1. **Alert Analysis:** A rule-based analyzer evaluates alert attributes and assigns preliminary severity.
2. **Conditional Routing:** LangGraph routes the alert according to whether the rules flag it for investigation.
3. **Evidence Collection:** The workflow searches for related alerts and relevant security knowledge.
4. **Context Retrieval:** The RAG component retrieves semantically similar security guidance using FAISS.
5. **LLM Investigation:** LangChain sends the collected alert evidence and retrieved context to the Groq-hosted model.
6. **Report Generation:** The model returns a structured investigation summary.
7. **Analyst Review:** Results are presented for human validation.

The workflow automates predefined steps rather than allowing an unrestricted autonomous agent to execute arbitrary security commands.

**Current implementation note:** Severity classification is rule-based. An ML-based intrusion-detection model and automated containment actions are future improvements, not currently implemented features.

## 📁 Project Structure

```text
SOC/
├── data/
│   ├── sample_alerts.json
│   └── security_knowledge.json
├── src/
│   ├── soc_agent/
│   │   ├── __init__.py
│   │   ├── alert_analyzer.py
│   │   ├── llm_analyzer.py
│   │   ├── graph.py
│   │   ├── tools.py
│   │   └── rag.py
│   ├── main.py
│   ├── api.py
│   ├── dashboard.py
│   ├── test_alert_analyzer.py
│   ├── test_routing.py
│   ├── test_graph.py
│   ├── test_llm.py
│   └── test_tools.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Prerequisites

- Python 3.12 recommended
- Git
- A Groq API key
- VS Code or another Python-compatible editor

### 2. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-soc-analyst-agent.git
cd ai-soc-analyst-agent
```

Replace `YOUR_USERNAME` with your GitHub username.

### 3. Create and Activate a Virtual Environment

**Windows PowerShell:**

```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

Use your own API key. Never commit `.env` to GitHub.

### 6. Run the Rule-Based Analyzer

```powershell
python .\src\main.py
```

This analyzes the supplied synthetic alerts using the configured severity rules.

## ▶️ Run the Application

### Start the FastAPI Backend

From the project root:

```powershell
uvicorn api:app --app-dir src --host 127.0.0.1 --port 8000 --reload
```

API documentation: http://127.0.0.1:8000/docs

Health check: http://127.0.0.1:8000/health

Alert analysis endpoint: `POST /analyze`

### Start the Streamlit Dashboard

Open a second terminal, activate the virtual environment, and run:

```powershell
streamlit run .\src\dashboard.py
```

Open the local address displayed by Streamlit, usually http://localhost:8501.

The dashboard communicates with the local API at `http://127.0.0.1:8000`.

## ☁️ Deployment

The application can be prepared for deployment as two services:

- **Backend:** FastAPI application served by Uvicorn.
- **Frontend:** Streamlit dashboard.

Suitable hosting options include platforms that support Python web services and Streamlit applications. Public deployment requires configuring the frontend to use the deployed backend URL rather than `127.0.0.1`.

### Deployment checklist

1. Push the project to GitHub.
2. Configure the backend service to install dependencies from `requirements.txt`.
3. Set `GROQ_API_KEY` and `GROQ_MODEL` as environment variables in the hosting platform's secret/environment settings.
4. Start the API using a production-appropriate command, for example:

   ```bash
   uvicorn api:app --app-dir src --host 0.0.0.0 --port $PORT
   ```

   Adapt the port configuration to the hosting provider.

5. Configure the Streamlit dashboard to use the deployed API URL.
6. Test `/health` and `/analyze` after deployment.
7. Configure appropriate authentication, access controls, and secret management before exposing sensitive services publicly.

**Deployment status:** The project deployed on render


- **Live Dashboard:** Not deployed yet
- **Backend API:** Not deployed yet
- **API Documentation:** Available locally at `/docs`

## 🧪 Testing

Run the alert-classification tests:

```powershell
python -m pytest .\src\test_alert_analyzer.py -v
```

Run the routing tests:

```powershell
python .\src\test_routing.py
```

The routing tests use mocked LLM and retrieval functions to test conditional workflow behavior without making live Groq requests.

## 🔐 Security Considerations and Limitations

- The supplied alerts are synthetic development examples.
- Current severity classification is based on manually configured rules, not a trained ML model.
- The RAG knowledge base is small and manually curated.
- The FAISS index is currently built in memory.
- The API does not yet implement authentication, rate limiting, persistent incident storage, or comprehensive audit logging.
- LLM-generated investigation reports may be incomplete or incorrect and require analyst validation.
- The application does not automatically block IP addresses, disable accounts, or execute containment actions.

Do not use this development version as a standalone production security-monitoring system.

## 👩‍💻 Author

**Sania Parveen**

B.S. in Data Science and Applications — IIT Madras

**Areas of Interest:** Artificial Intelligence, Machine Learning, Generative AI, Agentic AI, and Cybersecurity.

GitHub: [Saniaparveen0196](https://github.com/Saniaparveen0196)

---

*Developed as a learning and portfolio project exploring agentic AI, LLM-based investigation, RAG, and workflow automation for cybersecurity operations.*
