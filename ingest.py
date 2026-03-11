"""
ingest.py — One-time script to ingest all 5 PDFs into Chroma Cloud.
"""

import os
import sys
import uuid
import pdfplumber
import chromadb
from chromadb.auth.token_authn import TokenAuthClientProvider
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import (
    CHROMA_HOST, CHROMA_API_KEY, CHROMA_TENANT, CHROMA_DATABASE,
    COLLECTION_NAME, EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, DOCUMENTS
)


# PDF Extraction 

def extract_text_from_pdf(path: str) -> list:
    pages = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text and text.strip():
                    pages.append(text.strip())
    except Exception as e:
        print(f"Error reading {path}: {e}")
    return pages


# Chunking

def chunk_pages(pages: list, chunk_size: int, overlap: int) -> list:
    all_words = []
    for page in pages:
        all_words.extend(page.split())

    chunks = []
    step = chunk_size - overlap
    for i in range(0, len(all_words), step):
        chunk_words = all_words[i: i + chunk_size]
        if len(chunk_words) < 20:
            continue
        chunks.append(" ".join(chunk_words))
    return chunks


# Main Ingestion 

def ingest():
    print("\n" + "=" * 60)
    print("Indian Legal RAG — Chroma Cloud Ingestion")
    print("=" * 60)

    # Load embedding model
    print(f"\nLoading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)
    print("Embedding model loaded.")

    # Connect to Chroma Cloud
    print(f"\nConnecting to Chroma Cloud...")
    client = chromadb.CloudClient(
    tenant=CHROMA_TENANT,
    database=CHROMA_DATABASE,
    api_key=CHROMA_API_KEY
    )
    print("Connected to Chroma Cloud.")

    # Delete existing collection if re-running
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"\nOld collection deleted.")
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
    print(f"Collection '{COLLECTION_NAME}' created in Chroma Cloud.\n")

    total_chunks = 0

    for doc in DOCUMENTS:
        path   = doc["path"]
        source = doc["source"]
        name   = os.path.basename(path)

        if not os.path.exists(path):
            print(f"File not found, skipping: {path}")
            continue

        print(f"Processing: {name}  [{source}]")

        pages  = extract_text_from_pdf(path)
        print(f"   Pages extracted : {len(pages)}")

        chunks = chunk_pages(pages, CHUNK_SIZE, CHUNK_OVERLAP)
        print(f"   Chunks created  : {len(chunks)}")

        if not chunks:
            print(f"No usable text found, skipping.")
            continue

        print(f"   Embedding chunks...", end="", flush=True)
        embeddings = model.encode(
            chunks,
            batch_size=32,
            show_progress_bar=False,
            convert_to_numpy=True
        ).tolist()
        print(" done.")

        ids       = [str(uuid.uuid4()) for _ in chunks]
        metadatas = [{"source": source, "doc": name} for _ in chunks]

        # Store in batches of 100 (Chroma Cloud limit)
        batch_size = 100
        for start in range(0, len(chunks), batch_size):
            collection.add(
                documents  = chunks[start: start + batch_size],
                embeddings = embeddings[start: start + batch_size],
                ids        = ids[start: start + batch_size],
                metadatas  = metadatas[start: start + batch_size],
            )

        total_chunks += len(chunks)
        print(f"Stored {len(chunks)} chunks → Chroma Cloud [{source}]\n")

    print("=" * 60)
    print(f"Ingestion complete! Total chunks in cloud: {total_chunks}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    ingest()
