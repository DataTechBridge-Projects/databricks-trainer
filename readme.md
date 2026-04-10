# Tech Ramp Up Trainer

A three-agent LangGraph pipeline that generates 100-level technical training courses for **Solution Architects**. Courses are designed for breadth over depth — enough to hold a credible customer conversation, not pass a deep engineering exam.

Generated courses are published automatically to **GitHub Pages** via MkDocs.

---

## Onboarding a New Course

### 1. Add the course to `courses.json`

```json
"gcp": {
  "output_dir": "docs/gcp",
  "topic": "GCP Professional Data Engineer",
  "audience": "data engineers who want to pass the GCP Professional Data Engineer exam"
}
```

### 2. Set it as the active course in `config.py`

```python
ACTIVE_COURSE = "gcp"
```

### 3. Generate content

```bash
pip install -r requirements.txt
ollama pull nemotron-cascade-2

python generate.py
```

Runs the LLM pipeline and saves markdown to `docs/gcp/`. No git or mkdocs changes yet.

### 4. Publish to GitHub Pages

```bash
python publish.py --push
```

Patches `mkdocs.yml`, updates the home page and manifest, then commits and pushes. GitHub Actions deploys automatically.

> **Shortcut:** `python main.py` runs both steps in sequence.

---

## Scripts Reference

| Script | Purpose | When to use |
|---|---|---|
| `generate.py` | Runs the LLM pipeline, saves markdown to `docs/<course>/` | Every time you want to create or regenerate course content |
| `publish.py` | Patches `mkdocs.yml`, updates home page + manifest, optionally pushes | After generating, or any time you want to re-publish without regenerating |
| `main.py` | Runs `generate.py` then `publish.py` in sequence | When you want to do both in one command |

### publish.py options

```bash
python publish.py                             # patch nav/index for all courses, no push
python publish.py --course databricks         # one course only
python publish.py --push                      # commit and push → triggers GitHub Actions
python publish.py --push --message "add gcp"  # custom commit message
```

---

## Switching Between Existing Courses

Edit one line in `config.py`:

```python
ACTIVE_COURSE = "aws"  # any key defined in courses.json
```

Current courses: `databricks` | `aws` | `aws-sa` | `azure`

---

## How It Works

```
Supervisor → N parallel Workers → Summarizer → Notes Writer → MkDocs → GitHub Pages
```

| Agent | Role |
|---|---|
| **Supervisor** | Calls the LLM once to produce an ordered list of section titles |
| **Workers** | One per section, run in parallel — each generates full markdown content |
| **Summarizer** | Sorts sections, generates intro + table of contents, assembles final doc |
| **Notes Writer** | Generates a 1-page SA Quick Reference card per section (post-graph) |

---

## SA Competency Framework

This framework defines what a Solution Architect should be able to **do and say** after completing a course.

| Level | Name | What You Can Do |
|---|---|---|
| 1 | **Awareness** | Explain what the technology is and the core problem it solves |
| 2 | **Positioning** | Compare it to competitors; articulate the vendor's differentiators |
| 3 | **Discovery** | Lead a customer conversation; ask qualifying questions |
| 4 | **Solution Framing** | Whiteboard a reference architecture; describe the adoption journey |
| 5 | **Objection Handling** | Address top objections; navigate pricing and TCO conversations |

> Generated courses target **Levels 1–3**. Levels 4–5 require hands-on practice and deal experience.

---

## Key Config (`config.py`)

| Setting | Description |
|---|---|
| `ACTIVE_COURSE` | Which course to generate (must be a key in `courses.json`) |
| `MAX_WORKERS` | Max parallel section writers (set to `2` for large local models) |
| `NUM_PREDICT` | Max tokens per worker response (`-1` = unlimited) |

---

## Project Structure

```
courses.json              # Course registry — add new courses here
config.py                 # Active course + runtime settings
generate.py               # Step 1: LLM pipeline → docs/<course>/
publish.py                # Step 2: patch mkdocs.yml, update index, push to Pages
main.py                   # Shortcut: runs generate.py then publish.py
graph.py                  # LangGraph StateGraph definition
agents/
  supervisor.py           # Outline generation
  worker.py               # Section writing (parallel)
  summarizer.py           # Final assembly
  notes_writer.py         # SA Quick Reference cards
  tracker.py              # Resume interrupted runs via .plan.json
  logger.py               # Timestamped console + file logging
prompts/common.json       # Shared LLM prompts for all courses
docs/                     # Generated course content (committed, served by MkDocs)
mkdocs.yml                # Auto-patched by pipeline on each run
.github/workflows/        # GitHub Actions — deploys to GitHub Pages on push
```

---

## Requirements

- Python 3.11+
- [Ollama](https://ollama.com) running locally with `nemotron-cascade-2` pulled
- `pip install -r requirements.txt`
