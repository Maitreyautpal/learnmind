"""
pages/add_material.py

Lets the student add new learning material: PDF/TXT upload, a YouTube video
URL, or a YouTube playlist URL. Simulates the processing pipeline and shows
detected concepts once "processing" is done.

WHERE TO PLUG IN THE REAL BACKEND
----------------------------------
- File upload  -> api_client.upload_material()
- Processing   -> api_client.process_material()
Both already call your real FastAPI endpoints first, and fall back to mock
data automatically. You mainly need to update the endpoint paths/response
shape inside backend/api_client.py to match your actual FastAPI routes.
"""

import re
import streamlit as st
from backend import api_client
from components import cards

YOUTUBE_REGEX = re.compile(
    r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$"
)


def _is_valid_youtube_url(url: str) -> bool:
    return bool(url) and bool(YOUTUBE_REGEX.match(url.strip()))


def _reset_processing_state():
    st.session_state.processing_done = False
    st.session_state.detected_concepts = []


def render():
    cards.section_header("Add Learning Material", "Teach LearnMind using your own study material.")

    if "processing_done" not in st.session_state:
        _reset_processing_state()

    tab_upload, tab_video = st.tabs(["📄 Upload File", "🎥 Video"])

    material_ready_to_process = False
    process_payload = {}

    # ------------------------------------------------------------------
    # TAB 1 — UPLOAD FILE
    # ------------------------------------------------------------------
    with tab_upload:
        st.markdown("Upload a **PDF** or **TXT** file containing your notes.")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["pdf", "txt"],
            accept_multiple_files=False,
            key="file_uploader",
        )

        if uploaded_file is not None:
            st.success(f"✅ **{uploaded_file.name}** ready to process ({uploaded_file.size / 1024:.1f} KB)")
            if st.button("Process Material", type="primary", key="process_file_btn"):
                material_ready_to_process = True
                process_payload = {
                    "raw_text": None,  # backend will parse the uploaded file
                    "file": uploaded_file,
                }

    # ------------------------------------------------------------------
    # TAB 2 — VIDEO
    # ------------------------------------------------------------------
    with tab_video:
        st.markdown("Paste a **YouTube video URL** or a **playlist URL**.")

        youtube_url = st.text_input("Paste YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
        playlist_url = st.text_input(
            "Paste YouTube Playlist URL (optional)",
            placeholder="https://www.youtube.com/playlist?list=...",
        )

        st.info(
            "ℹ️ LearnMind will use available transcript/caption text to understand the lecture. "
            "The video itself does not need to be downloaded."
        )

        if playlist_url:
            st.caption("📌 Playlist processing support is coming soon — the URL will be saved for later.")

        if st.button("Process Material", type="primary", key="process_video_btn"):
            if not youtube_url and not playlist_url:
                st.error("Please paste a YouTube video or playlist URL before processing.")
            elif youtube_url and not _is_valid_youtube_url(youtube_url):
                st.error("That doesn't look like a valid YouTube URL. Please check and try again.")
            else:
                material_ready_to_process = True
                process_payload = {"youtube_url": youtube_url, "playlist_url": playlist_url}

    # ------------------------------------------------------------------
    # PROCESSING SIMULATION
    # ------------------------------------------------------------------
    if material_ready_to_process:
        with st.status("Processing your material...", expanded=True) as status:
            st.write("✓ Material received")
            st.write("✓ Text extracted")
            result = api_client.process_material(
                raw_text=process_payload.get("raw_text"),
                youtube_url=process_payload.get("youtube_url"),
                playlist_url=process_payload.get("playlist_url"),
            )
            st.write("✓ Concepts identified")
            st.write("✓ Knowledge base created")
            status.update(label="Processing complete!", state="complete")

        st.session_state.processing_done = True
        st.session_state.detected_concepts = result["data"]["concepts"]
        if result["source"] == "mock":
            cards.demo_mode_banner()

    # ------------------------------------------------------------------
    # RESULTS
    # ------------------------------------------------------------------
    if st.session_state.get("processing_done"):
        st.markdown("<div class='lm-spacer'></div>", unsafe_allow_html=True)
        st.markdown("### Detected Concepts")

        concepts = st.session_state.detected_concepts
        cols = st.columns(min(len(concepts), 5) or 1)
        for i, concept in enumerate(concepts):
            with cols[i % len(cols)]:
                with st.container(border=True):
                    st.markdown(f"**🧩 {concept}**")

        st.caption(f"{len(concepts)} concepts identified")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Go to My Learning", use_container_width=True):
                st.session_state.page = "My Learning"
                st.rerun()
        with col_b:
            if st.button("Ask AI Tutor about this", use_container_width=True, type="primary"):
                st.session_state.page = "AI Tutor"
                st.rerun()
