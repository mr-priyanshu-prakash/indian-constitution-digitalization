"""
streamlit_app.py — Indian Legal RAG System
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

# ---------------- CSS ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Serif+4:wght@300;400;600&family=JetBrains+Mono:wght@400;500&display=swap');

.stApp { background: #0a0e1a; font-family: 'Source Serif 4', serif; }

.stApp, .stApp p, .stApp div, .stApp span { color: #f0e6d3 !important; }

[data-testid="stSidebar"] {
background: #060912;
border-right: 1px solid #c9a84c33;
}
.stMarkdown pre {
    background: #0c1120 !important;
    border: 1px solid #c9a84c33 !important;
    border-radius: 4px !important;
    padding: 1rem !important;
}

.stMarkdown pre code {
    color: #f0e6d3 !important;
    background: transparent !important;
}

code {
    background: #1a2035 !important;
    color: #98d8a8 !important;
    padding: 0.2rem 0.4rem !important;
    border-radius: 3px !important;
}
.hero-header {
text-align:center;
padding:2.5rem 0 1.5rem;
border-bottom:1px solid #c9a84c44;
margin-bottom:2rem;
}

.hero-title{
font-family:'Playfair Display',serif;
font-size:3rem;
font-weight:900;
color:#c9a84c;
}

.hero-subtitle{
font-style:italic;
color:#aabbcc;
}

.hero-badge{
display:inline-block;
margin-top:1rem;
padding:0.3rem 1.2rem;
border:1px solid #c9a84c66;
font-family:'JetBrains Mono';
font-size:0.7rem;
color:#c9a84c;
}

.input-label{
font-family:'JetBrains Mono';
font-size:0.72rem;
letter-spacing:0.12em;
text-transform:uppercase;
color:#c9a84c;
}

.stTextInput input, .stTextArea textarea{
background:#060912 !important;
border:1px solid #c9a84c44 !important;
color:white !important;
}

.stButton > button{
width:100%;
background:linear-gradient(135deg,#c9a84c,#a8832a);
color:#0a0e1a;
font-weight:700;
font-size:1.05rem;
border:none;
padding:0.75rem;
}

.judgment-container{
background:#0c1120;
border:1px solid #c9a84c33;
border-top:3px solid #c9a84c;
padding:2rem;
margin-top:1.5rem;
}

.source-chip{
background:#1a2035;
border:1px solid #c9a84c33;
padding:0.2rem 0.7rem;
font-family:'JetBrains Mono';
font-size:0.68rem;
color:#c9a84c;
}

#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("""
    <div style="text-align:center">
    <div style="font-size:3rem;">⚖️</div>
    <div style="font-size:1.2rem;color:#c9a84c;font-weight:700">
    Legal RAG System
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📚 Ingested Documents")

    docs = [
        "Indian Constitution 2023",
        "BNS 2023",
        "IPC",
        "POCSO Act",
        "CrPC"
    ]

    for d in docs:
        st.markdown(f"• {d}")

    st.markdown("---")

    st.markdown(f"""
    Today: {date.today().strftime("%d %B %Y")}

    BNS 2023 ACTIVE  
    IPC REPEALED
    """)

# ---------------- HERO ----------------

st.markdown("""
<div class="hero-header">

<div class="hero-title">
Indian Legal AI Advisor
</div>

<div class="hero-subtitle">
Powered by BNS 2023 · IPC · POCSO · CrPC · Constitution of India
</div>

<div class="hero-badge">
RAG • Retrieval Augmented Generation • Legal Intelligence
</div>

</div>
""", unsafe_allow_html=True)

# ---------------- INPUT ----------------

col1, col2 = st.columns([1,2])

with col1:

    st.markdown('<div class="input-label">Name of Accused</div>', unsafe_allow_html=True)

    accused_input = st.text_input(
        label="accused",
        placeholder="Enter accused name",
        label_visibility="collapsed",
        key="accused"
    )

with col2:

    st.markdown('<div class="input-label">Crimes Committed</div>', unsafe_allow_html=True)

    crimes_input = st.text_area(
        label="crimes",
        placeholder="Describe the crime committed",
        height=80,
        label_visibility="collapsed",
        key="crimes"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Analyze button
_, btn_col, _ = st.columns([1,2,1])

with btn_col:
    analyze_btn = st.button("Analyze Case Under Indian Law")

# ---------------- ANALYSIS ----------------

if analyze_btn:

    accused = st.session_state.get("accused", accused_input).strip()
    crimes = st.session_state.get("crimes", crimes_input).strip()

    if not accused:
        st.warning("Please enter accused name")

    elif not crimes:
        st.warning("Please describe the crime")

    else:

        with st.spinner("Analyzing case using Indian law..."):

            try:

                from rag_pipeline import analyze_case

                result = analyze_case(accused=accused, crimes=crimes)

                # Court Header

                st.markdown(f"""
                <div class="judgment-container">

                <div style="text-align:center">

                <div style="font-family:'Playfair Display';font-size:1.8rem;color:#c9a84c;">
                ⚖️ IN THE COURT OF INDIAN LAW
                </div>

                <div style="font-family:'JetBrains Mono';font-size:0.7rem;color:#889;">
                AI LEGAL ANALYSIS • GENERATED JUDGMENT
                </div>

                </div>

                <br>

                <b>Case Title:</b> State vs {accused} <br>
                <b>Date:</b> {date.today().strftime("%d %B %Y")} <br>
                <b>Crime Alleged:</b> {crimes}

                </div>
                """, unsafe_allow_html=True)

                st.markdown(result["judgment"])

                # Sources

                with st.expander("View Retrieved Legal Sections"):

                    for src in result.get("sources", []):

                        st.markdown(f"""
                        <div style="background:#0c1120;padding:1rem;margin-bottom:0.6rem;">
                        <span class="source-chip">{src['source']}</span>

                        relevance: {src['relevance']:.3f}

                        <div style="margin-top:0.5rem;">
                        {src['text'][:500]}...
                        </div>
                        </div>
                        """, unsafe_allow_html=True)

            except Exception as e:

                st.error(f"Error: {str(e)}")

# ---------------- FOOTER ----------------

st.markdown("---")

st.markdown("""
<div style="text-align:center;font-size:0.65rem;color:#334;">
BUILT WITH: CHROMA · BAAI/bge-small · GROQ LLAMA3 · STREAMLIT
</div>
""", unsafe_allow_html=True)
