import streamlit as st
from main import (
    init_db, 
    get_recommendations_based_on_profile, 
    validate_github_profile_and_repo, 
    parse_resume_pdf, 
    generate_learning_roadmap, 
    generate_ai_reasoning, 
    get_dynamic_mentor_recommendation
)

# Initialize Database on Startup
init_db()

st.set_page_config(page_title="Ezitech AI Internship Portal", page_icon="🎓", layout="wide")

st.title("🎓 Ezitech AI-Powered Internship Recommendation & Mentor Matching Engine")
st.markdown("### EEF AI-001 Case Study Compliance Portal")
st.write("Welcome! Provide your professional details, resume, or GitHub profile below to receive personalized internship tracks, confidence scores, learning roadmaps, and mentor allocations.")

with st.sidebar:
    st.header("📋 Candidate Portal")
    uploaded_pdf = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    github_url = st.text_input("GitHub Profile/Repo URL", placeholder="https://github.com/username")
    user_skills_input = st.text_area("Core Technical Skills (comma separated)", placeholder="Python, PyTorch, AI, PHP, MySQL")
    submit_btn = st.button("Generate AI Recommendation")

if submit_btn:
    extracted_skills_from_pdf = ""
    if uploaded_pdf is not None:
        with st.spinner("Analyzing resume through PDF parsing engine..."):
            extracted_skills_from_pdf = parse_resume_pdf(uploaded_pdf)
            st.success("Resume parsed successfully!")
            
    combined_skills = user_skills_input + "," + extracted_skills_from_pdf
    
    if not combined_skills.strip():
        st.warning("Please provide your skills, upload a resume, or enter a GitHub URL.")
    else:
        st.divider()
        st.subheader("🔍 Profile Analysis & Validation")
        
        if github_url:
            gh_result = validate_github_profile_and_repo(github_url)
            if gh_result["valid"]:
                st.success(f"GitHub Validated: {gh_result['type']} ({gh_result['name']})")
            else:
                st.error(gh_result["error"])

        # Fetch Matching Internships
        matched_internships = get_recommendations_based_on_profile(combined_skills)
        
        if matched_internships:
            top_match = matched_internships[0]
            job_title, job_domain, job_desc, job_skills = top_match[0], top_match[1], top_match[2], top_match[3]
            
            # AI Reasoning & Confidence Score
            req_skills_list = [s.strip() for s in job_skills.split(',')]
            user_skills_list = [s.strip().lower() for s in combined_skills.lower().split(',')]
            matched_count = sum(1 for rs in req_skills_list if any(rs.lower() in us for us in user_skills_list))
            
            confidence_score, ai_summary = generate_ai_reasoning(req_skills_list[:max(matched_count, 1)], job_skills)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🏆 Recommended Internship Track")
                st.info(f"**Track:** {job_title}\n\n**Domain:** {job_domain}\n\n**Description:** {job_desc}")
                st.metric(label="AI Confidence Match Score", value=f"{confidence_score}%")
                st.write(f"**AI Reasoning Summary:** {ai_summary}")

            with col2:
                st.markdown("### 👨‍🏫 Assigned Mentor Recommendation")
                assigned_mentor = get_dynamic_mentor_recommendation(combined_skills, job_domain)
                if assigned_mentor:
                    st.success(f"**Mentor Name:** {assigned_mentor['name']}")
                    st.write(f"**Expertise Domain:** {assigned_mentor['domain']}")
                    st.write(f"**Core Skills:** {assigned_mentor['expertise']}")
                    st.write(f"**Official Contact:** {assigned_mentor['contact']}")
                else:
                    st.warning("No specific mentor match found. Default track supervisor assigned.")

            st.divider()
            st.markdown("### 🗺️ Personalized Learning Roadmap")
            missing_skills = [rs for rs in req_skills_list if not any(rs.lower() in us for us in user_skills_list)]
            roadmap_steps = generate_learning_roadmap(missing_skills)
            
            for idx, step in enumerate(roadmap_steps, 1):
                st.write(f"{idx}. {step}")
                
        else:
            st.warning("No exact internship matches found based on current profile metrics.")