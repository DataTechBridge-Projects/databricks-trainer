from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from pathlib import Path
from state import OverallState, WorkerState, SectionResult
from agents.supervisor import supervisor
from agents.worker import worker
from agents.summarizer import summarizer
from agents.tracker import get_pending_sections, get_completed_sections
from agents.logger import log


def _load_completed_section_result(s: dict, output_dir: str) -> SectionResult | None:
    """Read an already-written section file back into a SectionResult."""
    filename = s.get("filename")
    if not filename:
        return None
    path = Path(output_dir) / filename
    if not path.exists():
        log.info(f"[Router] Completed section file missing, re-queuing: {filename}")
        return None
    content = path.read_text(encoding="utf-8")
    return SectionResult(
        section_index=s["index"],
        section_title=s["title"],
        filename=filename,
        content=content,
    )


def route_to_workers(state: OverallState) -> list[Send]:
    """
    Conditional edge called after supervisor completes.

    - Skips sections already marked completed in .plan.json, injecting their
      results directly so the summarizer sees a full set of completed_sections.
    - Only queues pending sections as worker Send calls.

    Graph topology:
        START --> supervisor --> [route_to_workers] --> worker (x N, parallel)
                                                             |
                                                        summarizer --> END
    """
    output_dir = state["output_dir"]
    total = len(state["sections"])

    pending = get_pending_sections(output_dir)
    completed = get_completed_sections(output_dir)

    # Build Send calls for sections still pending
    sends: list[Send] = [
        Send(
            node="worker",
            arg=WorkerState(
                section=s["title"],
                section_index=s["index"],
                total_sections=total,
                course_topic=state["course_topic"],
                course_audience=state["course_audience"],
                output_dir=output_dir,
                worker_system=state["worker_system"],
                worker_prompt=state["worker_prompt"],
            ),
        )
        for s in pending
    ]

    if completed:
        log.info(f"[Router] Skipping {len(completed)} already-completed sections.")

    # Pre-load completed sections so the summarizer gets a full document.
    # We inject them via a synthetic Send to a pass-through node, or — simpler —
    # we return them through a dedicated injector node that merges them into state.
    # LangGraph Send can only target graph nodes, so we route via 'inject_completed'.
    if completed:
        pre_loaded = [_load_completed_section_result(s, output_dir) for s in completed]
        valid = [r for r in pre_loaded if r is not None]
        if valid:
            sends.append(Send("inject_completed", {"completed_sections": valid}))

    # Edge case: everything is already done — still need to reach summarizer
    if not sends:
        sends.append(Send("inject_completed", {"completed_sections": []}))

    return sends


def inject_completed(state: dict) -> dict:
    """
    Pass-through node that merges pre-loaded completed sections into state.
    The OverallState reducer (operator.add) handles the list concatenation.
    """
    return {"completed_sections": state.get("completed_sections", [])}


def build_graph():
    builder = StateGraph(OverallState)

    builder.add_node("supervisor", supervisor)
    builder.add_node("worker", worker)
    builder.add_node("inject_completed", inject_completed)
    builder.add_node("summarizer", summarizer)

    builder.add_edge(START, "supervisor")
    builder.add_conditional_edges(
        source="supervisor",
        path=route_to_workers,
        path_map=["worker", "inject_completed"],
    )
    builder.add_edge("worker", "summarizer")
    builder.add_edge("inject_completed", "summarizer")
    builder.add_edge("summarizer", END)

    return builder.compile()
