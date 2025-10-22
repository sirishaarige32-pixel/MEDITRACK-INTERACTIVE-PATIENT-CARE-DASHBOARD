# utils.py
import pandas as pd
import numpy as np
import streamlit as st

def load_and_prep_data(path: str) -> pd.DataFrame:
    """Load CSV and basic preprocessing. Returns a DataFrame with some useful derived columns."""
    try:
        df = pd.read_csv(path, low_memory=False)
    except Exception as e:
        st.error(f"Could not read CSV at {path}: {e}")
        return pd.DataFrame()

    # Standardize column names (strip)
    df.columns = [c.strip() for c in df.columns]

    # Ensure numeric where expected
    numeric_cols = ["age", "height_cm", "weight_kg", "bmi", "systolic_bp", "diastolic_bp",
                    "resting_heart_rate", "hba1c", "ldl", "hdl", "triglycerides",
                    "creatinine_mg_dl", "egfr", "turnaround_hours", "cost_usd", "adherence_percent"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Create age groups
    if "age" in df.columns:
        bins = [0, 18, 40, 60, 200]
        labels = ["0-18", "19-40", "41-60", ">60"]
        df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=True)
    else:
        df["age_group"] = np.nan

    # Normalize gender
    if "gender" in df.columns:
        df["gender"] = df["gender"].astype(str).str.title().replace({"M": "Male", "F": "Female"})
    # Create a visit_date if present in other name variants
    date_cols = [c for c in df.columns if "date" in c.lower() or "visit_date" in c.lower()]
    if date_cols:
        col = date_cols[0]
        df["visit_date"] = pd.to_datetime(df[col], errors="coerce")
    # If no dates, create an ordering index for trend plots
    if "visit_date" not in df.columns or df["visit_date"].isna().all():
        df["visit_order"] = np.arange(len(df))

    # Fill patient id as string
    if "patient_id" in df.columns:
        df["patient_id"] = df["patient_id"].astype(str)

    return df

# KPI helper
def compute_kpis(df):
    total_patients = df["patient_id"].nunique() if "patient_id" in df.columns else len(df)
    avg_age = df["age"].mean() if "age" in df.columns else None
    avg_bmi = df["bmi"].mean() if "bmi" in df.columns else None
    avg_adherence = df["adherence_percent"].mean() if "adherence_percent" in df.columns else None
    return {
        "total_patients": int(total_patients) if not pd.isna(total_patients) else 0,
        "avg_age": round(avg_age,1) if pd.notna(avg_age) else "N/A",
        "avg_bmi": round(avg_bmi,1) if pd.notna(avg_bmi) else "N/A",
        "avg_adherence": f"{round(avg_adherence,1)}%" if pd.notna(avg_adherence) else "N/A"
    }
