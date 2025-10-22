# pages/home.py
import streamlit as st
from utils import compute_kpis
import pandas as pd

def show_home(df: pd.DataFrame):
    # Title with larger font and blue color, centered
    st.markdown(
        """
        <h1 style='text-align: center; color: #1f77b4; font-family: "Times New Roman";'>
            MediTrack: An Interactive Dashboard for Patient Care and Diagnostics
        </h1>
        """, 
        unsafe_allow_html=True
    )
    st.write("")  # spacing

    # KPIs top row with colored background
    kpis = compute_kpis(df)
    cols = st.columns(4)

    kpi_style = "padding:15px; border-radius:10px; color:white; font-size:18px; text-align:center;"

    cols[0].markdown(f"<div style='{kpi_style} background-color:#2ca02c;'>Total Patients<br><b>{kpis['total_patients']}</b></div>", unsafe_allow_html=True)
    cols[1].markdown(f"<div style='{kpi_style} background-color:#ff7f0e;'>Average Age<br><b>{kpis['avg_age']}</b></div>", unsafe_allow_html=True)
    cols[2].markdown(f"<div style='{kpi_style} background-color:#d62728;'>Average BMI<br><b>{kpis['avg_bmi']}</b></div>", unsafe_allow_html=True)
    cols[3].markdown(f"<div style='{kpi_style} background-color:#9467bd;'>Average Adherence<br><b>{kpis['avg_adherence']}</b></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Patient Lookup")
    patient_id = st.text_input("Enter patient id to search (exact):")
    if patient_id:
        if "patient_id" in df.columns:
            res = df[df["patient_id"].astype(str) == str(patient_id)]
            if res.empty:
                st.warning("No patient found with that ID.")
            else:
                # show basic patient info and full row
                info_cols = ["patient_id","name","gender","age","city","state","pincode","blood_group","bmi","condition_primary"]
                available = [c for c in info_cols if c in res.columns]
                st.write(res[available].drop_duplicates().T)
                st.markdown("**All records for this patient:**")
                st.dataframe(res.sort_values(by=[c for c in ["visit_date","visit_order"] if c in res.columns], ascending=False))
        else:
            st.error("patient_id column not found in dataset.")
    else:
        st.info("Type a patient id above to view all details.")

    st.markdown("---")
    st.write("Footer: Contact us for more information — mail: 321002@svcp.edu.in")
