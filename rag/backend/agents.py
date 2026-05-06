from pydantic_ai import Agent
from rag.backend.constants import VECTOR_DB_PATH, MODEL
import lancedb
from rag.backend.data_model import RagResponse

from dotenv import load_dotenv 

load_dotenv()

vector_db = lancedb.connect(uri=VECTOR_DB_PATH)

rag_agent = Agent(
    model=MODEL,
    output_type=RagResponse,

    system_prompt="""
You are an employee at CSN that handles all of their data and information. You help customers with questions about CSN.
## Tone & Style
- Friendly, encouraging, helpful, and easy to understand
- Get straight to the point

## Answering Rules
- ALWAYS base your answer on retrieved documents
- If the question is outside the retrieved knowledge, say: "I don't have information about that, try asking about [topic]!"
- Never make up facts — honesty builds trust with young readers

## Off-topic Questions
- If the question is unrelated to CSN, loan, money, studdies, school, politely decline WITHOUT calling any tools
- Example: "That's outside my expertise! I'm here to help with questions about CSN"

## Response Format
- Answer the question
- End with: "📄 Source: [filename]"
""",
)


@rag_agent.tool_plain
def retrieve_top_documents(query: str, k: int = 3):
    """retrieves documents from knowledge base"""
    results = vector_db["articles"].search(query=query).limit(k).to_list()

    return f"""
    Filename: {results[0].get("document_name", "not found")},

    Content: {results[0].get("content", "not found")}
    """


async def bot_answer(question: str):
    result = await rag_agent.run(question)
    return result.output
