"""
Persistent plan tracker for course generation.

Saves a .plan.json file in the course output directory so that
re-running the pipeline resumes from where it left off.

Thread-safe: mark_completed uses a file lock so parallel workers
can update the plan without corrupting it.
"""

import json
import threading
from pathlib import Path

PLAN_FILENAME = ".plan.json"

_lock = threading.Lock()


# ── I/O helpers ────────────────────────────────────────────────────────────────

def _plan_path(output_dir: str) -> Path:
    return Path(output_dir) / PLAN_FILENAME


def load_plan(output_dir: str) -> dict | None:
    """Return the saved plan dict, or None if no plan exists yet."""
    p = _plan_path(output_dir)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def save_plan(output_dir: str, course_topic: str, sections: list[str]) -> None:
    """Persist a fresh plan with every section marked pending."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    plan = {
        "course_topic": course_topic,
        "sections": [
            {"index": i, "title": title, "status": "pending", "filename": None}
            for i, title in enumerate(sections)
        ],
    }
    _plan_path(output_dir).write_text(json.dumps(plan, indent=2), encoding="utf-8")


def mark_completed(output_dir: str, section_index: int, filename: str) -> None:
    """Thread-safe update: flip one section from pending → completed."""
    p = _plan_path(output_dir)
    with _lock:
        plan = json.loads(p.read_text(encoding="utf-8"))
        for s in plan["sections"]:
            if s["index"] == section_index:
                s["status"] = "completed"
                s["filename"] = filename
                break
        p.write_text(json.dumps(plan, indent=2), encoding="utf-8")


# ── Query helpers ──────────────────────────────────────────────────────────────

def get_all_sections(output_dir: str) -> list[dict]:
    """All section dicts from the saved plan (ordered by index)."""
    plan = load_plan(output_dir)
    if not plan:
        return []
    return sorted(plan["sections"], key=lambda s: s["index"])


def get_pending_sections(output_dir: str) -> list[dict]:
    """Section dicts whose status is still 'pending'."""
    return [s for s in get_all_sections(output_dir) if s["status"] == "pending"]


def get_completed_sections(output_dir: str) -> list[dict]:
    """Section dicts that have already been written."""
    return [s for s in get_all_sections(output_dir) if s["status"] == "completed"]
