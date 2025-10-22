# pages/prescription_insights.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def show_prescription_insights(df: pd.DataFrame):
    st.header("📊 Prescription Insights")

    # Top filter box with style
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
        doc_list = sorted(df["prescribing_doctor"].dropna().unique().tolist()) if "prescribing_doctor" in df.columns else []
        selected_doc = cols[0].selectbox("Select Doctor", options=["All"] + doc_list)

        drug_list = sorted(df["drug_category"].dropna().unique().tolist()) if "drug_category" in df.columns else []
        selected_drug = cols[1].selectbox("Select Drug Category", options=["All"] + drug_list)

    # Apply filters
    dff = df.copy()
    if selected_doc != "All":
        dff = dff[dff["prescribing_doctor"] == selected_doc]
    if selected_drug != "All":
        dff = dff[dff["drug_category"] == selected_drug]

    # ---------------- Graphs Layout ---------------- #
    g1, g2 = st.columns(2)

    # Top 10 prescribed drug categories
    with g1:
        st.subheader("Top 10 prescribed drug categories")
        if "drug_category" in dff.columns:
            top = dff["drug_category"].value_counts().head(10).reset_index()
            top.columns = ["drug_category","count"]
            fig = px.bar(top, x="drug_category", y="count", title="Top Prescribed Drugs")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"ℹ️ Showing top {len(top)} categories based on current filters.")
        else:
            st.info("No drug_category column present.")

    # Branded vs Generic pie
    with g2:
        st.subheader("Branded vs Generic prescriptions")
        if "generic" in dff.columns:
            gen = dff["generic"].astype(str).str.lower().replace(
                {"true":"Generic","false":"Branded","yes":"Generic","no":"Branded"}
            )
            gen_counts = gen.value_counts().reset_index()
            gen_counts.columns = ["type","count"]
            fig = px.pie(gen_counts, names="type", values="count", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("ℹ️ Distribution of prescriptions between Branded and Generic types.")
        else:
            st.info("generic column not present.")

    g3, g4 = st.columns(2)

    # Heatmap doctor vs prescription volume
    with g3:
        st.subheader("Doctor vs Prescription volume (heatmap)")
        if "prescribing_doctor" in dff.columns and "drug_category" in dff.columns:
            pivot = pd.crosstab(dff["prescribing_doctor"], dff["drug_category"])
            pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).head(15).index]
            fig = px.imshow(pivot, labels=dict(x="Drug Category", y="Doctor", color="Count"), aspect="auto")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("ℹ️ Heatmap highlights top doctors and their prescribing patterns.")
        else:
            st.info("prescribing_doctor or drug_category missing.")

    # Adherence % trend over time
    with g4:
        st.subheader("Adherence % trend over time")
        if "adherence_percent" in dff.columns:
            if "visit_date" in dff.columns and dff["visit_date"].notna().any():
                trend = (
                    dff.dropna(subset=["visit_date","adherence_percent"])
                    .groupby(pd.Grouper(key="visit_date", freq="M"))
                    .mean()["adherence_percent"]
                    .reset_index()
                )
                fig = px.line(trend, x="visit_date", y="adherence_percent", markers=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("ℹ️ Tracks patient adherence trends over time (monthly).")
            elif "visit_order" in dff.columns:
                trend = (
                    dff.dropna(subset=["adherence_percent"])
                    .groupby("visit_order")["adherence_percent"]
                    .mean()
                    .reset_index()
                    .head(200)
                )
                fig = px.line(trend, x="visit_order", y="adherence_percent", markers=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("ℹ️ Tracks patient adherence trends by visit order.")
            else:
                st.info("No date/order info to draw trend.")
        else:
            st.info("adherence_percent not present.")

    g5, g6 = st.columns(2)

    # Refills stacked bar
    with g5:
        st.subheader("Refills: completed vs missed (stacked)")
        if "refills" in dff.columns:
            r = dff[["patient_id","refills"]].dropna()
            r['refills'] = pd.to_numeric(r['refills'], errors='coerce').fillna(0)
            summary = r.groupby("patient_id")["refills"].sum().reset_index()
            summary["missed"] = np.where(summary["refills"]==0,1,0)
            summary["completed"] = np.where(summary["refills"]>0,1,0)
            agg = summary[["missed","completed"]].sum().to_frame().T
            agg = agg.rename(columns={"missed":"Missed","completed":"Completed"})
            fig = px.bar(agg, y=["Completed","Missed"], title="Refills Completed vs Missed")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("ℹ️ Comparison of completed vs missed refills.")
        else:
            st.info("refills column not present to compute refill metrics.")

    st.markdown("---")
    st.write("📩 Footer: Contact us for more information — **321002@svcp.edu.in**")
