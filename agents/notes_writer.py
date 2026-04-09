from pathlib import Path
from langchain_core.messages import HumanMessage, SystemMessage
from state import SectionResult
from config import make_llm
from agents.logger import log

_llm = make_llm(timeout=900)

NOTES_SUBDIR = "notes"


def write_notes(
    section: SectionResult,
    output_dir: Path,
    notes_system: str,
    notes_prompt: str,
) -> str:
    """
    Generate a 1-page SA Quick Reference card for a completed section.
    Saves to <output_dir>/notes/notes_<section_filename>.
    Returns the notes filename (not full path).
    """
    user_prompt = notes_prompt.format(
        section_title=section["section_title"],
        # Cap input to avoid flooding the context — SA briefs don't need the full text
        section_content=section["content"][:6000],
    )

    start = log.agent_start("Notes", section['section_title'])
    chunks = []
    for chunk in _llm.stream([
        SystemMessage(content=notes_system),
        HumanMessage(content=user_prompt),
    ]):
        chunks.append(chunk.content)

    notes_dir = output_dir / NOTES_SUBDIR
    notes_dir.mkdir(parents=True, exist_ok=True)

    notes_filename = f"notes_{section['filename']}"
    (notes_dir / notes_filename).write_text("".join(chunks), encoding="utf-8")
    log.agent_end("Notes", section['section_title'], start=start)
    log.info(f"[Notes] Saved: {notes_filename}")

    return notes_filename
