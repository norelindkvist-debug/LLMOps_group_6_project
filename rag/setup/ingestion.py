import lancedb
from rag.backend.data_model import Article
from rag.backend.constants import DATA_PATH, VECTOR_DB_PATH

def setup_vector_db(path):
    vector_db = lancedb.connect(uri=path)
    vector_db.create_table("articles", schema=Article, exist_ok=True)

    return vector_db

def ingest_docs_to_vector_db(table):
    for file in DATA_PATH.glob("*.md"):
        with open(file) as f:
            content = f.read()

        document_name = file.name
        table.delete(f"document_name = '{document_name}'")

        table.add([{
            "document_name": document_name,
            "filename": str(file),
            "content": content
        }])

        print(table.to_pandas()["document_name"])

if __name__ == "__main__":
    vector_db = setup_vector_db(VECTOR_DB_PATH)
    ingest_docs_to_vector_db(vector_db["articles"])