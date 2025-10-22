# pages/about.py
import streamlit as st

def show_about(image_path: str = None):
    st.header("About Me")

    # Create two columns: one for image, one for details
    col1, col2 = st.columns([1, 2])

    with col1:
        if image_path:
            try:
                st.image(image_path, caption="A. Sirisha", width=250)
            except Exception as e:
                st.error(f"Could not show image at {image_path}: {e}")

    with col2:
        st.markdown("""
        **Name:** A. Sirisha  
        **Reg No:** 321002  
        **College:** Shri Vishnu College of Pharmacy
        """)

    st.markdown("""
    ### About this project
    MediTrack is an interactive dashboard built with Streamlit for patient-level insights,
    prescription analytics, and lab/chronic disease monitoring.

    **Contact:** 321002@svcp.edu.in
    """)
