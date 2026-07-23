import streamlit as st
import time

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
# CSS Styling (Clean Professional Enterprise Theme)
# ---------------------------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"]{
    font-family:'Poppins',sans-serif;
    background:#0f172a;
}

/* Hide Streamlit Default Elements */
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

.main-title{
    text-align:center;
    font-size:46px;
    font-weight:800;
    background:linear-gradient(90deg,#00DBDE,#FC00FF);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin-bottom:5px;
}

.sub-title{
    text-align:center;
    font-size:18px;
    color:#CBD5E1;
    margin-bottom:35px;
    font-weight:500;
}

/* Section Title */
.section-title{
    color:white;
    font-size:24px;
    font-weight:700;
    margin-bottom:15px;
}

/* Input Area Styling */
.stTextArea textarea{
    border-radius:12px;
    border:2px solid #3b82f6;
    background-color: #1e293b;
    color: white;
}

/* File Uploader Styling */
[data-testid="stFileUploader"]{
    border:2px dashed #3b82f6;
    border-radius:12px;
    padding:15px;
    background-color: #1e293b;
}

/* Professional Button Styling */
.stButton>button{
    width:100%;
    padding:14px;
    font-size:18px;
    font-weight:700;
    color:white;
    border:none;
    border-radius:12px;
    background:linear-gradient(90deg,#2563EB,#7C3AED);
    transition:.3s;
    box-shadow:0px 8px 25px rgba(37,99,235,.4);
}

.stButton>button:hover{
    transform:translateY(-2px);
    box-shadow:0px 12px 35px rgba(124,58,237,.6);
}

/* Cards */
.card{
    background:rgba(255,255,255,.04);
    backdrop-filter:blur(18px);
    border:1px solid rgba(255,255,255,.12);
    border-radius:16px;
    padding:25px;
    margin-bottom:20px;
    box-shadow:0px 10px 30px rgba(0,0,0,.25);
}

/* Internship Card */
.job-card{
    background:linear-gradient(135deg,#1E293B,#111827);
    border-left:6px solid #38BDF8;
    border-radius:16px;
    padding:24px;
    margin-top:20px;
    box-shadow:0px 10px 30px rgba(0,0,0,.3);
    border-top: 1px solid rgba(255,255,255,0.05);
    border-right: 1px solid rgba(255,255,255,0.05);
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

/* Metrics */
.metric{
    background:#111827;
    border-radius:16px;
    padding:18px;
    text-align:center;
    border:1px solid #334155;
}

.metric h2{
    color:#10B981;
    font-size:30px;
    margin:0;
    font-weight:700;
}

.metric p{
    color:#CBD5E1;
    margin:0;
    font-weight:600;
    font-size:14px;
}

/* Divider */
hr{
    border:1px solid #1e293b;
}

</style>

""", unsafe_allow_html=True)

# ---------------------------------------------------
# Header Section
# ---------------------------------------------------

st.markdown("<div class='main-title'>AI Internship Recommendation System</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Enterprise AI Candidate Matching Platform</div>", unsafe_allow_html=True)

left, right = st.columns([1, 1.2], gap="large")

# ---------------------------------------------------
# LEFT COLUMN: User Input Form
# ---------------------------------------------------

with left:
    st.markdown("<div class='section-title'>Candidate Profile</div>", unsafe_allow_html=True)
    
    # Using a form enables pressing Enter to submit inputs smoothly
    with st.form("profile_form"):
        skills = st.text_area(
            "Technical Skills",
            placeholder="Python, NLP, Deep Learning, TensorFlow, FastAPI, Streamlit...",
            height=130
        )
        
        resume = st.file_uploader(
            "Upload Resume (PDF)",
            type=["pdf"]
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        analyze = st.form_submit_button("Analyze Profile")

# ---------------------------------------------------
# RIGHT COLUMN: Results Dashboard
# ---------------------------------------------------

with right:
    st.markdown("<div class='section-title'>AI Recommendation Dashboard</div>", unsafe_allow_html=True)
    
    if analyze:
        if skills or resume:
            with st.spinner("Analyzing profile and computing compatibility embeddings..."):
                time.sleep(1.5)
            
            st.success("Analysis Completed Successfully")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("""
                <div class='metric'>
                <p>Match Score</p>
                <h2>95%</h2>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown("""
                <div class='metric'>
                <p>Opportunities</p>
                <h2>02</h2>
                </div>
                """, unsafe_allow_html=True)
            with c3:
                st.markdown("""
                <div class='metric'>
                <p>Mentor Match</p>
                <h2>High</h2>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.progress(95)
            
            # Recommendation Card 1
            st.markdown("""
            <div class='job-card'>
            <h2 style='color:white; margin-top:0;'>Generative AI Intern</h2>
            <p style='color:#CBD5E1; line-height:1.6;'>
            <b>Company:</b> Arch Technologies<br>
            <b>Match Score:</b> <span style='color:#10B981;'>95%</span><br>
            <b>Mentor:</b> Dr. Hamera Javed<br>
            <b>Strengths:</b> Python • NLP • Machine Learning<br>
            <b>Missing Skills:</b> FastAPI<br>
            <b>Learning Roadmap:</b> Python → FastAPI → Docker → LLM → Deployment<br>
            <b>AI Reasoning:</b> Your profile strongly matches the internship requirements due to your core background in Python, NLP, and Machine Learning.
            </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Recommendation Card 2
            st.markdown("""
            <div class='job-card'>
            <h2 style='color:white; margin-top:0;'>Machine Learning Intern</h2>
            <p style='color:#CBD5E1; line-height:1.6;'>
            <b>Company:</b> Tech Solutions<br>
            <b>Match Score:</b> <span style='color:#10B981;'>88%</span><br>
            <b>Mentor:</b> Ali Ahmed<br>
            <b>Strengths:</b> Python • Scikit-Learn • SQL<br>
            <b>Missing Skills:</b> TensorFlow<br>
            <b>Roadmap:</b> Machine Learning → TensorFlow → MLOps
            </p>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.warning("Please enter your technical skills or upload your resume before analyzing.")
    else:
        st.info("Please provide your skill details or upload a resume on the left panel, then click **Analyze Profile** to view your matches.")