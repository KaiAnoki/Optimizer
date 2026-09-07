# ARES Optimizer

ARES Optimizer is a deterministic Python service that classifies requests, decides whether retrieval is useful, ranks local context, and selects an execution route. Every response includes a trace of the decisions made by the pipeline.

This repository is a working reference implementation. It does not call a hosted language model or claim that rule-based routing is machine learning.

## Request flow

```text
request -> classifier -> retrieval plan -> retriever -> reranker -> model router -> response
```

## What it demonstrates

- A typed FastAPI contract built with Pydantic
- Token-aware task classification
- Deterministic model and tool routing
- Local JSON retrieval with deduplication and scoring
- Trace IDs and step-level execution records
- Unit and API tests running in GitHub Actions
- Docker and command-line entry points

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API documentation.

## Example

```bash
curl -X POST http://127.0.0.1:8000/route \
  -H "Content-Type: application/json" \
  -d '{"message":"Debug a Python API"}'
```

The response contains the predicted task, retrieval plan, selected route, trace ID, and agent trace.

## Test it

```bash
pytest -q
```

The suite checks the routing pipeline, input validation, token matching, retrieval behavior, JSON serialization, and FastAPI endpoints.

## Author

Khyri Williams, preferred name Kai

## License

MIT
