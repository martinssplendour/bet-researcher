# AI / LLM App Starter Structure

Use this for AI assistants, RAG apps, speech apps, agentic workflows, or model-backed products.

```text
project_root/
|-- README.md
|-- .env.example
|-- docs/
|   |-- architecture/
|   |-- ai/
|   |-- api/
|   |-- operations/
|   `-- decisions/
|-- app/
|   |-- api/
|   |-- services/
|   |-- domain/
|   |-- prompts/
|   |-- evaluation/
|   |-- repositories/
|   |-- integrations/
|   |-- core/
|   `-- main.py
|-- tests/
|   |-- unit/
|   |-- integration/
|   |-- e2e/
|   `-- evals/
|-- scripts/
|-- deployment/
`-- .github/workflows/
```

## AI-Specific Docs

- `docs/ai/model-selection.md`
- `docs/ai/prompt-strategy.md`
- `docs/ai/evaluation.md`
- `docs/ai/safety.md`
- `docs/ai/cost-controls.md`

## Minimum Senior Checks

- Prompts are versioned.
- Model choice is documented in an ADR.
- Cost controls are configured.
- Evaluation set exists for important workflows.
- Data retention and privacy are documented.
- Retrieval quality is testable if using RAG.
- Fallback behavior is defined.
- LLM, embedding, retrieval, speech, and evaluation services live in separate files.
- Prompt handling, provider clients, and business workflows are not mixed in one file.
