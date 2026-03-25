# Architecture

## File structure

```
.
├── main.py             # entry point — runs graph, saves outputs
├── graph.py            # StateGraph definition + Send fan-out routing
├── state.py            # OverallState, WorkerState, SectionResult TypedDicts
├── config.py           # model, paths, course metadata
├── agents/
│   ├── supervisor.py   # outline generation
│   ├── worker.py       # section content generation (parallel)
│   └── summarizer.py   # final document assembly
└── docs/
    ├── agent/          # this documentation
    └── course/         # generated course content (written by pipeline)
```

## State schema

```python
class OverallState(TypedDict):
    course_topic: str
    course_audience: str
    sections: list[str]                                               # supervisor output
    completed_sections: Annotated[list[SectionResult], operator.add] # workers output
    final_document: str                                               # summarizer output

class WorkerState(TypedDict):
    section: str          # this worker's section title
    section_index: int    # position in the outline
    total_sections: int
    course_topic: str
    course_audience: str
```

The `Annotated[list, operator.add]` reducer on `completed_sections` is what allows N parallel workers to each append one result without overwriting each other. LangGraph applies the reducer atomically for each completed worker.

## Parallel execution detail

```python
def route_to_workers(state: OverallState) -> list[Send]:
    return [
        Send(node="worker", arg=WorkerState(
            section=title,
            section_index=i,
            ...
        ))
        for i, title in enumerate(state["sections"])
    ]
```

Each `Send` creates an independent worker invocation with its own isolated `WorkerState`. Workers share no memory and make independent LLM calls to Ollama.

## Incremental saves

Workers write their section file to `docs/course/` **immediately on completion** — before the graph finishes. If the run crashes mid-way, already-completed sections are preserved on disk.
