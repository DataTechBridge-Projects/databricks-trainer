from pathlib import Path
from config import OUTPUT_DIR, COURSE_TOPIC, COURSE_AUDIENCE
from graph import build_graph
from state import OverallState


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
