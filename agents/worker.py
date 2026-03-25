import re
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from state import WorkerState, SectionResult
from config import MODEL_NAME, OLLAMA_BASE_URL, OUTPUT_DIR, NUM_PREDICT

_llm = ChatOllama(
    model=MODEL_NAME,
    base_url=OLLAMA_BASE_URL,
    num_predict=NUM_PREDICT,
)

_SYSTEM = """You are an expert AWS Databricks instructor writing content for a Udemy course.
Your writing style is detailed, precise, and practical — like a well-structured technical book chapter."""


def _safe_filename(index: int, title: str) -> str:
    clean = re.sub(r"^section\s+\d+[:\-\s]+", "", title, flags=re.IGNORECASE)
    safe = re.sub(r"[^\w\s]", "", clean).strip().lower()
    safe = re.sub(r"\s+", "_", safe)[:50]
    return f"section_{index + 1:02d}_{safe}.md"


def worker(state: WorkerState) -> dict:
    """
    Generates full markdown content for one course section.
    Runs in parallel — one instance per section.
    Returns: {'completed_sections': [SectionResult]}
    The list wrapper is required so operator.add can concatenate results.
    """
    user_prompt = f"""Write the complete course content for this section:

Section Title: {state['section']}
Section {state['section_index'] + 1} of {state['total_sections']}
Course: {state['course_topic']}
Target Audience: {state['course_audience']}

Your content MUST include ALL of the following components, clearly labeled with markdown headings:

## {state['section']}

### Overview
[3-4 paragraphs of deep conceptual explanation written like a technical book]

### Core Concepts
[Detailed explanation of each concept with sub-sections as needed]

### Architecture / How It Works
[At least one ASCII diagram or mermaid diagram in a code block illustrating architecture or data flow.
Example:
```
+-------------------+       +------------------+       +-------------+
|   Raw S3 Bucket   |  -->  |   Auto Loader    |  -->  |  Delta Lake |
+-------------------+       +------------------+       +-------------+
```
]

### Hands-On: Key Operations
[Step-by-step PySpark / Python / SQL code examples with explanation of each block]

### AWS-Specific Considerations
[How this topic integrates with AWS: S3, IAM, Glue, EMR, Lake Formation, CloudWatch, etc.]

### Exam Focus Areas
[Bulleted list of what the Databricks Data Engineer Associate exam tests on this topic]

### Quick Recap
- [Key takeaway 1]
- [Key takeaway 2]
- [Key takeaway 3]
- [Key takeaway 4]
- [Key takeaway 5]

### Code References
[Links to official Databricks docs, Apache Spark docs, and relevant GitHub examples]

### Blog & Further Reading
[3-5 recommended articles or documentation pages with a one-line description each]

Be exhaustive. A presenter should be able to speak for 45-60 minutes using only this section."""

    response = _llm.invoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=user_prompt),
    ])

    content = response.content
    filename = _safe_filename(state["section_index"], state["section"])

    # Write to disk immediately — don't wait for the full graph to finish
    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / filename).write_text(content, encoding="utf-8")

    print(f"[Worker] Saved: section {state['section_index'] + 1} — {state['section']} ({len(content):,} chars) → output/{filename}")

    result: SectionResult = {
        "section_index": state["section_index"],
        "section_title": state["section"],
        "filename": filename,
        "content": content,
    }

    return {"completed_sections": [result]}
