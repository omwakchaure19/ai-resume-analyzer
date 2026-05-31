import streamlit as st
from pypdf import PdfReader
import requests

MODEL_NAME = "qwen2.5:1.5b"


def ask_ai(prompt):
    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        return response.json()["response"]

    except Exception as e:
        return f"Error: {e}"

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ----------------------------
# CUSTOM CSS
# ----------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #111827);
}

.block-container {
    padding-top: 2rem;
}

h1, h3 {
    text-align: center;
}

div[data-testid="stMetric"] {
    background-color: #1e293b;
    border: 1px solid #334155;
    padding: 20px;
    border-radius: 15px;
}

div[data-testid="stFileUploader"] {
    border: 2px dashed #3b82f6;
    border-radius: 15px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.title("📄 Resume Analyzer")
st.sidebar.caption("AI Powered Resume Screening")

st.sidebar.info(
    "Upload a resume PDF and receive an ATS score."
)

# ----------------------------
# HEADER
# ----------------------------
st.markdown("""
# 📄 AI Resume Analyzer

### Modern AI Powered Resume Screening Dashboard
""")

# ----------------------------
# FILE UPLOAD
# ----------------------------
uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

if uploaded_file:

    pdf_reader = PdfReader(uploaded_file)

    text = ""

    for page in pdf_reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    st.success("✅ Resume Loaded Successfully")

    # ----------------------------
    # SKILLS DATABASE
    # ----------------------------
    skills_db = [
        "Python",
        "Java",
        "C++",
        "JavaScript",
        "HTML",
        "CSS",
        "SQL",
        "MySQL",
        "MongoDB",
        "AWS",
        "Docker",
        "Kubernetes",
        "Git",
        "GitHub",
        "Machine Learning",
        "Data Science",
        "Artificial Intelligence",
        "React",
        "Node.js",
        "Linux",
        "Android",
        "Kotlin",
        "Firebase"
    ]

    found_skills = []

    for skill in skills_db:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    # ----------------------------
    # ATS SCORE
    # ----------------------------
    score = 0

    score += min(len(found_skills) * 5, 50)

    if "education" in text.lower():
        score += 15

    if "project" in text.lower():
        score += 15

    if "experience" in text.lower():
        score += 20

    score = min(score, 100)

    # ----------------------------
    # KPI DASHBOARD
    # ----------------------------
    colA, colB, colC = st.columns(3)

    with colA:
        st.metric(
            "ATS Score",
            f"{score}/100"
        )

    with colB:
        st.metric(
            "Skills Found",
            len(found_skills)
        )

    with colC:
        st.metric(
            "Resume Length",
            f"{len(text)} chars"
        )

    st.write("")

    # ----------------------------
    # MAIN LAYOUT
    # ----------------------------
    col1, col2 = st.columns([2, 1])

    with col1:

        st.subheader("📄 Resume Preview")

        st.text_area(
            "Resume Content",
            text[:4000],
            height=450
        )

    with col2:

        st.subheader("📊 ATS Score")

        st.progress(score / 100)

        st.write("")

        st.subheader("🛠 Skills Found")

        if found_skills:

            for skill in found_skills:
                st.success(skill)

        else:
            st.warning("No skills detected.")

    # ----------------------------
    # SUGGESTIONS
    # ----------------------------
     # ----------------------------
    # JOB DESCRIPTION MATCHING
    # ----------------------------

    st.write("---")

    st.subheader("📋 Job Description Matching")

    job_description = st.text_area(
        "Paste Job Description",
        height=200
    )

    match_score = 0
    missing_skills = []

    if job_description:

        matched_skills = []

        for skill in skills_db:

            if skill.lower() in job_description.lower():

                if skill.lower() in text.lower():
                    matched_skills.append(skill)
                else:
                    missing_skills.append(skill)

        total = len(matched_skills) + len(missing_skills)

        if total > 0:
            match_score = int(
                len(matched_skills) / total * 100
            )

        st.metric(
            "🎯 Job Match Score",
            f"{match_score}%"
        )

        st.progress(match_score / 100)

        col_match1, col_match2 = st.columns(2)

        with col_match1:

            st.subheader("✅ Matched Skills")

            for skill in matched_skills:
                st.success(skill)

        with col_match2:

            st.subheader("❌ Missing Skills")

            for skill in missing_skills:
                st.error(skill)
    st.subheader("💡 AI Resume Suggestions")

    if st.button("🤖 Generate AI Analysis"):

        with st.spinner("Analyzing Resume..."):

            summary_prompt = f"""
Summarize this resume professionally.

Resume:
{text[:5000]}
"""

            summary = ask_ai(summary_prompt)

            st.subheader("📄 AI Resume Summary")

            st.info(summary)

            suggestion_prompt = f"""
You are an ATS expert.

Analyze this resume and provide:

1. Strengths
2. Weaknesses
3. Resume Improvements
4. Skills to Learn

Resume:
{text[:5000]}
"""

            suggestions = ask_ai(
                suggestion_prompt
            )

            st.subheader("🚀 AI Improvement Suggestions")

            st.success(suggestions)

            if job_description:

                match_prompt = f"""
Compare this resume against this job description.

Resume:
{text[:4000]}

Job Description:
{job_description}

Provide:
1. Match Percentage
2. Strengths
3. Missing Skills
4. Recommendations
"""

                ai_match = ask_ai(
                    match_prompt
                )

                st.subheader(
                    "🎯 AI Job Match Analysis"
                )

                st.info(ai_match)
# ----------------------------
# FOOTER
# ----------------------------
st.write("---")

st.caption(
    "🚀 Built by Om Wakchaure | AI Resume Analyzer"
)