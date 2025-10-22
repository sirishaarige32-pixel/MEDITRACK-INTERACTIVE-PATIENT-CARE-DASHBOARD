# pages/dashboard_page.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def show_dashboard(df: pd.DataFrame):
    st.header("📊 Interactive Dashboard")

    # --------------------- TOP FILTERS -------------------------
    st.markdown("### 🔍 Quick Filters (apply to graphs below)")
    col1, col2, col3 = st.columns([1, 1, 1])

    # Age range filter
    if "age" in df.columns:
        min_age, max_age = int(df["age"].min()), int(df["age"].max())
        age_range = col1.slider("Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))
    else:
        age_range = None

    # Top N selector (for categories like drug or age groups)
    top_n = col2.selectbox("Show Top N Categories", options=[5, 10, 15, 20], index=1)

    # Theme selection
    theme = col3.radio("Graph Theme", ["Plotly", "Seaborn", "Simple White"], horizontal=True)

    # --------------------- SIDEBAR FILTERS ----------------------
    st.sidebar.markdown("## 📍 Dashboard Filters")
    city_list = sorted(df["city"].dropna().unique().tolist()) if "city" in df.columns else []
    state_list = sorted(df["state"].dropna().unique().tolist()) if "state" in df.columns else []
    selected_cities = st.sidebar.multiselect("City", options=city_list, default=None)
    selected_states = st.sidebar.multiselect("State", options=state_list, default=None)
    gender_filter = st.sidebar.multiselect("Gender", options=df["gender"].dropna().unique().tolist() if "gender" in df.columns else [], default=None)

    # --------------------- APPLY FILTERS ------------------------
    dff = df.copy()
    if selected_cities:
        dff = dff[dff["city"].isin(selected_cities)]
    if selected_states:
        dff = dff[dff["state"].isin(selected_states)]
    if gender_filter:
        dff = dff[dff["gender"].isin(gender_filter)]
    if age_range and "age" in dff.columns:
        dff = dff[(dff["age"] >= age_range[0]) & (dff["age"] <= age_range[1])]

    # --------------------- GRAPHS -------------------------------
    # Row 1 → Heatmap & Gender Pie
    st.subheader("📍 Patient Distribution & Demographics")
    col1, col2 = st.columns(2)

    with col1:
        if "state" in dff.columns and "city" in dff.columns:
            pivot = pd.crosstab(dff["state"], dff["city"])
            fig = px.imshow(
                pivot,
                labels=dict(x="City", y="State", color="Count"),
                aspect="auto",
                template=theme.lower()
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("State or City columns not present to draw heatmap.")

    with col2:
        if "gender" in dff.columns:
            gender_counts = dff["gender"].value_counts().reset_index()
            gender_counts.columns = ["gender","count"]
            gender_counts["label"] = gender_counts["gender"].replace({"Male":"♂ Male","Female":"♀ Female"})
            fig = px.pie(
                gender_counts,
                names="label",
                values="count",
                hole=0.45,
                template=theme.lower()
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Gender column missing.")

    # Row 2 → Age Groups & Adverse Events
    st.subheader("📈 Age & Drug Analysis")
    col1, col2 = st.columns(2)

    with col1:
        if "age_group" in dff.columns:
            age_counts = dff["age_group"].value_counts().reindex(["0-18","19-40","41-60",">60"]).fillna(0).reset_index()
            age_counts.columns = ["age_group","count"]
            fig = px.bar(
                age_counts,
                x="age_group",
                y="count",
                labels={"count":"Patients","age_group":"Age Group"},
                template=theme.lower()
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Age column missing to calculate age groups.")

    with col2:
        if "drug_category" in dff.columns and "adverse_event_reported" in dff.columns:
            adv = dff[dff["adverse_event_reported"].notna() & (dff["adverse_event_reported"].astype(str).str.lower() != "no")]
            if not adv.empty:
                adv_counts = adv["drug_category"].value_counts().reset_index().head(top_n)
                adv_counts.columns = ["drug_category","count"]
                fig = px.bar(
                    adv_counts,
                    x="drug_category",
                    y="count",
                    template=theme.lower()
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No adverse events flagged in the filtered dataset.")
        else:
            st.info("drug_category or adverse_event_reported column missing.")

    # --------------------- FOOTER -------------------------------
    st.markdown("---")
    st.caption("📩 Contact us for more information — mail: 321002@svcp.edu.in")
