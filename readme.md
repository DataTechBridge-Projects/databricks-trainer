# Data Engineer Hub — Multi-Agent Course Generator

A three-agent LangGraph pipeline that autonomously generates complete technical courses from a topic and audience description. Databricks is the first course — any engineering topic can be added as a new tab.

---

## Architecture

```
START
  │
  ▼
┌─────────────┐
│  Supervisor │  Creates a structured course outline (15 sections)
└──────┬──────┘
       │  conditional edge → Send API fans out to N parallel workers
       │
   ┌───┼──────────────────────┐
   ▼   ▼                      ▼
[Worker] [Worker]  ...  [Worker]   ← one instance per section, runs in parallel
   │       │                  │     each saves its file to disk immediately
   └───────┴──────────────────┘
       │  operator.add reducer merges all results into shared state
       ▼
┌─────────────┐
│  Summarizer │  Sorts sections, generates intro + ToC, assembles final doc
└──────┬──────┘
       │
      END
```

### The Three Agents

| Agent | Role | LangGraph Node |
|---|---|---|
| **Supervisor** | Produces a structured JSON outline of section titles | `supervisor` |
| **Worker** | Generates exhaustive markdown content for one section; N parallel instances via `Send` | `worker` |
| **Summarizer** | Sorts by `section_index`, writes course intro + ToC, assembles `complete_course.md` | `summarizer` |

### Why LangGraph?

- **Parallel execution** via the `Send` API — Supervisor fans out to one Worker per section, all running concurrently
- **Safe state merging** — `completed_sections` uses `Annotated[list, operator.add]` so parallel writes never collide
- **Deterministic ordering** — each `SectionResult` carries `section_index`; Summarizer sorts before assembling
- **Reusable** — swap `COURSE_TOPIC` and `COURSE_AUDIENCE` in `config.py` for any subject

---

## Project Structure

```
.
├── main.py                   # entry point
├── graph.py                  # StateGraph + Send fan-out routing
├── state.py                  # OverallState, WorkerState, SectionResult
├── config.py                 # model, paths, course topic/audience
├── agents/
│   ├── supervisor.py         # outline generation
│   ├── worker.py             # section content generation (parallel, incremental save)
│   └── summarizer.py         # final document assembly
├── docs/
│   ├── index.md              # site homepage
│   ├── agent/                # Agent tab — pipeline documentation
│   └── databricks/           # Databricks tab — generated course content
├── mkdocs.yml                # MkDocs Material site config
├── .github/workflows/
│   └── deploy-docs.yml       # auto-deploy to GitHub Pages on push
└── requirements.txt
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Pull the model (local Ollama — no API key needed)

```bash
ollama pull nemotron-cascade-2
```

### 3. Run

```bash
python main.py
```

The pipeline will:
1. Print the generated outline (Supervisor)
2. Show each worker saving its section in parallel
3. Save individual section files to `docs/databricks/`
4. Save `docs/databricks/complete_course.md` — the full combined course

---

## Output Format

Each section includes:

- **Overview** — deep conceptual explanation (book-level depth)
- **Core Concepts** — detailed sub-sections
- **Architecture / How It Works** — ASCII or Mermaid diagrams
- **Hands-On: Key Operations** — PySpark / Python / SQL code examples
- **AWS-Specific Considerations** — S3, IAM, Glue, Lake Formation integration notes
- **Exam Focus Areas** — what the certification tests
- **Quick Recap** — bullet-point summary for fast review
- **Code References** — official docs and GitHub links
- **Blog & Further Reading** — 3-5 recommended resources

---

## Configuration

Edit `config.py` to change:

| Setting | Default | Description |
|---|---|---|
| `MODEL_NAME` | `nemotron-cascade-2` | Local Ollama model |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `NUM_PREDICT` | `4096` | Max tokens per section — lower = faster |
| `COURSE_TOPIC` | AWS Databricks Data Engineer Certification | Course subject |
| `COURSE_AUDIENCE` | Spark + AWS Glue engineers | Target audience |
| `OUTPUT_DIR` | `docs/databricks` | Where to save generated files |

---

## Adding a new course

1. Update `config.py` with the new topic and audience
2. Change `OUTPUT_DIR` to `docs/<course-name>/`
3. Run `python main.py`
4. Commit and push — a new tab appears on the site automatically

---

## GitHub Pages

Site: `https://datatechbridge-projects.github.io/databricks-trainer/`

Tabs:
- **Agent** — pipeline documentation
- **Databricks** — AWS Databricks Data Engineer Certification course
- *(future courses appear as new tabs)*

---

## State Schema

```python
class OverallState(TypedDict):
    course_topic: str
    course_audience: str
    sections: list[str]                                               # supervisor output
    completed_sections: Annotated[list[SectionResult], operator.add] # workers output (reducer)
    final_document: str                                               # summarizer output

class WorkerState(TypedDict):
    section: str
    section_index: int
    total_sections: int
    course_topic: str
    course_audience: str
```

---

## Requirements

- Python 3.11+
- Ollama running locally with the model pulled
- See `requirements.txt` for package versions
