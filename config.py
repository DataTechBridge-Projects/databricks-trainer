# Model — local Ollama
MODEL_NAME      = "gemma4:26b" #"nemotron-cascade-2"
OLLAMA_BASE_URL = "http://localhost:11434"
NUM_PREDICT     =  -1   # max tokens per worker response; -1 = unlimited


def make_llm(**kwargs):
    """Return a ChatOllama instance with project-wide defaults. Pass kwargs to override."""
    from langchain_ollama import ChatOllama
    return ChatOllama(model=MODEL_NAME, base_url=OLLAMA_BASE_URL, **kwargs)

# Max parallel workers hitting Ollama simultaneously.
# Large local models (26B+) should use 1-2; smaller models can go up to 4.
MAX_WORKERS     = 1

# Default course when no --course arg is passed
ACTIVE_COURSE = "aws"
