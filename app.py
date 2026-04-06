"""
HireSense AI - Resume Analyzer
NLP-based Resume Parsing & Job Matching System
"""

import streamlit as st
import fitz  # PyMuPDF
import re
import json
from collections import Counter
import math

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HireSense AI – Resume Analyzer",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

:root {
    --bg: #0a0a0f;
    --surface: #13131a;
    --surface2: #1c1c27;
    --accent: #7c6aff;
    --accent2: #ff6a9b;
    --accent3: #6affb0;
    --text: #e8e8f0;
    --muted: #6b6b80;
    --border: #2a2a3a;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif;
}

[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * { color: var(--text) !important; }

h1, h2, h3 { font-family: 'Syne', sans-serif; font-weight: 800; }

.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.3s ease !important;
    letter-spacing: 0.05em;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(124,106,255,0.4) !important;
}

.stTextArea > div > div > textarea,
.stTextInput > div > div > input {
    background: var(--surface2) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
}

.stFileUploader {
    background: var(--surface2) !important;
    border: 1px dashed var(--accent) !important;
    border-radius: 12px !important;
}

.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}

.score-ring {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 120px;
    height: 120px;
    border-radius: 50%;
    border: 6px solid;
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    margin: 0 auto 1rem;
}

.skill-badge {
    display: inline-block;
    background: rgba(124,106,255,0.15);
    border: 1px solid rgba(124,106,255,0.4);
    color: #a99fff;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    margin: 0.2rem;
}

.match-skill-badge {
    background: rgba(106,255,176,0.15);
    border: 1px solid rgba(106,255,176,0.4);
    color: #6affb0;
}

.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.4rem;
}

.info-block {
    background: var(--surface2);
    border-left: 3px solid var(--accent);
    padding: 0.8rem 1rem;
    border-radius: 0 8px 8px 0;
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    margin-bottom: 0.5rem;
    line-height: 1.6;
}

[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

.stMarkdown p { color: var(--text); }
.stMarkdown li { color: var(--text); }
.stMarkdown h4 { color: var(--accent); }

div[data-testid="stMarkdownContainer"] p { color: var(--text); }

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #7c6aff, #ff6a9b, #6affb0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
}

.hero-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.9rem;
    color: var(--muted);
    margin-top: 0.3rem;
}
</style>
""", unsafe_allow_html=True)


# ─── NLP Utilities (Pure Python, no heavy dependencies) ───────────────────────

SKILLS_DB = {
    "programming": [
        "python","java","javascript","typescript","c++","c#","go","rust","kotlin","swift",
        "php","ruby","scala","r","matlab","perl","bash","shell","powershell","sql","nosql",
        "html","css","xml","json","yaml","graphql"
    ],
    "frameworks": [
        "django","flask","fastapi","spring","react","vue","angular","nextjs","nuxtjs",
        "express","nodejs","laravel","rails","tensorflow","pytorch","keras","scikit-learn",
        "pandas","numpy","spark","hadoop","kafka","airflow","celery","redis","rabbitmq"
    ],
    "databases": [
        "mysql","postgresql","mongodb","sqlite","oracle","cassandra","elasticsearch",
        "dynamodb","firebase","neo4j","influxdb","mariadb","mssql","snowflake","bigquery"
    ],
    "devops": [
        "docker","kubernetes","aws","azure","gcp","terraform","ansible","jenkins","gitlab",
        "github","ci/cd","devops","linux","nginx","apache","microservices","rest api",
        "graphql","grpc","prometheus","grafana","elk","datadog"
    ],
    "data_ml": [
        "machine learning","deep learning","nlp","computer vision","data analysis",
        "data science","statistics","tableau","power bi","excel","etl","feature engineering",
        "model deployment","mlops","llm","transformer","bert","gpt","embeddings","rag",
        "vector database","faiss","langchain","huggingface"
    ],
    "soft_skills": [
        "leadership","communication","teamwork","problem solving","agile","scrum",
        "project management","mentoring","collaboration","analytical","critical thinking"
    ]
}

EDUCATION_KEYWORDS = [
    "bachelor","master","phd","b.tech","m.tech","b.e","m.e","b.sc","m.sc","mba",
    "diploma","degree","university","college","institute","school","graduated","cgpa","gpa","percentage"
]

EXPERIENCE_KEYWORDS = [
    "experience","worked","developed","built","designed","implemented","led","managed",
    "created","deployed","maintained","collaborated","intern","internship","engineer",
    "developer","analyst","scientist","consultant","associate","senior","junior","lead",
    "years","months","project","team"
]

SECTION_PATTERNS = {
    "education": r"(?i)(education|academic|qualification|degree|university|college)",
    "experience": r"(?i)(experience|work|employment|career|professional|intern)",
    "skills": r"(?i)(skills|technologies|tools|expertise|competencies|proficiencies)",
    "projects": r"(?i)(projects|works|portfolio|achievements)",
    "contact": r"(?i)(contact|email|phone|address|linkedin|github)"
}


def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from uploaded PDF using PyMuPDF."""
    pdf_file.seek(0)
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s@.+#/()-]', ' ', text)
    return text.strip()


def extract_email(text: str) -> str:
    match = re.search(r'[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}', text)
    return match.group(0) if match else "Not found"


def extract_phone(text: str) -> str:
    match = re.search(r'(\+?\d[\d\s\-().]{8,14}\d)', text)
    return match.group(0).strip() if match else "Not found"


def extract_name(text: str) -> str:
    """Heuristic: first non-empty line that looks like a name."""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    for line in lines[:5]:
        # Likely a name: 2-4 words, mostly alpha
        words = line.split()
        if 1 < len(words) <= 4 and all(re.match(r"[A-Za-z.'-]+$", w) for w in words):
            return line
    return lines[0] if lines else "Unknown"


def extract_skills(text: str) -> dict:
    """Extract skills by category using keyword matching."""
    text_lower = text.lower()
    found = {}
    for category, skills in SKILLS_DB.items():
        matched = []
        for skill in skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                matched.append(skill)
        if matched:
            found[category] = matched
    return found


def extract_education(text: str) -> list:
    """Extract education-related lines."""
    lines = text.split('\n')
    edu_lines = []
    capture = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.search(SECTION_PATTERNS["education"], line):
            capture = True
            continue
        # Stop at next major section
        if capture and any(re.search(p, line) for k, p in SECTION_PATTERNS.items() if k != "education"):
            if len(edu_lines) > 0:
                capture = False
                break
        if capture or any(kw in line.lower() for kw in EDUCATION_KEYWORDS):
            if len(line) > 5:
                edu_lines.append(line)
    return edu_lines[:8]


def extract_experience(text: str) -> list:
    """Extract experience-related lines."""
    lines = text.split('\n')
    exp_lines = []
    capture = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.search(SECTION_PATTERNS["experience"], line):
            capture = True
            continue
        if capture and any(re.search(p, line) for k, p in SECTION_PATTERNS.items() if k != "experience"):
            if len(exp_lines) > 2:
                capture = False
                break
        if capture and len(line) > 10:
            exp_lines.append(line)
    return exp_lines[:10]


def tfidf_vectorize(docs: list) -> tuple:
    """Compute TF-IDF vectors from scratch."""
    tokenized = []
    for doc in docs:
        tokens = re.findall(r'\b[a-zA-Z][a-zA-Z0-9+#.]*\b', doc.lower())
        tokenized.append(tokens)

    # Build vocabulary
    vocab = sorted(set(t for tokens in tokenized for t in tokens))
    vocab_idx = {w: i for i, w in enumerate(vocab)}
    N = len(docs)

    # DF
    df = Counter()
    for tokens in tokenized:
        for t in set(tokens):
            df[t] += 1

    # IDF
    idf = {t: math.log((N + 1) / (df[t] + 1)) + 1 for t in vocab}

    # TF-IDF matrix
    vectors = []
    for tokens in tokenized:
        tf = Counter(tokens)
        total = len(tokens) if tokens else 1
        vec = [0.0] * len(vocab)
        for t, cnt in tf.items():
            if t in vocab_idx:
                vec[vocab_idx[t]] = (cnt / total) * idf[t]
        vectors.append(vec)

    return vectors, vocab


def cosine_similarity(v1: list, v2: list) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a ** 2 for a in v1))
    mag2 = math.sqrt(sum(b ** 2 for b in v2))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


def compute_match_score(resume_text: str, jd_text: str) -> dict:
    """Compute comprehensive match score."""
    vectors, vocab = tfidf_vectorize([resume_text, jd_text])
    tfidf_score = cosine_similarity(vectors[0], vectors[1])

    # Keyword overlap
    resume_words = set(re.findall(r'\b[a-z][a-z0-9+#.]{2,}\b', resume_text.lower()))
    jd_words = set(re.findall(r'\b[a-z][a-z0-9+#.]{2,}\b', jd_text.lower()))
    jd_skills = set()
    for skills in SKILLS_DB.values():
        jd_skills.update(s for s in skills if s in jd_words)

    matched_skills = jd_skills & resume_words
    skill_score = len(matched_skills) / max(len(jd_skills), 1)

    # Combined score
    final_score = round((0.6 * tfidf_score + 0.4 * skill_score) * 100, 1)

    return {
        "overall": min(final_score, 100),
        "tfidf": round(tfidf_score * 100, 1),
        "skill_overlap": round(skill_score * 100, 1),
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(jd_skills - resume_words),
        "jd_skills": sorted(jd_skills),
    }


def score_color(score):
    if score >= 75: return "#6affb0", "🟢 Excellent Match"
    if score >= 50: return "#ffd76a", "🟡 Good Match"
    if score >= 30: return "#ff9a6a", "🟠 Partial Match"
    return "#ff6a6a", "🔴 Low Match"


# ─── UI ───────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='padding: 1rem 0;'>
        <div class='hero-title' style='font-size:1.4rem;'>🧾 HireSense AI</div>
        <div class='hero-sub'>Resume Analyzer v1.0</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### 📌 How to use")
    st.markdown("""
    1. Upload your **PDF resume**
    2. Paste a **job description**
    3. Click **Analyze**
    4. View extracted info + match score
    """)
    st.markdown("---")
    st.markdown("#### ⚙️ Engine")
    st.markdown("""
    - **Parser**: PyMuPDF
    - **NLP**: Regex + Keyword NER
    - **Matching**: TF-IDF + Cosine
    - **Zero ML dependencies**
    """)

# Hero
st.markdown("""
<div style='margin-bottom: 2rem;'>
    <div class='hero-title'>Resume Analyzer</div>
    <div class='hero-sub'>// NLP-powered resume parsing & job description matching</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="section-header">📄 Upload Resume (PDF)</div>', unsafe_allow_html=True)
    resume_file = st.file_uploader("Upload Resume", type=["pdf"], key="resume", label_visibility="collapsed")

    st.markdown('<div class="section-header" style="margin-top:1.5rem;">📝 Job Description</div>', unsafe_allow_html=True)
    jd_text = st.text_area(
        " Job Description",
        height=280,
        placeholder="Paste the job description here...\n\nExample:\nWe are looking for a Python Developer with experience in FastAPI, Docker, PostgreSQL, machine learning, and REST APIs...",
        label_visibility="collapsed"
    )

    analyze_btn = st.button("🚀 Analyze Resume", use_container_width=True)

with col2:
    if analyze_btn:
        if not resume_file:
            st.error("⚠️ Please upload a PDF resume first.")
        elif not jd_text.strip():
            st.error("⚠️ Please enter a job description.")
        else:
            with st.spinner("Parsing resume..."):
                raw_text = extract_text_from_pdf(resume_file)
                cleaned = clean_text(raw_text)

                name = extract_name(raw_text)
                email = extract_email(raw_text)
                phone = extract_phone(raw_text)
                skills = extract_skills(cleaned)
                education = extract_education(raw_text)
                experience = extract_experience(raw_text)
                match = compute_match_score(cleaned, jd_text)

            # Contact info
            st.markdown('<div class="section-header">👤 Candidate Info</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;margin-bottom:0.5rem;">{name}</div>
                <div style="font-family:'Space Mono',monospace;font-size:0.8rem;color:#a0a0b0;">
                    📧 {email}<br>📱 {phone}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Match Score
            color, label = score_color(match["overall"])
            st.markdown('<div class="section-header">🎯 Match Score</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="metric-card" style="text-align:center;">
                <div class="score-ring" style="border-color:{color};color:{color};">{match['overall']}%</div>
                <div style="font-family:'Space Mono',monospace;font-size:0.9rem;color:{color};">{label}</div>
                <div style="display:flex;justify-content:space-around;margin-top:1rem;">
                    <div style="text-align:center;">
                        <div style="font-size:0.7rem;color:#6b6b80;font-family:'Space Mono',monospace;">TF-IDF SIM</div>
                        <div style="font-size:1.1rem;font-weight:700;color:#7c6aff;font-family:'Space Mono',monospace;">{match['tfidf']}%</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="font-size:0.7rem;color:#6b6b80;font-family:'Space Mono',monospace;">SKILL OVERLAP</div>
                        <div style="font-size:1.1rem;font-weight:700;color:#ff6a9b;font-family:'Space Mono',monospace;">{match['skill_overlap']}%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    elif not analyze_btn:
        st.markdown("""
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:400px;opacity:0.4;">
            <div style="font-size:4rem;">🧾</div>
            <div style="font-family:'Space Mono',monospace;font-size:0.9rem;color:#6b6b80;margin-top:1rem;text-align:center;">
                Upload a resume & job description<br>then click Analyze
            </div>
        </div>
        """, unsafe_allow_html=True)

# Full results below
if analyze_btn and resume_file and jd_text.strip():
    raw_text = extract_text_from_pdf(resume_file)
    cleaned = clean_text(raw_text)
    skills = extract_skills(cleaned)
    education = extract_education(raw_text)
    experience = extract_experience(raw_text)
    match = compute_match_score(cleaned, jd_text)

    st.markdown("---")
    r1, r2, r3 = st.columns(3, gap="large")

    with r1:
        st.markdown('<div class="section-header">🛠️ Extracted Skills</div>', unsafe_allow_html=True)
        if skills:
            for cat, skill_list in skills.items():
                st.markdown(f'<div style="font-size:0.75rem;color:#7c6aff;font-family:Space Mono,monospace;text-transform:uppercase;margin:0.5rem 0 0.2rem;">{cat.replace("_"," ")}</div>', unsafe_allow_html=True)
                badges = " ".join(f'<span class="skill-badge">{s}</span>' for s in skill_list)
                st.markdown(badges, unsafe_allow_html=True)
        else:
            st.info("No skills extracted.")

    with r2:
        st.markdown('<div class="section-header">🎓 Education</div>', unsafe_allow_html=True)
        if education:
            for line in education:
                st.markdown(f'<div class="info-block">{line}</div>', unsafe_allow_html=True)
        else:
            st.info("No education details found.")

        st.markdown('<div class="section-header" style="margin-top:1rem;">💼 Experience</div>', unsafe_allow_html=True)
        if experience:
            for line in experience[:6]:
                st.markdown(f'<div class="info-block">{line}</div>', unsafe_allow_html=True)
        else:
            st.info("No experience details found.")

    with r3:
        st.markdown('<div class="section-header">✅ Matched Skills</div>', unsafe_allow_html=True)
        if match["matched_skills"]:
            badges = " ".join(f'<span class="skill-badge match-skill-badge">{s}</span>' for s in match["matched_skills"])
            st.markdown(badges, unsafe_allow_html=True)
        else:
            st.info("No matching skills found.")

        st.markdown('<div class="section-header" style="margin-top:1rem;">❌ Missing Skills</div>', unsafe_allow_html=True)
        if match["missing_skills"]:
            for s in match["missing_skills"][:12]:
                st.markdown(f'<span class="skill-badge" style="background:rgba(255,106,106,0.15);border-color:rgba(255,106,106,0.4);color:#ff9a9a;">{s}</span>', unsafe_allow_html=True)
        else:
            st.success("No missing skills detected! 🎉")

    # Raw text expander
    with st.expander("📄 View Raw Extracted Text"):
        st.text_area("", raw_text[:3000], height=300, label_visibility="collapsed")
