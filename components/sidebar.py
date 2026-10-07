"""
components/sidebar.py

Renders the left-hand navigation sidebar and returns the page the
student wants to view. Also shows a small "Demo mode" badge when the
FastAPI backend is not reachable.
"""

import streamlit as st

PAGES = [
    ("🏠", "Dashboard"),
    ("📚", "My Learning"),
    ("➕", "Add Material"),
    ("🤖", "AI Tutor"),
    ("📝", "Practice Test"),
    ("🧠", "My Mastery"),
    ("🎯", "Recommendations"),
]


def render_sidebar(backend_online: bool) -> str:
    with st.sidebar:
        st.markdown(
            """
            <div class="lm-logo">
                <span class="lm-logo-icon">🧠</span>
                <span class="lm-logo-text">LearnMind</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div class='lm-sidebar-spacer'></div>", unsafe_allow_html=True)

        for icon, label in PAGES:
            is_active = st.session_state.page == label
            button_type = "primary" if is_active else "secondary"
            if st.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True, type=button_type):
                st.session_state.page = label
                st.rerun()

        st.markdown("<div class='lm-sidebar-flex-spacer'></div>", unsafe_allow_html=True)

        if backend_online:
            st.markdown(
                "<div class='lm-status lm-status-online'>🟢 Backend connected</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div class='lm-status lm-status-offline'>⚪ Demo mode — backend not connected</div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div class="lm-sidebar-footer">
                <div class="lm-sidebar-footer-title">LearnMind</div>
                <div class="lm-sidebar-footer-subtitle">Personal AI Learning Assistant</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return st.session_state.page
