import re
from datetime import datetime
from langchain_core.messages import HumanMessage, SystemMessage
from state import OverallState
from config import make_llm
from agents.logger import log

_llm = make_llm()

def summarizer(state: OverallState) -> dict:
    """
    Sorts worker results by section_index to restore outline order,
    generates a course introduction and table of contents, then
    assembles the complete course document.
    Returns: {'final_document': str}
    """
    ordered = sorted(state["completed_sections"], key=lambda x: x["section_index"])
    start = log.agent_start("Summarizer", f"{len(ordered)} sections")

    # Table of contents
    toc_lines = ["## Table of Contents\n"]
    for i, s in enumerate(ordered):
        anchor = re.sub(r"[^\w\s-]", "", s["section_title"]).strip().lower()
        anchor = re.sub(r"\s+", "-", anchor)
        toc_lines.append(f"{i + 1}. [{s['section_title']}](#{anchor})")
    toc = "\n".join(toc_lines)

    # Course introduction
    sections_list = [s["section_title"] for s in ordered]
    intro_prompt = state["summarizer_intro"].format(
        course_topic=state["course_topic"],
        course_audience=state["course_audience"],
        sections=sections_list,
    )
    intro_response = _llm.invoke([
        SystemMessage(content=state["summarizer_system"]),
        HumanMessage(content=intro_prompt),
    ])

    introduction = intro_response.content

    # Assemble final document
    header = (
        f"# {state['course_topic']}\n"
        f"### A Comprehensive Udemy Course Guide\n\n"
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d')}  \n"
        f"**Target Audience:** {state['course_audience']}  \n"
        f"**Total Sections:** {len(ordered)}\n\n"
        f"---\n\n"
    )

    sections_content = "\n\n---\n\n".join(s["content"] for s in ordered)

    final_document = (
        header
        + introduction
        + "\n\n---\n\n"
        + toc
        + "\n\n---\n\n"
        + sections_content
    )

    log.agent_end("Summarizer", f"{len(ordered)} sections", start=start)
    log.info(f"[Summarizer] Assembled {len(ordered)} sections — {len(final_document):,} total chars")

    return {"final_document": final_document}
