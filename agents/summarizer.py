import re
from datetime import datetime
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from state import OverallState
from config import MODEL_NAME, OLLAMA_BASE_URL

_llm = ChatOllama(
    model=MODEL_NAME,
    base_url=OLLAMA_BASE_URL,
)

_SYSTEM = "You are a senior Databricks instructor writing a compelling course introduction."


def summarizer(state: OverallState) -> dict:
    """
    Sorts worker results by section_index to restore outline order,
    generates a course introduction and table of contents, then
    assembles the complete course document.
    Returns: {'final_document': str}
    """
    ordered = sorted(state["completed_sections"], key=lambda x: x["section_index"])

    # Table of contents
    toc_lines = ["## Table of Contents\n"]
    for i, s in enumerate(ordered):
        anchor = re.sub(r"[^\w\s-]", "", s["section_title"]).strip().lower()
        anchor = re.sub(r"\s+", "-", anchor)
        toc_lines.append(f"{i + 1}. [{s['section_title']}](#{anchor})")
    toc = "\n".join(toc_lines)

    # Course introduction
    intro_response = _llm.invoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=f"""Write a compelling course introduction (400-600 words) for:

Course: {state['course_topic']}
Audience: {state['course_audience']}
Sections: {[s['section_title'] for s in ordered]}

Include: what the student will learn, prerequisites assumed, how to use this material,
and a brief overview of the Databricks Certified Data Engineer Associate exam.
Use markdown formatting."""),
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

    print(f"[Summarizer] Assembled {len(ordered)} sections — {len(final_document):,} total chars")

    return {"final_document": final_document}
