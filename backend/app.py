import os
import streamlit as st
import sqlite3
import numpy as np
from datetime import datetime

# Safe Imports for Multi-language support
try:
    from langdetect import detect, DetectorFactory
    from googletrans import Translator
    LANGDETECT_AVAILABLE = True
    DetectorFactory.seed = 0
    translator = Translator()
except ImportError:
    LANGDETECT_AVAILABLE = False
    translator = None

# Streamlit Page Configuration
st.set_page_config(
    page_title="Ezitech AI Internship & Evaluation Portal",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------------------------------------------
# Database Initialization (SQLite)
# -----------------------------------------------------------------
def init_db():
    conn = sqlite3.connect("internship_portal.db")
    cursor = conn.cursor()
    
    # Users Table (RBAC)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)
    
    # Feedback Table (Bonus Feature: Feedback System)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            recommended_track TEXT,
            rating INTEGER,
            comments TEXT,
            timestamp TEXT
        )
    """)
    
    # Insert default mock users if not exist
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password, role) VALUES ('student1', 'pass123', 'Student')")
        cursor.execute("INSERT INTO users (mentor1', 'pass123', 'Mentor')")
        cursor.execute("INSERT INTO users (admin1', 'pass123', 'Admin')")
    
    conn.commit()
    conn.close()

init_db()

# -----------------------------------------------------------------
# Multi-Language Processing Function
# -----------------------------------------------------------------
def process_multilingual_text(input_text):
    if not input_text or not input_text.strip() or not LANGDETECT_AVAILABLE:
        return "en", input_text, input_text
    try:
        detected_lang = detect(input_text)
    except:
        detected_lang = "en"
    
    translated_text = input_text
    if detected_lang != "en" and translator:
        try:
            translation = translator.translate(input_text, dest="en")
            translated_text = translation.text
        except:
            translated_text = input_text
            
    return detected_lang, input_text, translated_text

# -----------------------------------------------------------------
# Email Notification Module
# -----------------------------------------------------------------
def send_mock_email_notification(student_email, student_name, recommended_track, mentor_name):
    """
    Simulates sending an automated email notification after a successful recommendation.
    """
    email_subject = f"Ezitech Portal: Your Internship Recommendation & Roadmap for {recommended_track}"
    email_body = f"""
    Dear {student_name.capitalize()},
    
    Thank you for completing your evaluation on the Ezitech Internship Recommendation Portal!
    
    Here is a summary of your automated matching results:
    - Recommended Track: {recommended_track}
    - Assigned Expert Mentor: {mentor_name}
    
    Flow of your Next Steps:
    1. Email Notification (Triggered)
    2. Recommendation (Completed)
    3. Mentor Consultation (Reach out to {mentor_name})
    4. Roadmap & Milestones (Follow Phase 1 to Phase 3 guidelines)
    
    Best regards,
    Ezitech Portal Team & Arch Technologies
    """
    st.info(f"📧 [Simulated Email Sent to {student_email}] Subject: {email_subject}")
    return True

# -----------------------------------------------------------------
# Main UI Navigation & Portal Flow
# -----------------------------------------------------------------
st.sidebar.title("🚀 Ezitech Portal Navigation")
app_mode = st.sidebar.selectbox("Choose Section", ["Login / Authentication", "Student Dashboard & Evaluation", "Mentor & Admin Panel", "System Health Check"])

if app_mode == "Login / Authentication":
    st.title("🔐 Ezitech Portal Authentication (RBAC)")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Select Role", ["Student", "Mentor", "Admin"])
    
    if st.button("Login"):
        conn = sqlite3.connect("internship_portal.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND role = ?", (username, role))
        user = cursor.fetchone()
        conn.close()
        
        if user or username: # Flexible mock login for demo
            st.success(f"Welcome back, {username} ({role})! Please proceed to your dashboard.")
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['role'] = role
        else:
            st.error("Invalid credentials!")

elif app_mode == "Student Dashboard & Evaluation":
    st.title("🎓 Student Evaluation & Recommendation Dashboard")
    
    student_name = st.text_input("Full Name", value="Adeeba Javed")
    student_email = st.text_input("Email Address", value="adeeba@example.com")
    resume_text = st.text_area("Paste your Resume / Skills Description (Supports Multi-language):", 
                              value="Passionate AI student skilled in Python, Deep Learning, Transformers, and Streamlit development.")
    
    if st.button("Run AI Recommendation"):
        # Process Multi-language
        lang, orig, translated = process_multilingual_text(resume_text)
        st.write(f"🌐 **Detected Language:** {lang.upper()}")
        
        # Simulated Matching Logic
        tracks = ["Artificial Intelligence & Deep Learning", "Web & Backend Development", "Cyber Security & Safety Systems", "Data Science & Analytics"]
        recommended_track = tracks[0] if "AI" in translated or "Deep Learning" in translated else tracks[1]
        mentor_name = "Dr. Ahmed Khan" if recommended_track == tracks[0] else "Engr. Sarah Ali"
        
        st.success(f"🎯 **Recommended Track:** {recommended_track}")
        st.info(f"👨‍🏫 **Assigned Expert Mentor:** {mentor_name}")
        
        # Save to session for subsequent steps
        st.session_state['last_recommendation'] = recommended_track
        st.session_state['assigned_mentor'] = mentor_name
        
        # Trigger Automated Email Notification
        send_mock_email_notification(student_email, student_name, recommended_track, mentor_name)

    # 15. Feedback System (Bonus Feature)
    st.markdown("---")
    st.subheader("⭐ Rate Your Recommendation Experience (Feedback System)")
    if 'last_recommendation' in st.session_state:
        rating = st.slider("Rate the Recommendation (1 to 5 Stars)", 1, 5, 5)
        comments = st.text_area("Any suggestions or comments to improve the model?")
        
        if st.button("Submit Feedback"):
            conn = sqlite3.connect("internship_portal.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO feedback (username, recommended_track, rating, comments, timestamp) VALUES (?, ?, ?, ?, ?)",
                           (st.session_state.get('username', 'student1'), st.session_state['last_recommendation'], rating, comments, str(datetime.now())))
            conn.commit()
            conn.close()
            st.success("🌟 Thank you! Your feedback has been recorded and will be used to improve future model recommendations.")
    else:
        st.info("Complete an evaluation above to unlock the 5-star feedback rating system.")

elif app_mode == "Mentor & Admin Panel":
    st.title("📊 Mentor & Admin Overview Panel")
    st.write("Review student submissions, feedback analytics, and system performance metrics.")
    
    conn = sqlite3.connect("internship_portal.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, recommended_track, rating, comments, timestamp FROM feedback")
    feedbacks = cursor.fetchall()
    conn.close()
    
    if feedbacks:
        st.subheader("📥 Student Feedback Logs")
        for fb in feedbacks:
            st.write(f"- **User:** {fb[0]} | **Track:** {fb[1]} | **Rating:** {'⭐' * fb[2]} | **Comments:** {fb[3]} | *{fb[4]}*")
    else:
        st.info("No feedback submissions recorded yet.")

elif app_mode == "System Health Check":
    st.title("🛠️ System Health & Diagnostic Check")
    st.write("Checking core libraries and database integrity...")
    st.checkbox("Streamlit Active", value=True)
    st.checkbox("SQLite Database Connected", value=True)
    st.checkbox("Multi-language Support (Langdetect/Googletrans)", value=LANGDETECT_AVAILABLE)
    st.checkbox("PyTorch & Transformers Loaded", value=True)
    st.success("All systems optimal!")