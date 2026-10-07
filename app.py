"""
app.py

Entry point for the LearnMind Streamlit frontend.

RUN THIS FILE WITH:
    streamlit run app.py

WHAT THIS FILE DOES
--------------------
1. Configures the page (title, icon, wide layout).
2. Injects custom CSS so the app looks like a polished product, not a
   default Streamlit demo.
3. Initializes all the st.session_state values the rest of the app relies on.
4. Checks whether the FastAPI backend is reachable (for the "Demo mode" badge).
5. Renders the sidebar and routes to the correct page module.

You should NOT need to touch this file often. Almost all product logic lives
inside pages/, components/, backend/, and utils/.
"""

import streamlit as st

from backend import api_client
from components.sidebar import render_sidebar
from pages import (
    dashboard,
    learning,
    add_material,
    tutor,
    practice,
    mastery,
    recommendations,
)

# ---------------------------------------------------------------------------
# PAGE CONFIG — must be the first Streamlit command
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="LearnMind — Personal AI Learning Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# CUSTOM CSS — this is what makes the app look "designed" rather than default.
# Everything here is pure CSS; no JavaScript, nothing fragile.
# ---------------------------------------------------------------------------
def inject_custom_css():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

            html, body, [class*="css"] {
                font-family: 'Inter', sans-serif;
            }

            /* Hide default Streamlit chrome for a cleaner product feel */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header[data-testid="stHeader"] { background: transparent; }

            /* Overall background */
            .stApp {
                background-color: #F8FAFC;
            }

            /* Page title / subtitle */
            .lm-page-title {
                font-size: 2rem;
                font-weight: 800;
                color: #111827;
                margin-bottom: 0.1rem;
            }
            .lm-page-subtitle {
                font-size: 1.02rem;
                color: #6B7280;
                margin-bottom: 1.6rem;
            }

            /* Spacers */
            .lm-spacer { margin-top: 1.6rem; }
            .lm-spacer-sm { margin-top: 0.7rem; }

            /* Cards (st.container(border=True)) */
            div[data-testid="stVerticalBlockBorderWrapper"] {
                border-radius: 14px !important;
                border: 1px solid #E5E7EB !important;
                background-color: #FFFFFF;
            }

            /* Buttons */
            .stButton button {
                border-radius: 10px;
                font-weight: 600;
                padding: 0.5rem 1rem;
            }
            .stButton button[kind="primary"] {
                background-color: #4F46E5;
                border-color: #4F46E5;
            }
            .stButton button[kind="primary"]:hover {
                background-color: #4338CA;
                border-color: #4338CA;
            }

            /* Progress bars */
            .stProgress > div > div > div > div {
                background-color: #4F46E5;
            }

            /* Concept chips */
            .lm-chip-row { display: flex; flex-wrap: wrap; gap: 0.5rem; }
            .lm-chip {
                background-color: #EEF2FF;
                color: #4338CA;
                padding: 6px 14px;
                border-radius: 999px;
                font-size: 0.85rem;
                font-weight: 600;
            }

            /* AI Tutor "currently studying" banner */
            .lm-current-material {
                background-color: #EEF2FF;
                color: #3730A3;
                padding: 10px 16px;
                border-radius: 10px;
                margin-bottom: 1rem;
                font-size: 0.95rem;
            }

            /* Sidebar */
            section[data-testid="stSidebar"] {
                background-color: #111827;
            }
            section[data-testid="stSidebar"] * {
                color: #E5E7EB !important;
            }
            section[data-testid="stSidebar"] .stButton button {
                background-color: transparent;
                border: none;
                text-align: left;
                justify-content: flex-start;
                font-weight: 500;
            }
            section[data-testid="stSidebar"] .stButton button:hover {
                background-color: #1F2937;
                color: #FFFFFF !important;
            }
            section[data-testid="stSidebar"] .stButton button[kind="primary"] {
                background-color: #4F46E5 !important;
                color: #FFFFFF !important;
            }

            .lm-logo {
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 0.5rem 0 1rem 0;
            }
            .lm-logo-icon { font-size: 1.6rem; }
            .lm-logo-text { font-size: 1.35rem; font-weight: 800; color: #FFFFFF !important; }

            .lm-sidebar-spacer { margin-top: 0.5rem; }
            .lm-sidebar-flex-spacer { margin-top: 2rem; }

            .lm-status {
                font-size: 0.8rem;
                padding: 8px 10px;
                border-radius: 8px;
                margin-top: 1rem;
                background-color: #1F2937;
            }
            .lm-status-online { color: #34D399 !important; }
            .lm-status-offline { color: #9CA3AF !important; }

            .lm-sidebar-footer {
                margin-top: 1.2rem;
                padding-top: 1rem;
                border-top: 1px solid #374151;
            }
            .lm-sidebar-footer-title {
                font-weight: 700;
                font-size: 0.95rem;
                color: #FFFFFF !important;
            }
            .lm-sidebar-footer-subtitle {
                font-size: 0.78rem;
                color: #9CA3AF !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------------------------------
def init_session_state():
    defaults = {
        "page": "Dashboard",
        "selected_material_id": None,
        "selected_material_title": None,
        "chat_history": [],
        "demo_mode": True,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ---------------------------------------------------------------------------
# ROUTING
# ---------------------------------------------------------------------------
PAGE_MODULES = {
    "Dashboard": dashboard,
    "My Learning": learning,
    "Add Material": add_material,
    "AI Tutor": tutor,
    "Practice Test": practice,
    "My Mastery": mastery,
    "Recommendations": recommendations,
}


@st.cache_data(ttl=15, show_spinner=False)
def _cached_backend_status():
    """Cached so we don't hit the backend on every single rerun/click."""
    return api_client.check_backend_status()


def main():
    inject_custom_css()
    init_session_state()

    backend_online = _cached_backend_status()
    st.session_state.demo_mode = not backend_online

    current_page = render_sidebar(backend_online)

    # Extra safety net: never show a raw traceback to the student.
    try:
        page_module = PAGE_MODULES.get(current_page, dashboard)
        page_module.render()
    except Exception:
        st.error(
            "😕 Something went wrong while loading this page. "
            "Please try again, or head back to the Dashboard."
        )
        if st.button("Go to Dashboard"):
            st.session_state.page = "Dashboard"
            st.rerun()


if __name__ == "__main__":
    main()
