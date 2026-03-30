import re
from pathlib import Path
from config import OUTPUT_DIR, COURSE_TOPIC, COURSE_AUDIENCE, PROMPT_MODULE
from graph import build_graph
from state import OverallState

MKDOCS_FILE = Path("mkdocs.yml")

# Each course folder maps to its own nav marker in mkdocs.yml
_NAV_MARKERS = {
    "docs/databricks": ("    # DATABRICKS_SECTIONS_START", "    # DATABRICKS_SECTIONS_END"),
    "docs/aws":        ("    # AWS_SECTIONS_START",        "    # AWS_SECTIONS_END"),
    "docs/azure":      ("    # AZURE_SECTIONS_START",      "    # AZURE_SECTIONS_END"),
}
NAV_START, NAV_END = _NAV_MARKERS.get(OUTPUT_DIR.as_posix(), ("    # DATABRICKS_SECTIONS_START", "    # DATABRICKS_SECTIONS_END"))


def _write_index(final_state: OverallState) -> None:
    """Regenerate docs/databricks/index.md with section links after each run."""
    ordered = sorted(final_state["completed_sections"], key=lambda x: x["section_index"])

    toc_lines = []
    for s in ordered:
        toc_lines.append(f"- [{s['section_title']}]({s['filename']})")

    index = (
        f"# {COURSE_TOPIC}\n\n"
        f"**Target audience:** {COURSE_AUDIENCE}\n\n"
        f"---\n\n"
        f"## Course Sections\n\n"
        + "\n".join(toc_lines)
    )

    (OUTPUT_DIR / "index.md").write_text(index, encoding="utf-8")
    print(f"  Saved: {OUTPUT_DIR / 'index.md'}")


def _update_mkdocs_nav(final_state: OverallState) -> None:
    """Replace the section entries between nav markers in mkdocs.yml."""
    ordered = sorted(final_state["completed_sections"], key=lambda x: x["section_index"])

    # Build clean nav entries — number. Title: path
    lines = []
    for s in ordered:
        num = s["section_index"] + 1
        title = s["section_title"]
        # Strip any "Section N:" / "Section N –" prefix the LLM may have added
        title = re.sub(r"^section\s+\d+[\s:\-–]+", "", title, flags=re.IGNORECASE).strip()
        folder = OUTPUT_DIR.as_posix()  # e.g. docs/databricks
        lines.append(f'    - "{num}. {title}": {folder}/{s["filename"]}')

    new_block = "\n".join([NAV_START] + lines + [NAV_END])

    content = MKDOCS_FILE.read_text(encoding="utf-8")
    content = re.sub(
        rf"{re.escape(NAV_START)}.*?{re.escape(NAV_END)}",
        new_block,
        content,
        flags=re.DOTALL,
    )
    MKDOCS_FILE.write_text(content, encoding="utf-8")
    print(f"  Updated: {MKDOCS_FILE} nav ({len(ordered)} sections)")


def save_outputs(final_state: OverallState) -> None:
    # Section files are already saved incrementally by each worker.
    # Save combined doc to output/ (not docs/) to keep it out of the MkDocs sidebar.
    OUTPUT_DIR.mkdir(exist_ok=True)
    archive_dir = Path("output")
    archive_dir.mkdir(exist_ok=True)

    combined_path = archive_dir / "complete_course.md"
    combined_path.write_text(final_state["final_document"], encoding="utf-8")
    print(f"  Saved: {combined_path}")

    _write_index(final_state)
    _update_mkdocs_nav(final_state)


def main() -> None:
    print("=" * 60)
    print(f"Course Generator: {COURSE_TOPIC}")
    print("=" * 60)

    graph = build_graph()

    initial_state: OverallState = {
        "course_topic": COURSE_TOPIC,
        "course_audience": COURSE_AUDIENCE,
        "sections": [],
        "completed_sections": [],
        "final_document": "",
    }

    print("\n[Graph] Starting...\n")

    final_state = graph.invoke(
        initial_state,
        config={"recursion_limit": 100},
    )

    print("\n[Main] Saving output files...")
    save_outputs(final_state)

    sections_count = len(final_state["completed_sections"])
    doc_size = len(final_state["final_document"])
    print(f"\n[Main] Done. {sections_count} sections, {doc_size:,} chars total.")
    print(f"       Output directory: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
