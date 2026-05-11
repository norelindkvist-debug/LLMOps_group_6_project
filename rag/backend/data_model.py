from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry
from rag.backend.constants import EMBEDDING_MODEL
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

embedding_model = get_registry().get("cohere").create(name=EMBEDDING_MODEL)


class Article(LanceModel):
    document_name: str
    filename: str
    content: str = embedding_model.SourceField()
    embedding: Vector(embedding_model.ndims()) = embedding_model.VectorField()


class Prompt(BaseModel):
    prompt: str = Field(
        description="prompt from user, if empty consider prompt as missing"
    )


class RagResponse(BaseModel):
    filename: str | None = Field(
        default=None,
        description="filename of retrieved file"
    )
    answer: str = Field(
        description="answer based on retrieved file, concise but capture essential meaning"
    )