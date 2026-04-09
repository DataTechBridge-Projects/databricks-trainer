# Agents

Four agents make up the pipeline. They do not call each other — LangGraph wires them together via `graph.py`. See the root README for the full architecture diagram and config reference.

---

## `supervisor.py` — Planner

**Does:** Calls the LLM once with the course topic and audience, returns an ordered JSON list of section titles.

**Does NOT:** Write any content. Output only — no files touched.

**State output:** `sections: list[str]`

---

## `worker.py` — Section Writer

**Does:** Receives one section title via LangGraph's `Send` API, generates full markdown content for that section, saves the file to `docs/<course>/` immediately (does not wait for the graph to finish), and appends its result to shared state.

**Does NOT:** Know about other sections. Each instance is fully independent.

**Concurrency:** All N workers are dispatched in parallel by LangGraph, but a `threading.Semaphore(MAX_WORKERS)` limits how many call Ollama simultaneously. For large local models (26B+) set `MAX_WORKERS = 2` in `config.py`.

**State output:** One `SectionResult` appended to `completed_sections` (thread-safe via `operator.add` reducer in `state.py`)

**Files written:** `docs/<course>/section_NN_<title>.md`

---

## `summarizer.py` — Assembler

**Does:** Waits for all workers (LangGraph enforces this), sorts results back into outline order (workers may finish out of order), generates a course intro + table of contents via one LLM call, assembles the full document.

**Does NOT:** Re-read files from disk — uses `content` already held in state.

**State output:** `final_document: str`

---

## `notes_writer.py` — SA Quick Reference Generator

**Does:** Generates a 1-page SA Quick Reference card per section. Called by `main.py` in a **sequential loop after the graph completes** — it is not a LangGraph node.

**Does NOT:** Run in parallel (intentional — avoids Ollama overload in the post-graph phase).

**Input:** First 6,000 characters of a section's content.

**Files written:** `docs/<course>/notes/notes_section_NN_<title>.md`
