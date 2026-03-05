"""
streamlit_app.py — Merged Indian Legal RAG System
No FastAPI needed — calls rag_pipeline directly.
Deploy on Streamlit Cloud as a single file.
"""

import streamlit as st
from datetime import date
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Page Config 

st.set_page_config(
    page_title="Indian Legal AI Advisor",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=Source+Serif+4:ital,wght@0,300;0,400;0,600;1,300&family=JetBrains+Mono:wght@400;500&display=swap');

    .stApp { background: #0a0e1a; font-family: 'Source Serif 4', serif; }
    .stApp > header { background: transparent; }
    .stApp, .stApp p, .stApp div, .stApp span, .stApp li { color: #f0e6d3 !important; }

    [data-testid="stSidebar"] { background: #060912; border-right: 1px solid #c9a84c33; }
    [data-testid="stSidebar"] * { color: #d4b896 !important; }

    .hero-header { text-align: center; padding: 2.5rem 0 1.5rem; border-bottom: 1px solid #c9a84c44; margin-bottom: 2rem; }
    .hero-title { font-family: 'Playfair Display', serif; font-size: 3rem; font-weight: 900; color: #c9a84c; letter-spacing: 0.02em; margin: 0; line-height: 1.1; text-shadow: 0 0 40px #c9a84c44; }
    .hero-subtitle { font-family: 'Source Serif 4', serif; font-style: italic; font-size: 1.05rem; color: #aabbcc; margin-top: 0.5rem; }
    .hero-badge { display: inline-block; margin-top: 1rem; padding: 0.25rem 1.2rem; border: 1px solid #c9a84c66; border-radius: 2px; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #c9a84c; letter-spacing: 0.15em; text-transform: uppercase; }

    .input-label { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; letter-spacing: 0.12em; text-transform: uppercase; color: #c9a84c; margin-bottom: 0.5rem; }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #060912 !important; border: 1px solid #c9a84c44 !important;
        border-radius: 3px !important; color: #ffffff !important;
        font-family: 'Source Serif 4', serif !important; font-size: 1rem !important;
    }

    .stButton > button {
        width: 100%; background: linear-gradient(135deg, #c9a84c, #a8832a) !important;
        color: #0a0e1a !important; font-family: 'Playfair Display', serif !important;
        font-weight: 700 !important; font-size: 1.05rem !important;
        border: none !important; border-radius: 3px !important;
        padding: 0.75rem 2rem !important; transition: all 0.2s !important;
    }
    .stButton > button:hover { background: linear-gradient(135deg, #e0bc5e, #c9a84c) !important; }

    .judgment-container { background: #0c1120; border: 1px solid #c9a84c33; border-top: 3px solid #c9a84c; border-radius: 4px; padding: 2rem 2.5rem; margin-top: 1.5rem; }
    .judgment-header { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; letter-spacing: 0.15em; text-transform: uppercase; color: #c9a84c; padding-bottom: 1rem; border-bottom: 1px solid #c9a84c22; margin-bottom: 1.5rem; }

    .stMarkdown p { color: #f0e6d3 !important; font-size: 1rem !important; line-height: 1.8 !important; }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #c9a84c !important; font-family: 'Playfair Display', serif !important; }
    .stMarkdown li { color: #f0e6d3 !important; line-height: 1.8 !important; }
    .stMarkdown strong { color: #ffffff !important; font-weight: 700 !important; }
    .stMarkdown code { background: #1a2035 !important; color: #98d8a8 !important; padding: 0.2rem 0.4rem !important; border-radius: 3px !important; }
    .stMarkdown pre { background: #060912 !important; border: 1px solid #c9a84c22 !important; border-radius: 3px !important; padding: 1rem !important; }
    .stMarkdown pre code { color: #98d8a8 !important; }
    .stMarkdown table { width: 100% !important; border-collapse: collapse !important; margin: 1rem 0 !important; }
    .stMarkdown th { background: #1a2035 !important; color: #c9a84c !important; padding: 0.6rem 1rem !important; text-align: left !important; border: 1px solid #c9a84c33 !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.8rem !important; }
    .stMarkdown td { padding: 0.6rem 1rem !important; border: 1px solid #c9a84c22 !important; color: #f0e6d3 !important; font-size: 0.95rem !important; }
    .stMarkdown tr:nth-child(even) td { background: #0f1526 !important; }
    .stMarkdown tr:nth-child(odd) td { background: #0a0e1a !important; }

    .source-chip { display: inline-block; background: #1a2035; border: 1px solid #c9a84c33; border-radius: 2px; padding: 0.2rem 0.7rem; font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #c9a84c; letter-spacing: 0.08em; margin: 0.2rem; }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# Sidebar 
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1.5rem 0 1rem;">
        <div style="font-size: 3rem;">⚖️</div>
        <div style="font-family:'Playfair Display',serif; font-size:1.2rem; color:#c9a84c; font-weight:700;">
            Legal RAG System
        </div>
        <div style="font-size:0.7rem; color:#556; letter-spacing:0.1em; margin-top:0.3rem;">
            POWERED BY BNS 2023 + POCSO + IPC
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="font-family:JetBrains Mono,monospace; font-size:0.65rem; letter-spacing:0.12em; text-transform:uppercase; color:#c9a84c; margin-bottom:0.5rem;">📚 Ingested Documents</div>', unsafe_allow_html=True)

    docs = [
        ("🏛️", "Indian Constitution 2023", "402 pages"),
        ("📖", "BNS 2023",                  "102 pages — Replaces IPC"),
        ("📜", "IPC",                        "119 pages — Legacy reference"),
        ("👶", "POCSO Act 2012",             "17 pages — Child protection"),
        ("⚖️", "CrPC",                       "119 pages — Procedure"),
    ]
    for icon, name, detail in docs:
        st.markdown(f"""
        <div style="background:#0f1526; border:1px solid #c9a84c22; border-radius:4px; padding:0.8rem; margin-bottom:0.5rem;">
            <span style="font-size:1rem;">{icon}</span>
            <span style="color:#c9d4c0; font-weight:600;"> {name}</span><br>
            <span style="color:#667; font-size:0.78rem;">{detail}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#445; text-align:center;">
        Today: {date.today().strftime("%d %B %Y")}<br>
        BNS 2023 ACTIVE · IPC REPEALED<br><br>
        LLM: llama-3.3-70b via Groq<br>
        Embeddings: BAAI/bge-small-en-v1.5<br>
        Vector DB: Chroma Cloud 
    </div>
    """, unsafe_allow_html=True)


#Hero 

st.markdown("""
<div class="hero-header">
    <div class="hero-title">Indian Legal AI Advisor</div>
    <div class="hero-subtitle">Powered by BNS 2023 · IPC · POCSO · CrPC · Constitution of India</div>
    <div class="hero-badge">RAG • Retrieval Augmented Generation • Legal Intelligence</div>
</div>
""", unsafe_allow_html=True)


#Input 

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="input-label">Name of Accused</div>', unsafe_allow_html=True)
    accused_input = st.text_input(
        label="accused", placeholder="e.g., Tunny",
        label_visibility="collapsed", key="accused"
    )

with col2:
    st.markdown('<div class="input-label">Crimes Committed</div>', unsafe_allow_html=True)
    crimes_input = st.text_area(
        label="crimes",
        placeholder="e.g., Rape of a minor girl child and murder of the victim",
        height=80, label_visibility="collapsed", key="crimes"
    )

# Quick examples
st.markdown('<div style="margin: 0.5rem 0 0.2rem; font-family:JetBrains Mono,monospace; font-size:0.65rem; letter-spacing:0.1em; color:#556; text-transform:uppercase;">Quick Examples →</div>', unsafe_allow_html=True)

examples = [
    ("Murder",               "Intentional murder of a person"),
    ("Rape + Murder",        "Rape of a minor girl child and murder"),
    ("Kidnapping + Rape",    "Kidnapping and rape of an adult woman"),
    ("Child Sexual Assault", "Sexual assault on a 10-year-old child"),
    ("Robbery + Murder",     "Armed robbery and murder of shopkeeper"),
]

ex_cols = st.columns(len(examples))
for i, (label, crime_text) in enumerate(examples):
    with ex_cols[i]:
        if st.button(label, key=f"ex_{i}", use_container_width=True):
            st.session_state["crimes"]  = crime_text
            st.session_state["accused"] = "Accused"
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    analyze_btn = st.button("Analyze Case Under Indian Law", type="primary")


# Analysis 

if analyze_btn:
    accused = st.session_state.get("accused", accused_input).strip()
    crimes  = st.session_state.get("crimes",  crimes_input).strip()

    if not accused:
        st.warning("Please enter the accused's name.")
    elif not crimes:
        st.warning("Please describe the crimes committed.")
    else:
        with st.spinner("Retrieving legal sections from Chroma Cloud and analyzing..."):
            try:
                from rag_pipeline import analyze_case
                result = analyze_case(accused=accused, crimes=crimes)

                # Judgment
                st.markdown("""
                <div class="judgment-container">
                    <div class="judgment-header">
                        LEGAL JUDGMENT &nbsp;|&nbsp; INDIAN COURT ANALYSIS &nbsp;|&nbsp; GENERATED BY RAG SYSTEM
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(result["judgment"])

                # Sources
                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander("View Retrieved Legal Sections", expanded=False):
                    for src in result.get("sources", []):
                        st.markdown(f"""
                        <div style="background:#0c1120; border:1px solid #c9a84c22; border-radius:3px; padding:1rem; margin-bottom:0.6rem;">
                            <span class="source-chip">{src['source']}</span>
                            <span style="font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#667; margin-left:1rem;">
                                relevance: {src['relevance']:.3f}
                            </span>
                            <div style="font-size:0.85rem; color:#aabbcc; margin-top:0.5rem; line-height:1.6;">
                                {src['text'][:500]}...
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            except ValueError as e:
                st.error(f"Configuration Error: {str(e)}")
            except Exception as e:
                st.error(f"Error: {str(e)}")


# Footer 

st.markdown("---")
st.markdown("""
<div style="text-align:center; font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#334; padding:1rem 0;">
    BUILT WITH: CHROMA CLOUD · BAAI/bge-small · GROQ LLAMA-3.3-70B · STREAMLIT
</div>
""", unsafe_allow_html=True)
