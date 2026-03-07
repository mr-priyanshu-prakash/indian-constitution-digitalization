import streamlit as st
from datetime import date
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ---------------- PAGE CONFIG ----------------

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

/* MAIN BACKGROUND */

.stApp{
background: radial-gradient(circle at top,#0f172a,#020617);
font-family:'Source Serif 4',serif;
color:#f1f5f9;
}

/* SIDEBAR */

[data-testid="stSidebar"]{
background:#020617;
border-right:1px solid #c9a84c33;
}

[data-testid="stSidebar"] *{
color:#f8fafc;
}

/* HERO HEADER */

.hero-header{
text-align:center;
padding:3rem 0 2rem;
border-bottom:1px solid #c9a84c44;
margin-bottom:2rem;
}

.hero-title{
font-family:'Playfair Display',serif;
font-size:3.2rem;
font-weight:900;
color:#d4af37;
}

.hero-subtitle{
font-style:italic;
color:#cbd5f5;
margin-top:0.4rem;
}

.hero-badge{
display:inline-block;
margin-top:1rem;
padding:0.35rem 1.3rem;
border:1px solid #d4af3780;
font-family:'JetBrains Mono';
font-size:0.7rem;
color:#d4af37;
}

/* INPUT */

.input-label{
font-family:'JetBrains Mono';
font-size:0.72rem;
letter-spacing:0.14em;
text-transform:uppercase;
color:#d4af37;
margin-bottom:4px;
}

.stTextInput input,
.stTextArea textarea{
background:#020617 !important;
border:1px solid #d4af3744 !important;
color:#f8fafc !important;
border-radius:6px;
}

/* BUTTON */

.stButton>button{
width:100%;
background:linear-gradient(135deg,#d4af37,#a67c00);
color:#020617;
font-weight:700;
font-size:1.05rem;
border:none;
padding:0.8rem;
border-radius:6px;
}

/* JUDGMENT BLOCK */

.judgment-container{
background:#020617;
border:1px solid #d4af3744;
border-top:4px solid #d4af37;
padding:2rem;
margin-top:2rem;
border-radius:6px;
}

/* SOURCE CHIP */

.source-chip{
background:#020617;
border:1px solid #d4af3744;
padding:0.2rem 0.8rem;
font-family:'JetBrains Mono';
font-size:0.68rem;
color:#d4af37;
border-radius:4px;
}

/* CODE BLOCKS */

.stMarkdown pre{
background:#020617 !important;
border:1px solid #d4af3744 !important;
border-radius:6px !important;
padding:1rem !important;
}

/* REMOVE STREAMLIT DEFAULT UI */

#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("""
    <div style="text-align:center">
    <div style="font-size:3rem;">⚖️</div>
    <div style="font-size:1.2rem;color:#d4af37;font-weight:700">
    Legal RAG System
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📚 Ingested Legal Documents")

    docs = [
        "Indian Constitution 2023",
        "Bharatiya Nyaya Sanhita (BNS) 2023",
        "Indian Penal Code (IPC)",
        "POCSO Act",
        "CrPC"
    ]

    for d in docs:
        st.markdown(f"• {d}")

    st.markdown("---")

    st.markdown(f"""
    **Today:** {date.today().strftime("%d %B %Y")}

    **BNS 2023:** ACTIVE  
    **IPC:** REPEALED
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

# ---------------- BUTTON ----------------

_, btn_col, _ = st.columns([1,2,1])

with btn_col:
    analyze_btn = st.button("Analyze Case Under Indian Law")

# ---------------- ANALYSIS ----------------

if analyze_btn:

    accused = st.session_state.get("accused", accused_input).strip()
    crimes  = st.session_state.get("crimes",  crimes_input).strip()

    if not accused:
        st.warning("Please enter accused name")

    elif not crimes:
        st.warning("Please describe the crime")

    else:

        with st.spinner("⚖️ Consulting Indian law and legal precedents..."):

            try:

                from rag_pipeline import analyze_case

                result = analyze_case(accused=accused, crimes=crimes)

                # SAVE to session_state so result persists across reruns
                st.session_state["result"]        = result
                st.session_state["accused_final"] = accused
                st.session_state["crimes_final"]  = crimes

            except Exception as e:

                st.error(f"Error: {str(e)}")

# DISPLAY — outside if analyze_btn so it survives reconnects
if "result" in st.session_state:

    result  = st.session_state["result"]
    accused = st.session_state["accused_final"]
    crimes  = st.session_state["crimes_final"]

    # ---------------- COURT HEADER ----------------

    st.markdown(f"""
    <div class="judgment-container">

    <div style="text-align:center">

    <div style="font-family:'Playfair Display';font-size:2rem;color:#d4af37;">
    ⚖️ SUPREME COURT OF INDIAN LAW
    </div>

    <div style="font-family:'JetBrains Mono';font-size:0.7rem;color:#94a3b8;">
    AI LEGAL ANALYSIS • GENERATED JUDGMENT
    </div>

    </div>

    <br>

    <b>Case:</b> State vs {accused} <br>
    <b>Date:</b> {date.today().strftime("%d %B %Y")} <br>
    <b>Alleged Crime:</b> {crimes}

    </div>
    """, unsafe_allow_html=True)

    # ---------------- JUDGMENT ----------------

    st.markdown(result["judgment"])

    # ---------------- SOURCES ----------------

    with st.expander("Retrieved Legal Sections"):

        for src in result.get("sources", []):

            st.markdown(f"""
            <div style="background:#020617;padding:1rem;margin-bottom:0.7rem;border:1px solid #d4af3744;border-radius:5px;">

            <span class="source-chip">{src['source']}</span>

            <div style="font-size:0.75rem;color:#94a3b8;margin-top:4px;">
            relevance score: {src['relevance']:.3f}
            </div>

            <div style="margin-top:0.6rem;">
            {src['text'][:500]}...
            </div>

            </div>
            """, unsafe_allow_html=True)

# ---------------- FOOTER ----------------

st.markdown("---")

st.markdown("""
<div style="text-align:center;font-size:0.65rem;color:#64748b;">
BUILT WITH: CHROMA · BGE EMBEDDINGS · GROQ LLAMA3 · STREAMLIT
</div>
""", unsafe_allow_html=True)
