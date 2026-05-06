from pathlib import Path

ROOT_PATH = Path(__file__).parents[1]
DATA_PATH = ROOT_PATH / "data"
VECTOR_DB_PATH = ROOT_PATH / "knowledge_base"
EMBEDDING_MODEL = "embed-multilingual-light-v3.0"
MODEL = "openrouter:nvidia/nemotron-3-nano-30b-a3b:free"
LLM_JUDGE = "openrouter:/nvidia/nemotron-3-nano-30b-a3b:free"
EXPERIMENT_NAME = "CSN-chatbot"