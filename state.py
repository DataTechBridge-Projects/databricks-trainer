from typing import Annotated, TypedDict
import operator


class SectionResult(TypedDict):
    """Output produced by one Worker instance."""
    section_index: int
    section_title: str
    filename: str
    content: str


class OverallState(TypedDict):
    """
    Shared state for the entire graph.

    completed_sections uses operator.add as its reducer so that N parallel
    Worker nodes can each append one SectionResult without race conditions.
    LangGraph merges all parallel writes atomically via this reducer.
    """
    course_topic: str
    course_audience: str
    sections: list[str]                                               # written by supervisor
    completed_sections: Annotated[list[SectionResult], operator.add]  # written by workers
    final_document: str                                               # written by summarizer


class WorkerState(TypedDict):
    """
    Private state passed to each parallel Worker instance via Send.
    Minimal — carries only what the worker needs.
    """
    section: str
    section_index: int
    total_sections: int
    course_topic: str
    course_audience: str
