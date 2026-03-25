from pathlib import Path

# Model — local Ollama
MODEL_NAME = "nemotron-cascade-2"
OLLAMA_BASE_URL = "http://localhost:11434"
NUM_PREDICT = 4096   # max tokens per worker response; increase for deeper content, decrease to speed up

# ── Active course ──────────────────────────────────────────────────────────────
# Switch between courses by changing these three lines.
# Each course has its own prompt file under prompts/ and output folder under docs/
# ──────────────────────────────────────────────────────────────────────────────

# PROMPT_MODULE = "prompts.databricks"           # prompts.databricks | prompts.aws_data_engineer
# OUTPUT_DIR    = Path("docs/databricks")        # docs/databricks    | docs/aws

# COURSE_TOPIC    = "AWS Databricks Data Engineer Certification"
# COURSE_AUDIENCE = (
#     "data engineers familiar with Apache Spark and AWS Glue who want to "
#     "prepare for the Databricks Certified Data Engineer Associate exam on AWS"
# )

# ── AWS Data Engineer course (uncomment to switch) ────────────────────────────
PROMPT_MODULE   = "prompts.aws_data_engineer"
OUTPUT_DIR      = Path("docs/aws")
COURSE_TOPIC    = "AWS Certified Data Engineer Associate (DEA-C01)"
COURSE_AUDIENCE = (
    "cloud engineers and developers familiar with AWS core services who want to "
    "pass the AWS Certified Data Engineer Associate exam"
)
