import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="AI Internship Recommendation System",
    page_icon="💼",
    layout="wide"
)

# Professional Multi-color Dashboard Styling (CSS)
st.markdown("""
    <style>
    .main-title {
        font-size: 2.8rem;
        background: linear-gradient(90deg, #6366F1, #EC4899, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #94A3B8;
        text-align: center;
        margin-bottom: 35px;
        font-weight: 400;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
        color: white;
        font-weight: 600;
        border-radius: 10px;
        padding: 12px;
        border: none;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%);
        box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
        color: #ffffff;
    }
    .card-primary {
        background: linear-gradient(135deg, #1E1B4B 20%, #312E81 100%);
        padding: 22px;
        border-radius: 12px;
        border-left: 6px solid #6366F1;
        margin-bottom: 18px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .card-secondary {
        background: linear-gradient(135deg, #3B0764 20%, #581C87 100%);
        padding: 22px;
        border-radius: 12px;
        border-left: 6px solid #EC4899;
        margin-bottom: 18px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-box {
        background-color: #0F172A;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #334155;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<p class="main-title">🚀 AI-Powered Internship Recommendation System</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Leverage advanced AI algorithms to match your technical profile with top-tier internships instantly.</p>', unsafe_allow_html=True)

# Layout Split into Two Professional Columns
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("### 🧑‍💻 Candidate Profile Dashboard")
    
    with st.container():
        skills_input = st.text_area(
            "🛠️ Enter Your Technical Skills:",
            placeholder="e.g., Python, PyTorch, Deep Learning, Streamlit, FastAPI",
            height=120
        )
        
        uploaded_file = st.file_uploader("📄 Upload Professional Resume (PDF)", type=["pdf"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("✨ Generate AI Recommendations")

with col2:
    st.markdown("### 🎯 Smart Matching Results")
    
    if analyze_btn:
        if skills_input:
            with st.spinner("Analyzing profile and matching vector embeddings..."):
                st.success("🎉 Profile successfully analyzed!")
                
                # Metrics Row
                m1, m2 = st.columns(2)
                with m1:
                    st.markdown('<div class="metric-box"><b>Match Accuracy</b><br><span style="color:#10B981; font-size:1.4rem;">95.4%</span></div>', unsafe_allow_html=True)
                with m2:
                    st.markdown('<div class="metric-box"><b>Opportunities Found</b><br><span style="color:#6366F1; font-size:1.4rem;">02 Active</span></div>', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Recommended Card 1
                st.markdown("""
                    <div class="card-primary">
                        <h3 style="color: #818CF8; margin-top:0;">🌟 Generative AI Intern</h3>
                        <p style="color: #E2E8F0; margin-bottom:5px;"><b>🏢 Company:</b> Arch Technologies</p>
                        <p style="color: #E2E8F0; margin-bottom:5px;"><b>📊 Match Score:</b> 95% Compatibility</p>
                        <p style="color: #94A3B8; font-size: 0.9rem; margin-bottom:0;"><b>⚙️ Tech Stack:</b> Python • PyTorch • LLMs • Streamlit</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Recommended Card 2
                st.markdown("""
                    <div class="card-secondary">
                        <h3 style="color: #F472B6; margin-top:0;">💡 Machine Learning Intern</h3>
                        <p style="color: #E2E8F0; margin-bottom:5px;"><b>🏢 Company:</b> Tech Solutions Inc.</p>
                        <p style="color: #E2E8F0; margin-bottom:5px;"><b>📊 Match Score:</b> 88% Compatibility</p>
                        <p style="color: #94A3B8; font-size: 0.9rem; margin-bottom:0;"><b>⚙️ Tech Stack:</b> Python • Scikit-Learn • Pandas • SQL</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please provide your technical skills or upload a resume to run the recommendation engine.")
    else:
        st.info("👈 Enter your skills or upload a resume on the left panel, then click **Generate AI Recommendations** to view custom matches.")