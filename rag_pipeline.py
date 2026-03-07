import os
import sys
from datetime import date
from dotenv import load_dotenv
import torch

load_dotenv()

import chromadb
from groq import Groq
from sentence_transformers import SentenceTransformer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    CHROMA_HOST,
    CHROMA_API_KEY,
    CHROMA_TENANT,
    CHROMA_DATABASE,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    GROQ_API_KEY,
    GROQ_MODEL,
    GROQ_TEMP,
    GROQ_MAX_TOKENS,
    TOP_K
)

# ---------------- SINGLETONS ----------------

_embedder = None
_collection = None
_groq_client = None


# ---------------- EMBEDDER ----------------

def _get_embedder():
    global _embedder

    if _embedder is None:
        print(f"[RAG] Loading embedding model: {EMBEDDING_MODEL}")

        # Force CPU device to avoid meta tensor issue
        _embedder = SentenceTransformer(
            EMBEDDING_MODEL,
            device="cpu"
        )

        # Ensure model is properly moved off meta device
        _embedder._first_module().to(torch.device("cpu"))

        print("[RAG] Embedder ready (CPU)")

    return _embedder


# ---------------- CHROMA ----------------

def _get_collection():
    global _collection

    if _collection is None:

        print("[RAG] Using local Chroma database...")

        client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        _collection = client.get_or_create_collection(
            name=COLLECTION_NAME
        )

        print(f"[RAG] Chroma ready — collection: {COLLECTION_NAME}")

    return _collection


# ---------------- GROQ ----------------

def _get_groq():
    global _groq_client

    if _groq_client is None:

        if not GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY not set! Add it to your .env file.\n"
                "Get free key at: https://console.groq.com"
            )

        _groq_client = Groq(api_key=GROQ_API_KEY)

        print(f"[RAG] Groq ready — model: {GROQ_MODEL}")

    return _groq_client


# ---------------- RETRIEVAL ----------------

def retrieve_chunks(query: str, top_k: int = TOP_K) -> list:

    embedder = _get_embedder()
    collection = _get_collection()

    prefixed_query = f"Represent this sentence for searching relevant passages: {query}"

    q_emb = embedder.encode(
        [prefixed_query],
        convert_to_numpy=True,
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=q_emb,
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    chunks = []

    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):

        chunks.append({
            "text": doc,
            "source": meta.get("source", "Unknown"),
            "relevance": round(1 - dist, 3)
        })

    return chunks


# ---------------- PROMPT ----------------

def build_prompt(accused: str, crimes: str, chunks: list) -> str:

    today = date.today().strftime("%d %B %Y")

    grouped = {}

    for c in chunks:
        grouped.setdefault(c["source"], []).append(c["text"])

    context_parts = []

    for source, texts in grouped.items():

        combined = " ".join(texts)[:1500]

        context_parts.append(f"### [{source}]\n{combined}")

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a senior Indian legal expert and judge with complete knowledge of:

- BNS 2023 (Bharatiya Nyaya Sanhita)
- IPC (Indian Penal Code)
- POCSO Act 2012
- CrPC (Code of Criminal Procedure)
- Constitution of India

TODAY'S DATE: {today}

IMPORTANT:
BNS 2023 applies for crimes committed today (IPC repealed July 2024).
POCSO applies for crimes involving minors.

--- RETRIEVED LEGAL CONTEXT ---
{context}
--- END CONTEXT ---

CASE DETAILS
Accused: {accused}
Crimes: {crimes}

Respond EXACTLY in this format:

## Case: State vs {accused}

Crimes Committed: {crimes}
Date of Crime: {today}

Charges & Sections

| Law | Section | Offence | Punishment |
|-----|--------|--------|------------|
Fill applicable rows

Final Judgment Summary

ACCUSED         : {accused}
CHARGES         : list all charges
MINIMUM SENTENCE: minimum punishment
MAXIMUM SENTENCE: maximum punishment
LIKELY SENTENCE : realistic sentence
TRIED IN        : court name
FINE            : fine details

Key Legal Points

List 5 important legal observations.
"""

    return prompt
