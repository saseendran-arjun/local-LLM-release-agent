\# Local LLM Release Preparation Agent

This project demonstrates a \*\*local AI agent\*\* for software release preparation and QA qualification

using an open-source LLM (via Ollama) and Python.

\## What it does

\- Reads a release request (requirements, scope, constraints)

\- Parses test logs to extract failures (deterministic Python tool)

\- Uses a local LLM to:

&nbsp; - Generate a release preparation checklist

&nbsp; - Propose a qualification plan

&nbsp; - Produce a QA qualification report (PASS / FAIL + actions)

No paid APIs are used. All inference runs locally.

\## Architecture
release_request.txt
│
▼
release_agent.py
│
├── Python log parser (FAIL / ERROR extraction)
│
├── LLM planning (release checklist)
│
└── LLM reporting (qualification summary)

## Tech Stack

- Python 3
- Ollama (local LLM runtime)
- LLaMA / Phi / Gemma models (configurable)

## How to run

1. Start Ollama and pull a model:

```bash
ollama pull llama3.2




```
