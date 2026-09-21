# 🧪 Agentic AI Lab (Internal)

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Gemini](https://img.shields.io/badge/LLM-Gemini-orange)
![Status](https://img.shields.io/badge/status-internal--demo-lightgrey)

Standalone, Gemini-powered agentic AI demos built with Google's `google-genai` SDK. Each script is independently runnable and shows a different agentic pattern — RAG, text-to-SQL, and a multi-agent pipeline.

## Quickstart

```bash
git clone https://github.com/Mandadapu-Kinnera/Agentic_AI_Lab_Internal.git
cd Agentic_AI_Lab_Internal
pip install -r requirements.txt
cp .env.example .env   # then add your GEMINI_API_KEY
```

Get a key at [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key).

## What's Inside

| Script | Pattern | Models Used | What it does |
|---|---|---|---|
| [`rag_qa.py`](./rag_qa.py) | Retrieval-Augmented Generation | `gemini-embedding-2`, `gemini-3.1-flash-lite` | Embeds a small knowledge base, retrieves the most relevant docs for a question, answers from context (falls back to general knowledge if context isn't relevant) |
| [`text_to_sql.py`](./text_to_sql.py) | Text-to-SQL | `gemini-3.1-flash-lite` | Reads a SQLite schema, converts a natural-language question into SQL, executes it, and prints the results |
| [`run_sdr.py`](./run_sdr.py) + [`sdr_system/`](./sdr_system) | Multi-agent pipeline | `gemini-3.1-flash-lite` | Three chained agents — lead generation → qualification (Hot/Warm/Cold) → email drafting (dry-run only) |

## Running Each Demo

```bash
python rag_qa.py          # ask a question, get a RAG-grounded answer
python text_to_sql.py     # ask a question about the sample employees table
python run_sdr.py         # run the full SDR pipeline with the default ICP
python run_sdr.py "VP of Sales at SaaS companies, 100-500 employees"  # custom ICP
```

## SDR Pipeline Detail

```
ICP description
      │
      ▼
1. Lead Generation Agent   → filters mock prospect pool for ICP fit
      │
      ▼
2. Qualification Agent     → BANT-style scoring, tiers Hot / Warm / Cold
      │
      ▼
3. Email Agent             → drafts outreach (dry-run, saved to output/outbox/)
```

All leads in `sdr_system/data/raw_leads.py` are fictitious (`@example.com`). No real emails are ever sent.

## Repo Layout

```
Agentic_Exam/
├── rag_qa.py
├── text_to_sql.py
├── run_sdr.py
├── requirements.txt
├── .env.example
├── company.db              (git-ignored)
└── sdr_system/
    ├── config.py            # shared Gemini client + retry logic
    ├── orchestrator.py       # runs the 3 agents in sequence
    ├── agents/               # lead_gen_agent.py, qualification_agent.py, email_agent.py
    ├── data/raw_leads.py     # mock prospect pool
    └── output/               (git-ignored)
```

## Stack

- Python 3.12 · [`google-genai`](https://pypi.org/project/google-genai/) · `python-dotenv` · SQLite (stdlib)
- `.env`, `company.db`, `__pycache__/`, `sdr_system/output/` are git-ignored — no credentials or generated artifacts committed.
