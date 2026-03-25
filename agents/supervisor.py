import json
import re
import importlib
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from state import OverallState
from config import MODEL_NAME, OLLAMA_BASE_URL, PROMPT_MODULE

_llm = ChatOllama(
    model=MODEL_NAME,
    base_url=OLLAMA_BASE_URL,
)

_SYSTEM = """You are a senior technical curriculum designer specializing in cloud data engineering.
Your task is to create a comprehensive, well-structured course outline."""


def supervisor(state: OverallState) -> dict:
    """
    Creates the course outline using the prompt from the active PROMPT_MODULE.
    Returns: {'sections': list[str]}
    """
    prompts = importlib.import_module(PROMPT_MODULE)
    user_prompt = prompts.SUPERVISOR_PROMPT.format(
        course_topic=state["course_topic"],
        course_audience=state["course_audience"],
    )

    response = _llm.invoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=user_prompt),
    ])

    raw = response.content.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    sections: list[str] = json.loads(raw)

    print(f"\n[Supervisor] Created outline with {len(sections)} sections:")
    for i, s in enumerate(sections):
        print(f"  {i + 1:02d}. {s}")

    return {"sections": sections}
