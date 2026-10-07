"""
pages/tutor.py

A ChatGPT-like interface for asking questions about the student's own
learning material (this will be powered by your RAG pipeline).

WHERE TO PLUG IN THE REAL BACKEND
----------------------------------
Replace api_client.ask_question() — it already calls:
    POST /ask   { "question": ..., "material_id": ... }
    -> { "answer": ..., "sources": [...] }
on your real backend first, and only falls back to a mock answer if that
request fails.
"""

import streamlit as st
from backend import api_client
from components import cards


def render():
    cards.section_header("AI Tutor", "Ask questions about your learning material.")

    material_title = st.session_state.get("selected_material_title", "General Knowledge Base")
    st.markdown(
        f"<div class='lm-current-material'>📚 Currently studying: <strong>{material_title}</strong></div>",
        unsafe_allow_html=True,
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    top_col1, top_col2 = st.columns([5, 1])
    with top_col2:
        if st.button("🗑️ Clear chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("<div class='lm-spacer-sm'></div>", unsafe_allow_html=True)

    # --- Render chat history --------------------------------------------
    chat_container = st.container(height=430, border=True)
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown(
                "<div style='text-align:center; color:#9CA3AF; padding-top: 2.5rem;'>"
                "💬 Ask your first question about this material to get started."
                "</div>",
                unsafe_allow_html=True,
            )

        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message["role"] == "assistant" and message.get("sources"):
                    with st.expander("📎 Sources"):
                        for source in message["sources"]:
                            st.markdown(f"- **{source['material']}** — Concept: *{source['concept']}*")

    # --- Chat input -------------------------------------------------------
    question = st.chat_input("Ask anything about your material...")

    if question:
        question = question.strip()
        if not question:
            st.warning("Please type a question before sending.")
        else:
            st.session_state.chat_history.append({"role": "user", "content": question})

            material_id = st.session_state.get("selected_material_id")
            with st.spinner("LearnMind is thinking..."):
                result = api_client.ask_question(question, material_id=material_id)

            answer_data = result["data"]
            assistant_message = {
                "role": "assistant",
                "content": answer_data["answer"],
                "sources": answer_data.get("sources", []),
            }
            st.session_state.chat_history.append(assistant_message)

            if result["source"] == "mock":
                st.session_state.tutor_demo_mode = True

            st.rerun()

    if st.session_state.get("tutor_demo_mode"):
        cards.demo_mode_banner()
