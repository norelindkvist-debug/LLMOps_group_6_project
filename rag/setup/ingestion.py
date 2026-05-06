import os
from pathlib import Path
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from rag.backend.constants import DATA_PATH, 

# Path to the data folder

CHROMA_DIR = Path(__file__).parent.parent / "chroma_db"

def load_and_parse_files():
    documents = []
    for file in DATA_PATH.glob("*"):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(content, "html.parser")
        
        # Remove scripts and navigation
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        
        text = soup.get_text(separator=" ", strip=True)
        
        if text:
            documents.append({"text": text, "source": file.name})
    
    print(f"Loaded {len(documents)} files")
    return documents

def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    
    chunks = []
    for doc in documents:
        splits = splitter.split_text(doc["text"])
        for split in splits:
            chunks.append({"text": split, "source": doc["source"]})
    
    print(f"Created {len(chunks)} chunks")
    return chunks

def store_in_chroma(chunks):
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    
    texts = [c["text"] for c in chunks]
    metadatas = [{"source": c["source"]} for c in chunks]
    
    vectorstore = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=str(CHROMA_DIR)
    )
    
    print(f"Stored {len(texts)} chunks in ChromaDB")
    return vectorstore

if __name__ == "__main__":
    documents = load_and_parse_files()
    chunks = chunk_documents(documents)
    store_in_chroma(chunks)
    print("Ingestion complete!")