# pages/lab_chronic_insights.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def show_lab_chronic_insights(df: pd.DataFrame):
    st.header("🧪 Lab Insights & Chronic Disease Burden")

    # ---------------- FILTER BOX ----------------
    with st.container():
        st.markdown(
            """
            <div style="background-color:#f0f2f6; padding:15px; border-radius:10px; margin-bottom:20px;">
                <h4 style="margin-bottom:10px;">🔍 Apply Filters</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )
        cols = st.columns(2)
        condition_filters = sorted(df["condition_primary"].dropna().unique().tolist()) if "condition_primary" in df.columns else []
        selected_conditions = cols[0].multiselect("Primary Condition", options=condition_filters, default=None)

        test_filters = sorted(df["test_name"].dropna().unique().tolist()) if "test_name" in df.columns else []
        selected_tests = cols[1].multiselect("Lab Test", options=test_filters, default=None)

    # Apply filters
    dff = df.copy()
    if selected_conditions:
        dff = dff[dff["condition_primary"].isin(selected_conditions)]
    if selected_tests:
        dff = dff[dff["test_name"].isin(selected_tests)]

    # ---------------- CHARTS ----------------
    g1, g2 = st.columns(2)

    # Chronic disease prevalence
    with g1:
        st.subheader("Chronic Disease Prevalence (stacked)")
        if "condition_primary" in dff.columns:
            counts = dff["condition_primary"].value_counts().reset_index()
            counts.columns = ["condition","count"]
            top = counts.head(8)
            fig = px.bar(top, x="condition", y="count", title="Top Chronic Conditions")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("ℹ️ Shows the top chronic conditions in patients. Helps administrators identify the most common burdens.")
        else:
            st.info("condition_primary column missing.")

    # HbA1c trend
    with g2:
        st.subheader("Average HbA1c trend (diabetics)")
        if "hba1c" in dff.columns and "condition_primary" in dff.columns:
            diabetics = dff[dff["condition_primary"].str.contains("diab", case=False, na=False)]
            if not diabetics.empty:
                if "visit_date" in diabetics.columns and diabetics["visit_date"].notna().any():
                    trend = (
                        diabetics.dropna(subset=["visit_date","hba1c"])
                        .groupby(pd.Grouper(key="visit_date", freq="M"))["hba1c"]
                        .mean().reset_index()
                    )
                    fig = px.line(trend, x="visit_date", y="hba1c", markers=True)
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown("ℹ️ Tracks average HbA1c levels in diabetic patients over time. Useful for monitoring diabetes control at a population level.")
                elif "visit_order" in diabetics.columns:
                    trend = (
                        diabetics.dropna(subset=["hba1c"])
                        .groupby("visit_order")["hba1c"]
                        .mean().reset_index().head(200)
                    )
                    fig = px.line(trend, x="visit_order", y="hba1c", markers=True)
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown("ℹ️ Tracks HbA1c across visits when date information is missing.")
                else:
                    st.info("No date/order to create trend.")
            else:
                st.info("No diabetic patients found in filtered data.")
        else:
            st.info("hba1c or condition_primary missing.")

    g3, g4 = st.columns(2)

    # Hypertension Control Rate (new insight instead of box plot)
    with g3:
        st.subheader("Hypertension Control Rate (%)")
        if "systolic_bp" in dff.columns and "diastolic_bp" in dff.columns:
            # controlled BP: systolic < 140 and diastolic < 90
            dff["controlled"] = np.where((dff["systolic_bp"] < 140) & (dff["diastolic_bp"] < 90), "Controlled", "Uncontrolled")
            bp_rate = dff["controlled"].value_counts(normalize=True).reset_index()
            bp_rate.columns = ["status","percent"]
            bp_rate["percent"] *= 100
            fig = px.pie(bp_rate, names="status", values="percent", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("ℹ️ Proportion of patients with controlled vs uncontrolled blood pressure. Key quality indicator for cardiovascular health.")
        else:
            st.info("systolic_bp or diastolic_bp missing.")

    # Lab turnaround time gauge
    with g4:
        st.subheader("Lab Turnaround Time")
        if "turnaround_hours" in dff.columns:
            avg_turn = dff["turnaround_hours"].dropna().mean()
            target = st.number_input("Turnaround target (hours)", value=24)
            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=avg_turn if not np.isnan(avg_turn) else 0,
                gauge={
                    'axis': {'range': [0, max(48, target*2)]},
                    'threshold': {'line': {'color': "red", 'width': 4}, 'thickness':0.75, 'value': target}
                },
                title={'text': "Average turnaround hours"}
            ))
            st.plotly_chart(gauge, use_container_width=True)
            st.markdown("ℹ️ Tracks average lab turnaround time vs target. Useful for monitoring operational efficiency.")
        else:
            st.info("turnaround_hours column missing.")

    g5, g6 = st.columns(2)

    # Lab metrics (HbA1c, LDL abnormal %)
    with g5:
        st.subheader("Lab Insights")
        if "hba1c" in dff.columns:
            pct_above = (dff["hba1c"] > 7).mean() * 100
            st.metric("HbA1c > 7 (%)", f"{pct_above:.1f}%")
        if "ldl" in dff.columns:
            pct_ldl = (dff["ldl"] > 130).mean() * 100
            st.metric("LDL > 130 (%)", f"{pct_ldl:.1f}%")
        st.markdown("ℹ️ Provides quick KPIs for key chronic disease markers like diabetes (HbA1c) and cholesterol (LDL).")

    # Pareto of lab tests
    with g6:
        st.subheader("Pareto: Most frequently ordered tests")
        if "test_name" in dff.columns:
            tests = dff["test_name"].value_counts().reset_index()
            tests.columns = ["test_name","count"]
            tests = tests.head(20)
            tests["cum_percent"] = tests["count"].cumsum() / tests["count"].sum() * 100
            fig = go.Figure()
            fig.add_trace(go.Bar(x=tests["test_name"], y=tests["count"], name="Count"))
            fig.add_trace(go.Scatter(x=tests["test_name"], y=tests["cum_percent"], name="Cumulative %", yaxis="y2", marker=dict(color="black")))
            fig.update_layout(yaxis2=dict(overlaying="y", side="right", range=[0,110], title="Cumulative %"))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("ℹ️ Pareto chart shows which tests are most frequently ordered. Helps optimize lab resources.")
        else:
            st.info("test_name column missing.")

    # ---------------- FOOTER ----------------
    st.markdown("---")
    st.write("📩 Footer: Contact us for more information — **321002@svcp.edu.in**")
