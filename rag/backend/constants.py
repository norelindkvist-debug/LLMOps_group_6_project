from pathlib import Path

ROOT_PATH = Path(__file__).parents[1]
DATA_PATH = ROOT_PATH / "data"
VECTOR_DB_PATH = ROOT_PATH / "knowledge_base"
EMBEDDING_MODEL = "embed-multilingual-light-v3.0"
MODEL = "openrouter:openai/gpt-oss-120b:free"
LLM_JUDGE = "openrouter:/liquid/lfm-2.5-1.2b-instruct:free"
EXPERIMENT_NAME = "CSN-chatbot"