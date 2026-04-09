import re
import threading
from datetime import datetime
from agents.logger import log
from pathlib import Path
from langchain_core.messages import HumanMessage, SystemMessage
from state import WorkerState, SectionResult
from config import make_llm, NUM_PREDICT, MAX_WORKERS
from agents.tracker import mark_completed

_llm = make_llm(num_predict=NUM_PREDICT, timeout=900)

# Limits how many workers call Ollama simultaneously so the local model isn't overwhelmed.
_semaphore = threading.Semaphore(MAX_WORKERS)


def _safe_filename(index: int, title: str) -> str:
    clean = re.sub(r"^section\s+\d+[:\-\s]+", "", title, flags=re.IGNORECASE)
    safe = re.sub(r"[^\w\s]", "", clean).strip().lower()
    safe = re.sub(r"\s+", "_", safe)[:50]
    return f"section_{index + 1:02d}_{safe}.md"


def worker(state: WorkerState) -> dict:
    """
    Generates full markdown content for one course section.
    Reads worker_system, worker_prompt, and output_dir from state.
    Runs in parallel — one instance per section.
    Returns: {'completed_sections': [SectionResult]}
    """
    user_prompt = state["worker_prompt"].format(
        section=state["section"],
        section_index=state["section_index"] + 1,
        total_sections=state["total_sections"],
        course_topic=state["course_topic"],
        course_audience=state["course_audience"],
    )

    idx = state['section_index'] + 1
    label = f"section {idx} — {state['section']}"
    log.info(f"[Worker] Queued {label}")
    filename = _safe_filename(state["section_index"], state["section"])
    output_dir = Path(state["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / filename

    with _semaphore:
        start = log.agent_start("Worker", label)
        chunks = []
        with out_path.open("w", encoding="utf-8") as f:
            for chunk in _llm.stream([
                SystemMessage(content=state["worker_system"]),
                HumanMessage(content=user_prompt),
            ]):
                token = chunk.content
                f.write(token)
                f.flush()
                chunks.append(token)
        content = "".join(chunks)
        log.agent_end("Worker", label, start=start)

    log.info(f"[Worker] Saved: {label} ({len(content):,} chars) → {output_dir / filename}")
    mark_completed(state["output_dir"], state["section_index"], filename)

    result: SectionResult = {
        "section_index": state["section_index"],
        "section_title": state["section"],
        "filename": filename,
        "content": content,
    }

    return {"completed_sections": [result]}
