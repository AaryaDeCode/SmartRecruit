import streamlit as st
from pages import recruiter_dashboard

st.set_page_config(page_title="CareerYatra - Resume Ranking", layout="wide")

st.sidebar.title("🔎 Navigation")
page = st.sidebar.radio("Go to:", ["Recruiter Dashboard"])

if page == "Recruiter Dashboard":
    recruiter_dashboard.show()
