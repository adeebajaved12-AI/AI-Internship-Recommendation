import os
import streamlit as st
from main import (
    analyze_github_repo_live,
    get_realtime_recommendations,
    init_db,
    parse_resume_pdf,
)

init_db()

st.set_page_config(
    page_title="Real-Time AI Internship & Matching Engine",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ Real-Time AI Internship & Matching Engine")
st.markdown(
    "<b>Candidate:</b> Adeeba Javed | <b>Architecture:</b> EEF AI-001 Live API"
    " Pipeline",
    unsafe_allow_html=True,
)

github_input = st.text_input("🔗 Enter GitHub Repository URL for Live Analysis:")
resume_upload = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

if st.button("Run Real-Time Analysis"):
  combined_skills = "Python, PyTorch, AI, Streamlit"

  if github_input:
    with st.spinner("Querying GitHub REST API in real time..."):
      repo_data = analyze_github_repo_live(github_input)
      if repo_data.get("status") == "Success":
        st.success(
            f"✅ Live Repository Connected: {repo_data.get('repo_name')}"
        )
        detected_lang = repo_data.get("language", "Python")
        if detected_lang:
          combined_skills += f", {detected_lang}"
          st.info(
              "Detected Primary Language/Technology from Live API:"
              f" {detected_lang}"
          )
      else:
        st.error(
            repo_data.get("message", "Invalid repository format or not found.")
        )

  if resume_upload:
    with st.spinner("Parsing resume and extracting competencies..."):
      resume_text = parse_resume_pdf(resume_upload)
      if not resume_text.startswith("Error"):
        combined_skills += f", {resume_text[:400]}"
        st.success("✅ Resume successfully parsed and embedded!")

  st.markdown("### 🎯 Real-Time Vector Similarity Results")
  recommendations = get_realtime_recommendations(combined_skills)

  for rec in recommendations[:3]:
    st.markdown(
        f"""
        <div style='background: #0f172a; border-left: 6px solid #2563eb; padding: 15px; border-radius: 8px; margin-bottom: 10px; color: white;'>
            <h4>🔥 {rec['title']}</h4>
            <p><b>Domain:</b> {rec['domain']}</p>
            <p><b>Description:</b> {rec['description']}</p>
            <p><b>Matched Skills:</b> <span style='color: #38bdf8;'>{rec['skills']}</span> (Score: {rec['match_score']})</p>
        </div>
        """,
        unsafe_allow_html=True,
    )