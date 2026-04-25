# ARES Optimizer

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-ready-green) ![Status](https://img.shields.io/badge/Status-public--safe%20showcase-purple) ![License](https://img.shields.io/badge/License-MIT-yellow)

**Public-safe AI routing, retrieval, and orchestration layer for A.R.E.S.**

Built by **Kai Harris** — aspiring ML / AI Software Engineer.

ARES Optimizer demonstrates how an AI assistant can move beyond a single-model chatbot architecture by adding a decision layer that classifies requests, plans retrieval, selects execution paths, and produces traceable system behavior.

> This repository is intentionally public-safe. It shows the architecture, interfaces, and runnable demonstration while protecting proprietary scoring, private policy tuning, and production deployment internals.

---

## Why This Project Matters

Most assistant projects use a simple flow:

```text
User Input -> One Model -> Response
```

ARES Optimizer uses a system-level flow:

```text
User Input
   -> Task Classification
   -> Retrieval Planning
   -> Context Selection
   -> Model Routing
   -> A.R.E.S Backend / Local LLM
   -> Traceable Response
```

That shift matters because real AI systems need different paths for different work: coding, reasoning, retrieval, memory, tool use, and fast conversation.

---

## Recruiter / Reviewer Highlights

- **AI systems architecture:** modular orchestration rather than a single monolithic chatbot
- **Routing intelligence:** task classification and route selection for specialized model paths
- **RAG-ready design:** retrieval planning, context scoring, and reranking hooks
- **Local-first compatibility:** designed around local A.R.E.S / OpenAI-style backend integration
- **Traceability:** every request returns an agent trace for inspection
- **GitHub-ready engineering:** tests, CI workflow, Dockerfile, typed schemas, and clear docs
- **Public/private separation:** demonstrates product architecture without exposing sensitive optimizer logic

---

## Architecture

```text
                          +----------------+
                          |   User Input   |
                          +-------+--------+
                                  |
                                  v
+---------------------------------------------------------------+
|                    ARES Optimizer Layer                       |
|                                                               |
|  +-------------+   +----------------+   +------------------+  |
|  | Classifier  |-> | Retrieval Plan |-> | Context Retriever |  |
|  +-------------+   +----------------+   +------------------+  |
|          |                  |                    |             |
|          v                  v                    v             |
|  +-------------+   +----------------+   +------------------+  |
|  | Reranker    |-> | Model Router   |-> | Response Adapter |  |
|  +-------------+   +----------------+   +------------------+  |
+---------------------------------------------------------------+
                                  |
                                  v
                    +----------------------------+
                    | A.R.E.S Backend / Local LLM |
                    +----------------------------+
```

---

## Public Showcase vs. Private Production System

| Area | Public Repository | Private / Production Layer |
|---|---|---|
| Classifier | transparent scoring demo | learned policy + advanced signals |
| Retrieval | local JSON corpus demo | vector DB, memory, docs, live sources |
| Reranking | deterministic public scoring | proprietary ranking and tuning |
| Routing | explainable route choice | adaptive model routing policy |
| Backend | demo responder | A.R.E.S local LLM / OpenAI-compatible server |
| Feedback | public hooks | production optimization loop |

This is intentional. The repo is designed to impress reviewers while keeping the most valuable implementation details protected.

---

## Core Features

### Dynamic Task Classification
Routes user messages into categories such as:

- chat
- retrieval
- reasoning
- coding
- memory
- tool use
- vision

### Retrieval Planning
Determines whether context is needed and selects a retrieval strategy.

### Context Retrieval and Reranking
Demonstrates how memory, knowledge, and cached context can be selected before generation.

### Adaptive Model Routing
Chooses a model path such as:

- fast model
- reasoning model
- coding model
- tool agent
- vision model

### Traceable Agent Flow
Each response includes an agent trace showing the high-level decision path.

---

## Example Response Shape

```json
{
  "answer": "ARES Optimizer routed this request to `reasoning_model`...",
  "task": {
    "label": "reasoning",
    "confidence": 0.86
  },
  "retrieval": {
    "enabled": true,
    "source": "hybrid",
    "top_k": 3
  },
  "route": {
    "route": "reasoning_model",
    "confidence": 0.86
  },
  "trace_id": "...",
  "agent_trace": [
    {"name": "classifier", "status": "ok"},
    {"name": "retrieval_controller", "status": "ok"},
    {"name": "retrieval", "status": "ok"},
    {"name": "model_router", "status": "ok"},
    {"name": "responder", "status": "ok"}
  ]
}
```

---

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Service health check |
| `GET` | `/healthz` | Alternate health check |
| `POST` | `/route` | Return route decision without full chat focus |
| `POST` | `/chat` | Run the full public optimizer pipeline |

---

## Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then call:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Explain the ARES optimizer architecture"}'
```

CLI demo:

```bash
python run_cli.py "Write Python code for a router"
```

---

## Testing

```bash
pytest -q
```

The repo includes a GitHub Actions workflow that runs tests on push and pull request.

---

## Project Structure

```text
app/
  classifier.py              # public-safe task classification interface
  retrieval_controller.py    # retrieval decision logic
  retriever.py               # public corpus retrieval demo
  reranker.py                # deterministic public reranking demo
  model_router.py            # model path selection
  responder.py               # public-safe response adapter
  orchestrator.py            # pipeline controller
  schemas.py                 # typed request/response models

data/
  knowledge_base.json        # public demo corpus
  memory_store.json          # public demo memory
  web_cache.json             # public demo cache

docs/
  ARCHITECTURE.md
  PUBLIC_SAFE_STRATEGY.md
  ROADMAP.md

tests/
  test_public_pipeline.py
```

---

## Roadmap

- private A.R.E.S backend adapter
- vector database retrieval
- dashboard for traces and route analytics
- reinforcement-learning-inspired policy tuning
- multi-agent execution graph
- streaming response support

---

## Positioning

ARES Optimizer is built as a portfolio-quality AI systems project. It demonstrates practical understanding of routing, retrieval, orchestration, traceability, and public/private code separation — skills that matter for machine learning software engineering and AI infrastructure roles.
