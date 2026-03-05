# 🏛️ Indian Constitution Legal RAG System

RAG-powered legal advisor using BNS 2023, IPC, POCSO, CrPC & Constitution of India.
Deployed as a single Streamlit app on Streamlit Cloud.

---

## 🏗️ Architecture

```
User Query
    ↓
Streamlit App (streamlit_app.py)
    ↓ calls directly
RAG Pipeline (rag_pipeline.py)
    ├── Embed query → BAAI/bge-small-en-v1.5 (local, 130MB)
    ├── Retrieve chunks → Chroma Cloud ☁️
    └── Generate verdict → Groq llama-3.3-70b (free, 300 tok/sec)
    ↓
Structured Legal Judgment
```

---

## 📁 Project Structure

```
indian-constitution-digitalization/
├── streamlit_app.py      ← Main app (merged, no FastAPI)
├── rag_pipeline.py       ← RAG logic (Chroma Cloud + Groq)
├── config.py             ← All settings
├── ingest.py             ← Run once to push PDFs to Chroma Cloud
├── requirements.txt      ← Dependencies
├── .env.example          ← Copy to .env for local dev
├── .gitignore            ← Protects secrets
└── .streamlit/
    └── secrets.toml      ← Streamlit Cloud secrets (never commit!)
```

---

## 🚀 Local Setup

```bash
# 1. Install
pip install -r requirements.txt

# 2. Create .env
cp .env.example .env
# Fill in your keys

# 3. Place PDFs in data/ folder and ingest (ONE TIME)
python ingest.py

# 4. Run
streamlit run streamlit_app.py
```

---

## ☁️ Deploy to Streamlit Cloud

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/indian-constitution-rag.git
git push -u origin main
```

### Step 2 — Deploy on Streamlit Cloud
1. Go to **https://share.streamlit.io**
2. Click **New app**
3. Select your GitHub repo
4. Set **Main file path** → `streamlit_app.py`
5. Click **Advanced settings → Secrets**
6. Paste your secrets:
```toml
GROQ_API_KEY = "gsk_your_key"
CHROMA_HOST = "api.trychroma.com"
CHROMA_API_KEY = "ck-your_key"
CHROMA_TENANT = "your_tenant_uuid"
CHROMA_DATABASE = "indian_con_digital"
```
7. Click **Deploy!**

Your app will be live at:
`https://yourusername-indian-constitution-rag-streamlit-app-xxxxx.streamlit.app`

---

## ⚠️ Disclaimer
For educational and research purposes only. Not legal advice.
