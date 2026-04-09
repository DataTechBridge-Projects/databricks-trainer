"""
All course definitions in one place.
Each entry contains course metadata only — topic, audience, and output directory.
All LLM prompts are loaded from prompts/common.json and are shared across courses.

To add a new course, add a new key here and add the matching nav markers to mkdocs.yml.
"""

import json
from pathlib import Path

_ROOT = Path(__file__).parent
_PROMPTS = json.loads((_ROOT / "prompts" / "common.json").read_text(encoding="utf-8"))


def _course(output_dir: str, topic: str, audience: str) -> dict:
    return {"output_dir": _ROOT / output_dir, "topic": topic, "audience": audience, **_PROMPTS}


COURSES: dict[str, dict] = {

    # ── Databricks Data Engineer ──────────────────────────────────────────────
    "databricks": _course(
        output_dir="docs/databricks",
        topic="AWS Databricks Data Engineer Certification",
        audience=(
            "data engineers familiar with Apache Spark and AWS Glue who want to "
            "prepare for the Databricks Certified Data Engineer Associate exam on AWS"
        ),
    ),

    # ── AWS SA Enablement (100-level, full AWS portfolio, pre-sales focused) ────
    "aws-sa": _course(
        output_dir="docs/aws-sa",
        topic="AWS — Pre-Sales SA Enablement (Full Portfolio)",
        audience=(
            "pre-sales Solution Architects with a general IT background who need to hold "
            "credible customer conversations across the full AWS portfolio — compute, storage, "
            "networking, databases, security, analytics, AI/ML and more — no hands-on "
            "engineering depth required"
        ),
    ),

    # ── AWS Data Engineer ─────────────────────────────────────────────────────
    "aws": _course(
        output_dir="docs/aws",
        topic="AWS Certified Data Engineer Associate (DEA-C01)",
        audience=(
            "cloud engineers and developers familiar with AWS core services who want to "
            "pass the AWS Certified Data Engineer Associate exam"
        ),
    ),

    # ── Azure Data Engineer ───────────────────────────────────────────────────
    "azure": _course(
        output_dir="docs/azure",
        topic="Azure Data Engineer Associate (DP-203)",
        audience=(
            "data engineers familiar with SQL and cloud fundamentals who want to "
            "pass the Microsoft Azure Data Engineer Associate DP-203 exam"
        ),
    ),
}
