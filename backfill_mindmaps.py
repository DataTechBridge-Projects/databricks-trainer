"""
backfill_mindmaps.py — Generate mind maps for existing courses without re-running the full pipeline.

Usage:
    python backfill_mindmaps.py                  # all courses in courses.json
    python backfill_mindmaps.py --course aws     # one course only
"""

import argparse
from pathlib import Path

from courses import COURSES
from config import ACTIVE_COURSE
from agents.tracker import load_plan
from agents.mindmap_writer import write_mindmap
from generate import _write_course_index


def _build_fake_state(output_dir: Path, plan: dict) -> dict:
    """Reconstruct a minimal OverallState from saved section files."""
    completed = sorted(
        [s for s in plan["sections"] if s["status"] == "completed" and s.get("filename")],
        key=lambda s: s["index"],
    )
    sections = []
    for s in completed:
        filepath = output_dir / s["filename"]
        content = filepath.read_text(encoding="utf-8") if filepath.exists() else ""
        sections.append({
            "section_index": s["index"],
            "section_title": s["title"],
            "filename": s["filename"],
            "content": content,
        })
    return {"completed_sections": sections}


def backfill_course(course_key: str, cfg: dict) -> None:
    output_dir: Path = cfg["output_dir"]
    topic: str       = cfg["topic"]
    audience: str    = cfg["audience"]

    plan = load_plan(output_dir.as_posix())
    if not plan:
        print(f"  [Skip] No plan for '{course_key}' — run generate.py first.")
        return

    completed = [s for s in plan["sections"] if s["status"] == "completed"]
    if not completed:
        print(f"  [Skip] No completed sections for '{course_key}'.")
        return

    print(f"\n[Mindmap] Generating for '{course_key}' ({len(completed)} sections)...")
    fake_state = _build_fake_state(output_dir, plan)
    out = write_mindmap(fake_state, course_key, topic, audience)
    if out:
        print(f"  Done: {out}")
        # Update course index.md with mind map button link
        _write_course_index(fake_state, output_dir, topic, audience, course_key)
    else:
        print(f"  [Error] Mind map generation failed for '{course_key}'.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill mind maps for existing courses")
    parser.add_argument("--course", default=None, metavar="KEY",
                        help=f"Course key to backfill. Known: {', '.join(COURSES)}")
    args = parser.parse_args()

    if args.course:
        if args.course not in COURSES:
            parser.error(f"Unknown course '{args.course}'. Known: {', '.join(COURSES)}")
        target = {args.course: COURSES[args.course]}
    else:
        target = COURSES

    for key, cfg in target.items():
        backfill_course(key, cfg)

    print("\n[Done] Run 'python publish.py --push' to deploy.")


if __name__ == "__main__":
    main()
