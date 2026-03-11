import os
import sys
from datetime import date
from dotenv import load_dotenv
import torch
#import chromadb
from groq import Groq
from sentence_transformers import SentenceTransformer
import requests

load_dotenv()

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

        _embedder = SentenceTransformer(
            EMBEDDING_MODEL,
            device="cpu"
        )

        _embedder._first_module().to(torch.device("cpu"))

        print("[RAG] Embedder ready (CPU)")

    return _embedder


# ---------------- CHROMA CLOUD ----------------
'''
def _get_collection():
    global _collection

    if _collection is None:

        print("[RAG] Connecting to Chroma Cloud...")

        client = chromadb.CloudClient(
            tenant=CHROMA_TENANT,
            database=CHROMA_DATABASE,
            api_key=CHROMA_API_KEY
        )

        _collection = client.get_collection(name=COLLECTION_NAME)

        print(f"[RAG] Chroma Cloud ready — collection: {COLLECTION_NAME}")

    return _collection
'''
def _query_chroma(query_embedding: list, top_k: int) -> dict:

    headers = {
        "x-chroma-token": CHROMA_API_KEY,
        "Content-Type": "application/json"
    }

    base_url = f"https://{CHROMA_HOST}/api/v2"

    # Get collection ID
    col_resp = requests.get(
        f"{base_url}/tenants/{CHROMA_TENANT}/databases/{CHROMA_DATABASE}/collections/{COLLECTION_NAME}",
        headers=headers
    )

    print(f"[DEBUG] Collection status: {col_resp.status_code}")
    print(f"[DEBUG] Collection response: {col_resp.text}")

    col_data = col_resp.json()

    if "id" not in col_data:
        raise ValueError(f"Chroma collection error: {col_data}")

    collection_id = col_data["id"]

    # Query
    query_resp = requests.post(
        f"{base_url}/tenants/{CHROMA_TENANT}/databases/{CHROMA_DATABASE}/collections/{collection_id}/query",
        headers=headers,
        json={
            "query_embeddings": [query_embedding],
            "n_results": top_k,
            "include": ["documents", "metadatas", "distances"]
        }
    )

    return query_resp.json()
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
'''
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

'''
def retrieve_chunks(query: str, top_k: int = TOP_K) -> list:

    embedder = _get_embedder()

    prefixed_query = f"Represent this sentence for searching relevant passages: {query}"

    q_emb = embedder.encode(
        [prefixed_query],
        convert_to_numpy=True,
        normalize_embeddings=True
    ).tolist()[0]  # single vector

    results = _query_chroma(q_emb, top_k)

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


# ---------------- GENERATION ----------------

def generate_verdict(prompt: str) -> str:

    client = _get_groq()

    print(f"[RAG] Sending to Groq ({GROQ_MODEL})...")

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert Indian legal advisor. "
                    "Always give complete structured legal analysis "
                    "with exact BNS 2023, IPC, and POCSO section numbers. "
                    "Never truncate. Always complete the full judgment."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=GROQ_TEMP,
        max_tokens=GROQ_MAX_TOKENS,
    )

    verdict = response.choices[0].message.content.strip()
    usage = response.usage
    print(f"[RAG] Done — tokens: {usage.total_tokens}")

    return verdict


# ---------------- MAIN FUNCTION ----------------

def analyze_case(accused: str, crimes: str) -> dict:

    query = f"Indian law punishment sections for: {crimes}. BNS IPC POCSO imprisonment death penalty"

    chunks = retrieve_chunks(query)

    print(f"[RAG] Retrieved {len(chunks)} chunks from: {set(c['source'] for c in chunks)}")

    prompt = build_prompt(accused, crimes, chunks)
    verdict = generate_verdict(prompt)

    return {
        "accused":  accused,
        "crimes":   crimes,
        "judgment": verdict,
        "sources":  [
            {
                "source":    c["source"],
                "text":      c["text"][:400] + "...",
                "relevance": c["relevance"]
            }
            for c in chunks
        ]
    }
