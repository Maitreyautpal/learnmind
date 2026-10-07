"""
pages/learning.py

Shows every material the student has added, with quick actions to study,
ask the AI tutor, or start a practice test on that material.

WHERE TO PLUG IN THE REAL BACKEND
----------------------------------
Replace api_client.get_materials() — it already tries GET /materials first.
"""

import streamlit as st
from backend import api_client
from components import cards


def render():
    cards.section_header("My Learning", "All the material you've taught LearnMind so far.")

    result = api_client.get_materials()
    materials = result["data"]

    if result["source"] == "mock":
        cards.demo_mode_banner()

    if not materials:
        cards.empty_state("You haven't added any learning material yet.")
        if st.button("➕ Add your first material", type="primary"):
            st.session_state.page = "Add Material"
            st.rerun()
        return

    def go_study(material):
        st.session_state.selected_material_id = material["id"]
        st.session_state.selected_material_title = material["title"]
        st.session_state.page = "My Mastery"
        st.rerun()

    def go_ask(material):
        st.session_state.selected_material_id = material["id"]
        st.session_state.selected_material_title = material["title"]
        st.session_state.page = "AI Tutor"
        st.rerun()

    def go_practice(material):
        st.session_state.selected_material_id = material["id"]
        st.session_state.selected_material_title = material["title"]
        st.session_state.page = "Practice Test"
        st.rerun()

    for material in materials:
        cards.material_card(material, on_study=go_study, on_ask=go_ask, on_practice=go_practice)
