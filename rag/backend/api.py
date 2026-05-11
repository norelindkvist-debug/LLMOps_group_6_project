from fastapi import FastAPI
from rag.backend.data_model import Prompt, RagResponse
from rag.backend.agents import bot_answer

app = FastAPI()

@app.post("/rag/query", response_model=RagResponse)
async def query_documentation(query: Prompt) -> RagResponse:
    result = await bot_answer(query.prompt)
    return result