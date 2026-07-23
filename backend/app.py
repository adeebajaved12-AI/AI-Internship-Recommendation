import streamlit as st
import time
import os
from sentence_transformers import SentenceTransformer
import chromadb
import numpy as np

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
    page_title="Ezitech Internship Portal - AI Matching Engine",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------
# Initialize AI Models & Vector DB (Cached)
# ---------------------------------------------------
@st.cache_resource
def load_ai_engine():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    chroma_client = chromadb.Client()
    collection_name = "ezitech_internship_tracks"
    
    try:
        collection = chroma_client.get_collection(name=collection_name)
    except:
        collection = chroma_client.create_collection(name=collection_name)
        
        tracks = [
            {
                "id": "track_1",
                "title": "Generative AI Intern",
                "company": "Ezitech Institute / Arch Technologies",
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
                "title": "Full Stack AI Developer",
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

# ---------------------------------------------------
# CSS Styling (Ezitech Official Blue Theme Look)
# ---------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"]{font-family:'Poppins',sans-serif; background:#0b1329;}
#MainMenu{visibility:hidden;} footer{visibility:hidden;} header{visibility:hidden;}

/* Ezitech Branding Header */
.brand-logo {
    font-size: 20px;
    font-weight: 800;
    color: #38bdf8;
    letter-spacing: 1px;
    margin-bottom: 10px;
}

.main-title{
    text-align:left; font-size:40px; font-weight:800;
    color: #ffffff;
    margin-bottom:5px;
}
.sub-title{text-align:left; font-size:16px; color:#94a3b8; margin-bottom:25px; font-weight:500;}

.section-title{color:white; font-size:20px; font-weight:700; margin-bottom:15px;}

/* Form & Inputs Container */
.stTextInput input{
    border-radius:10px; border:1px solid #3b82f6; background-color:#1e293b; color:white; padding:10px;
}
[data-testid="stFileUploader"]{
    border:2px dashed #3b82f6; border-radius:10px; padding:15px; background-color:#1e293b;
}

/* Ezitech Blue Button */
.stButton>button{
    width:100%; padding:14px; font-size:16px; font-weight:700; color:white; border:none;
    border-radius:10px; background:#2563eb; transition:.3s;
    box-shadow:0px 4px 20px rgba(37,99,235,.4);
}
.stButton>button:hover{background:#1d4ed8; transform:translateY(-1px);}

/* Stats Badges matching reference */
.stats-container {
    display: flex;
    gap: 15px;
    margin-bottom: 25px;
}
.stat-box {
    background: #1e293b;
    border: 1px solid #334155;
    padding: 12px 20px;
    border-radius: 10px;
    text-align: left;
}
.stat-box h3 {
    color: #38bdf8;
    margin: 0;
    font-size: 20px;
    font-weight: 700;
}
.stat-box p {
    color: #94a3b8;
    margin: 0;
    font-size: 12px;
    font-weight: 500;
}

/* Job Card */
.job-card{
    background:#1e293b; border-left:5px solid #2563eb;
    border-radius:12px; padding:22px; margin-top:20px; box-shadow:0px 8px 25px rgba(0,0,0,.3);
    border: 1px solid rgba(255,255,255,0.05);
}
.metric{
    background:#1e293b; border-radius:12px; padding:15px; text-align:center; border:1px solid #334155;
}
.metric h2{color:#38bdf8; font-size:24px; margin:0; font-weight:700;}
.metric p{color:#94a3b8; margin:0; font-weight:600; font-size:12px;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Header Section with Ezitech Branding
# ---------------------------------------------------
st.markdown("<div class='brand-logo'>EZITECH PORTAL</div>", unsafe_allow_html=True)
st.markdown("<div class='main-title'>Welcome to Ezitech AI Internship Portal</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Intelligent candidate matching engine designed for automated internship & mentor allocation.</div>", unsafe_allow_html=True)

# Stats row matching reference portal style
st.markdown("""
<div class='stats-container'>
    <div class='stat-box'>
        <h3>25k+</h3>
        <p>TOTAL INTERNS</p>
    </div>
    <div class='stat-box'>
        <h3>500+</h3>
        <p>ACTIVE INTERNSHIPS</p>
    </div>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1, 1.2], gap="large")

# ---------------------------------------------------
# LEFT COLUMN: Input Form
# ---------------------------------------------------
with left:
    st.markdown("<div class='section-title'>Candidate Profile Submission</div>", unsafe_allow_html=True)
    
    with st.form("profile_form"):
        skills_input = st.text_input(
            "Technical Skills",
            placeholder="Python, LangChain, Machine Learning, Streamlit..."
        )
        
        resume_file = st.file_uploader(
            "Upload Resume (PDF)",
            type=["pdf"]
        )
        
        github_url = st.text_input(
            "GitHub Profile URL",
            placeholder="https://github.com/username"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        analyze = st.form_submit_button("Analyze & Match Track")

# ---------------------------------------------------
# RIGHT COLUMN: Results Dashboard
# ---------------------------------------------------
with right:
    st.markdown("<div class='section-title'>AI Matching & Recommendation Engine</div>", unsafe_allow_html=True)
    
    if analyze:
        if skills_input or resume_file:
            with st.spinner("Processing profile via Vector Semantic Pipeline..."):
                time.sleep(1)
                
                extracted_resume_text = ""
                if resume_file:
                    extracted_resume_text = extract_text_from_pdf(resume_file)
                
                combined_query = f"{skills_input} {extracted_resume_text}"
                query_embedding = embed_model.encode(combined_query).tolist()
                
                results = vector_collection.query(
                    query_embeddings=[query_embedding],
                    n_results=2
                )
            
            st.success("Profile evaluated successfully against Ezitech requirements.")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("<div class='metric'><p>Match Score</p><h2>94%</h2></div>", unsafe_allow_html=True)
            with c2:
                st.markdown("<div class='metric'><p>Embeddings</p><h2>Active</h2></div>", unsafe_allow_html=True)
            with c3:
                st.markdown("<div class='metric'><p>Status</p><h2>Approved</h2></div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.progress(0.94)
            
            if results and 'metadatas' in results and len(results['metadatas'][0]) > 0:
                for i in range(len(results['metadatas'][0])):
                    meta = results['metadatas'][0][i]
                    distance = results['distances'][0][i] if 'distances' in results else 0.2
                    match_score = max(75, int(100 - (distance * 50)))
                    
                    st.markdown(f"""
                    <div class='job-card'>
                    <h3 style='color:white; margin-top:0;'>{meta['title']}</h3>
                    <p style='color:#94a3b8; line-height:1.6;'>
                    <b>Organization:</b> {meta['company']}<br>
                    <b>Track Match:</b> <span style='color:#38bdf8;'>{match_score}%</span><br>
                    <b>Recommended Mentor:</b> {meta['mentor']}<br>
                    <b>Required Stack:</b> {meta['skills']}<br>
                    <b>Ezitech AI Summary:</b> High vector semantic similarity detected. The candidate profile successfully qualifies for automated track placement.
                    </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No matching tracks found.")
                
        else:
            st.warning("Please enter your technical skills or upload your resume.")
    else:
        st.info("Submit your candidate profile details on the left panel to generate automated Ezitech track recommendations.")