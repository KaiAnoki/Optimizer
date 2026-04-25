# Architecture

ARES Optimizer is structured as a decision layer that sits before an A.R.E.S backend or local LLM.

## Pipeline

1. **Request Ingestion**
   - Accepts a user message and metadata.

2. **Task Classification**
   - Determines the high-level type of work.
   - Public categories include chat, retrieval, reasoning, coding, memory, tool use, and vision.

3. **Retrieval Planning**
   - Decides whether context is needed.
   - Selects a public retrieval source: none, docs, memory, or hybrid.

4. **Context Retrieval**
   - Searches public-safe JSON corpus files.
   - Production systems can replace this layer with vector databases or private memory services.

5. **Reranking**
   - Deduplicates and orders retrieved context.

6. **Model Routing**
   - Selects the most appropriate execution path.

7. **Response Adapter**
   - Public version generates a demonstration response.
   - Private version can forward payloads to local A.R.E.S model endpoints.

## Design Principle

The external interfaces are stable, while the internal optimizer can evolve. That means the public project remains understandable without exposing the highest-value private implementation logic.
