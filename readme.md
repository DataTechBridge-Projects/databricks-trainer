# Tech Ramp Up — Multi-Agent Course Generator

A three-agent LangGraph pipeline that autonomously generates complete technical courses from a topic and audience description. Databricks is the first course — any engineering topic can be added as a new tab.

---

## Pre-Sales SA Competency Framework

This framework defines what a pre-sales Solution Architect should be able to **do and say** after ramping up on any technology. It is technology-agnostic — use it to measure readiness before a customer engagement or as a rubric when reviewing generated course content.

### Level 1 — Awareness *(Can explain the basics)*
- Describe what the technology is and the core problem it solves in 2–3 sentences
- Name the primary use cases and which industries or personas care about it
- Explain the key components or building blocks at a conceptual level
- Avoid common misconceptions customers have when they first hear about it

### Level 2 — Positioning *(Can place it in the market)*
- Compare it to 2–3 direct competitors — where it wins, where it doesn't
- Articulate the vendor's differentiators without reading from a slide
- Map it to the customer's existing stack (what it replaces, what it complements)
- Explain the licensing / consumption model at a high level (how customers pay)

### Level 3 — Discovery *(Can lead a customer conversation)*
- Ask qualifying questions that uncover whether the technology is a fit
- Identify common pain points that signal a good opportunity
- Recognize red flags or anti-patterns where the tech is a poor fit
- Translate customer requirements into technology capabilities

### Level 4 — Solution Framing *(Can shape a solution)*
- Whiteboard a reference architecture for a common use case
- Explain integration points with adjacent technologies in the customer's environment
- Describe the typical adoption journey (crawl / walk / run)
- Speak to security, compliance, and governance considerations at a high level

### Level 5 — Objection Handling *(Can hold the room)*
- Address the top 5 objections confidently with data or customer proof points
- Navigate pricing and TCO conversations without getting stuck
- Know when to escalate to a specialist and how to set that up cleanly
- Leave the customer with a clear next step tied to their business outcome

---

> **How this maps to the course generator:** Each generated course targets **Levels 1–3**. Levels 4–5 require product-specific enablement, customer-facing practice, and deal experience.

---

## Technology Topic Checklist

For any technology, a ramped SA should be able to speak to each of these areas. Use this as a content checklist when reviewing generated courses or preparing for a customer call.

| # | Topic Area | What to Know |
|---|---|---|
| 1 | **What & Why** | What problem does it solve? Why does it exist? What's the origin story? |
| 2 | **Core Architecture** | Key components, how data/requests flow, what runs where |
| 3 | **Primary Use Cases** | Top 3–5 scenarios customers actually use it for |
| 4 | **Key Personas** | Who buys it, who uses it, who operates it |
| 5 | **Deployment Models** | Cloud, on-prem, hybrid, SaaS — what's available and what's common |
| 6 | **Integration Landscape** | What it connects to natively; what requires custom work |
| 7 | **Security & Compliance** | Auth/authz model, data encryption, common certifications (SOC 2, HIPAA, etc.) |
| 8 | **Pricing & Licensing** | Unit of consumption, pricing tiers, what drives cost up |
| 9 | **Competitive Landscape** | Top 2–3 alternatives; where this wins and where it doesn't |
| 10 | **Adoption Journey** | How customers typically start, expand, and scale |
| 11 | **Common Objections** | Price, complexity, lock-in, incumbent — and how to respond |
| 12 | **Proof Points** | 2–3 customer stories or industry references worth knowing |
| 13 | **Limitations & Anti-Patterns** | When *not* to recommend it; known gaps or constraints |
| 14 | **Roadmap Awareness** | What's coming next; any known GA dates or public announcements |
| 15 | **Demo / Whiteboard Narrative** | A 5-minute verbal walkthrough of the technology without slides |

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
├── courses.py                # all course definitions (topic, audience, output dir)
├── agents/
│   ├── supervisor.py         # outline generation
│   ├── worker.py             # section content generation (parallel, incremental save)
│   ├── summarizer.py         # final document assembly
│   ├── notes_writer.py       # SA Quick Reference card generation (post-graph)
│   ├── tracker.py            # .plan.json persistence — resume interrupted runs
│   └── logger.py             # centralised timestamped logger (console + file)
├── prompts/
│   └── common.json           # shared LLM prompt templates for all courses
├── docs/
│   ├── aws/                  # AWS Data Engineer course content
│   ├── databricks/           # Databricks course content
│   └── azure/                # Azure course content
├── mkdocs.yml                # MkDocs Material site config
├── .github/workflows/
│   └── deploy-docs.yml       # auto-deploy to GitHub Pages on push
└── requirements.txt
```

### File Usage Reference

| File | Status | Used By | Purpose |
|---|---|---|---|
| `main.py` | active | — | Entry point; orchestrates graph run, saves output, generates notes |
| `graph.py` | active | `main.py` | Builds the LangGraph `StateGraph` with Supervisor → Workers → Summarizer |
| `state.py` | active | `graph.py`, agents | `OverallState`, `WorkerState`, `SectionResult` type definitions |
| `config.py` | active | all modules | LLM config (`MODEL_NAME`, `make_llm()`), `ACTIVE_COURSE`, `MAX_WORKERS` |
| `courses.py` | active | `main.py` | Course registry — topic, audience, output dir; loads prompts from `common.json` |
| `agents/supervisor.py` | active | `graph.py` | First graph node — generates section outline as JSON |
| `agents/worker.py` | active | `graph.py` | Parallel graph nodes — generates markdown content for one section each |
| `agents/summarizer.py` | active | `graph.py` | Final graph node — sorts sections, assembles complete document |
| `agents/notes_writer.py` | active | `main.py` | Post-graph — generates 1-page SA Quick Reference cards per section |
| `agents/tracker.py` | active | `main.py` | Persists `.plan.json` so interrupted runs resume from where they left off |
| `agents/logger.py` | active | `main.py`, agents | Centralised logger — timestamped output to console and `logs/` directory |
| `prompts/common.json` | active | `courses.py` | Shared prompt templates (`WORKER_SYSTEM`, `WORKER_PROMPT`, `NOTES_PROMPT`, etc.) |
| `prompts/aws_data_engineer.py` | **dead** | nobody | Legacy — superseded by `common.json`; safe to delete |
| `prompts/databricks.py` | **dead** | nobody | Legacy — superseded by `common.json`; safe to delete |
| `prompts/azure_data_engineer.py` | **dead** | nobody | Legacy — superseded by `common.json`; safe to delete |

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
python main.py --course aws --course aws --num-workers 4 --poll-interval 10
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

Site: `https://datatechbridge-projects.github.io/sa-ramp-up/`

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
