import streamlit as st
import time
import os
from sentence_transformers import SentenceTransformer
import chromadb
import numpy as np
from auth import init_db, register_user, authenticate_user

# Initialize SQLite database for users
init_db()

# Safe import for PDF parsing (PyMuPDF / fitz)
try:
    import fitz
    PDF_PARSER_AVAILABLE = True
except ImportError:
    PDF_PARSER_AVAILABLE = False

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="AI Internship Recommendation System",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Session state initialization for Authentication & Submissions
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# Shared storage for capstone submissions (for demo/session continuity)
if "submissions" not in st.session_state:
    st.session_state.submissions = [
        {
            "student_name": "adeeba",
            "track": "Generative AI Intern",
            "repo": "https://github.com/adeeba/capstone-project",
            "live_url": "https://share.streamlit.io/adeeba/project",
            "notes": "Built local LLM RAG interface with Streamlit and ChromaDB.",
            "status": "Pending",
            "feedback": ""
        }
    ]

# ---------------------------------------------------
# 1. AI Models & Vector DB Initialization (Cached)
# ---------------------------------------------------
@st.cache_resource
def load_ai_engine():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    chroma_client = chromadb.Client()
    collection_name = "ezitech_ai_internship_tracks"
    
    try:
        collection = chroma_client.get_collection(name=collection_name)
    except:
        collection = chroma_client.create_collection(name=collection_name)
        
        tracks = [
            {
                "id": "track_1",
                "title": "Generative AI Intern",
                "company": "Ezitech Portal / Arch Technologies",
                "mentor": "Dr. Hamera Javed",
                "skills": "Python, NLP, Deep Learning, TensorFlow, PyTorch, LangChain, LLMs, Streamlit",
                "description": "Build local LLM interfaces, RAG pipelines, and generative applications using state-of-the-art frameworks."
            },
            {
                "id": "track_2",
                "title": "Machine Learning Intern",
                "company": "Ezitech Portal Track",
                "mentor": "Ali Ahmed",
                "skills": "Python, Scikit-Learn, Pandas, NumPy, SQL, Data Analysis, Machine Learning",
                "description": "Develop and deploy predictive models, handle large datasets, and optimize machine learning workflows."
            },
            {
                "id": "track_3",
                "title": "Computer Vision Intern",
                "company": "Ezitech Vision Lab",
                "mentor": "Dr. Kamran",
                "skills": "Python, OpenCV, PyTorch, CNN, Image Processing, YOLO",
                "description": "Build object detection, segmentation, and advanced computer vision architectures."
            },
            {
                "id": "track_4",
                "title": "Web & Full Stack AI Developer",
                "company": "Ezitech Solutions",
                "mentor": "Sara Khan",
                "skills": "Python, FastAPI, Streamlit, Docker, MySQL, REST APIs, Git",
                "description": "Build robust web architectures, integrate AI models into production endpoints, and manage cloud deployment."
            }
        ]
        
        for track in tracks:
            embedding = model.encode(track["skills"] + " " + track["description"]).tolist()
            collection.add(
                documents=[track["description"]],
                embeddings=[embedding],
                metadatas=[{
                    "title": track["title"],
                    "company": track["company"],
                    "mentor": track["mentor"],
                    "skills": track["skills"]
                }],
                ids=[track["id"]]
            )
            
    return model, collection

embed_model, vector_collection = load_ai_engine()

# ---------------------------------------------------
# 2. Independent Utility & Processing Functions
# ---------------------------------------------------
def extract_text_from_pdf(uploaded_file):
    text = ""
    if not PDF_PARSER_AVAILABLE:
        return "PDF parsing library not loaded."
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def validate_github_url(url):
    if not url:
        return True
    cleaned_url = url.strip().lower()
    if cleaned_url.startswith("https://github.com/") and len(cleaned_url) > 19:
        return True
    return False

def analyze_and_extract_skills(resume_text, manual_skills):
    processed_skills = f"Manual Skills: {manual_skills} | Resume Context: {resume_text[:1200]}"
    return processed_skills

def run_vector_semantic_search(query_text):
    query_embedding = embed_model.encode(query_text).tolist()
    search_results = vector_collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )
    return search_results

# ---------------------------------------------------
# Professional CSS Styling
# ---------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background-color: #050b18;
    color: #ffffff;
}

#MainMenu {visibility: hidden;} 
footer {visibility: hidden;} 
header {visibility: hidden;}

.brand-logo {
    font-size: 22px;
    font-weight: 900;
    color: #38bdf8;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
    text-transform: uppercase;
}

.main-title {
    text-align: left; 
    font-size: 40px; 
    font-weight: 900;
    color: #ffffff;
    margin-bottom: 5px;
}

.sub-title {
    text-align: left; 
    font-size: 16px; 
    color: #cbd5e1; 
    margin-bottom: 25px; 
    font-weight: 600;
}

.section-title {
    color: #ffffff; 
    font-size: 22px; 
    font-weight: 800; 
    margin-bottom: 15px;
    border-left: 4px solid #2563eb;
    padding-left: 10px;
}

label {
    font-weight: 700 !important;
    color: #e2e8f0 !important;
}

.stTextInput input, .stTextArea textarea {
    border-radius: 10px; 
    border: 2px solid #2563eb; 
    background-color: #0f172a; 
    color: #ffffff; 
    padding: 12px;
    font-weight: 600;
}

[data-testid="stFileUploader"] {
    border: 2px dashed #3b82f6; 
    border-radius: 10px; 
    padding: 15px; 
    background-color: #0f172a;
}

.stButton>button {
    width: 100%; 
    padding: 12px; 
    font-size: 16px; 
    font-weight: 800; 
    color: #ffffff; 
    border: none;
    border-radius: 10px; 
    background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
    transition: 0.3s;
    box-shadow: 0px 6px 20px rgba(37, 99, 235, 0.5);
    letter-spacing: 0.5px;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%);
    transform: translateY(-2px);
}

.job-card {
    background: #0f172a; 
    border-left: 6px solid #2563eb;
    border-radius: 12px; 
    padding: 24px; 
    margin-top: 20px; 
    box-shadow: 0px 8px 30px rgba(0,0,0,0.5);
    border-top: 1px solid #1e293b;
    border-right: 1px solid #1e293b;
    border-bottom: 1px solid #1e293b;
}

.metric {
    background: #0f172a; 
    border-radius: 12px; 
    padding: 18px; 
    text-align: center; 
    border: 2px solid #1e293b;
}
.metric h2 {
    color: #38bdf8; 
    font-size: 26px; 
    margin: 0; 
    font-weight: 900;
}
.metric p {
    color: #94a3b8; 
    margin: 0; 
    font-weight: 800; 
    font-size: 12px;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# AUTHENTICATION SCREEN
# ---------------------------------------------------
if not st.session_state.logged_in:
    st.markdown("<div class='brand-logo'>EZITECH PORTAL</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-title'>🔐 Portal Authentication</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Secure access control for Students, Mentors, and Administrators.</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("<div class='section-title'>Select Options</div>", unsafe_allow_html=True)
        auth_mode = st.radio("Choose Action", ["Login", "Sign Up"], horizontal=True)
        role = st.selectbox("Select Role", ["Student", "Mentor", "Admin"])
        
    with col2:
        if auth_mode == "Login":
            st.markdown(f"<div class='section-title'>{role} Portal Login</div>", unsafe_allow_html=True)
            with st.form("login_form"):
                email = st.text_input("Email Address")
                password = st.text_input("Password", type="password")
                submit_login = st.form_submit_button("Login")
                
                if submit_login:
                    user = authenticate_user(email, password, role)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_role = role
                        st.session_state.user_name = user[1]
                        st.success(f"Welcome back, {user[1]}!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials or role mismatch!")
        else:
            st.markdown(f"<div class='section-title'>{role} Registration</div>", unsafe_allow_html=True)
            with st.form("signup_form"):
                name = st.text_input("Full Name")
                email = st.text_input("Email Address")
                password = st.text_input("Password", type="password")
                submit_signup = st.form_submit_button("Register")
                
                if submit_signup:
                    if name and email and password:
                        success, msg = register_user(name, email, password, role)
                        if success:
                            st.success(msg + " Please switch to Login tab.")
                        else:
                            st.error(msg)
                    else:
                        st.warning("Please fill all fields.")

else:
    # ---------------------------------------------------
    # MAIN PORTAL (After Successful Authentication)
    # ---------------------------------------------------
    st.sidebar.markdown(f"**Logged in as:** {st.session_state.user_name}")
    st.sidebar.markdown(f"**Role:** {st.session_state.user_role}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.user_name = ""
        st.rerun()

    st.markdown("<div class='brand-logo'>EZITECH PORTAL</div>", unsafe_allow_html=True)
    
    # ---------------------------------------------------
    # STUDENT VIEW
    # ---------------------------------------------------
    if st.session_state.user_role == "Student":
        st.markdown(f"<div class='main-title'>Welcome, {st.session_state.user_name}!</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>Here is an overview of your internship application, vector recommendation, and final phase status.</div>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("<div class='metric'><p>Resume Status</p><h2>Verified</h2></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='metric'><p>Recommended Track</p><h2>GenAI / LLMs</h2></div>", unsafe_allow_html=True)
        with c3:
            st.markdown("<div class='metric'><p>Mentor Assigned</p><h2>Dr. Hamera Javed</h2></div>", unsafe_allow_html=True)
        with c4:
            user_sub_status = "Pending"
            for sub in st.session_state.submissions:
                if sub["student_name"].lower() == st.session_state.user_name.lower():
                    user_sub_status = sub["status"]
            st.markdown(f"<div class='metric'><p>Project Status</p><h2>{user_sub_status}</h2></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        tab_dash, tab_rec, tab_roadmap, tab_phase3, tab_certs = st.tabs([
            "📊 Dashboard Overview", 
            "🔍 Match & Recommendation", 
            "🗺️ Roadmap", 
            "🚀 Phase 3: Final Deployment", 
            "📜 Certificates"
        ])

        with tab_dash:
            st.markdown("<div class='section-title'>Student Activity Hub</div>", unsafe_allow_html=True)
            st.info("Monitor your overall progress across modules, execute semantic matching, and complete final phase requirements.")

        with tab_rec:
            st.markdown("<div class='section-title'>AI Matching & Recommendation Engine</div>", unsafe_allow_html=True)
            left, right = st.columns([1, 1.2], gap="large")

            with left:
                st.markdown("### Candidate Profile Submission")
                with st.form("profile_form"):
                    skills_input = st.text_input("Technical Skills", placeholder="Python, LangChain, Machine Learning, Streamlit...")
                    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
                    github_url = st.text_input("GitHub Profile URL", placeholder="https://github.com/username")
                    st.markdown("<br>", unsafe_allow_html=True)
                    analyze = st.form_submit_button("Analyze & Match Track")

            with right:
                st.markdown("### Evaluation Results")
                if analyze:
                    is_github_valid = validate_github_url(github_url)
                    if not is_github_valid:
                        st.error("❌ **Invalid GitHub URL!** Please provide a valid URL starting with `https://github.com/`")
                    elif not skills_input and not resume_file:
                        st.warning("⚠️ Please provide either technical skills or upload your resume PDF to proceed.")
                    else:
                        with st.spinner("Step 1/3: Parsing Candidate Resume PDF..."):
                            time.sleep(0.3)
                            resume_text = extract_text_from_pdf(resume_file) if resume_file else ""
                        with st.spinner("Step 2/3: Analyzing Skills & Processing Profile Context..."):
                            time.sleep(0.3)
                            fused_profile_data = analyze_and_extract_skills(resume_text, skills_input)
                        with st.spinner("Step 3/3: Running ChromaDB Semantic Search & Vector Matching..."):
                            time.sleep(0.3)
                            search_results = run_vector_semantic_search(fused_profile_data)
                        
                        st.success("✅ **Enterprise Evaluation Completed Successfully!**")
                        st.progress(0.95)
                        
                        if search_results and 'metadatas' in search_results and len(search_results['metadatas'][0]) > 0:
                            for i in range(len(search_results['metadatas'][0])):
                                meta = search_results['metadatas'][0][i]
                                distance = search_results['distances'][0][i] if 'distances' in search_results else 0.15
                                match_score = max(80, int(100 - (distance * 45)))
                                
                                st.markdown(f"""
                                <div class='job-card'>
                                <h3>{meta['title']}</h3>
                                <p style='line-height:1.7;'>
                                <b>Organization:</b> {meta['company']}<br>
                                <b>Compatibility Match:</b> <span style='color:#38bdf8; font-weight:900;'>{match_score}%</span><br>
                                <b>Assigned Mentor:</b> {meta['mentor']}<br>
                                <b>Required Stack:</b> {meta['skills']}<br>
                                </p>
                                </div>
                                """, unsafe_allow_html=True)
                else:
                    st.info("💡 **Submit candidate details on the left panel to execute separated CV parsing, skill evaluation, and vector matching.**")

        with tab_roadmap:
            st.markdown("<div class='section-title'>Learning & Internship Roadmap</div>", unsafe_allow_html=True)
            st.success("✅ **Phase 1:** Core Foundations & Environment Setup (Completed)")
            st.success("✅ **Phase 2:** RAG Pipelines, Fine-Tuning & Multi-Role Integration (Completed)")
            st.info("🔄 **Phase 3:** Final Cloud Deployment, System Evaluation & Capstone Presentation (Active)")

        with tab_phase3:
            st.markdown("<div class='section-title'>🚀 Phase 3: Final Deployment & Evaluation Module</div>", unsafe_allow_html=True)
            st.write("Submit your final project repository link and deployment URL for final mentor review.")
            
            with st.form("phase3_submission"):
                final_repo = st.text_input("GitHub Repository URL (Capstone Project)", placeholder="https://github.com/username/project-repo")
                live_url = st.text_input("Live Application URL (Streamlit Cloud / Render / HuggingFace)", placeholder="https://share.streamlit.io/...")
                project_notes = st.text_area("Implementation Summary & Key Highlights", placeholder="Briefly explain the architecture and tech stack used...")
                submit_capstone = st.form_submit_button("Submit Capstone for Final Evaluation")
                
                if submit_capstone:
                    if final_repo and live_url:
                        existing = False
                        for sub in st.session_state.submissions:
                            if sub["student_name"].lower() == st.session_state.user_name.lower():
                                sub["repo"] = final_repo
                                sub["live_url"] = live_url
                                sub["notes"] = project_notes
                                sub["status"] = "Under Review"
                                existing = True
                        if not existing:
                            st.session_state.submissions.append({
                                "student_name": st.session_state.user_name,
                                "track": "Generative AI Intern",
                                "repo": final_repo,
                                "live_url": live_url,
                                "notes": project_notes,
                                "status": "Under Review",
                                "feedback": ""
                            })
                        st.success("🎉 **Capstone Submitted Successfully!** Forwarded to Dr. Hamera Javed for evaluation.")
                    else:
                        st.warning("⚠️ Please provide both the GitHub repository and live deployment URL.")

        with tab_certs:
            st.markdown("<div class='section-title'>📜 Certificates & Achievements</div>", unsafe_allow_html=True)
            is_approved = False
            mentor_feedback = ""
            for sub in st.session_state.submissions:
                if sub["student_name"].lower() == st.session_state.user_name.lower():
                    if sub["status"] == "Approved":
                        is_approved = True
                        mentor_feedback = sub["feedback"]
            
            if is_approved:
                st.success("🏆 **Congratulations! Your capstone project has been approved by your mentor.**")
                st.info(f"**Mentor Comments:** {mentor_feedback}")
                st.balloons()
                st.button("Download Official Completion Certificate (PDF)")
            else:
                st.info("Your official internship completion certificate will become downloadable here once your Phase 3 submission is approved and commented on by your assigned mentor.")

    # ---------------------------------------------------
    # MENTOR VIEW
    # ---------------------------------------------------
    elif st.session_state.user_role == "Mentor":
        st.markdown(f"<div class='main-title'>👨‍🏫 Mentor Portal Dashboard ({st.session_state.user_name})</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>Review assigned student capstone submissions, evaluate code, accept/reject, and provide feedback.</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>Assigned Students & Capstone Submissions</div>", unsafe_allow_html=True)

        if not st.session_state.submissions:
            st.info("No student submissions found yet.")
        else:
            for idx, sub in enumerate(st.session_state.submissions):
                with st.container():
                    st.markdown(f"""
                    <div class='job-card'>
                    <h3>Student: {sub['student_name'].capitalize()} ({sub['track']})</h3>
                    <p style='line-height:1.7;'>
                    <b>GitHub Repository:</b> <a href='{sub['repo']}' target='_blank'>{sub['repo']}</a><br>
                    <b>Live Deployment:</b> <a href='{sub['live_url']}' target='_blank'>{sub['live_url']}</a><br>
                    <b>Summary Notes:</b> {sub['notes']}<br>
                    <b>Current Status:</b> <span style='color:#38bdf8; font-weight:900;'>{sub['status']}</span><br>
                    <b>Existing Feedback:</b> {sub['feedback'] if sub['feedback'] else 'None provided yet.'}
                    </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.form(f"eval_form_{idx}"):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            action = st.selectbox("Action", ["Pending", "Approved", "Rejected"], index=["Pending", "Approved", "Rejected"].index(sub['status']))
                        with col_b:
                            feedback_input = st.text_input("Mentor Comments & Feedback", value=sub['feedback'])
                        
                        update_btn = st.form_submit_button("Submit Evaluation & Feedback")
                        
                        if update_btn:
                            sub['status'] = action
                            sub['feedback'] = feedback_input
                            st.success(f"Successfully updated evaluation for {sub['student_name']}!")
                            st.rerun()

    # ---------------------------------------------------
    # ADMIN VIEW (Enhanced with Full Stats & Charts)
    # ---------------------------------------------------
    elif st.session_state.user_role == "Admin":
        st.markdown(f"<div class='main-title'>🛠️ Admin Intelligence Dashboard ({st.session_state.user_name})</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>Comprehensive overview of platform demographics, domain distributions, and vector tracking metrics.</div>", unsafe_allow_html=True)
        
        # Row 1: Key Metrics (Total Students, AI, ML, CV, Web, Recommendations, Mentors)
        st.markdown("<div class='section-title'>System Analytics Overview</div>", unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("<div class='metric'><p>Total Students</p><h2>42</h2></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='metric'><p>AI Tracks (GenAI)</p><h2>14</h2></div>", unsafe_allow_html=True)
        with c3:
            st.markdown("<div class='metric'><p>ML Tracks</p><h2>12</h2></div>", unsafe_allow_html=True)
        with c4:
            st.markdown("<div class='metric'><p>Computer Vision (CV)</p><h2>8</h2></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        c5, c6, c7, c8 = st.columns(4)
        with c5:
            st.markdown("<div class='metric'><p>Web & Full Stack</p><h2>8</h2></div>", unsafe_allow_html=True)
        with c6:
            st.markdown("<div class='metric'><p>Total Recommendations</p><h2>128</h2></div>", unsafe_allow_html=True)
        with c7:
            st.markdown("<div class='metric'><p>Active Mentors</p><h2>3</h2></div>", unsafe_allow_html=True)
        with c8:
            approved_total = sum(1 for s in st.session_state.submissions if s['status'] == 'Approved')
            st.markdown(f"<div class='metric'><p>Approved Capstones</p><h2>{approved_total}</h2></div>", unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)

        # Row 2: Visual Charts & Domain Breakdown
        st.markdown("<div class='section-title'>Domain Enrollment & Performance Visualizer</div>", unsafe_allow_html=True)
        
        chart_col1, chart_col2 = st.columns(2, gap="large")
        
        with chart_col1:
            st.markdown("### 📊 Domain Distribution (Student Count)")
            domain_data = {
                "Generative AI": 14,
                "Machine Learning": 12,
                "Computer Vision": 8,
                "Web & Full Stack": 8
            }
            st.bar_chart(domain_data)
            
        with chart_col2:
            st.markdown("### 📈 Vector Matching Activity Trend")
            activity_trend = {
                "Phase 1 Setup": 42,
                "Phase 2 RAG": 38,
                "Phase 3 Capstone": len(st.session_state.submissions)
            }
            st.bar_chart(activity_trend)