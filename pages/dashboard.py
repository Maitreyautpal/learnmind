"""
pages/dashboard.py

The student's home screen: quick stats, "continue learning" shortcuts,
weakest concepts, and one highlighted recommendation.

WHERE TO PLUG IN THE REAL BACKEND
----------------------------------
Replace the calls to `api_client.get_progress()`, `get_mastery()`, and
`get_recommendations()` — they already call your real API first and only
fall back to mock data if it's unavailable, so usually you don't need to
change anything here at all once FastAPI is running.
"""

import streamlit as st
from backend import api_client
from components import cards
from utils import mock_data


def render():
    cards.section_header("Good morning 👋", "Continue learning and focus on what matters most.")

    # --- Metrics -----------------------------------------------------
    progress_result = api_client.get_progress()
    metrics = progress_result["data"]

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        cards.metric_card("Overall Mastery", f"{metrics['overall_mastery']}%")
    with m2:
        cards.metric_card("Concepts Learned", metrics["concepts_learned"])
    with m3:
        cards.metric_card("Questions Attempted", metrics["questions_attempted"])
    with m4:
        cards.metric_card("Current Streak", f"{metrics['current_streak']} 🔥")

    st.markdown("<div class='lm-spacer'></div>", unsafe_allow_html=True)

    # --- Continue Learning --------------------------------------------
    st.markdown("### Continue Learning")
    topics = mock_data.get_mock_continue_learning()
    cols = st.columns(2)
    for i, topic in enumerate(topics):
        with cols[i % 2]:
            def go_to_material(t=topic):
                st.session_state.page = "AI Tutor"
                st.session_state.selected_material_title = t["topic"]
                st.rerun()

            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{topic['topic']}**")
                with col2:
                    st.markdown(
                        f"<div style='text-align:right; color:{cards.mastery_color(topic['mastery'])}; font-weight:600;'>{topic['mastery']}%</div>",
                        unsafe_allow_html=True,
                    )
                st.progress(topic["mastery"] / 100)
                if st.button("Continue", key=f"continue_{i}", use_container_width=True):
                    go_to_material()

    st.markdown("<div class='lm-spacer'></div>", unsafe_allow_html=True)

    # --- Weak Concepts ---------------------------------------------------
    st.markdown("### Weak Concepts")
    weak_concepts = mock_data.get_mock_weak_concepts(top_n=3)
    w_cols = st.columns(3)
    for i, wc in enumerate(weak_concepts):
        with w_cols[i]:
            cards.weak_concept_card(wc["concept"], wc["mastery"], wc["status"])

    st.markdown("<div class='lm-spacer'></div>", unsafe_allow_html=True)

    # --- Recommended for You ---------------------------------------------
    st.markdown("### Recommended for You")
    rec = mock_data.get_mock_recommendation_highlight()
    with st.container(border=True):
        st.markdown(f"💡 {rec['text']}")
        if st.button("Start Recommendation", type="primary"):
            st.session_state.page = "Recommendations"
            st.rerun()
