import html
import os
import sys
from datetime import date

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="VerdictAI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

DOCS = [
    "Indian Constitution 2023",
    "Bharatiya Nyaya Sanhita (BNS) 2023",
    "Indian Penal Code (IPC) 1860",
    "POCSO Act 2012",
    "Code of Criminal Procedure (CrPC)",
]

# ---------------- STYLES ----------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

:root{
  --surface:#f8f9ff; --card:#ffffff; --low:#eff4ff; --mid:#e5eeff;
  --ink:#0b1c30; --muted:#45464d; --navy:#131b2e;
  --accent:#9b4500; --accent-bg:#ffdbca; --line:#d9e2f3;
}

.stApp{background:var(--surface);color:var(--ink);font-family:'Plus Jakarta Sans',sans-serif;}
.block-container{max-width:1080px;padding-top:2.2rem;padding-bottom:3rem;}
header[data-testid="stHeader"]{background:transparent;}
#MainMenu, footer{visibility:hidden;}

/* sidebar */
[data-testid="stSidebar"]{background:var(--card);border-right:1px solid var(--line);}
[data-testid="stSidebar"] *{color:var(--ink);}

.side-brand{display:flex;align-items:center;gap:.7rem;padding:.4rem 0 1rem;}
.logo{width:40px;height:40px;border-radius:6px;background:var(--navy);display:flex;
  align-items:center;justify-content:center;font-size:1.25rem;flex-shrink:0;}
.logo, .logo *{color:#fff !important;}
.brand-name{font-family:'Merriweather',serif;font-weight:700;font-size:1.02rem;line-height:1.25;}
.brand-sub{font-size:.68rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted) !important;margin-top:2px;}

.side-label{font-size:.68rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  color:var(--muted) !important;margin:1.2rem 0 .5rem;}
.doc-item{display:flex;align-items:center;gap:.55rem;padding:.5rem .65rem;border-radius:6px;
  background:var(--low);margin-bottom:.4rem;font-size:.84rem;}
.doc-dot{width:6px;height:6px;border-radius:50%;background:var(--accent);flex-shrink:0;}
.status-row{display:flex;justify-content:space-between;font-size:.8rem;padding:.3rem 0;
  border-bottom:1px solid var(--line);}
.status-row span:last-child{font-weight:600;}

/* top bar */
.topbar{display:flex;align-items:center;justify-content:center;text-align:center;gap:1rem;flex-wrap:wrap;
  padding-bottom:1.1rem;border-bottom:1px solid var(--line);margin-bottom:1.4rem;}
.topbar .brand-name{font-size:1.5rem;}
.topbar .pill{font-size:.72rem;font-weight:600;letter-spacing:.04em;padding:.35rem .8rem;border-radius:999px;
  background:var(--accent-bg);color:#331200 !important;}

/* notice */
.notice{background:var(--accent-bg);border-left:4px solid var(--accent);border-radius:6px;
  padding:.8rem 1rem;font-size:.85rem;line-height:1.55;color:#331200;margin-bottom:1.3rem;}
.notice b{color:#331200;}

/* cards */
.card-title{font-family:'Merriweather',serif;font-weight:700;font-size:1.1rem;color:var(--ink);}
.card-sub{font-size:.8rem;color:var(--muted);margin:2px 0 .9rem;}
.field-label{font-size:.72rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;
  color:var(--ink);margin-bottom:.3rem;}

/* inputs */
:root{color-scheme:light;}
.stTextInput div[data-baseweb="input"], .stTextInput div[data-baseweb="base-input"],
.stTextArea div[data-baseweb="textarea"], .stTextArea div[data-baseweb="base-input"]{
  background:var(--low) !important;border-radius:6px !important;}
.stTextInput input:-webkit-autofill{
  -webkit-box-shadow:0 0 0 1000px #eff4ff inset !important;-webkit-text-fill-color:#0b1c30 !important;}
.stTextInput input, .stTextArea textarea{
  background:var(--low) !important;color:var(--ink) !important;
  caret-color:var(--ink) !important;-webkit-text-fill-color:var(--ink) !important;
  border:1px solid var(--line) !important;border-radius:6px !important;
  font-family:'Plus Jakarta Sans',sans-serif !important;}
.stTextInput input:focus, .stTextArea textarea:focus{border-color:var(--navy) !important;box-shadow:none !important;}
.stTextInput input::placeholder, .stTextArea textarea::placeholder{
  color:#76777d !important;-webkit-text-fill-color:#76777d !important;}

/* button */
.stButton>button{width:100%;background:var(--navy);border:none;border-radius:8px;padding:.7rem 1rem;
  font-weight:600;font-size:.95rem;transition:background .15s;}
.stButton>button, .stButton>button p{color:#fff !important;}
.stButton>button:hover{background:#000;}
.stButton>button:focus{box-shadow:none;outline:none;}

/* result header */
.case-head{display:flex;flex-wrap:wrap;gap:1.6rem;align-items:flex-start;justify-content:space-between;}
.case-head .k{font-size:.68rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);}
.case-head .v{font-size:.98rem;font-weight:600;margin-top:2px;overflow-wrap:anywhere;}
.badge{display:inline-block;font-size:.68rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
  padding:.25rem .65rem;border-radius:4px;background:var(--mid);color:var(--ink);}

/* sources */
.src{background:var(--low);border-radius:8px;padding:.85rem 1rem;margin-bottom:.6rem;}
.src-top{display:flex;justify-content:space-between;gap:.6rem;flex-wrap:wrap;align-items:center;}
.src-name{font-weight:600;font-size:.86rem;}
.src-score{font-size:.72rem;font-weight:700;color:var(--accent);}
.src-text{font-size:.84rem;line-height:1.6;color:var(--muted);margin-top:.45rem;}

.badge.lock{background:var(--accent-bg);color:#331200;}
.lock-box{display:flex;align-items:center;gap:.9rem;background:var(--low);border:1px dashed #b9c4d8;
  border-radius:8px;padding:1rem 1.1rem;}
.lock-icon{font-size:1.3rem;}
.lock-title{font-weight:600;font-size:.92rem;color:var(--ink);}
.lock-text{font-size:.84rem;color:var(--muted);margin-top:2px;line-height:1.5;}
.disclaimer{font-size:.78rem;color:var(--muted);background:var(--low);border-radius:6px;
  padding:.7rem 1rem;margin-top:1rem;line-height:1.55;}
.footer{text-align:center;font-size:.68rem;letter-spacing:.06em;text-transform:uppercase;
  color:#76777d;margin-top:2.2rem;padding-top:1rem;border-top:1px solid var(--line);}

/* markdown inside the analysis card */
[data-testid="stMarkdownContainer"] h1,[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3{font-family:'Merriweather',serif;color:var(--ink);}
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li{line-height:1.7;}
[data-testid="stExpander"]{border:1px solid var(--line);border-radius:10px;background:var(--card);}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown(
        """
<div class="side-brand">
  <div class="logo">⚖</div>
  <div><div class="brand-name">VerdictAI</div>
  <div class="brand-sub">Prototype</div></div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="side-label">Ingested Legal Documents</div>', unsafe_allow_html=True)
    st.markdown(
        "".join(f'<div class="doc-item"><span class="doc-dot"></span>{html.escape(d)}</div>' for d in DOCS),
        unsafe_allow_html=True,
    )

    st.markdown('<div class="side-label">Status</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
<div class="status-row"><span>Today</span><span>{date.today().strftime("%d %b %Y")}</span></div>
<div class="status-row"><span>BNS 2023</span><span>In force</span></div>
<div class="status-row"><span>IPC 1860</span><span>Repealed</span></div>
""",
        unsafe_allow_html=True,
    )

# ---------------- HEADER ----------------
st.markdown(
    """
<div class="topbar">
  <div class="brand-name">VerdictAI</div>
</div>

<div class="notice">
  <b>Transition note:</b> Offences committed on or after <b>1 July 2024</b> are governed by the
  Bharatiya Nyaya Sanhita (BNS) 2023, which replaced the Indian Penal Code, 1860. IPC provisions
  remain relevant for offences committed before that date.
</div>
""",
    unsafe_allow_html=True,
)

# ---------------- INTAKE ----------------
with st.container(border=True):
    st.markdown(
        '<div class="card-title">Case Intake</div>'
        '<div class="card-sub">Enter the accused and the alleged offence to analyse.</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="field-label">Name of Accused</div>', unsafe_allow_html=True)
        accused_input = st.text_input(
            "Name of accused",
            placeholder="Enter accused name",
            autocomplete="off",
            label_visibility="collapsed",
            key="accused",
        )
    with col2:
        st.markdown('<div class="field-label">Crimes Committed</div>', unsafe_allow_html=True)
        crimes_input = st.text_area(
            "Crimes committed",
            placeholder="Describe the alleged offence and relevant facts",
            height=100,
            label_visibility="collapsed",
            key="crimes",
        )

    analyze_btn = st.button("Analyze Case Under Indian Law")

# ---------------- ANALYSIS ----------------
if analyze_btn:
    accused = accused_input.strip()
    crimes = crimes_input.strip()

    if not accused:
        st.warning("Please enter the name of the accused.")
    elif not crimes:
        st.warning("Please describe the alleged offence.")
    else:
        with st.spinner("Consulting Indian law and legal precedents..."):
            try:
                from rag_pipeline import analyze_case

                result = analyze_case(accused=accused, crimes=crimes)
                st.session_state["result"] = result
                st.session_state["accused_final"] = accused
                st.session_state["crimes_final"] = crimes
            except Exception as e:
                st.error(f"Error: {e}")

# ---------------- RESULT (survives reruns) ----------------
if "result" in st.session_state:
    result = st.session_state["result"]
    accused = st.session_state["accused_final"]
    crimes = st.session_state["crimes_final"]

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(
            f"""
<div class="case-head">
  <div><div class="k">Case</div><div class="v">State vs {html.escape(accused)}</div></div>
  <div><div class="k">Date</div><div class="v">{date.today().strftime("%d %B %Y")}</div></div>
  <div style="flex-basis:100%"><div class="k">Alleged offence</div>
  <div class="v" style="font-weight:500">{html.escape(crimes)}</div></div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(
            '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.6rem">'
            '<div class="card-title">Legal Analysis</div><span class="badge">AI generated</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(result["judgment"])

    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)

    sources = result.get("sources", [])
    with st.expander(f"Retrieved Legal Sections ({len(sources)})"):
        for src in sources:
            st.markdown(
                f"""
<div class="src">
  <div class="src-top">
    <span class="src-name">{html.escape(str(src.get("source", "")))}</span>
    <span class="src-score">Relevance {float(src.get("relevance", 0)):.3f}</span>
  </div>
  <div class="src-text">{html.escape(str(src.get("text", ""))[:500])}…</div>
</div>
""",
                unsafe_allow_html=True,
            )

    # ---- Similar judgments (licensed feature - locked placeholder) ----
    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(
            """
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.7rem">
  <div class="card-title">Similar Supreme Court &amp; High Court Judgments</div>
  <span class="badge lock">Licensed version</span>
</div>
<div class="lock-box">
  <div class="lock-icon">🔒</div>
  <div>
    <div class="lock-title">Available in the licensed version only</div>
    <div class="lock-text">Similar Supreme Court and High Court cases and judgments are
    not included in this version.</div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

#    st.markdown(
#        '<div class="disclaimer"><b>Note:</b> This analysis is AI-generated to support legal research. '
#        "Verify all provisions and citations against official sources before relying on it. "
#        "It is not a substitute for advice from a qualified advocate.</div>",
#        unsafe_allow_html=True,
#    )

# ---------------- FOOTER ----------------
#st.markdown(
#    '<div class="footer">Built with Chroma · BGE embeddings · Groq · Streamlit</div>',
#    unsafe_allow_html=True,
#)
