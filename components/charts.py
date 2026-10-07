"""
components/charts.py

Chart helpers built on Altair (bundled with Streamlit, no extra install needed).
"""

import pandas as pd
import altair as alt
import streamlit as st


def mastery_overview_chart(mastery: dict):
    """
    Horizontal bar chart of mastery per concept, colored by risk band.
    `mastery` is a dict like {"Recursion": 61, "Graphs": 72, ...}
    """
    df = pd.DataFrame(
        [{"concept": k, "mastery": v} for k, v in mastery.items()]
    ).sort_values("mastery", ascending=True)

    def band(value):
        if value >= 75:
            return "Strong (75%+)"
        if value >= 50:
            return "Developing (50-74%)"
        return "Needs Attention (<50%)"

    df["band"] = df["mastery"].apply(band)

    color_scale = alt.Scale(
        domain=["Needs Attention (<50%)", "Developing (50-74%)", "Strong (75%+)"],
        range=["#DC2626", "#D97706", "#16A34A"],
    )

    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6, height=22)
        .encode(
            x=alt.X("mastery:Q", title="Mastery (%)", scale=alt.Scale(domain=[0, 100])),
            y=alt.Y("concept:N", sort="x", title=""),
            color=alt.Color("band:N", scale=color_scale, legend=alt.Legend(title="Mastery Level")),
            tooltip=[alt.Tooltip("concept:N", title="Concept"), alt.Tooltip("mastery:Q", title="Mastery %")],
        )
        .properties(height=max(220, len(df) * 45))
    )

    st.altair_chart(chart, use_container_width=True)
