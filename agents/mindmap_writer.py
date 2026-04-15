"""
agents/mindmap_writer.py

Generates a D3 force-directed mind map HTML file for a course.

Called once after notes generation in generate.py.
Output: docs/<course_key>-mindmap.html
"""

import json
import re
from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage

from config import make_llm
from state import OverallState
from agents.logger import log

# _llm = make_llm(timeout=900)
from langchain_ollama import ChatOllama
_llm = ChatOllama(model="qwen2.5:14b-instruct", base_url="http://localhost:11434", timeout=900)

TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "mindmap_template.html"

DOMAIN_COLORS = [
    "#4a90d9",  # blue
    "#e8834a",  # orange
    "#7ac47a",  # green
    "#c47ad4",  # purple
    "#e8c84a",  # yellow
    "#4ac4c4",  # teal
    "#e84a6e",  # red-pink
    "#8ab4e8",  # light blue
]

_SYSTEM = """\
You are a Solution Architect enablement expert building interactive mind maps for SA training.
Return ONLY valid JSON — no markdown fences, no explanation."""

_PROMPT = """\
Build a mind map data structure for the course: "{topic}"
Audience: {audience}

The mind map must cover these REQUIRED domains (always include them):
1. Core Architecture
2. Security & Identity
3. Cost & Billing
4. Migration & Adoption
5. Monitoring & Operations

Plus add 2-3 additional topic-specific domains that matter most for SA conversations.

For each domain, generate 5-8 leaf nodes. Each node represents a key concept an SA needs to know.

Return a JSON object in EXACTLY this shape:
{{
  "title": "<short display title, e.g. AWS Data Engineer>",
  "domains": ["Domain Name 1", "Domain Name 2", ...],
  "colors": [],
  "children": [
    {{
      "name": "Domain Name 1",
      "nodes": [
        {{
          "name": "Short concept name (2-4 words)",
          "desc": "One sentence on what it is. One sentence on why a customer cares.",
          "chips": ["term1", "term2", "term3", "term4", "term5"],
          "priority": "critical",
          "section_index": 2
        }}
      ]
    }}
  ]
}}

Priority values: "critical" (must know before any customer call), "quick" (good to know), "new" (recently GA, worth flagging), "skip" (completeness only).
ML/AI topics should be "critical".
The "colors" array should be empty — it will be filled in automatically.

"section_index" must be the 0-based index of the most relevant course section from the list below.
Every node must have a section_index. Choose the section whose content best covers that concept.

Course sections (use their index numbers):
{sections}
"""


def _extract_json(text: str) -> dict:
    """Strip markdown fences if present and parse JSON."""
    text = text.strip()
    # Remove ```json ... ``` or ``` ... ```
    text = re.sub(r"^```[a-z]*\n?", "", text)
    text = re.sub(r"\n?```$", "", text)
    return json.loads(text.strip())


def write_mindmap(
    final_state: OverallState,
    course_key: str,
    topic: str,
    audience: str,
) -> Path | None:
    """
    Generate a D3 mind map HTML for the course.
    Returns the output path, or None if generation fails.
    """
    ordered = sorted(final_state["completed_sections"], key=lambda x: x["section_index"])
    # Numbered list so LLM can reference by index
    section_list = "\n".join(f"{i}. {s['section_title']}" for i, s in enumerate(ordered))
    # Relative URLs — mindmap is at docs/<course>-mindmap.html, sections at docs/<course>/section_XX/
    # Relative path works both with mkdocs serve (localhost) and GitHub Pages
    index_to_url = {
        i: f"{course_key}/{Path(s['filename']).stem}/"
        for i, s in enumerate(ordered)
    }

    user_prompt = _PROMPT.format(topic=topic, audience=audience, sections=section_list)

    start = log.agent_start("Mindmap", topic)
    chunks = []
    try:
        for chunk in _llm.stream([
            SystemMessage(content=_SYSTEM),
            HumanMessage(content=user_prompt),
        ]):
            chunks.append(chunk.content)
    except Exception as exc:
        log.info(f"[Mindmap] LLM error: {exc}")
        return None

    raw_text = "".join(chunks)
    log.agent_end("Mindmap", topic, start=start)

    try:
        data = _extract_json(raw_text)
    except json.JSONDecodeError as exc:
        log.info(f"[Mindmap] JSON parse error: {exc}\nRaw: {raw_text[:500]}")
        return None

    # Fill colors from our palette
    n_domains = len(data.get("domains", []))
    data["colors"] = [DOMAIN_COLORS[i % len(DOMAIN_COLORS)] for i in range(n_domains)]

    # Resolve section_index → section_url on every leaf node
    for domain in data.get("children", []):
        for node in domain.get("nodes", []):
            idx = node.pop("section_index", None)
            if idx is not None and idx in index_to_url:
                node["section_url"] = index_to_url[idx]

    return _render_template(data, course_key, topic, index_to_url, ordered)


def _render_template(data: dict, course_key: str, title: str, index_to_url: dict, sections: list) -> Path:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    # Inject color CSS variables (pad to 8 slots)
    colors = data["colors"]
    for i in range(8):
        c = colors[i] if i < len(colors) else "#475569"
        template = template.replace(f"__COLOR_{i}__", c)

    # Inject title
    template = template.replace("__TITLE__", title)

    # Build SECTIONS_MAP: { "section title": "url" } for JS substring matching
    sections_map = {s["section_title"]: index_to_url[i] for i, s in enumerate(sections) if i in index_to_url}
    sections_map_json = json.dumps(sections_map, ensure_ascii=False, indent=2)
    template = template.replace("__SECTIONS_MAP__", sections_map_json)

    # Inject graph data
    graph_json = json.dumps(data, ensure_ascii=False, indent=2)
    template = template.replace("__GRAPH_DATA__", graph_json)

    out_path = Path("docs") / f"{course_key}-mindmap.html"
    out_path.write_text(template, encoding="utf-8")
    log.info(f"[Mindmap] Saved: {out_path}")
    print(f"  Saved: {out_path}")
    return out_path
