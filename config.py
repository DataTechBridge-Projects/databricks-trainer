from pathlib import Path

# Model — local Ollama
MODEL_NAME = "nemotron-cascade-2"
OLLAMA_BASE_URL = "http://localhost:11434"
NUM_PREDICT = 4096   # max tokens per worker response; increase for deeper content, decrease to speed up

# Paths
OUTPUT_DIR = Path("output")

# Course metadata
COURSE_TOPIC = "AWS Databricks Data Engineer Certification"
COURSE_AUDIENCE = (
    "data engineers familiar with Apache Spark and AWS Glue who want to "
    "prepare for the Databricks Certified Data Engineer Associate exam on AWS"
)
