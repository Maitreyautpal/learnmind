"""
pages/mastery.py

Visualizes the learner model: overall mastery, per-concept mastery,
a chart, and a ranked "concepts to improve" table.

WHERE TO PLUG IN THE REAL BACKEND
----------------------------------
Replace api_client.get_mastery() — it already calls GET /mastery on your
real backend first. The BKT calculation itself must live in the backend;
this page only displays the numbers it receives.
"""

import streamlit as st
from backend import api_client
from components import cards, charts
from utils import mock_data


def render():
    cards.section_header("My Mastery", "Understand what you know and what needs attention.")

    result = api_client.get_mastery()
    mastery = result["data"]

    if result["source"] == "mock":
        cards.demo_mode_banner()

    overall = round(sum(mastery.values()) / len(mastery)) if mastery else 0

    col1, col2 = st.columns([1, 2])
    with col1:
        cards.metric_card("Overall Mastery", f"{overall}%")
    with col2:
        st.progress(overall / 100)

    st.markdown("<div class='lm-spacer'></div>", unsafe_allow_html=True)
    st.markdown("### Concept Mastery")

    sorted_mastery = sorted(mastery.items(), key=lambda x: x[1], reverse=True)
    cols = st.columns(2)
    for i, (concept, score) in enumerate(sorted_mastery):
        with cols[i % 2]:
            with st.container(border=True):
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"**{concept}**")
                with col_b:
                    st.markdown(
                        f"<div style='text-align:right; color:{cards.mastery_color(score)}; font-weight:600;'>{score}%</div>",
                        unsafe_allow_html=True,
                    )
                st.progress(score / 100)

    st.markdown("<div class='lm-spacer'></div>", unsafe_allow_html=True)
    st.markdown("### Mastery Overview")
    charts.mastery_overview_chart(mastery)

    st.markdown("<div class='lm-spacer'></div>", unsafe_allow_html=True)
    st.markdown("### Concepts to Improve")

    concepts_to_improve = mock_data.get_mock_concepts_to_improve()
    for row in concepts_to_improve:
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1.3])
            with col1:
                st.markdown(f"**{row['concept']}**")
            with col2:
                st.markdown(f"{row['mastery']}%")
            with col3:
                st.markdown(cards.risk_badge(row["risk"]), unsafe_allow_html=True)
            with col4:
                st.caption(f"Last practiced: {row['last_practiced']}")
