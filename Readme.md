# Agentic ATS Resume Tailoring System

An asynchronous, enterprise-grade AI Agent infrastructure built with **LangGraph**, **FastAPI**, **Celery**, and **Qdrant**. This system enables job seekers to interact with a conversational AI Career Architect entirely through **WhatsApp** (powered by Twilio).

The platform orchestrates a deep multi-agent workflow: parsing incoming PDF resumes, analyzing skill gaps against real-time Job Descriptions, cross-referencing strict structural Applicant Tracking System (ATS) parsing rules, and rendering a dynamically optimized, ATS-compliant PDF resume.

To ensure strict data security and compliance, the application implements a structural **PII Anonymization Layer** using Microsoft Presidio and an adversarial **Self-Correction Guardrail Loop** to completely neutralize LLM hallucinations.

---

## 🏢 Enterprise Architecture Overview

The system decouples synchronous message ingestion from heavy LLM execution layers to completely prevent webhook timeouts, utilizing an event-driven background processing architecture.

```
                     ┌────────────────────────────────────────┐
                     │          WhatsApp / Meta API           │
                     └───────────────────┬────────────────────┘
                                         │
                        1. User sends message / PDF
                                         │
                                         ▼
                     ┌────────────────────────────────────────┐
                     │         Twilio API Gateway             │
                     └───────────────────┬────────────────────┘
                                         │
                        2. Forwards webhook payload
                                         │
                                         ▼
                     ┌────────────────────────────────────────┐
                     │          FastAPI Webhook Server        │
                     └─────┬───────────────────────────▲──────┘
                           │                           │
  3. Enqueues Task         │                           │ 6. Dispatches Final
  (Returns HTTP 200)       │                           │    Media & State Summary
                           ▼                           │
                     ┌─────────────────────────────────┴──────┐
                     │         Redis Message Broker           │
                     └───────────────────┬────────────────────┘
                                         │
                        4. Worker consumes task
                                         │
                                         ▼
                     ┌────────────────────────────────────────┐
                     │          Celery Background Worker      │
                     │  ┌──────────────────────────────────┐  │
                     │  │      LangGraph Orchestrator      │  │
                     │  └────────────────┬─────────────────┘  │
                     └───────────────────┼────────────────────┘
                                         │
                     5. State Graph Orchestration
                                         │
       ┌─────────────────────────┼─────────────────────────┐
       ▼                         ▼                         ▼
┌──────────────┐          ┌──────────────┐          ┌──────────────┐
│  PostgreSQL  │          │  Qdrant VDB  │          │  Microsoft   │
│ Checkpointer │          │  (ATS / Tech │          │   Presidio   │
│ (State/Sync) │          │  Knowledge)  │          │ (PII Masking)│
└──────────────┘          └──────────────┘          └──────────────┘
```

---

## 🛠️ Core Features & Business Capabilities

**Asynchronous State Machine Infrastructure**
Leverages LangGraph persistence engines, allowing users to send their resume in the morning and paste a job description hours later without losing multi-turn conversation context.

**Data Security & PII Sanitization**
Implements a strict Microsoft Presidio gateway node that scrubs all Personally Identifiable Information (names, phone numbers, addresses, emails) before sending data blocks to downstream foundational model APIs.

**Responsible AI Alignment Guardrails**
Features a deterministic verification engine that cross-examines modified resume text against the user's original documentation to verify that no skills, certificates, or growth metrics were fabricated by the primary LLM.

**RAG-Grounding Engine**
Contextualizes the tailoring engine with an indexed Qdrant vector database filled with empirical parser limitations (e.g., table layouts, columns, font restrictions) belonging to legacy tracking suites like Workday, Greenhouse, and Taleo.

**Rate-Limiting & High Availability**
Protects operational margins and API limits with an isolated, endpoint-level rate limiting layer.

---

## 📁 Repository Structure

```
Whatsapp_agent/
├── app/
│   ├── graph/
│   ├── rag/
│   ├── pii/
│   ├── pdf/
│   ├── workers/
│   ├── main.py
│   ├── celery_app.py
│   ├── config.py
│   ├── rate_limit.py
│   ├── twilio_utils.py
│   └── schemas.py
├── notebooks/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
└── .env
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Whatsapp_agent.git
cd Whatsapp_agent
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running Locally

Start each service in a separate terminal window in the following order:

### 1. Start Redis Server

```bash
redis-server
```

### 2. Start Qdrant Server

```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 3. Start Celery Worker

```bash
celery -A app.workers.tasks worker --loglevel=info
```

### 4. Start FastAPI Server

```bash
uvicorn app.main:app --reload --port 8000
```

### 5. Expose Webhook via ngrok

```bash
ngrok http 8000
```

---

## 🧪 System Usage Flow

This details the sequential end-to-end execution loop triggered when a user engages the WhatsApp endpoint:

| Step | Stage | Description |
|------|-------|-------------|
| 1 | **Document Ingestion** | The user uploads their resume (via raw text or a PDF attachment) over the WhatsApp thread. |
| 2 | **State Initialization** | The FastAPI gateway captures the payload and instantiates a state instance inside the LangGraph persistence engine, mapped to the user's phone number. |
| 3 | **Context Completion** | The user submits the target Job Description (JD) text block to complete the processing criteria. |
| 4 | **Data Masking** | The system passes both inputs through the Microsoft Presidio engine to redact sensitive personal identifiers before hitting external network endpoints. |
| 5 | **RAG Augmentation** | The engine splits the job requirements and searches the Qdrant vector database to extract structural parser compatibility constraints. |
| 6 | **Iterative Engineering** | The primary optimization LLM transforms legacy experience bullet layers into modern, metric-focused impact summaries. |
| 7 | **Adversarial Verification** | The self-correction guardrail node analyzes the revisions against the original raw material to strip out unauthorized skill fabrications or hallucinated statistics. |
| 8 | **Artifact Delivery** | The system converts the sanitized, tailored copy into a clean single-column format layout and streams it back to the user's handset. |

---

## 🔐 Environment Variables

Create a `.env` file in the project root and populate it with the following keys:

```env
# Twilio
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp_number


# LLM Provider
OPENAI_API_KEY=your_openai_api_key

# Redis
REDIS_URL=redis://localhost:6379/0

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/ats_db

# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-----------|
| Messaging Gateway | Twilio / WhatsApp Business API |
| API Server | FastAPI |
| Task Queue | Celery + Redis |
| AI Orchestration | LangGraph |
| Vector Database | Qdrant |
| State Persistence | PostgreSQL |
| PII Anonymization | Microsoft Presidio |
| PDF Processing | Custom PDF rendering pipeline |
| Tunnel (local dev) | ngrok |

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.