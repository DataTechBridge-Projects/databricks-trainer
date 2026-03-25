# Setup

## Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com) running locally with your model pulled

## Install dependencies

```bash
pip install -r requirements.txt
```

## Pull the model

```bash
ollama pull nemotron-cascade-2
```

Verify Ollama is running:
```bash
curl http://localhost:11434/api/tags
```

## Configure

Edit `config.py`:

```python
MODEL_NAME = "nemotron-cascade-2"      # your Ollama model
OLLAMA_BASE_URL = "http://localhost:11434"
NUM_PREDICT = 4096                     # max tokens per section — lower = faster

COURSE_TOPIC = "AWS Databricks Data Engineer Certification"
COURSE_AUDIENCE = "data engineers familiar with Apache Spark and AWS Glue..."
```

## Run

```bash
python main.py
```

Output is written to `docs/course/` — one markdown file per section, plus `complete_course.md`.

## Tuning speed vs. depth

| `NUM_PREDICT` | Output depth | Approx. time per section |
|---|---|---|
| `2048` | Concise | Faster |
| `4096` | Detailed (default) | Moderate |
| `8192` | Exhaustive | Slower |
