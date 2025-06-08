import streamlit as st
from utils.api_client import APIClient
import pandas as pd

def show():
    st.title("🚀 Recruiter Dashboard – Resume Filtering & Ranking")

    st.subheader("📄 Enter Job Description")
    jd_text = st.text_area("Paste the job description here", height=200)

    st.subheader("📤 Upload Resumes")
    uploaded_files = st.file_uploader("Upload multiple resumes", type=["pdf"], accept_multiple_files=True)

    client = APIClient()

    if st.button("🔍 Rank Resumes") and jd_text and uploaded_files:
        st.info("Processing resumes...")
        results = []

        for resume_file in uploaded_files:
            file_bytes = resume_file.read()  # ✅ read it once
            result = client.upload_resume(resume_file.name, file_bytes, jd_text)  # ✅ send bytes, not file object
            result['filename'] = resume_file.name
            result['file_bytes'] = file_bytes
            results.append(result)



        st.success("✅ Resume ranking complete!")

        # Filter and sort
        valid_results = [r for r in results if "scores" in r and "final" in r["scores"]]
        results = sorted(valid_results, key=lambda x: x['scores']['final'], reverse=True)

        st.subheader("📊 Ranked Results (Uploaded Now)")
        for idx, res in enumerate(results):
            st.markdown(f"### 🥇 Rank {idx+1}: `{res['filename']}`")
            scores = res['scores']
            st.markdown(f"""
                **Semantic Similarity:** `{scores.get('semantic', 0):.2f}`  
                **Graph Match:** `{scores.get('graph', 0):.2f}`  
                **Rule-based Skill Match:** `{scores.get('rule_based', 0):.2f}`  
                **Cultural Fit:** `{scores.get('cultural_fit', 0):.2f}`  
                **🧠 Final Score:** `{scores.get('final', 0):.2f}`  
                **🔑 Matched Keywords:** `{', '.join(res.get('keywords', []))}`  
            """)

            # Add View/Download Resume Button
            st.download_button(
                label="📄 View / Download Resume",
                data=res['file_bytes'],                  # ✅ now valid binary data
                file_name=res['filename'],
                mime='application/pdf'
            )

            st.markdown("---")
