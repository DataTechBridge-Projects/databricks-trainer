# Agent — Overview

The Tech Ramp Up agent is a three-agent LangGraph pipeline that autonomously generates a complete course from a single topic and audience description. No human input required after the initial run.

---

## How it works

```
START
  │
  ▼
┌─────────────┐
│  Supervisor │  Plans the course outline (list of section titles)
└──────┬──────┘
       │  Send API fans out — one Worker per section
       │
   ┌───┼──────────────────────┐
   ▼   ▼                      ▼
[Worker] [Worker]  ...  [Worker]   ← parallel, independent
   │       │                  │     each saves its file immediately
   └───────┴──────────────────┘
       │  operator.add merges results
       ▼
┌─────────────┐
│  Summarizer │  Assembles final course document + table of contents
└─────────────┘
```

Each agent is **independent** — workers have no shared context with each other.
The Supervisor only plans. Workers only write. The Summarizer only assembles.

---

## The three agents

### Supervisor
- Receives: course topic + target audience
- Produces: ordered list of 15 section titles (JSON array)
- Has no knowledge of section content

### Worker
- Receives: one section title, its position, course topic, audience
- Produces: full markdown content for that section
- Runs as N parallel instances — one per section
- **Saves to disk immediately** on completion (incremental — no data lost if run crashes)

### Summarizer
- Receives: all completed sections (sorted by original order)
- Produces: course introduction, table of contents, and combined document

---

## Why LangGraph?

| Feature | How it's used |
|---|---|
| `Send` API | Supervisor fans out to N parallel Worker instances |
| `operator.add` reducer | Safely merges parallel worker results into shared state |
| `section_index` | Workers complete out of order — index restores correct ordering |
| Conditional edges | `route_to_workers` converts outline into parallel `Send` objects |

---

## Reusable for any topic

Change two lines in `config.py`:

```python
COURSE_TOPIC = "Your Topic Here"
COURSE_AUDIENCE = "Description of your target audience"
```

Run `python main.py` — a full course is generated automatically.
