# Databricks Course Generator — Multi-Agent LangGraph System

A three-agent LangGraph pipeline that autonomously generates a complete Udemy course for the **AWS Databricks Data Engineer Certification**, targeting engineers familiar with Apache Spark and AWS Glue.

---

## Architecture

```
START
  │
  ▼
┌─────────────┐
│  Supervisor │  Creates a structured course outline (12-16 sections)
└──────┬──────┘
       │  conditional edge → Send API fans out to N parallel workers
       │
   ┌───┼──────────────────────┐
   ▼   ▼                      ▼
[Worker] [Worker]  ...  [Worker]   ← one instance per section, runs in parallel
   │       │                  │
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
| **Supervisor** | Calls Claude to produce a JSON array of section titles | `supervisor` |
| **Worker** | Generates exhaustive markdown content for one section; runs as N parallel instances via `Send` | `worker` |
| **Summarizer** | Sorts worker results by `section_index`, writes course intro + ToC, assembles `complete_course.md` | `summarizer` |

### Why LangGraph?

- **Parallel execution** via the `Send` API — the Supervisor fans out to one Worker per section, all running concurrently.
- **Safe state merging** — `completed_sections` uses `Annotated[list, operator.add]` so parallel writes never collide.
- **Deterministic ordering** — each `SectionResult` carries `section_index`; the Summarizer sorts before assembling.
- **Reusable** — swap `COURSE_TOPIC` and `COURSE_AUDIENCE` in `config.py` to generate a course on any subject.

---

## Project Structure

```
.
├── main.py             # entry point
├── graph.py            # StateGraph definition + route_to_workers (Send fan-out)
├── state.py            # OverallState, WorkerState, SectionResult TypedDicts
├── config.py           # model, paths, course metadata
├── agents/
│   ├── supervisor.py   # outline generation
│   ├── worker.py       # section content generation (parallel)
│   └── summarizer.py   # final document assembly
├── output/             # auto-created at runtime
│   ├── section_01_*.md
│   ├── section_02_*.md
│   └── complete_course.md
├── requirements.txt
├── .env.example
└── README.md
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set your Anthropic API key

```bash
cp .env.example .env
# edit .env and add your key:
# ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Run

```bash
python main.py
```

The pipeline will:
1. Print the generated outline (Supervisor)
2. Show each worker completing its section in parallel
3. Save individual section files to `output/`
4. Save `output/complete_course.md` — the full combined course

---

## Output Format

Each section file includes:

- **Overview** — deep conceptual explanation (book-level depth)
- **Core Concepts** — detailed sub-sections
- **Architecture / How It Works** — ASCII or Mermaid diagrams
- **Hands-On: Key Operations** — PySpark / Python / SQL code examples
- **AWS-Specific Considerations** — S3, IAM, Glue, Lake Formation integration notes
- **Exam Focus Areas** — what the Databricks certification tests
- **Quick Recap** — bullet-point summary for fast review
- **Code References** — official docs and GitHub links
- **Blog & Further Reading** — 3-5 recommended resources

---

## Configuration

Edit `config.py` to change:

| Setting | Default | Description |
|---|---|---|
| `MODEL_NAME` | `claude-opus-4-6` | Anthropic model to use |
| `COURSE_TOPIC` | AWS Databricks Data Engineer Certification | Course subject |
| `COURSE_AUDIENCE` | Spark + AWS Glue engineers | Target audience description |
| `OUTPUT_DIR` | `output/` | Where to save generated files |
| `MAX_TOKENS_WORKER` | `8192` | Max tokens per section (controls depth) |

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
- `ANTHROPIC_API_KEY` environment variable
- See `requirements.txt` for package versions
