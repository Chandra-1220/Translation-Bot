# app.py

import streamlit as st
from transformers import pipeline

# ---- Page Config ----
st.set_page_config(page_title="Lingua Bridge", page_icon="🗺️", layout="centered")

# ---- Custom CSS ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --ink: #1D2B4F;
    --ink-soft: #3B4C7A;
    --paper: #EEF1F6;
    --card: #FFFFFF;
    --brass: #C9A24B;
    --brass-deep: #A97F2E;
    --line: #D6DCE8;
}

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
    color: var(--ink);
}

.stApp {
    background: var(--paper);
}

/* Header */
.lb-header {
    text-align: center;
    padding: 2.2rem 1rem 1.6rem 1rem;
    border-bottom: 1px solid var(--line);
    margin-bottom: 1.8rem;
    position: relative;
}
.lb-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--brass-deep);
    margin-bottom: 0.5rem;
}
.lb-title {
    font-family: 'Fraunces', serif;
    font-size: 2.6rem;
    font-weight: 600;
    color: var(--ink);
    margin: 0;
    letter-spacing: -0.01em;
}
.lb-sub {
    font-size: 0.95rem;
    color: var(--ink-soft);
    margin-top: 0.5rem;
}

/* Signature arc between languages */
.lb-arc-wrap {
    display: flex;
    justify-content: center;
    margin: 0.4rem 0 1.2rem 0;
}
.lb-arc-wrap svg { display: block; }

/* Language cards */
.lb-lang-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--brass-deep);
    margin-bottom: 0.3rem;
    display: block;
}

/* Streamlit widget overrides */
div[data-baseweb="select"] > div {
    background-color: var(--card) !important;
    border: 1px solid var(--line) !important;
    border-radius: 8px !important;
}
.stTextArea textarea {
    background-color: var(--card) !important;
    border: 1px solid var(--line) !important;
    border-radius: 10px !important;
    color: var(--ink) !important;
    font-size: 1rem !important;
}
.stTextArea textarea:focus {
    border-color: var(--brass) !important;
    box-shadow: 0 0 0 1px var(--brass) !important;
}

/* Translate button */
.stButton > button {
    background: var(--ink) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.65rem 1.6rem !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em;
    transition: background 0.2s ease, transform 0.15s ease;
    width: 100%;
}
.stButton > button:hover {
    background: var(--brass-deep) !important;
    transform: translateY(-1px);
}

/* Result card */
.lb-result {
    background: var(--card);
    border: 1px solid var(--line);
    border-left: 4px solid var(--brass);
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin-top: 0.6rem;
}
.lb-result-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--brass-deep);
    margin-bottom: 0.5rem;
    display: block;
}
.lb-result-text {
    font-family: 'Fraunces', serif;
    font-size: 1.3rem;
    line-height: 1.5;
    color: var(--ink);
}

/* Comparison panels */
.lb-compare {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    height: 100%;
}
.lb-compare-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--ink-soft);
    margin-bottom: 0.5rem;
}

footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---- Header ----
st.markdown("""
<div class="lb-header">
    <div class="lb-eyebrow">200 languages · one model</div>
    <div class="lb-title">Lingua Bridge</div>
    <div class="lb-sub">Carry meaning across languages, not just words.</div>
</div>
""", unsafe_allow_html=True)

# ---- Signature arc (visual bridge motif) ----
st.markdown("""
<div class="lb-arc-wrap">
<svg width="280" height="50" viewBox="0 0 280 50" fill="none">
    <path d="M20 45 Q140 -10 260 45" stroke="#C9A24B" stroke-width="2" fill="none" stroke-dasharray="1 7" stroke-linecap="round"/>
    <circle cx="20" cy="45" r="4" fill="#1D2B4F"/>
    <circle cx="260" cy="45" r="4" fill="#1D2B4F"/>
</svg>
</div>
""", unsafe_allow_html=True)

# ---- Language Code Mapping (FLORES-200 codes used by NLLB) ----
LANGUAGES = {
    "English": "eng_Latn",
    "French": "fra_Latn",
    "German": "deu_Latn",
    "Spanish": "spa_Latn",
    "Hindi": "hin_Deva",
    "Chinese (Simplified)": "zho_Hans",
    "Japanese": "jpn_Jpan",
    "Korean": "kor_Hang",
    "Arabic": "arb_Arab",
    "Portuguese": "por_Latn",
    "Russian": "rus_Cyrl",
    "Italian": "ita_Latn",
    "Bengali": "ben_Beng",
    "Tamil": "tam_Taml",
    "Telugu": "tel_Telu",
    "Urdu": "urd_Arab",
    "Turkish": "tur_Latn",
    "Vietnamese": "vie_Latn",
    "Dutch": "nld_Latn",
    "Thai": "tha_Thai",
}

# ---- Load Model ----
@st.cache_resource
def load_translator():
    return pipeline(
        "translation",
        model="facebook/nllb-200-distilled-600M",
        device=0  # remove or set -1 for CPU-only environments
    )

translator = load_translator()

# ---- Language Selectors ----
col1, col2 = st.columns(2)
with col1:
    st.markdown('<span class="lb-lang-label">From</span>', unsafe_allow_html=True)
    source_lang = st.selectbox(" ", list(LANGUAGES.keys()), index=0, label_visibility="collapsed", key="src")
with col2:
    st.markdown('<span class="lb-lang-label">To</span>', unsafe_allow_html=True)
    target_lang = st.selectbox(" ", list(LANGUAGES.keys()), index=1, label_visibility="collapsed", key="tgt")

# ---- Text Input ----
st.markdown('<span class="lb-lang-label">Your text</span>', unsafe_allow_html=True)
text = st.text_area(" ", height=140, placeholder="Type or paste text here...", label_visibility="collapsed")

translate_clicked = st.button("Translate →")

# ---- Run Translation ----
if translate_clicked:
    if not text.strip():
        st.warning("Please enter some text to translate.")
    elif source_lang == target_lang:
        st.warning("Source and target languages must be different.")
    else:
        src_code = LANGUAGES[source_lang]
        tgt_code = LANGUAGES[target_lang]

        with st.spinner("Translating..."):
            result = translator(text, src_lang=src_code, tgt_lang=tgt_code, max_length=400)

        translated_text = result[0]["translation_text"]

        st.markdown(f"""
        <div class="lb-result">
            <span class="lb-result-label">{target_lang}</span>
            <div class="lb-result-text">{translated_text}</div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="lb-compare">
                <div class="lb-compare-title">Original · {source_lang}</div>
                {text}
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="lb-compare">
                <div class="lb-compare-title">Translated · {target_lang}</div>
                {translated_text}
            </div>
            """, unsafe_allow_html=True)
