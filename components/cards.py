"""
components/cards.py

Small, reusable UI building blocks. Every page imports from here instead of
re-writing the same st.container/st.columns layout over and over.

Keeping these in one place means: if you want to restyle every "topic card"
in the whole app, you only change it here.
"""

import streamlit as st


def section_header(title: str, subtitle: str = ""):
    st.markdown(f"<h1 class='lm-page-title'>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p class='lm-page-subtitle'>{subtitle}</p>", unsafe_allow_html=True)


def metric_card(label: str, value, help_text: str = None):
    with st.container(border=True):
        st.metric(label=label, value=value, help=help_text)


def mastery_color(percent: int) -> str:
    """Returns a semantic color for a mastery percentage."""
    if percent >= 75:
        return "#16A34A"  # green
    if percent >= 50:
        return "#D97706"  # amber
    return "#DC2626"      # red


def topic_progress_card(topic: str, mastery: int, key: str, button_label: str = "Continue"):
    """Card used on the Dashboard's 'Continue Learning' section."""
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{topic}**")
        with col2:
            st.markdown(
                f"<div style='text-align:right; color:{mastery_color(mastery)}; font-weight:600;'>{mastery}%</div>",
                unsafe_allow_html=True,
            )
        st.progress(mastery / 100)
        st.button(button_label, key=f"btn_{key}", use_container_width=True)


def weak_concept_card(concept: str, mastery: int, status: str):
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{concept}**")
            st.caption(status)
        with col2:
            st.markdown(
                f"<div style='text-align:right; color:{mastery_color(mastery)}; font-weight:600; font-size:1.1rem;'>{mastery}%</div>",
                unsafe_allow_html=True,
            )
        st.progress(mastery / 100)


def concept_chip_row(concepts: list):
    """Renders a row of small pill-shaped concept chips."""
    chips_html = "".join(
        f"<span class='lm-chip'>{concept}</span>" for concept in concepts
    )
    st.markdown(f"<div class='lm-chip-row'>{chips_html}</div>", unsafe_allow_html=True)


def material_card(material: dict, on_study=None, on_ask=None, on_practice=None):
    """Card used on the 'My Learning' page."""
    with st.container(border=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"### {material['icon']} {material['title']}")
            st.caption(f"{material['type']} · {material['concepts']} concepts · Added {material['date_added']}")
        with col2:
            st.markdown(
                f"<div style='text-align:right; color:{mastery_color(material['progress'])}; font-weight:700; font-size:1.3rem;'>{material['progress']}%</div>",
                unsafe_allow_html=True,
            )
            st.caption(material["status"])

        st.progress(material["progress"] / 100)

        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("Study", key=f"study_{material['id']}", use_container_width=True):
                if on_study:
                    on_study(material)
        with b2:
            if st.button("Ask AI", key=f"ask_{material['id']}", use_container_width=True):
                if on_ask:
                    on_ask(material)
        with b3:
            if st.button("Practice", key=f"practice_{material['id']}", use_container_width=True):
                if on_practice:
                    on_practice(material)


def recommendation_card(rec: dict, on_action=None):
    with st.container(border=True):
        st.markdown(f"#### {rec['emoji']} {rec['priority']}")
        st.markdown(f"### {rec['concept']}")
        st.caption(f"Mastery: {rec['mastery']}%")
        st.progress(rec["mastery"] / 100)
        st.markdown(f"**Reason:** {rec['reason']}")
        if st.button(rec["action_label"], key=f"rec_{rec['concept']}", use_container_width=True, type="primary"):
            if on_action:
                on_action(rec)


def risk_badge(risk: str) -> str:
    colors = {"High": "#DC2626", "Medium": "#D97706", "Low": "#16A34A"}
    color = colors.get(risk, "#6B7280")
    return f"<span style='color:white; background:{color}; padding:2px 10px; border-radius:12px; font-size:0.8rem; font-weight:600;'>{risk}</span>"


def demo_mode_banner():
    st.info("🔧 **Demo mode** — backend not connected. Showing sample data so you can preview the UI.")


def empty_state(message: str, icon: str = "📭"):
    with st.container(border=True):
        st.markdown(
            f"<div style='text-align:center; padding: 2rem 0; color:#6B7280;'>"
            f"<div style='font-size:2.5rem;'>{icon}</div>"
            f"<div style='margin-top:0.5rem;'>{message}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
