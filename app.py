import streamlit as st
import pandas as pd
from resume_parser import extract_text_from_resume
from job_description_parser import extract_text_from_jd
from matching_engine import match_resumes_to_jd

# Page setup
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="🧠",
    layout="wide"
)

# App header
st.markdown(
    """
    <h1 style='text-align: center;'>📄 AI-Powered Resume Screening Assistant</h1>
    <p style='text-align: center; color: gray;'>Match candidate resumes against job descriptions using NLP and OCR</p>
    <hr>
    """,
    unsafe_allow_html=True
)

# Sidebar: File Uploads
st.sidebar.header("📤 Upload Files")
jd_file = st.sidebar.file_uploader("Upload Job Description (TXT or PDF)", type=["txt", "pdf"])
uploaded_resumes = st.sidebar.file_uploader("Upload Resume Files (PDF, PNG, JPG)", type=["pdf", "png", "jpg"], accept_multiple_files=True)

# Sidebar: Run
st.sidebar.markdown("---")
run_screening = st.sidebar.button("🚀 Run Screening")

# Output Area
if run_screening:
    if not jd_file or not uploaded_resumes:
        st.warning("⚠️ Please upload both a Job Description and at least one Resume.")
    else:
        with st.spinner("🔍 Processing..."):
            jd_text = extract_text_from_jd(jd_file)
            results = []

            for file in uploaded_resumes:
                resume_text = extract_text_from_resume(file)
                score = match_resumes_to_jd(resume_text, jd_text)
                results.append({
                    "Filename": file.name,
                    "Score": round(score * 100, 2)
                })

            df = pd.DataFrame(results).sort_values(by="Score", ascending=False)

        # Display results
        st.success("✅ Screening Complete!")

        st.subheader("📊 Top Matching Resumes")
        st.dataframe(df, use_container_width=True)

        st.bar_chart(df.set_index("Filename")["Score"])

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Results as CSV", data=csv, file_name="screening_results.csv", mime='text/csv')

# Footer
st.markdown(
    "<hr><center>Made with 💙 by Akshay | Resume Screener AI | Final Year BI Project</center>",
    unsafe_allow_html=True
)
