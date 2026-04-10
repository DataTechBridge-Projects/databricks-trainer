import argparse
import json
import re
import sys
from pathlib import Path

from courses import COURSES
from config import ACTIVE_COURSE
from graph import build_graph
from state import OverallState
from agents.notes_writer import write_notes, NOTES_SUBDIR
from agents.tracker import load_plan
from agents.logger import log

MKDOCS_FILE = Path("mkdocs.yml")

# Nav markers for known courses — auto-populated at runtime by _ensure_course_registered()
_NAV_MARKERS: dict[str, tuple[str, str]] = {}
_NOTES_NAV_MARKERS: dict[str, tuple[str, str]] = {}


def _ensure_course_registered(folder: str, course_key: str, topic: str) -> None:
    """Auto-register a course in _NAV_MARKERS, _NOTES_NAV_MARKERS, and mkdocs.yml nav
    if it isn't already present. Safe to call on every run — skips if already registered."""
    tag = course_key.upper().replace("-", "_")
    sec_start  = f"    # {tag}_SECTIONS_START"
    sec_end    = f"    # {tag}_SECTIONS_END"
    notes_start = f"      # {tag}_NOTES_START"
    notes_end   = f"      # {tag}_NOTES_END"

    _NAV_MARKERS[folder]       = (sec_start, sec_end)
    _NOTES_NAV_MARKERS[folder] = (notes_start, notes_end)

    content = MKDOCS_FILE.read_text(encoding="utf-8")
    if sec_start in content:
        return  # already in mkdocs.yml

    course_name = topic.split()[0] if topic else course_key.title()
    rel_folder  = re.sub(r"^docs/", "", folder)
    nav_block = (
        f"  - {course_name}:\n"
        f"    - Home: {rel_folder}/index.md\n"
        f"    {sec_start}\n"
        f"    {sec_end}\n"
        f"    - SA Quick Reference:\n"
        f"      {notes_start}\n"
        f'      - "Notes": {rel_folder}/index.md\n'
        f"      {notes_end}\n"
    )

    # Insert before the first top-level nav entry that isn't Home
    insert_pattern = r"(nav:\n  - Home: index\.md\n)"
    if re.search(insert_pattern, content):
        content = re.sub(insert_pattern, r"\1" + nav_block, content, count=1)
    else:
        content += "\n" + nav_block

    MKDOCS_FILE.write_text(content, encoding="utf-8")
    print(f"  [Nav] Auto-registered '{course_key}' in {MKDOCS_FILE}")


# ── Course resolution ──────────────────────────────────────────────────────────

def _read_prompt_file(path_str: str) -> str:
    p = Path(path_str)
    if not p.exists():
        sys.exit(f"File not found: {p}")
    return p.read_text(encoding="utf-8")


def _prompt_for_course(key: str) -> dict:
    """Interactively collect config for a course key not in courses.py."""
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

    # Use aws prompts as built-in defaults — generic enough for any tech course
    _defaults = COURSES["aws"]

    def _load(label: str, default_key: str) -> str:
        print(f"\n{label}")
        path_str = input("  File path (.txt), or press Enter to use built-in template: ").strip()
        if path_str:
            return _read_prompt_file(path_str)
        print(f"  Using built-in '{default_key}' template.")
        return _defaults[default_key]

    supervisor_prompt = _load("Supervisor prompt  — tells the LLM how to build the course outline", "supervisor_prompt")
    worker_system     = _load("Worker system prompt — LLM persona for section writing",              "worker_system")
    worker_prompt     = _load("Worker prompt — section content template",                            "worker_prompt")
    notes_system      = _load("Notes system prompt — LLM persona for SA quick-ref cards",           "notes_system")
    notes_prompt      = _load("Notes prompt — SA quick-ref card template",                           "notes_prompt")

    return {
        "output_dir":       output_dir,
        "topic":            topic,
        "audience":         audience,
        "supervisor_prompt": supervisor_prompt,
        "worker_system":    worker_system,
        "worker_prompt":    worker_prompt,
        "notes_system":     notes_system,
        "notes_prompt":     notes_prompt,
    }


def resolve_course(key: str) -> dict:
    """Return a course config dict for the given key, prompting if unknown."""
    if key in COURSES:
        return COURSES[key]
    return _prompt_for_course(key)


# ── Output helpers (all take explicit config params, no module globals) ────────

def _write_index(final_state: OverallState, output_dir: Path, topic: str, audience: str) -> None:
    """Regenerate docs/<course>/index.md with section links after each run."""
    ordered = sorted(final_state["completed_sections"], key=lambda x: x["section_index"])
    toc_lines = [f"- [{s['section_title']}]({s['filename']})" for s in ordered]

    index = (
        f"# {topic}\n\n"
        f"**Target audience:** {audience}\n\n"
        f"---\n\n"
        f"## Course Sections\n\n"
        + "\n".join(toc_lines)
    )

    (output_dir / "index.md").write_text(index, encoding="utf-8")
    print(f"  Saved: {output_dir / 'index.md'}")


def _update_mkdocs_nav(final_state: OverallState, output_dir: Path) -> None:
    """Replace the section entries between nav markers in mkdocs.yml.
    Silently skips if no markers exist for this course (e.g. custom courses)."""
    folder = output_dir.as_posix()
    markers = _NAV_MARKERS.get(folder)
    if not markers:
        print(f"  [Nav] No mkdocs.yml markers for '{folder}' — skipping nav patch.")
        return

    nav_start, nav_end = markers
    ordered = sorted(final_state["completed_sections"], key=lambda x: x["section_index"])

    lines = []
    for s in ordered:
        num = s["section_index"] + 1
        title = re.sub(r"^section\s+\d+[\s:\-–]+", "", s["section_title"], flags=re.IGNORECASE).strip()
        rel_folder = re.sub(r"^docs/", "", folder)
        lines.append(f'    - "{num}. {title}": {rel_folder}/{s["filename"]}')

    new_block = "\n".join([nav_start] + lines + [nav_end])
    content = MKDOCS_FILE.read_text(encoding="utf-8")
    content = re.sub(
        rf"{re.escape(nav_start)}.*?{re.escape(nav_end)}",
        new_block,
        content,
        flags=re.DOTALL,
    )
    MKDOCS_FILE.write_text(content, encoding="utf-8")
    print(f"  Updated: {MKDOCS_FILE} nav ({len(ordered)} sections)")


def _update_mkdocs_notes_nav(notes_map: dict[str, str], output_dir: Path) -> None:
    """Patch the SA Quick Reference section in mkdocs.yml nav.
    Silently skips if no markers exist for this course."""
    folder = output_dir.as_posix()
    markers = _NOTES_NAV_MARKERS.get(folder)
    if not markers:
        print(f"  [Notes Nav] No mkdocs.yml notes markers for '{folder}' — skipping.")
        return

    notes_nav_start, notes_nav_end = markers
    course_folder = output_dir.name

    lines = []
    for section_title, notes_filename in notes_map.items():
        clean_title = re.sub(r"^section\s+\d+[\s:\-–]+", "", section_title, flags=re.IGNORECASE).strip()
        path = f"{course_folder}/{NOTES_SUBDIR}/{notes_filename}"
        lines.append(f'      - "{clean_title}": {path}')

    new_block = "\n".join([notes_nav_start] + lines + [notes_nav_end])
    content = MKDOCS_FILE.read_text(encoding="utf-8")
    content = re.sub(
        rf"{re.escape(notes_nav_start)}.*?{re.escape(notes_nav_end)}",
        new_block,
        content,
        flags=re.DOTALL,
    )
    MKDOCS_FILE.write_text(content, encoding="utf-8")
    print(f"  [Notes] Updated {MKDOCS_FILE} notes nav ({len(notes_map)} entries)")


def generate_notes(
    final_state: OverallState,
    output_dir: Path,
    notes_system: str,
    notes_prompt: str,
) -> dict[str, str]:
    """Generate one SA Quick Reference card per section.
    Returns {section_title: notes_filename} for mind map patching."""
    print("\n[Notes] Generating SA Quick Reference cards...")
    notes_map: dict[str, str] = {}
    ordered = sorted(final_state["completed_sections"], key=lambda x: x["section_index"])
    for section in ordered:
        notes_filename = write_notes(section, output_dir, notes_system, notes_prompt)
        notes_map[section["section_title"]] = notes_filename
    _update_mkdocs_notes_nav(notes_map, output_dir)
    return notes_map


def _update_mindmap_notes(notes_map: dict[str, str], output_dir: Path) -> None:
    """Patch the NOTES_MAP constant in the course mind map HTML."""
    mindmap_candidates = {
        "docs/aws":        Path("docs/aws-mindmap.html"),
        "docs/aws-sa":     Path("docs/aws-mindmap.html"),
        "docs/databricks": Path("docs/databricks-mindmap.html"),
        "docs/azure":      Path("docs/azure-mindmap.html"),
    }
    mindmap_path = mindmap_candidates.get(output_dir.as_posix())
    if not mindmap_path or not mindmap_path.exists():
        print(f"  [Notes] No mind map found for {output_dir.as_posix()}, skipping patch.")
        return

    course_folder = output_dir.name
    js_entries: list[str] = []
    for section_title, notes_filename in notes_map.items():
        notes_stem = notes_filename.removesuffix(".md")
        notes_url = f"{course_folder}/{NOTES_SUBDIR}/{notes_stem}/"
        safe_title = section_title.replace("'", "\\'")
        js_entries.append(f"  '{safe_title}': '{notes_url}'")

    new_notes_map = "const NOTES_MAP = {\n" + ",\n".join(js_entries) + "\n};"
    content = mindmap_path.read_text(encoding="utf-8")
    content = re.sub(
        r"const NOTES_MAP = \{[^}]*\};",
        new_notes_map,
        content,
        flags=re.DOTALL,
    )
    mindmap_path.write_text(content, encoding="utf-8")
    print(f"  [Notes] Patched NOTES_MAP in {mindmap_path} ({len(notes_map)} entries)")


DOCS_DIR = Path("docs")
MANIFEST_FILE = DOCS_DIR / "manifest.json"


def update_reader_manifest() -> None:
    """
    Rebuild docs/manifest.json by scanning every known course's .plan.json.
    The standalone index.html reader uses this to populate the course tabs
    and section list without any server-side logic.
    """
    courses_out = []

    for key, cfg in COURSES.items():
        output_dir: Path = cfg["output_dir"]
        plan = load_plan(output_dir.as_posix())
        if not plan:
            continue  # course has never been run

        completed = [s for s in plan["sections"] if s["status"] == "completed" and s.get("filename")]
        if not completed:
            continue

        completed.sort(key=lambda s: s["index"])

        # Strip the leading "docs/" so paths are relative to the docs/ root
        rel_dir = output_dir.resolve().relative_to(DOCS_DIR.resolve()).as_posix()

        courses_out.append({
            "key":      key,
            "title":    cfg["topic"],
            "audience": cfg["audience"],
            "sections": [
                {
                    "index": s["index"],
                    "title": s["title"],
                    "file":  f"{rel_dir}/{s['filename']}",
                }
                for s in completed
            ],
        })

    manifest = {"courses": courses_out}
    DOCS_DIR.mkdir(exist_ok=True)
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"  [Reader] manifest.json updated — {len(courses_out)} course(s)")


def save_outputs(final_state: OverallState, output_dir: Path, topic: str, audience: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_dir = Path("output")
    archive_dir.mkdir(exist_ok=True)

    combined_path = archive_dir / "complete_course.md"
    combined_path.write_text(final_state["final_document"], encoding="utf-8")
    print(f"  Saved: {combined_path}")

    _write_index(final_state, output_dir, topic, audience)
    _update_mkdocs_nav(final_state, output_dir)


# ── Entry point ────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Tech RampUp Trainer — course generator")
    parser.add_argument(
        "--course",
        default=None,
        metavar="KEY",
        help=f"Course to generate. Known: {', '.join(COURSES)}. "
             "Pass any other key to configure a custom course interactively.",
    )
    args = parser.parse_args()

    course_key = args.course or ACTIVE_COURSE
    course = resolve_course(course_key)

    output_dir: Path = course["output_dir"]
    topic: str       = course["topic"]
    audience: str    = course["audience"]

    _ensure_course_registered(output_dir.as_posix(), course_key, topic)

    log.info(f"Log file: {log.log_file}")
    print("=" * 60)
    print(f"Course Generator: {topic}")
    print(f"Output:           {output_dir}")
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

    print("\n[Main] Saving output files...")
    save_outputs(final_state, output_dir, topic, audience)

    notes_map = generate_notes(final_state, output_dir, course["notes_system"], course["notes_prompt"])
    _update_mindmap_notes(notes_map, output_dir)

    print("\n[Main] Updating reader manifest...")
    update_reader_manifest()

    sections_count = len(final_state["completed_sections"])
    doc_size = len(final_state["final_document"])
    print(f"\n[Main] Done. {sections_count} sections, {doc_size:,} chars total.")
    print(f"       Output directory: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
