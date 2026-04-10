"""
generate.py — Step 1: Run the LLM pipeline to create course content.

Usage:
    python generate.py                   # uses ACTIVE_COURSE from config.py
    python generate.py --course aws      # override course
"""

import argparse
import sys
from pathlib import Path

from courses import COURSES
from config import ACTIVE_COURSE
from graph import build_graph
from state import OverallState
from agents.notes_writer import write_notes, NOTES_SUBDIR
from agents.mindmap_writer import write_mindmap
from agents.logger import log


# ── Course resolution ──────────────────────────────────────────────────────────

def _read_prompt_file(path_str: str) -> str:
    p = Path(path_str)
    if not p.exists():
        sys.exit(f"File not found: {p}")
    return p.read_text(encoding="utf-8")


def _prompt_for_course(key: str) -> dict:
    """Interactively collect config for a course key not in courses.json."""
    known = ", ".join(COURSES)
    print(f"\nCourse '{key}' is not a known course ({known}).")
    print("Let's configure it.\n")

    topic = input("Topic (e.g. 'GCP Professional Data Engineer'): ").strip()
    if not topic:
        sys.exit("Topic is required.")

    audience = input("Audience (who is this course for?): ").strip()
    if not audience:
        sys.exit("Audience is required.")

    default_dir = f"docs/{key}"
    raw_dir = input(f"Output directory [{default_dir}]: ").strip()
    output_dir = Path(raw_dir) if raw_dir else Path(default_dir)

    _defaults = COURSES["aws"]

    def _load(label: str, default_key: str) -> str:
        print(f"\n{label}")
        path_str = input("  File path (.txt), or press Enter to use built-in template: ").strip()
        if path_str:
            return _read_prompt_file(path_str)
        print(f"  Using built-in '{default_key}' template.")
        return _defaults[default_key]

    return {
        "output_dir":        output_dir,
        "topic":             topic,
        "audience":          audience,
        "supervisor_system": _load("Supervisor system prompt", "supervisor_system"),
        "supervisor_prompt": _load("Supervisor prompt", "supervisor_prompt"),
        "worker_system":     _load("Worker system prompt", "worker_system"),
        "worker_prompt":     _load("Worker prompt", "worker_prompt"),
        "summarizer_system": _load("Summarizer system prompt", "summarizer_system"),
        "summarizer_intro":  _load("Summarizer intro prompt", "summarizer_intro"),
        "notes_system":      _load("Notes system prompt", "notes_system"),
        "notes_prompt":      _load("Notes prompt", "notes_prompt"),
    }


def resolve_course(key: str) -> dict:
    if key in COURSES:
        return COURSES[key]
    return _prompt_for_course(key)


# ── Output helpers ─────────────────────────────────────────────────────────────

def _write_course_index(final_state: OverallState, output_dir: Path, topic: str, audience: str, course_key: str = "") -> None:
    """Write docs/<course>/index.md with a section TOC."""
    ordered = sorted(final_state["completed_sections"], key=lambda x: x["section_index"])
    toc_lines = [f"- [{s['section_title']}]({s['filename']})" for s in ordered]

    mindmap_link = ""
    if course_key:
        mindmap_link = f"\n[🗺 Open Interactive Mind Map](../{course_key}-mindmap.html){{ .md-button }}\n"

    index = (
        f"# {topic}\n\n"
        f"**Target audience:** {audience}\n\n"
        f"{mindmap_link}"
        f"\n---\n\n"
        f"## Course Sections\n\n"
        + "\n".join(toc_lines)
    )
    (output_dir / "index.md").write_text(index, encoding="utf-8")
    print(f"  Saved: {output_dir / 'index.md'}")


def generate_notes(
    final_state: OverallState,
    output_dir: Path,
    notes_system: str,
    notes_prompt: str,
) -> dict[str, str]:
    """Generate one SA Quick Reference card per section.
    Returns {section_title: notes_filename}."""
    print("\n[Notes] Generating SA Quick Reference cards...")
    notes_map: dict[str, str] = {}
    ordered = sorted(final_state["completed_sections"], key=lambda x: x["section_index"])
    for section in ordered:
        notes_filename = write_notes(section, output_dir, notes_system, notes_prompt)
        notes_map[section["section_title"]] = notes_filename
    return notes_map


# ── Entry point ────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Tech RampUp — generate course content via LLM")
    parser.add_argument(
        "--course",
        default=None,
        metavar="KEY",
        help=f"Course to generate. Known: {', '.join(COURSES)}. "
             "Pass any other key to configure a custom course interactively.",
    )
    args = parser.parse_args()

    course_key = args.course or ACTIVE_COURSE
    if not course_key:
        parser.error("No course specified. Pass --course <key> or set ACTIVE_COURSE in config.py.")

    course = resolve_course(course_key)

    output_dir: Path = course["output_dir"]
    topic: str       = course["topic"]
    audience: str    = course["audience"]

    log.info(f"Log file: {log.log_file}")
    print("=" * 60)
    print(f"Course:  {topic}")
    print(f"Output:  {output_dir}")
    print("=" * 60)

    graph = build_graph()

    initial_state: OverallState = {
        "course_topic":       topic,
        "course_audience":    audience,
        "output_dir":         output_dir.as_posix(),
        "supervisor_system":  course["supervisor_system"],
        "supervisor_prompt":  course["supervisor_prompt"],
        "worker_system":      course["worker_system"],
        "worker_prompt":      course["worker_prompt"],
        "summarizer_system":  course["summarizer_system"],
        "summarizer_intro":   course["summarizer_intro"],
        "sections":           [],
        "completed_sections": [],
        "final_document":     "",
    }

    print("\n[Graph] Starting...\n")
    final_state = graph.invoke(initial_state, config={"recursion_limit": 100})

    print("\n[Generate] Saving course files...")
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_dir = Path("output")
    archive_dir.mkdir(exist_ok=True)

    combined_path = archive_dir / "complete_course.md"
    combined_path.write_text(final_state["final_document"], encoding="utf-8")
    print(f"  Saved: {combined_path}")

    _write_course_index(final_state, output_dir, topic, audience, course_key)

    generate_notes(final_state, output_dir, course["notes_system"], course["notes_prompt"])

    print("\n[Mindmap] Generating mind map...")
    write_mindmap(final_state, course_key, topic, audience)

    sections_count = len(final_state["completed_sections"])
    doc_size = len(final_state["final_document"])
    print(f"\n[Generate] Done. {sections_count} sections, {doc_size:,} chars total.")
    print(f"           Output: {output_dir.resolve()}")
    print("\nNext step: python publish.py")


if __name__ == "__main__":
    main()
