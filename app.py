import streamlit as st
import os
from main import init_db, analyze_github_repo_live, parse_resume_pdf, get_realtime_recommendations

init_db()

st.set_page_config(
    page_title="Real-Time AI Internship & Matching Engine",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Real-Time AI Internship & Matching Engine")
st.markdown("<b>Candidate:</b> Adeeba Javed | <b>Architecture:</b> EEF AI-001 Live API Pipeline", unsafe_allow_html=True)

github_input = st.text_input("🔗 Enter GitHub Repository URL for Live Analysis:")
resume_upload = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

if st.button("Run Real-Time Analysis"):
    combined_skills = "Python, PyTorch, AI, Streamlit"
    
    if github_input:
        with st.spinner("Querying GitHub REST API in real time..."):
            repo_data = analyze_github_repo_live(github_input)
            if repo_data.get("valid"):
                st.success(f"✅ Live Repository Connected: {repo_data.get('name')}")
                detected_langs = ", ".join(repo_data.get("languages", []))
                combined_skills += f", {detected_langs}"
                st.info(f"Detected Languages/Technologies from Live API: {detected_langs}")
            else:
                st.error(repo_data.get("error"))
                
    if resume_upload:
        with st.spinner("Parsing resume and extracting competencies..."):
            resume_text = parse_resume_pdf(resume_upload)
            if not resume_text.startswith("Error"):
                combined_skills += f", {resume_text[:400]}"
                st.success("✅ Resume successfully parsed and embedded!")

    st.markdown("### 🎯 Real-Time Vector Similarity Results")
    recommendations = get_realtime_recommendations(combined_skills)
    
    for rec in recommendations[:3]:
        st.markdown(f"""
        <div style='background: #0f172a; border-left: 6px solid #2563eb; padding: 15px; border-radius: 8px; margin-bottom: 10px; color: white;'>
            <h4>🔥 {rec[0]}</h4>
            <p><b>Domain:</b> {rec[1]}</p>
            <p><b>Description:</b> {rec[2]}</p>
            <p><b>Matched Skills:</b> <span style='color: #38bdf8;'>{rec[3]}</span></p>
        </div>
        """, unsafe_allow_html=True)