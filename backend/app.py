import streamlit as st
import torch
import chromadb

st.set_page_config(page_title="AI Internship Recommendation System", layout="centered")

st.title("💼 AI-Powered Internship Recommendation System")
st.write("Apni skills aur resume details enter karein taake hum aapko behtareen internship recommend kar sakein!")

# User input form
user_skills = st.text_area("Apni skills yahan likhein (e.g., Python, PyTorch, FastAPI, Machine Learning):")

if st.button("Recommendations Hasil Karein"):
    if user_skills.strip() == "":
        st.warning("Pehle kuch skills toh enter karein!")
    else:
        with st.spinner("AI analysis ho rahi hai..."):
            # Yahan aap apna ChromaDB aur PyTorch model ka logic call kar sakti hain
            # Maslan: recommendations = get_recommendations(user_skills)
            
            # Temporary output display ke liye
            st.success("Yeh rahi aapke liye recommendations:")
            st.info(f"Aapki entered skills: {user_skills}")
            
            # Sample mock result
            st.markdown("### 🚀 Top Recommended Internships:")
            st.markdown("- **Generative AI Intern** at Arch Technologies")
            st.markdown("- **Machine Learning Intern** at Tech Solutions")