import os
from dotenv import load_dotenv

load_dotenv()

# Groq API 
GROQ_API_KEY    = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL      = "llama-3.3-70b-versatile"
GROQ_TEMP       = 0.1
GROQ_MAX_TOKENS = 1500

#  Chroma Cloud 
CHROMA_HOST     = os.environ.get("CHROMA_HOST", "api.trychroma.com")
CHROMA_API_KEY  = os.environ.get("CHROMA_API_KEY", "")
CHROMA_TENANT   = os.environ.get("CHROMA_TENANT", "")
CHROMA_DATABASE = os.environ.get("CHROMA_DATABASE", "indian_con_digital")

#  Collection 
COLLECTION_NAME = "indian_legal_docs"

#  Embedding model
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

# RAG settings 
CHUNK_SIZE    = 400
CHUNK_OVERLAP = 60
TOP_K         = 8

#  Data directory (for ingest.py) 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

DOCUMENTS = [
    {"path": os.path.join(DATA_DIR, "Indian Constitution.pdf"), "source": "Indian Constitution 2023"},
    {"path": os.path.join(DATA_DIR, "BNS.pdf"),                 "source": "BNS 2023 (Bharatiya Nyaya Sanhita)"},
    {"path": os.path.join(DATA_DIR, "IPC.pdf"),                 "source": "IPC (Indian Penal Code)"},
    {"path": os.path.join(DATA_DIR, "CRPC.pdf"),                "source": "CrPC (Criminal Procedure Code)"},
    {"path": os.path.join(DATA_DIR, "pocso.pdf"),               "source": "POCSO Act 2012"},
]
