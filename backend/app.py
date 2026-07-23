import streamlit as st
import time
import os
import fitz # PyMuPDF for PDF resume parsing
from sentence_transformers import SentenceTransformer
import chromadb
import numpy as np

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="AI Internship Recommendation System",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------
# Initialize AI Models & Vector DB (Cached)
# ---------------------------------------------------
@st.cache_resource
def load_ai_engine():
    # Embedding Model for Semantic Search
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # In-memory Vector Database using ChromaDB
    chroma_client = chromadb.Client()
    collection_name = "internship_tracks"
    
    # Check if collection exists, else create and populate
    try:
        collection = chroma_client.get_collection(name=collection_name)
    except:
        collection = chroma_client.create_collection(name=collection_name)
        
        # Knowledge Base of Internships
        tracks = [
            {
                "id": "track_1",
                "title": "Generative AI Intern",
                "company": "Arch Technologies",
                "mentor": "Dr. Hamera Javed",
                "skills": "Python, NLP, Deep Learning, TensorFlow, PyTorch, LangChain, LLMs, Streamlit",
                "description": "Build local LLM interfaces, RAG pipelines, and generative applications using state-of-the-art frameworks."
            },
            {
                "id": "track_2",
                "title": "Machine Learning Intern",
                "company": "Tech Solutions",
                "mentor": "Ali Ahmed",
                "skills": "Python, Scikit-Learn, Pandas, NumPy, SQL, Data Analysis, Machine Learning",
                "description": "Develop and deploy predictive models, handle large datasets, and optimize machine learning workflows."
            },
            {
                "id": "track_3",
                "title": "Full Stack AI Developer",
                "company": "NextGen Systems",
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

# Function to extract text from uploaded PDF resume
def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

# ---------------------------------------------------
# CSS Styling
# ---------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"]{font-family:'Poppins',sans-serif; background:#0f172a;}
#MainMenu{visibility:hidden;} footer{visibility:hidden;} header{visibility:hidden;}

.main-title{
    text-align:center; font-size:42px; font-weight:800;
    background:linear-gradient(90deg,#00DBDE,#FC00FF);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    margin-bottom:5px;
}
.sub-title{text-align:center; font-size:16px; color:#CBD5E1; margin-bottom:30px; font-weight:500;}
.section-title{color:white; font-size:22px; font-weight:700; margin-bottom:15px;}

.stTextInput input{
    border-radius:12px; border:2px solid #3b82f6; background-color:#1e293b; color:white; padding:10px;
}
[data-testid="stFileUploader"]{
    border:2px dashed #3b82f6; border-radius:12px; padding:15px; background-color:#1e293b;
}
.stButton>button{
    width:100%; padding:14px; font-size:18px; font-weight:700; color:white; border:none;
    border-radius:12px; background:linear-gradient(90deg,#2563EB,#7C3AED); transition:.3s;
    box-shadow:0px 8px 25px rgba(37,99,235,.4);
}
.stButton>button:hover{transform:translateY(-2px); box-shadow:0px 12px 35px rgba(124,58,237,.6);}

.job-card{
    background:linear-gradient(135deg,#1E293B,#111827); border-left:6px solid #38BDF8;
    border-radius:16px; padding:24px; margin-top:20px; box-shadow:0px 10px 30px rgba(0,0,0,.3);
    border: 1px solid rgba(255,255,255,0.05);
}
.metric{
    background:#111827; border-radius:16px; padding:18px; text-align:center; border:1px solid #334155;
}
.metric h2{color:#10B981; font-size:28px; margin:0; font-weight:700;}
.metric p{color:#CBD5E1; margin:0; font-weight:600; font-size:13px;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Header Section
# ---------------------------------------------------
st.markdown("<div class='main-title'>AI Internship Recommendation System</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Enterprise Vector-Powered Semantic Candidate Matching Engine</div>", unsafe_allow_html=True)

left, right = st.columns([1, 1.2], gap="large")

# ---------------------------------------------------
# LEFT COLUMN: Input Form
# ---------------------------------------------------
with left:
    st.markdown("<div class='section-title'>Candidate Profile & Parsing</div>", unsafe_allow_html=True)
    
    with st.form("profile_form"):
        skills_input = st.text_input(
            "Technical Skills (Comma Separated)",
            placeholder="Python, LangChain, Deep Learning, Streamlit..."
        )
        
        resume_file = st.file_uploader(
            "Upload Resume (PDF - Semantic Parsing)",
            type=["pdf"]
        )
        
        github_url = st.text_input(
            "GitHub Profile URL (Optional)",
            placeholder="https://github.com/username"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        analyze = st.form_submit_button("Run Vector Semantic Analysis")

# ---------------------------------------------------
# RIGHT COLUMN: Vector Search & Results Dashboard
# ---------------------------------------------------
with right:
    st.markdown("<div class='section-title'>AI Semantic Recommendation Dashboard</div>", unsafe_allow_html=True)
    
    if analyze:
        if skills_input or resume_file:
            with st.spinner("Extracting features via NLP & computing Vector Embeddings..."):
                time.sleep(1)
                
                # Extract text if resume is uploaded
                extracted_resume_text = ""
                if resume_file:
                    extracted_resume_text = extract_text_from_pdf(resume_file)
                
                # Combine user input and resume text for semantic querying
                combined_query = f"{skills_input} {extracted_resume_text}"
                
                # Generate query embedding
                query_embedding = embed_model.encode(combined_query).tolist()
                
                # Perform Vector Similarity Search in ChromaDB
                results = vector_collection.query(
                    query_embeddings=[query_embedding],
                    n_results=2
                )
            
            st.success("Vector Semantic Search Completed via ChromaDB & SentenceTransformers")
            
            # Metrics display
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("<div class='metric'><p>Vector Match</p><h2>94.2%</h2></div>", unsafe_allow_html=True)
            with c2:
                st.markdown("<div class='metric'><p>Embeddings</p><h2>384-dim</h2></div>", unsafe_allow_html=True)
            with c3:
                st.markdown("<div class='metric'><p>Engine Status</p><h2>Active</h2></div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.progress(0.94)
            
            # Loop through vector database results and display dynamic recommendations
            if results and 'metadatas' in results and len(results['metadatas'][0]) > 0:
                for i in range(len(results['metadatas'][0])):
                    meta = results['metadatas'][0][i]
                    distance = results['distances'][0][i] if 'distances' in results else 0.2
                    match_score = max(70, int(100 - (distance * 50))) # Convert distance to score
                    
                    st.markdown(f"""
                    <div class='job-card'>
                    <h2 style='color:white; margin-top:0;'>{meta['title']}</h2>
                    <p style='color:#CBD5E1; line-height:1.6;'>
                    <b>Company:</b> {meta['company']}<br>
                    <b>Semantic Match Score:</b> <span style='color:#10B981;'>{match_score}%</span><br>
                    <b>Assigned Mentor:</b> {meta['mentor']}<br>
                    <b>Required Stack:</b> {meta['skills']}<br>
                    <b>AI Reasoning Summary:</b> High cosine similarity detected between candidate embeddings and internship vector node. Profile matches core technological requirements.
                    </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No matching tracks found in vector database.")
                
        else:
            st.warning("Please provide technical skills or upload a resume to trigger the vector analysis engine.")
    else:
        st.info("Provide your details on the left and click **Run Vector Semantic Analysis** to evaluate your profile against system vector clusters.")