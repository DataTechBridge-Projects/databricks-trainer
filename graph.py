from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from state import OverallState, WorkerState
from agents.supervisor import supervisor
from agents.worker import worker
from agents.summarizer import summarizer


def route_to_workers(state: OverallState) -> list[Send]:
    """
    Conditional edge called after supervisor completes.
    Returns one Send per section — LangGraph executes all in parallel.

    Graph topology:
        START --> supervisor --> [route_to_workers] --> worker (x N, parallel)
                                                             |
                                                        summarizer --> END
    """
    return [
        Send(
            node="worker",
            arg=WorkerState(
                section=section_title,
                section_index=i,
                total_sections=len(state["sections"]),
                course_topic=state["course_topic"],
                course_audience=state["course_audience"],
            ),
        )
        for i, section_title in enumerate(state["sections"])
    ]


def build_graph():
    builder = StateGraph(OverallState)

    builder.add_node("supervisor", supervisor)
    builder.add_node("worker", worker)
    builder.add_node("summarizer", summarizer)

    builder.add_edge(START, "supervisor")
    builder.add_conditional_edges(
        source="supervisor",
        path=route_to_workers,
        path_map=["worker"],   # declares 'worker' as reachable via Send
    )
    builder.add_edge("worker", "summarizer")
    builder.add_edge("summarizer", END)

    return builder.compile()
