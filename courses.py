"""
Course registry loader. To add a new course, add an entry to courses.json.
The pipeline auto-registers it in mkdocs.yml on first run.
"""

import json
from pathlib import Path

_ROOT = Path(__file__).parent
_PROMPTS = json.loads((_ROOT / "prompts" / "common.json").read_text(encoding="utf-8"))
_RAW = json.loads((_ROOT / "courses.json").read_text(encoding="utf-8"))

COURSES: dict[str, dict] = {
    key: {
        "output_dir": _ROOT / entry["output_dir"],
        "topic":      entry["topic"],
        "audience":   entry["audience"],
        **_PROMPTS,
    }
    for key, entry in _RAW.items()
}
