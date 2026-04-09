import json
import re
from langchain_core.messages import HumanMessage, SystemMessage
from state import OverallState
from config import make_llm
from agents.logger import log
from agents.tracker import load_plan, save_plan, get_pending_sections

_llm = make_llm()

def supervisor(state: OverallState) -> dict:
    """
    Creates (or resumes) the course outline.

    - If a .plan.json exists in output_dir, loads the previous plan and
      skips the LLM call — the pipeline will only run pending sections.
    - Otherwise, calls the LLM to create a fresh outline and persists it.

    Returns: {'sections': list[str]}
    """
    output_dir = state["output_dir"]
    existing_plan = load_plan(output_dir)

    if existing_plan:
        sections = [s["title"] for s in sorted(existing_plan["sections"], key=lambda s: s["index"])]
        pending = get_pending_sections(output_dir)
        log.info(
            f"[Supervisor] Resuming plan for '{state['course_topic']}': "
            f"{len(sections)} total sections, {len(pending)} pending."
        )
        for s in existing_plan["sections"]:
            status = "✓" if s["status"] == "completed" else "○"
            log.info(f"  {status} {s['index'] + 1:02d}. {s['title']}")
        return {"sections": sections}

    # No plan exists — ask the LLM to build one
    user_prompt = state["supervisor_prompt"].format(
        course_topic=state["course_topic"],
        course_audience=state["course_audience"],
    )

    start = log.agent_start("Supervisor", state["course_topic"])

    response = _llm.invoke([
        SystemMessage(content=state["supervisor_system"]),
        HumanMessage(content=user_prompt),
    ])

    raw = response.content.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    sections: list[str] = json.loads(raw)

    log.agent_end("Supervisor", state["course_topic"], start=start)
    log.info(f"[Supervisor] Created outline with {len(sections)} sections:")
    for i, s in enumerate(sections):
        log.info(f"  {i + 1:02d}. {s}")

    save_plan(output_dir, state["course_topic"], sections)
    log.info(f"[Supervisor] Plan saved to {output_dir}/.plan.json")

    return {"sections": sections}
