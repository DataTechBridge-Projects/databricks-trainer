import re
import importlib
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from state import WorkerState, SectionResult
from config import MODEL_NAME, OLLAMA_BASE_URL, OUTPUT_DIR, NUM_PREDICT, PROMPT_MODULE

_llm = ChatOllama(
    model=MODEL_NAME,
    base_url=OLLAMA_BASE_URL,
    num_predict=NUM_PREDICT,
)


def _safe_filename(index: int, title: str) -> str:
    clean = re.sub(r"^section\s+\d+[:\-\s]+", "", title, flags=re.IGNORECASE)
    safe = re.sub(r"[^\w\s]", "", clean).strip().lower()
    safe = re.sub(r"\s+", "_", safe)[:50]
    return f"section_{index + 1:02d}_{safe}.md"


def worker(state: WorkerState) -> dict:
    """
    Generates full markdown content for one course section.
    Loads WORKER_PROMPT and WORKER_SYSTEM from the active PROMPT_MODULE.
    Runs in parallel — one instance per section.
    Returns: {'completed_sections': [SectionResult]}
    """
    prompts = importlib.import_module(PROMPT_MODULE)
    user_prompt = prompts.WORKER_PROMPT.format(
        section=state["section"],
        section_index=state["section_index"] + 1,
        total_sections=state["total_sections"],
        course_topic=state["course_topic"],
        course_audience=state["course_audience"],
    )

    response = _llm.invoke([
        SystemMessage(content=prompts.WORKER_SYSTEM),
        HumanMessage(content=user_prompt),
    ])

    content = response.content
    filename = _safe_filename(state["section_index"], state["section"])

    # Write to disk immediately — don't wait for the full graph to finish
    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / filename).write_text(content, encoding="utf-8")

    print(f"[Worker] Saved: section {state['section_index'] + 1} — {state['section']} ({len(content):,} chars) → output/{filename}")

    result: SectionResult = {
        "section_index": state["section_index"],
        "section_title": state["section"],
        "filename": filename,
        "content": content,
    }

    return {"completed_sections": [result]}
