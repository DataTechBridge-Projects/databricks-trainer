import json
import re
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from state import OverallState
from config import MODEL_NAME, OLLAMA_BASE_URL

_llm = ChatOllama(
    model=MODEL_NAME,
    base_url=OLLAMA_BASE_URL,
)

_SYSTEM = """You are a senior technical curriculum designer specializing in cloud data engineering.
Your task is to create a comprehensive, well-structured course outline."""


def supervisor(state: OverallState) -> dict:
    """
    Creates the course outline.
    Returns: {'sections': list[str]}
    """
    user_prompt = f"""Create a Udemy course outline for: "{state['course_topic']}"

Target audience: {state['course_audience']}

REQUIRED sections (must appear, in this order):
1. Course Introduction — what the course covers, how to use it, prerequisites
2. Exam Overview and Strategy — exam format, domains, question types, time management, passing score
3. AWS Setup — IAM, S3, networking, and Databricks workspace provisioning on AWS
4. Databricks Platform — clusters, notebooks, DBFS, Repos, and the Databricks UI
5. Apache Spark on Databricks — architecture, execution model, DataFrames, RDDs (framed for DE exam, NOT ML)
6. Delta Lake Core Concepts — ACID transactions, time travel, schema enforcement, transaction log
7. Medallion Architecture and Lakehouse Pattern — Bronze/Silver/Gold layers, design principles, real-world patterns
8. Data Ingestion with Auto Loader — structured streaming, cloud file source, checkpointing, schema inference
9. Data Transformation and ETL Pipelines — Spark SQL, DLT (Delta Live Tables), batch vs streaming ETL
10. Unity Catalog and Data Governance — metastore, catalogs, schemas, row/column-level security, lineage
11. Workflows and Orchestration — Databricks Jobs, multi-task workflows, cluster policies, scheduling
12. Performance Tuning — partitioning, caching, shuffle tuning, Spark configs, adaptive query execution
13. Advanced Delta Optimization — Z-Ordering, data skipping, OPTIMIZE, VACUUM, liquid clustering
14. Testing, Debugging, and Monitoring — unit testing notebooks, Spark UI, logs, alerts, cost monitoring
15. Capstone and Exam Readiness — end-to-end pipeline review, practice questions, exam day tips

Rules:
- Do NOT include any ML, MLflow, or Feature Engineering sections — this is a Data Engineer cert, not ML
- Keep section titles concise and action/topic oriented
- Return ONLY a valid JSON array of the 15 section title strings. No markdown fences, no explanation."""

    response = _llm.invoke([
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=user_prompt),
    ])

    raw = response.content.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    sections: list[str] = json.loads(raw)

    print(f"\n[Supervisor] Created outline with {len(sections)} sections:")
    for i, s in enumerate(sections):
        print(f"  {i + 1:02d}. {s}")

    return {"sections": sections}
