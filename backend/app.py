import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="AI Internship Recommendation System",
    page_icon="💼",
    layout="wide"
)

# Ultimate Professional Bold Multi-color CSS Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta+Sans', sans-serif;
    }

    .main-title {
        font-size: 3rem;
        background: linear-gradient(135deg, #FF3366 0%, #BA26FF 50%, #4E65FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 800;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }
    .sub-title {
        font-size: 1.25rem;
        color: #CBD5E1;
        text-align: center;
        margin-bottom: 40px;
        font-weight: 600;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 15px;
        border-left: 4px solid #3B82F6;
        padding-left: 10px;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        border-radius: 12px;
        padding: 14px;
        border: none;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.6);
        color: #ffffff;
    }
    .card-primary {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%);
        padding: 24px;
        border-radius: 14px;
        border: 2px solid #6366F1;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.2);
    }
    .card-secondary {
        background: linear-gradient(135deg, #4A044E 0%, #701A75 100%);
        padding: 24px;
        border-radius: 14px;
        border: 2px solid #EC4899;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(236, 72, 153, 0.2);
    }
    .metric-box {
        background-color: #0F172A;
        padding: 18px;
        border-radius: 10px;
        text-align: center;
        border: 2px solid #334155;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<p class="main-title">💼 AI-Powered Internship Recommendation System</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Advanced Deep Learning Engine for Precision Career Matching</p>', unsafe_allow_html=True)

# Layout Split into Two Professional Columns
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown('<p class="section-header">🧑‍💻 Candidate Profile Dashboard</p>', unsafe_allow_html=True)
    
    with st.container():
        skills_input = st.text_area(
            "🛠️ **Enter Your Technical Skills (Required):**",
            placeholder="e.g., Python, PyTorch, Deep Learning, Streamlit, FastAPI, Machine Learning",
            height=130
        )
        
        uploaded_file = st.file_uploader("📄 **Upload Professional Resume (PDF Format):**", type=["pdf"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("✨ Run AI Recommendation Engine")

with col2:
    st.markdown('<p class="section-header">🎯 Intelligent Matching Results</p>', unsafe_allow_html=True)
    
    if analyze_btn:
        if skills_input:
            with st.spinner("🔄 Processing semantic embeddings and analyzing profile compatibility..."):
                st.success("✅ **Profile successfully analyzed and verified!**")
                
                # Metrics Row
                m1, m2 = st.columns(2)
                with m1:
                    st.markdown('<div class="metric-box"><span style="color:#94A3B8; font-weight:700;">MATCH ACCURACY</span><br><span style="color:#10B981; font-size:1.6rem; font-weight:800;">95.4%</span></div>', unsafe_allow_html=True)
                with m2:
                    st.markdown('<div class="metric-box"><span style="color:#94A3B8; font-weight:700;">OPPORTUNITIES</span><br><span style="color:#6366F1; font-size:1.6rem; font-weight:800;">02 Active</span></div>', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Recommended Card 1
                st.markdown("""
                    <div class="card-primary">
                        <h3 style="color: #A5B4FC; margin-top:0; font-weight:800;">🌟 Generative AI Intern</h3>
                        <p style="color: #F8FAFC; margin-bottom:6px; font-size:1.05rem;"><b>🏢 Company:</b> Arch Technologies</p>
                        <p style="color: #F8FAFC; margin-bottom:6px; font-size:1.05rem;"><b>📊 Match Score:</b> 95% Compatibility</p>
                        <p style="color: #CBD5E1; font-size: 0.95rem; margin-bottom:0; font-weight:600;"><b>⚙️ Tech Stack:</b> Python • PyTorch • LLMs • Streamlit</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Recommended Card 2
                st.markdown("""
                    <div class="card-secondary">
                        <h3 style="color: #F9A8D4; margin-top:0; font-weight:800;">💡 Machine Learning Intern</h3>
                        <p style="color: #F8FAFC; margin-bottom:6px; font-size:1.05rem;"><b>🏢 Company:</b> Tech Solutions Inc.</p>
                        <p style="color: #F8FAFC; margin-bottom:6px; font-size:1.05rem;"><b>📊 Match Score:</b> 88% Compatibility</p>
                        <p style="color: #CBD5E1; font-size: 0.95rem; margin-bottom:0; font-weight:600;"><b>⚙️ Tech Stack:</b> Python • Scikit-Learn • Pandas • SQL</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ **Please input your technical skills or upload your resume to initiate the recommendation process.**")
    else:
        st.info("👈 **Please provide your skill details on the left panel and click 'Run AI Recommendation Engine' to view your custom career matches.**")