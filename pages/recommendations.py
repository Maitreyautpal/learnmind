"""
pages/recommendations.py

Shows ranked next-topic recommendations. The ranking logic itself
(BKT + forgetting curve + priority ranking) belongs in the backend —
this page only renders whatever the backend (or mock data) returns.

WHERE TO PLUG IN THE REAL BACKEND
----------------------------------
Replace api_client.get_recommendations() — it already calls
GET /recommendations on your real backend first.
"""

import streamlit as st
from backend import api_client
from components import cards


def render():
    cards.section_header("Your Learning Plan", "Learn what will have the biggest impact next.")

    result = api_client.get_recommendations()
    recommendations = result["data"]

    if result["source"] == "mock":
        cards.demo_mode_banner()

    if not recommendations:
        cards.empty_state("No recommendations yet — take a practice test to get personalized suggestions.")
        return

    def handle_action(rec):
        concept = rec["concept"]
        st.session_state.selected_material_title = concept
        if rec["action_label"] in ("Practice", "Take Advanced Test"):
            st.session_state.page = "Practice Test"
        else:
            st.session_state.page = "AI Tutor"
        st.rerun()

    cols = st.columns(len(recommendations))
    for i, rec in enumerate(recommendations):
        with cols[i]:
            cards.recommendation_card(rec, on_action=handle_action)
