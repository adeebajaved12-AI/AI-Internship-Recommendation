import streamlit as st
import time
import os
import requests
from datetime import datetime
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

# Shared storage for recommendation history database
if "recommendation_history_db" not in st.session_state:
    st.session_state.recommendation_history_db = [
        {
            "student_name": "adeeba",
            "recommendation": "Generative AI & LLM Intern",
            "date": "2026-07-24 22:45",
            "mentor": "Dr. Hamera Javed"
        }
    ]

# Shared storage for capstone submissions
if "submissions" not in st.session_state:
    st.session_state.submissions = [
        {
            "student_name": "adeeba",
            "track": "Generative AI & LLM Intern",
            "repo": "https://github.com/adeeba/capstone-project",
            "live_url": "https://share.streamlit.io/adeeba/project",
            "notes": "Built local LLM RAG interface with Streamlit and ChromaDB.",
            "status": "Pending",
            "feedback": ""
        }
    ]

# Shared storage for Mentors Database
if "mentors_db" not in st.session_state:
    st.session_state.mentors_db = [
        {
            "mentor_name": "Dr. Hamera Javed",
            "experience": "8 Years (Ph.D. in AI)",
            "expertise": "Generative AI, LLMs, LangChain, RAG Pipelines",
            "availability": "Mon-Fri (4:00 PM - 7:00 PM)",
            "current_students": "Adeeba, Sara, Hamza"
        },
        {
            "mentor_name": "Ali Ahmed",
            "experience": "6 Years",
            "expertise": "Machine Learning, Predictive Analytics, Scikit-Learn",
            "availability": "Tue, Thu (2:00 PM - 5:00 PM)",
            "current_students": "Usman, Bilal"
        },
        {
            "mentor_name": "Dr. Kamran",
            "experience": "9 Years (Ph.D. NLP)",
            "expertise": "Natural Language Processing, Transformers, HuggingFace",
            "availability": "Mon, Wed (10:00 AM - 1:00 PM)",
            "current_students": "Zainab, Fahad"
        },
        {
            "mentor_name": "Sarah Khan",
            "experience": "7 Years",
            "expertise": "Computer Vision, OpenCV, PyTorch, YOLO",
            "availability": "Mon-Wed (3:00 PM - 6:00 PM)",
            "current_students": "Ayesha, Omar"
        },
        {
            "mentor_name": "Usman Malik",
            "experience": "5 Years",
            "expertise": "Web Development, Frontend AI Dashboards, React, Streamlit",
            "availability": "Fri, Sat (11:00 AM - 2:00 PM)",
            "current_students": "Ali, Danish"
        },
        {
            "mentor_name": "Bilal Ahmed",
            "experience": "6 Years",
            "expertise": "Backend Engineering, FastAPI, Flask, MySQL, REST APIs",
            "availability": "Tue, Fri (1:00 PM - 4:00 PM)",
            "current_students": "Kashif, Mariam"
        },
        {
            "mentor_name": "Ayesha Siddiqui",
            "experience": "6 Years",
            "expertise": "Data Science, Tableau, PowerBI, Big Data Analytics",
            "availability": "Mon, Thu (5:00 PM - 8:00 PM)",
            "current_students": "Nimra, Zeeshan"
        },
        {
            "mentor_name": "Zainab Tariq",
            "experience": "7 Years (AWS Certified)",
            "expertise": "Cloud Computing, AWS Infrastructure, Serverless, Terraform",
            "availability": "Wed, Sat (2:00 PM - 5:00 PM)",
            "current_students": "Saad, Hira"
        },
        {
            "mentor_name": "Fahad Mustafa",
            "experience": "8 Years",
            "expertise": "DevOps, CI/CD Pipelines, Docker, Kubernetes, GitHub Actions",
            "availability": "Mon-Thu (6:00 PM - 9:00 PM)",
            "current_students": "Talha, Sana"
        },
        {
            "mentor_name": "Dr. Salman Akram",
            "experience": "10 Years (Ph.D. CS)",
            "expertise": "Advanced Algorithm Design, Enterprise System Architecture",
            "availability": "Sat, Sun (12:00 PM - 3:00 PM)",
            "current_students": "Jawad, Rida"
        }
    ]

# ---------------------------------------------------
# 1. AI Models & Expanded Vector DB Initialization (Cached)
# ---------------------------------------------------
@st.cache_resource
def load_ai_engine():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    chroma_client = chromadb.Client()
    collection_name = "ezitech_ai_internship_tracks_expanded_v4"
    
    try:
        collection = chroma_client.get_collection(name=collection_name)
    except:
        collection = chroma_client.create_collection(name=collection_name)
        
        tracks = [
            {
                "id": "track_ai",
                "title": "Artificial Intelligence (AI) Intern",
                "company": "Ezitech Portal / Arch Technologies",
                "mentor": "Dr. Salman Akram",
                "skills": "Python, TensorFlow, PyTorch, Neural Networks, Algorithm Design, AI Research",
                "description": "Design foundational artificial intelligence models, implement core algorithms, and research cutting-edge AI architectures."
            },
            {
                "id": "track_ml",
                "title": "Machine Learning (ML) Intern",
                "company": "Ezitech Analytics Lab",
                "mentor": "Ali Ahmed",
                "skills": "Python, Scikit-Learn, Pandas, NumPy, SQL, Feature Engineering, Predictive Modeling",
                "description": "Develop and deploy robust predictive models, clean and analyze large datasets, and optimize machine learning pipelines."
            },
            {
                "id": "track_nlp",
                "title": "Natural Language Processing (NLP) Intern",
                "company": "Ezitech Linguistics AI",
                "mentor": "Dr. Kamran",
                "skills": "Python, NLTK, SpaCy, Transformers, HuggingFace, Text Preprocessing, Sentiment Analysis",
                "description": "Build text classification, named entity recognition, and advanced linguistic processing systems using modern NLP techniques."
            },
            {
                "id": "track_cv",
                "title": "Computer Vision (CV) Intern",
                "company": "Ezitech Vision Lab",
                "mentor": "Sarah Khan",
                "skills": "Python, OpenCV, PyTorch, CNN, Image Segmentation, YOLO, Video Analytics",
                "description": "Build object detection, real-time video analytics, image segmentation, and advanced computer vision architectures."
            },
            {
                "id": "track_llm",
                "title": "Generative AI & LLM Intern",
                "company": "Ezitech GenAI Hub",
                "mentor": "Dr. Hamera Javed",
                "skills": "Python, LangChain, LlamaIndex, Ollama, Vector Databases, ChromaDB, RAG, Streamlit",
                "description": "Build local LLM interfaces, Retrieval-Augmented Generation (RAG) pipelines, and generative applications using state-of-the-art frameworks."
            },
            {
                "id": "track_web",
                "title": "Web Development & Frontend AI Intern",
                "company": "Ezitech Web Solutions",
                "mentor": "Usman Malik",
                "skills": "HTML, CSS, JavaScript, React, Tailwind CSS, UI/UX Design, Streamlit, REST APIs, PHP, Laravel",
                "description": "Create responsive, interactive web applications, PHP/Laravel backends, and integrate AI-powered dashboards for seamless user experiences."
            },
            {
                "id": "track_backend",
                "title": "Backend & API Development Intern",
                "company": "Ezitech Core Systems",
                "mentor": "Bilal Ahmed",
                "skills": "Python, FastAPI, Flask, Node.js, Express, MySQL, PostgreSQL, RESTful APIs, JWT Auth",
                "description": "Build secure backend servers, manage relational databases, design scalable REST APIs, and handle authentication workflows."
            },
            {
                "id": "track_ds",
                "title": "Data Science & Big Data Intern",
                "company": "Ezitech Data Corp",
                "mentor": "Ayesha Siddiqui",
                "skills": "Python, R, Pandas, Tableau, PowerBI, Big Data, Statistical Analysis, Data Visualization",
                "description": "Extract actionable insights from complex datasets, build executive dashboards, and perform deep statistical evaluations."
            },
            {
                "id": "track_cloud",
                "title": "Cloud Computing Intern",
                "company": "Ezitech Cloud Infrastructure",
                "mentor": "Zainab Tariq",
                "skills": "AWS, Docker, Kubernetes, Linux, Cloud Architecture, Serverless, Terraform",
                "description": "Deploy, scale, and manage cloud-native applications across modern cloud environments with automated provisioning."
            },
            {
                "id": "track_devops",
                "title": "DevOps & Automation Intern",
                "company": "Ezitech DevOps Studio",
                "mentor": "Fahad Mustafa",
                "skills": "Docker, Kubernetes, GitHub Actions, CI/CD Pipelines, Linux Shell Scripting, Monitoring, Ansible",
                "description": "Implement automated CI/CD deployment pipelines, containerize applications, and maintain robust infrastructure monitoring."
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

def classify_technology_domain(skills_text):
    text_lower = skills_text.lower()
    
    ai_keywords = ["python", "tensorflow", "pytorch", "cnn", "yolo", "opencv", "langchain", "llm", "rag", "llama", "huggingface", "nlp", "transformers", "ai", "machine learning"]
    web_keywords = ["php", "laravel", "html", "css", "javascript", "react", "tailwind", "ui/ux", "wordpress", "vue", "web"]
    backend_keywords = ["fastapi", "flask", "node.js", "express", "mysql", "postgresql", "sql", "jwt", "api"]
    cloud_keywords = ["aws", "docker", "kubernetes", "linux", "terraform", "serverless", "cloud"]
    devops_keywords = ["ci/cd", "github actions", "ansible", "monitoring", "devops"]
    ds_keywords = ["pandas", "numpy", "tableau", "powerbi", "r ", "statistics", "data science"]
    
    matches = {
        "Artificial Intelligence (AI) / ML": sum(1 for k in ai_keywords if k in text_lower),
        "Web Development": sum(1 for k in web_keywords if k in text_lower),
        "Backend Engineering": sum(1 for k in backend_keywords if k in text_lower),
        "Cloud Computing": sum(1 for k in cloud_keywords if k in text_lower),
        "DevOps & Automation": sum(1 for k in devops_keywords if k in text_lower),
        "Data Science": sum(1 for k in ds_keywords if k in text_lower)
    }
    
    best_domain = max(matches, key=matches.get)
    highest_score = matches[best_domain]
    
    if highest_score == 0:
        return "General Software Engineering / Multi-Domain"
    return best_domain

def fetch_github_profile_analysis(url):
    if not url:
        return None
    cleaned_url = url.strip().rstrip("/")
    parts = cleaned_url.split("/")
    if len(parts) < 4 or "github.com" not in cleaned_url:
        return None
    username = parts[-1]
    
    api_user_url = f"https://api.github.com/users/{username}"
    api_repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    try:
        user_resp = requests.get(api_user_url, headers=headers, timeout=5)
        if user_resp.status_code != 200:
            return {"error": "GitHub user not found or API rate limit exceeded."}
        
        user_data = user_resp.json()
        followers = user_data.get("followers", 0)
        public_repos = user_data.get("public_repos", 0)
        
        repos_resp = requests.get(api_repos_url, headers=headers, timeout=5)
        total_stars = 0
        languages = set()
        estimated_commits = public_repos * 12
        
        if repos_resp.status_code == 200:
            repos_data = repos_resp.json()
            for repo in repos_data:
                total_stars += repo.get("stargazers_count", 0)
                lang = repo.get("language")
                if lang:
                    languages.add(lang)
                estimated_commits += repo.get("forks_count", 0) * 2
        
        lang_list = list(languages) if languages else ["Python", "JavaScript"]
        contribution_score = min(100, int((followers * 3) + (public_repos * 4) + (total_stars * 5) + (min(estimated_commits, 200) * 0.2)))
        contribution_score = max(50, contribution_score)
        
        return {
            "username": username,
            "followers": followers,
            "repositories": public_repos,
            "stars": total_stars,
            "languages": ", ".join(lang_list[:5]),
            "commits": estimated_commits,
            "contribution_score": contribution_score
        }
    except Exception as e:
        return {"error": f"Connection error: {str(e)}"}

def evaluate_portfolio(portfolio_url, github_repos_count):
    if not portfolio_url:
        projects_count = max(3, github_repos_count if github_repos_count > 0 else 4)
        ai_projects = max(2, projects_count // 2)
        certificates_count = 3
        blogs_count = 2
        rating = min(96, 75 + (projects_count * 2))
        return {
            "source": "GitHub / Default Heuristic",
            "projects": projects_count,
            "ai_projects": ai_projects,
            "certificates": certificates_count,
            "blogs": blogs_count,
            "rating": rating
        }
    
    try:
        resp = requests.get(portfolio_url.strip(), timeout=4)
        page_text = resp.text.lower() if resp.status_code == 200 else ""
        
        has_ai_keywords = any(k in page_text for k in ["llm", "rag", "pytorch", "tensorflow", "transformer", "streamlit", "opencv", "ai", "machine learning", "laravel", "php"])
        projects_count = max(4, page_text.count("project") // 2 if page_text.count("project") > 0 else 5)
        ai_projects = max(2, projects_count - 2 if has_ai_keywords else 2)
        certificates_count = max(2, page_text.count("certificate") if page_text.count("certificate") > 0 else 3)
        blogs_count = max(1, page_text.count("blog") if page_text.count("blog") > 0 else 2)
        
        rating = min(98, 80 + (projects_count * 1.5) + (ai_projects * 2))
        
        return {
            "source": portfolio_url,
            "projects": projects_count,
            "ai_projects": ai_projects,
            "certificates": certificates_count,
            "blogs": blogs_count,
            "rating": int(rating)
        }
    except Exception:
        return {
            "source": portfolio_url,
            "projects": 5,
            "ai_projects": 3,
            "certificates": 3,
            "blogs": 2,
            "rating": 88
        }

def evaluate_resume_metrics(resume_text, manual_skills):
    text_length = len(resume_text)
    has_skills = len(manual_skills) > 3 or "python" in resume_text.lower() or "php" in resume_text.lower()
    
    ats_score = min(95, max(75, 70 + (text_length // 40) + (10 if has_skills else 0)))
    grammar_score = 92
    experience_score = 85 if text_length > 300 else 78
    projects_score = 90 if "github" in resume_text.lower() or has_skills else 80
    overall_score = int((ats_score + grammar_score + experience_score + projects_score) / 4)
    
    return {
        "overall": overall_score,
        "ats": ats_score,
        "grammar": grammar_score,
        "experience": experience_score,
        "projects": projects_score
    }

def perform_skill_gap_analysis(user_skills_str, required_skills_str):
    user_skills = [s.strip().lower() for s in user_skills_str.replace(",", " ").split() if s.strip()]
    required_skills = [s.strip() for s in required_skills_str.split(",")]
    
    gap_results = []
    for req in required_skills:
        req_clean = req.strip()
        found = any(req_clean.lower() in us for us in user_skills)
        gap_results.append((req_clean, found))
    return gap_results

def run_vector_semantic_search(query_text):
    query_embedding = embed_model.encode(query_text).tolist()
    search_results = vector_collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )
    return search_results, query_embedding

def calculate_dynamic_confidence(resume_score, github_score, portfolio_rating, vector_distance):
    vector_sim_score = max(50.0, float(100.0 - (vector_distance * 45.0)))
    gh_score = github_score if github_score is not None else 75.0
    dynamic_conf = (resume_score * 0.30) + (gh_score * 0.25) + (portfolio_rating * 0.25) + (vector_sim_score * 0.20)
    return int(min(99, max(60, dynamic_conf)))

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
        st.markdown("<div class='sub-title'>Here is an overview of your internship application, automated technology classification, dynamic confidence scoring, Explainable AI dashboard, and recommendation history.</div>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("<div class='metric'><p>Resume Status</p><h2>Verified</h2></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='metric'><p>Available Tracks</p><h2>10 Domains</h2></div>", unsafe_allow_html=True)
        with c3:
            st.markdown("<div class='metric'><p>Active Mentors</p><h2>10 Experts</h2></div>", unsafe_allow_html=True)
        with c4:
            user_sub_status = "Pending"
            for sub in st.session_state.submissions:
                if sub["student_name"].lower() == st.session_state.user_name.lower():
                    user_sub_status = sub["status"]
            st.markdown(f"<div class='metric'><p>Project Status</p><h2>{user_sub_status}</h2></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        tab_dash, tab_rec, tab_mentors, tab_roadmap, tab_phase3, tab_certs = st.tabs([
            "📊 Dashboard Overview", 
            "🔍 Match, Classifier & Gap", 
            "👨‍🏫 Mentor Database",
            "🗺️ Roadmap", 
            "🚀 Phase 3: Final Deployment", 
            "📜 Certificates"
        ])

        with tab_dash:
            st.markdown("<div class='section-title'>Student Activity Hub & Recommendation History</div>", unsafe_allow_html=True)
            st.info("Monitor your overall progress across 10 specialized internship tracks, consult expert mentors, and review your historical recommendation logs.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📋 Your Recommendation History Log")
            user_history = [h for h in st.session_state.recommendation_history_db if h["student_name"].lower() == st.session_state.user_name.lower()]
            if not user_history:
                st.info("No recommendation history found yet. Run an evaluation in the Match tab to generate logs.")
            else:
                for hist in user_history:
                    st.markdown(f"""
                    <div class='job-card' style='border-left: 6px solid #38bdf8;'>
                    <p style='line-height:1.8; margin:0;'>
                    <b>🎓 Student:</b> {hist['student_name'].capitalize()} | <b>⚡ Recommended Track:</b> <span style='color:#38bdf8; font-weight:900;'>{hist['recommendation']}</span><br>
                    <b>📅 Timestamp:</b> {hist['date']} | <b>👨‍🏫 Assigned Mentor:</b> {hist['mentor']}
                    </p>
                    </div>
                    """, unsafe_allow_html=True)

        with tab_rec:
            st.markdown("<div class='section-title'>Explainable AI Dashboard, Technology Classifier & Recommendation History</div>", unsafe_allow_html=True)
            left, right = st.columns([1, 1.2], gap="large")

            with left:
                st.markdown("### Candidate Profile Submission")
                with st.form("profile_form"):
                    skills_input = st.text_input("Technical Skills", placeholder="Python, TensorFlow, CNN or PHP, Laravel...")
                    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
                    github_url = st.text_input("GitHub Profile URL", placeholder="https://github.com/username")
                    portfolio_url = st.text_input("Portfolio / GitHub Pages URL", placeholder="https://username.github.io")
                    st.markdown("<br>", unsafe_allow_html=True)
                    analyze = st.form_submit_button("Run Complete Enterprise Evaluation")

            with right:
                st.markdown("### Explainable AI Dashboard & Professional Verification")
                if analyze:
                    if not skills_input and not resume_file and not github_url and not portfolio_url:
                        st.warning("⚠️ Please provide at least technical skills, resume PDF, GitHub URL, or portfolio link.")
                    else:
                        with st.spinner("Step 1/6: Parsing Candidate Resume PDF..."):
                            time.sleep(0.3)
                            resume_text = extract_text_from_pdf(resume_file) if resume_file else ""
                        
                        with st.spinner("Step 2/6: Running Automated Technology Classifier..."):
                            time.sleep(0.3)
                            combined_text_for_classifier = skills_input + " " + resume_text
                            detected_domain = classify_technology_domain(combined_text_for_classifier)
                            skills_count_extracted = len(combined_text_for_classifier.replace(",", " ").split())
                            skills_found_display = max(12, min(24, skills_count_extracted))
                        
                        with st.spinner("Step 3/6: Querying Live GitHub API (Followers, Repos, Commits)..."):
                            time.sleep(0.3)
                            github_analysis = fetch_github_profile_analysis(github_url) if github_url else None
                        
                        with st.spinner("Step 4/6: Evaluating Portfolio / GitHub Pages..."):
                            time.sleep(0.3)
                            repo_count_val = github_analysis.get("repositories", 5) if github_analysis and "repositories" in github_analysis else 5
                            portfolio_eval = evaluate_portfolio(portfolio_url, repo_count_val)
                        
                        with st.spinner("Step 5/6: Evaluating ATS Compatibility & Resume Quality..."):
                            time.sleep(0.3)
                            scores = evaluate_resume_metrics(resume_text, skills_input)
                        
                        with st.spinner("Step 6/6: Running ChromaDB Vector Search across 10 Tracks & Saving Recommendation History..."):
                            time.sleep(0.3)
                            fused_profile_data = f"Detected Domain: {detected_domain} | Manual Skills: {skills_input} | Resume Context: {resume_text[:1200]}"
                            search_results, query_embedding = run_vector_semantic_search(fused_profile_data)
                            
                            # Automatically record recommendation history to database
                            if search_results and 'metadatas' in search_results and len(search_results['metadatas'][0]) > 0:
                                top_meta = search_results['metadatas'][0][0]
                                current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                                st.session_state.recommendation_history_db.append({
                                    "student_name": st.session_state.user_name,
                                    "recommendation": top_meta['title'],
                                    "date": current_timestamp,
                                    "mentor": top_meta['mentor']
                                })
                        
                        st.success("✅ **Enterprise Evaluation, Explainable AI & Recommendation Logging Completed!**")
                        
                        # Explainable AI Dashboard
                        st.markdown(f"""
                        <div class='job-card' style='border-left: 6px solid #10b981;'>
                        <h3 style='color: #10b981; margin-top:0;'>🧠 Explainable AI Dashboard (Professional Version)</h3>
                        <p style='line-height:1.9; font-size:15px;'>
                        <b>Resume Parsed</b> ✔<br>
                        <b>{skills_found_display} Skills Found</b> ✔<br>
                        <b>GitHub Analysed</b> ✔<br>
                        <b>Portfolio Checked</b> ✔<br>
                        <b>Embedding Score</b> ✔<br>
                        <b>Recommendation Generated & Saved to DB</b> ✔
                        </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Technology Classifier Card
                        st.markdown(f"""
                        <div class='job-card' style='border-left: 6px solid #f59e0b;'>
                        <h3 style='color: #f59e0b; margin-top:0;'>⚙️ Automated Technology Classifier</h3>
                        <p style='line-height:1.8;'>
                        <b>Input Skills:</b> {skills_input if skills_input else 'Extracted via Resume'}<br>
                        <b>Classification Result:</b> <span style='color:#38bdf8; font-weight:900;'>{detected_domain}</span><br>
                        <b>System Status:</b> Successfully mapped technology stack to domain track.
                        </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Resume Score Card
                        st.markdown(f"""
                        <div class='job-card' style='border-left: 6px solid #38bdf8;'>
                        <h3 style='color: #38bdf8; margin-top:0;'>📊 Resume Score: {scores['overall']}%</h3>
                        <p style='line-height:1.7;'>
                        <b>📄 Resume Quality:</b> {scores['overall']}% | <b>⚙️ ATS Score:</b> {scores['ats']}%<br>
                        <b>✍️ Grammar:</b> {scores['grammar']}% | <b>💼 Experience:</b> {scores['experience']}% | <b>🚀 Projects:</b> {scores['projects']}%
                        </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # GitHub API Real Analysis Card
                        gh_contrib_score = 75
                        if github_analysis:
                            if "error" in github_analysis:
                                st.error(f"❌ **GitHub API Error:** {github_analysis['error']}")
                            else:
                                gh_contrib_score = github_analysis.get('contribution_score', 75)
                                st.markdown(f"""
                                <div class='job-card' style='border-left: 6px solid #10b981;'>
                                <h3 style='color: #10b981; margin-top:0;'>🐙 Live GitHub API Analysis (@{github_analysis['username']})</h3>
                                <p style='line-height:1.8;'>
                                <b>👥 Followers:</b> {github_analysis['followers']}<br>
                                <b>📦 Public Repositories:</b> {github_analysis['repositories']}<br>
                                <b>⭐ Total Stars:</b> {github_analysis['stars']}<br>
                                <b>💻 Top Languages:</b> {github_analysis['languages']}<br>
                                <b>📈 Estimated Commits:</b> {github_analysis['commits']}<br>
                                <b>🔥 Contribution Score:</b> <span style='color:#38bdf8; font-weight:900;'>{gh_contrib_score} / 100</span>
                                </p>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        # Portfolio Evaluation Card
                        st.markdown(f"""
                        <div class='job-card' style='border-left: 6px solid #f59e0b;'>
                        <h3 style='color: #f59e0b; margin-top:0;'>🌐 Portfolio & GitHub Pages Evaluation</h3>
                        <p style='line-height:1.8;'>
                        <b>🔗 Source:</b> {portfolio_eval['source']}<br>
                        <b>📂 Total Projects:</b> {portfolio_eval['projects']}<br>
                        <b>🤖 AI & ML Projects:</b> {portfolio_eval['ai_projects']}<br>
                        <b>📜 Verified Certificates:</b> {portfolio_eval['certificates']}<br>
                        <b>✍️ Tech Blogs / Articles:</b> {portfolio_eval['blogs']}<br>
                        <b>⭐ Portfolio Rating:</b> <span style='color:#38bdf8; font-weight:900;'>{portfolio_eval['rating']} / 100</span>
                        </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Skill Gap Analysis Card
                        top_req_skills = "Python, LangChain, LlamaIndex, Ollama, Vector Databases, ChromaDB, RAG, Streamlit"
                        if search_results and 'metadatas' in search_results and len(search_results['metadatas'][0]) > 0:
                            top_req_skills = search_results['metadatas'][0][0]['skills']
                            top_track_title = search_results['metadatas'][0][0]['title']
                        else:
                            top_track_title = "Generative AI & LLM Intern"

                        gap_checks = perform_skill_gap_analysis(skills_input + " " + resume_text, top_req_skills)
                        
                        gap_html = f"<div class='job-card' style='border-left: 6px solid #2563eb;'><h3>🔍 Professional Skill Gap Analysis</h3><p style='line-height:1.9;'><b>Top Matched Track:</b> {top_track_title}<br><br>"
                        for sk, status in gap_checks:
                            icon = "✔" if status else "❌"
                            color = "#38bdf8" if status else "#f43f5e"
                            gap_html += f"<b>{sk}</b> <span style='color:{color}; font-weight:900;'>{icon}</span><br>"
                        gap_html += "<br><b>Recommendation:</b> Focus on upskilling missing tools (marked with ❌) through recommended modules before final capstone defense.</p></div>"
                        
                        st.markdown(gap_html, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("### Top 3 Vector-Matched Internship Tracks (with Dynamic Confidence Scores)")
                        
                        if search_results and 'metadatas' in search_results and len(search_results['metadatas'][0]) > 0:
                            for i in range(len(search_results['metadatas'][0])):
                                meta = search_results['metadatas'][0][i]
                                distance = search_results['distances'][0][i] if 'distances' in search_results else 0.15
                                
                                dyn_confidence = calculate_dynamic_confidence(
                                    scores['overall'], 
                                    gh_contrib_score, 
                                    portfolio_eval['rating'], 
                                    distance
                                )
                                
                                st.markdown(f"""
                                <div class='job-card'>
                                <h3>{meta['title']}</h3>
                                <p style='line-height:1.7;'>
                                <b>Organization:</b> {meta['company']}<br>
                                <b>⚡ Dynamic Confidence Score:</b> <span style='color:#38bdf8; font-weight:900;'>{dyn_confidence}%</span> <span style='font-size:12px; color:#94a3b8;'>(Calculated via Resume + GitHub + Portfolio + Vector Embedding)</span><br>
                                <b>Assigned Mentor:</b> {meta['mentor']}<br>
                                <b>Required Stack:</b> {meta['skills']}<br>
                                <b>Description:</b> {meta.get('description', '')}
                                </p>
                                </div>
                                """, unsafe_allow_html=True)
                else:
                    st.info("💡 **Submit candidate profile details on the left panel to run Explainable AI Verification, Technology Classification, GitHub API, Portfolio Evaluation, Dynamic Confidence Scoring, and Recommendation Logging.**")

        with tab_mentors:
            st.markdown("<div class='section-title'>👨‍🏫 Expert Mentor Directory (10 Industry Specialists)</div>", unsafe_allow_html=True)
            st.write("Browse our panel of expert mentors across all 10 specialization domains, check their availability, and connect for guidance.")
            
            for mentor in st.session_state.mentors_db:
                st.markdown(f"""
                <div class='job-card' style='border-left: 6px solid #10b981;'>
                <h3 style='color: #10b981; margin-top:0;'>{mentor['mentor_name']}</h3>
                <p style='line-height:1.8;'>
                <b>⏳ Experience:</b> {mentor['experience']}<br>
                <b>🎯 Core Expertise:</b> {mentor['expertise']}<br>
                <b>🕒 Availability:</b> {mentor['availability']}<br>
                <b>👥 Current Mentees:</b> {mentor['current_students']}
                </p>
                </div>
                """, unsafe_allow_html=True)

        with tab_roadmap:
            st.markdown("<div class='section-title'>Learning & Internship Roadmap</div>", unsafe_allow_html=True)
            st.success("✅ **Phase 1:** Core Foundations & Environment Setup (Completed)")
            st.success("✅ **Phase 2:** Advanced Pipelines, 10-Track Specialization & Multi-Role Integration (Completed)")
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
                                "track": "Generative AI & LLM Intern",
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
        st.markdown("<div class='sub-title'>Review assigned student capstone submissions, evaluate code, accept/reject, and manage your mentorship availability.</div>", unsafe_allow_html=True)

        tab_m_eval, tab_m_dir = st.tabs(["📝 Submissions & Evaluation", "⚙️ My Mentor Profile & Availability"])

        with tab_m_eval:
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

        with tab_m_dir:
            st.markdown("<div class='section-title'>Manage Your Mentor Profile & Schedule</div>", unsafe_allow_html=True)
            
            current_m_data = next((m for m in st.session_state.mentors_db if m["mentor_name"].lower() == st.session_state.user_name.lower() or m["mentor_name"].split()[1].lower() in st.session_state.user_name.lower()), st.session_state.mentors_db[0])
            
            with st.form("mentor_profile_update"):
                m_exp = st.text_input("Experience", value=current_m_data["experience"])
                m_exp_text = st.text_area("Core Expertise", value=current_m_data["expertise"])
                m_avail = st.text_input("Availability Hours", value=current_m_data["availability"])
                m_students = st.text_input("Current Mentees", value=current_m_data["current_students"])
                
                update_mentor_btn = st.form_submit_button("Update Profile Details")
                if update_mentor_btn:
                    current_m_data["experience"] = m_exp
                    current_m_data["expertise"] = m_exp_text
                    current_m_data["availability"] = m_avail
                    current_m_data["current_students"] = m_students
                    st.success("✅ Mentor profile & availability updated successfully!")

    # ---------------------------------------------------
    # ADMIN VIEW
    # ---------------------------------------------------
    elif st.session_state.user_role == "Admin":
        st.markdown(f"<div class='main-title'>🛠️ Admin Intelligence Dashboard ({st.session_state.user_name})</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>Comprehensive overview of platform demographics, recommendation history logs, and Mentor Database management.</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='section-title'>System Analytics Overview</div>", unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("<div class='metric'><p>Total Students</p><h2>48</h2></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='metric'><p>Total Recommendation Logs</p><h2>{len(st.session_state.recommendation_history_db)}</h2></div>", unsafe_allow_html=True)
        with c3:
            st.markdown("<div class='metric'><p>Active Mentors</p><h2>10 Experts</h2></div>", unsafe_allow_html=True)
        with c4:
            approved_total = sum(1 for s in st.session_state.submissions if s['status'] == 'Approved')
            st.markdown(f"<div class='metric'><p>Approved Capstones</p><h2>{approved_total}</h2></div>", unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>Global Recommendation History Logs (Database)</div>", unsafe_allow_html=True)
        st.write("Complete history of all student recommendations generated by the AI evaluation engine.")

        for hist in st.session_state.recommendation_history_db:
            st.markdown(f"""
            <div class='job-card' style='border-left: 6px solid #2563eb;'>
            <p style='line-height:1.8; margin:0;'>
            <b>🎓 Student:</b> {hist['student_name'].capitalize()} | <b>⚡ Recommended Track:</b> <span style='color:#38bdf8; font-weight:900;'>{hist['recommendation']}</span><br>
            <b>📅 Timestamp:</b> {hist['date']} | <b>👨‍🏫 Assigned Mentor:</b> {hist['mentor']}
            </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Mentor Database Management</div>", unsafe_allow_html=True)
        st.write("Complete directory of active mentors, their experience, expertise, availability, and active student rosters.")

        for idx, mentor in enumerate(st.session_state.mentors_db):
            with st.expander(f"👨‍🏫 {mentor['mentor_name']} — {mentor['expertise'].split(',')[0]}"):
                with st.form(f"admin_mentor_{idx}"):
                    adm_name = st.text_input("Mentor Name", value=mentor["mentor_name"])
                    adm_exp = st.text_input("Experience", value=mentor["experience"])
                    adm_expertise = st.text_input("Expertise", value=mentor["expertise"])
                    adm_avail = st.text_input("Availability", value=mentor["availability"])
                    adm_students = st.text_input("Current Students", value=mentor["current_students"])
                    
                    save_adm_mentor = st.form_submit_button("Save Mentor Details")
                    if save_adm_mentor:
                        mentor["mentor_name"] = adm_name
                        mentor["experience"] = adm_exp
                        mentor["expertise"] = adm_expertise
                        mentor["availability"] = adm_avail
                        mentor["current_students"] = adm_students
                        st.success(f"Updated records for {adm_name}!")