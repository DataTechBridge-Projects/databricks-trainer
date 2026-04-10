"""
publish.py — Step 2: Register courses in mkdocs.yml and publish to GitHub Pages.

Reads existing docs/<course>/ files — does NOT call the LLM.
Run this after generate.py, or any time you want to re-publish without regenerating.

Usage:
    python publish.py                    # publishes all courses found in docs/
    python publish.py --course aws       # publish a specific course only
    python publish.py --push             # also commit and push to trigger GitHub Actions
"""

import argparse
import json
import re
import subprocess
from pathlib import Path

from courses import COURSES
from config import ACTIVE_COURSE
from agents.notes_writer import NOTES_SUBDIR
from agents.tracker import load_plan

MKDOCS_FILE = Path("mkdocs.yml")
DOCS_DIR    = Path("docs")
MANIFEST_FILE = DOCS_DIR / "manifest.json"

# Populated at runtime by _ensure_course_registered()
_NAV_MARKERS: dict[str, tuple[str, str]] = {}
_NOTES_NAV_MARKERS: dict[str, tuple[str, str]] = {}


# ── Course registration ────────────────────────────────────────────────────────

def _ensure_course_registered(folder: str, course_key: str, topic: str) -> None:
    """Add the course nav block to mkdocs.yml if not already present.
    Also populates the in-memory _NAV_MARKERS / _NOTES_NAV_MARKERS dicts."""
    tag = course_key.upper().replace("-", "_")
    sec_start   = f"    # {tag}_SECTIONS_START"
    sec_end     = f"    # {tag}_SECTIONS_END"
    notes_start = f"      # {tag}_NOTES_START"
    notes_end   = f"      # {tag}_NOTES_END"

    _NAV_MARKERS[folder]       = (sec_start, sec_end)
    _NOTES_NAV_MARKERS[folder] = (notes_start, notes_end)

    content = MKDOCS_FILE.read_text(encoding="utf-8")
    if sec_start in content:
        return  # already registered

    course_name = topic.split()[0] if topic else course_key.title()
    rel_folder  = Path(folder).name
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

    insert_pattern = r"(nav:\n  - Home: index\.md\n)"
    if re.search(insert_pattern, content):
        content = re.sub(insert_pattern, r"\1" + nav_block, content, count=1)
    else:
        content += "\n" + nav_block

    MKDOCS_FILE.write_text(content, encoding="utf-8")
    print(f"  [Nav] Auto-registered '{course_key}' in {MKDOCS_FILE}")


# ── Nav patching ───────────────────────────────────────────────────────────────

def _patch_sections_nav(course_key: str, output_dir: Path, plan: dict) -> None:
    """Replace section entries between nav markers from the course plan."""
    folder  = output_dir.as_posix()
    markers = _NAV_MARKERS.get(folder)
    if not markers:
        print(f"  [Nav] No markers for '{folder}' — skipping.")
        return

    nav_start, nav_end = markers
    completed = sorted(
        [s for s in plan["sections"] if s["status"] == "completed" and s.get("filename")],
        key=lambda s: s["index"],
    )
    rel_folder = output_dir.name

    lines = []
    for s in completed:
        title = re.sub(r"^section\s+\d+[\s:\-–]+", "", s["title"], flags=re.IGNORECASE).strip()
        lines.append(f'    - "{s["index"] + 1}. {title}": {rel_folder}/{s["filename"]}')

    new_block = "\n".join([nav_start] + lines + [nav_end])
    content = MKDOCS_FILE.read_text(encoding="utf-8")
    content = re.sub(
        rf"{re.escape(nav_start)}.*?{re.escape(nav_end)}",
        new_block, content, flags=re.DOTALL,
    )
    MKDOCS_FILE.write_text(content, encoding="utf-8")
    print(f"  [Nav] Patched sections nav — {len(lines)} entries")


def _patch_notes_nav(course_key: str, output_dir: Path, plan: dict) -> None:
    """Replace notes entries between nav markers, built from existing notes files."""
    folder  = output_dir.as_posix()
    markers = _NOTES_NAV_MARKERS.get(folder)
    if not markers:
        print(f"  [Notes Nav] No markers for '{folder}' — skipping.")
        return

    notes_nav_start, notes_nav_end = markers
    course_folder = output_dir.name
    notes_dir = output_dir / NOTES_SUBDIR

    completed = sorted(
        [s for s in plan["sections"] if s["status"] == "completed" and s.get("filename")],
        key=lambda s: s["index"],
    )

    lines = []
    for s in completed:
        stem = Path(s["filename"]).stem
        notes_file = notes_dir / f"notes_{stem}.md"
        if not notes_file.exists():
            continue
        title = re.sub(r"^section\s+\d+[\s:\-–]+", "", s["title"], flags=re.IGNORECASE).strip()
        path = f"{course_folder}/{NOTES_SUBDIR}/notes_{stem}.md"
        lines.append(f'      - "{title}": {path}')

    if not lines:
        return  # no notes generated yet

    new_block = "\n".join([notes_nav_start] + lines + [notes_nav_end])
    content = MKDOCS_FILE.read_text(encoding="utf-8")
    content = re.sub(
        rf"{re.escape(notes_nav_start)}.*?{re.escape(notes_nav_end)}",
        new_block, content, flags=re.DOTALL,
    )
    MKDOCS_FILE.write_text(content, encoding="utf-8")
    print(f"  [Notes Nav] Patched notes nav — {len(lines)} entries")


def _patch_mindmap_notes(course_key: str, output_dir: Path, plan: dict) -> None:
    """Patch NOTES_MAP in the course mind map HTML."""
    # Derive mindmap path from course key; fall back to output_dir name
    mindmap_path = Path("docs") / f"{course_key}-mindmap.html"
    if not mindmap_path.exists():
        # Try output_dir folder name as fallback (e.g. docs/aws-sa -> aws-sa-mindmap.html)
        mindmap_path = Path("docs") / f"{output_dir.name}-mindmap.html"
    if not mindmap_path.exists():
        return

    course_folder = output_dir.name
    notes_dir = output_dir / NOTES_SUBDIR
    completed = sorted(
        [s for s in plan["sections"] if s["status"] == "completed" and s.get("filename")],
        key=lambda s: s["index"],
    )

    js_entries = []
    for s in completed:
        stem = Path(s["filename"]).stem
        notes_file = notes_dir / f"notes_{stem}.md"
        if not notes_file.exists():
            continue
        notes_url  = f"{course_folder}/{NOTES_SUBDIR}/notes_{stem}/"
        safe_title = s["title"].replace("'", "\\'")
        js_entries.append(f"  '{safe_title}': '{notes_url}'")

    if not js_entries:
        return

    new_notes_map = "const NOTES_MAP = {\n" + ",\n".join(js_entries) + "\n};"
    content = mindmap_path.read_text(encoding="utf-8")
    content = re.sub(
        r"const NOTES_MAP = \{[^}]*\};",
        new_notes_map, content, flags=re.DOTALL,
    )
    mindmap_path.write_text(content, encoding="utf-8")
    print(f"  [Mindmap] Patched NOTES_MAP in {mindmap_path}")


# ── Manifest + home index ──────────────────────────────────────────────────────

def _build_manifest_and_index(all_courses: dict[str, dict]) -> None:
    """Rebuild manifest.json and docs/index.md from all courses with completed sections."""
    courses_out = []

    for key, cfg in all_courses.items():
        output_dir: Path = cfg["output_dir"]
        plan = load_plan(output_dir.as_posix())
        if not plan:
            continue

        completed = sorted(
            [s for s in plan["sections"] if s["status"] == "completed" and s.get("filename")],
            key=lambda s: s["index"],
        )
        if not completed:
            continue

        rel_dir = output_dir.resolve().relative_to(DOCS_DIR.resolve()).as_posix()
        courses_out.append({
            "key":      key,
            "title":    cfg["topic"],
            "audience": cfg["audience"],
            "sections": [
                {"index": s["index"], "title": s["title"], "file": f"{rel_dir}/{s['filename']}"}
                for s in completed
            ],
        })

    DOCS_DIR.mkdir(exist_ok=True)
    MANIFEST_FILE.write_text(json.dumps({"courses": courses_out}, indent=2), encoding="utf-8")
    print(f"  [Manifest] Updated — {len(courses_out)} course(s)")

    # Home index
    rows = "\n".join(
        f"| [{c['title']}]({c['key']}/index.md) | {c['audience']} |"
        for c in courses_out
    )
    home = (
        "# Tech Ramp Up\n\n"
        "A multi-agent AI system that generates 100-level technical training courses for **Solution Architects**.\n\n"
        "Courses are designed for breadth over depth — enough to hold a credible customer conversation, "
        "understand what the technology does, why it matters, and how it compares to alternatives.\n\n"
        "---\n\n"
        "## Available Courses\n\n"
        "| Course | Description |\n"
        "|--------|-------------|\n"
        f"{rows}\n\n"
        "---\n"
    )
    (DOCS_DIR / "index.md").write_text(home, encoding="utf-8")
    print(f"  [Home] docs/index.md updated — {len(courses_out)} course(s)")


# ── Git push ───────────────────────────────────────────────────────────────────

def _git_push(message: str) -> None:
    print(f"\n[Git] Committing and pushing...")
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", message], check=True)
    subprocess.run(["git", "push"], check=True)
    print("[Git] Pushed — GitHub Actions will deploy to GitHub Pages.")


# ── Publish a single course ────────────────────────────────────────────────────

def publish_course(course_key: str, cfg: dict) -> bool:
    """Register and patch nav for one course. Returns True if it had completed sections."""
    output_dir: Path = cfg["output_dir"]
    topic: str       = cfg["topic"]

    plan = load_plan(output_dir.as_posix())
    if not plan:
        print(f"  [Skip] No plan found for '{course_key}' — run generate.py first.")
        return False

    completed = [s for s in plan["sections"] if s["status"] == "completed"]
    if not completed:
        print(f"  [Skip] No completed sections for '{course_key}'.")
        return False

    print(f"\n[Publish] {course_key} — {len(completed)} sections")
    _ensure_course_registered(output_dir.as_posix(), course_key, topic)
    _patch_sections_nav(course_key, output_dir, plan)
    _patch_notes_nav(course_key, output_dir, plan)
    _patch_mindmap_notes(course_key, output_dir, plan)
    return True


# ── Entry point ────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Tech RampUp — publish courses to GitHub Pages")
    parser.add_argument(
        "--course",
        default=None,
        metavar="KEY",
        help="Publish a specific course only. Omit to publish all courses with completed content.",
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Commit and push after publishing to trigger GitHub Actions deployment.",
    )
    parser.add_argument(
        "--message",
        default="publish: update course content",
        help="Git commit message (used with --push).",
    )
    args = parser.parse_args()

    # Determine which courses to publish
    if args.course:
        course_key = args.course
        if course_key not in COURSES:
            parser.error(
                f"Unknown course '{course_key}'.\n"
                f"  Known courses: {', '.join(COURSES)}\n"
                f"  To add a new course, add it to courses.json first."
            )
        target_courses = {course_key: COURSES[course_key]}
    else:
        # Default: publish ACTIVE_COURSE; use --course to override or omit to do all
        target_courses = COURSES

    published_any = False
    for key, cfg in target_courses.items():
        if publish_course(key, cfg):
            published_any = True

    if not published_any:
        print("\nNothing to publish. Run generate.py first.")
        return

    print("\n[Publish] Updating manifest and home index...")
    _build_manifest_and_index(COURSES)

    if args.push:
        _git_push(args.message)
    else:
        print("\n[Publish] Done. To deploy to GitHub Pages:")
        print("          git add . && git commit -m 'publish' && git push")


if __name__ == "__main__":
    main()
