# app.py
import streamlit as st
from utils import load_and_prep_data
from pages.home import show_home
from pages.dashboard_page import show_dashboard
from pages.prescription_insights import show_prescription_insights
from pages.lab_chronic_insights import show_lab_chronic_insights
from pages.about import show_about

st.set_page_config(page_title="MediTrack", layout="wide", initial_sidebar_state="expanded")

CSV_PATH = r"C:\Users\hp\OneDrive\Desktop\AI python\MINI PROJECT\merged_hospital_data_final.csv"
ABOUT_IMAGE_PATH = r"C:\Users\hp\OneDrive\Desktop\certificates amd my documents\my pics.jpg"
# If you copied the image to assets/my_pics.jpg, set ABOUT_IMAGE_PATH = "assets/my_pics.jpg"

# Load once
df = load_and_prep_data(CSV_PATH)

# Sidebar (global)
with st.sidebar:
    st.image(ABOUT_IMAGE_PATH, width=160)  # small logo in sidebar
    st.title("MediTrack")
    st.write("Navigation")
    page = st.radio("", ["Home", "Dashboard", "Prescription Insights", "Lab & Chronic Insights", "About Me"], index=1)

    st.markdown("---")
    st.write("General Settings")
    if st.button("Sign out"):
        st.warning("Sign out clicked (placeholder).")
    if st.button("Help"):
        st.info("For help contact: 321002@svcp.edu.in")

st.markdown("""
<style>
/* center title Times New Roman */
.main-title { font-family: 'Times New Roman', Times, serif; text-align:center; font-size:28px; }
</style>
""", unsafe_allow_html=True)

# Route pages
if page == "Home":
    show_home(df)
elif page == "Dashboard":
    show_dashboard(df)
elif page == "Prescription Insights":
    show_prescription_insights(df)
elif page == "Lab & Chronic Insights":
    show_lab_chronic_insights(df)
elif page == "About Me":
    show_about(ABOUT_IMAGE_PATH)
