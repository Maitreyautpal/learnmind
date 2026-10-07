"""
pages/practice.py

Three phases, all controlled through st.session_state:
  1. SETUP     -> student picks concept / number of questions / difficulty
  2. IN_TEST   -> one question shown at a time, with Previous/Next
  3. RESULTS   -> score, accuracy, concept-wise breakdown, mastery change

WHERE TO PLUG IN THE REAL BACKEND
----------------------------------
- Generating questions -> api_client.generate_test()
- Scoring the test      -> api_client.submit_test()
Both already call your real FastAPI endpoints first (POST /test and
POST /test/submit) and fall back to mock data/scoring only if those fail.
"""

import streamlit as st
from backend import api_client
from components import cards
from utils import mock_data

CONCEPT_OPTIONS = ["Dynamic Programming", "Recursion", "Graphs", "Functions", "Python Basics", "Trees"]
DIFFICULTY_OPTIONS = ["Adaptive", "Easy", "Medium", "Hard"]


def _init_state():
    defaults = {
        "test_phase": "setup",       # setup | in_test | results
        "test_questions": [],
        "test_current_index": 0,
        "test_answers": {},
        "test_source": "mock",
        "test_result": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _reset_test():
    st.session_state.test_phase = "setup"
    st.session_state.test_questions = []
    st.session_state.test_current_index = 0
    st.session_state.test_answers = {}
    st.session_state.test_result = None


def render():
    _init_state()
    cards.section_header("Practice Test", "Test yourself based on what you've learned.")

    if st.session_state.test_phase == "setup":
        _render_setup()
    elif st.session_state.test_phase == "in_test":
        _render_test()
    elif st.session_state.test_phase == "results":
        _render_results()


# ---------------------------------------------------------------------------
# PHASE 1 — SETUP
# ---------------------------------------------------------------------------

def _render_setup():
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            concept = st.selectbox("Concept", CONCEPT_OPTIONS)
        with col2:
            num_questions = st.select_slider("Questions", options=[5, 10, 15, 20], value=10)
        with col3:
            difficulty = st.selectbox("Difficulty", DIFFICULTY_OPTIONS)

        st.markdown("<div class='lm-spacer-sm'></div>", unsafe_allow_html=True)

        if st.button("Generate Test", type="primary", use_container_width=True):
            material_id = st.session_state.get("selected_material_id")
            with st.spinner("Generating your personalized test..."):
                result = api_client.generate_test(
                    material_id=material_id,
                    concept=concept,
                    num_questions=num_questions,
                    difficulty=difficulty,
                )

            questions = result["data"]["questions"]
            if not questions:
                st.error("No questions could be generated. Please try a different concept.")
                return

            st.session_state.test_questions = questions
            st.session_state.test_answers = {}
            st.session_state.test_current_index = 0
            st.session_state.test_source = result["source"]
            st.session_state.test_phase = "in_test"
            st.rerun()


# ---------------------------------------------------------------------------
# PHASE 2 — IN TEST (one question at a time)
# ---------------------------------------------------------------------------

def _render_test():
    if st.session_state.test_source == "mock":
        cards.demo_mode_banner()

    questions = st.session_state.test_questions
    total = len(questions)
    idx = st.session_state.test_current_index
    question = questions[idx]

    st.progress((idx + 1) / total, text=f"Question {idx + 1} of {total}")

    with st.container(border=True):
        st.caption(f"Concept: {question['concept']}")
        st.markdown(f"#### {question['question']}")

        previous_answer = st.session_state.test_answers.get(question["id"])
        options = question["options"]
        default_index = options.index(previous_answer) if previous_answer in options else None

        selected = st.radio(
            "Choose one answer:",
            options,
            index=default_index,
            key=f"radio_q_{question['id']}",
        )
        st.session_state.test_answers[question["id"]] = selected

    st.markdown("<div class='lm-spacer-sm'></div>", unsafe_allow_html=True)

    col_prev, col_next, col_submit = st.columns([1, 1, 2])
    with col_prev:
        if st.button("⬅️ Previous", use_container_width=True, disabled=(idx == 0)):
            st.session_state.test_current_index -= 1
            st.rerun()
    with col_next:
        if st.button("Next ➡️", use_container_width=True, disabled=(idx == total - 1)):
            st.session_state.test_current_index += 1
            st.rerun()
    with col_submit:
        answered_count = len(st.session_state.test_answers)
        if st.button(
            f"✅ Submit Test ({answered_count}/{total} answered)",
            type="primary",
            use_container_width=True,
        ):
            _submit_test()


def _submit_test():
    questions = st.session_state.test_questions
    answers = st.session_state.test_answers

    with st.spinner("Scoring your test..."):
        result = api_client.submit_test(test_id="demo_test", questions=questions, answers=answers)

    st.session_state.test_result = result["data"]
    st.session_state.test_source = result["source"]
    st.session_state.test_phase = "results"
    st.rerun()


# ---------------------------------------------------------------------------
# PHASE 3 — RESULTS
# ---------------------------------------------------------------------------

def _render_results():
    if st.session_state.test_source == "mock":
        cards.demo_mode_banner()

    result = st.session_state.test_result

    st.markdown("## Test Complete 🎉")

    col1, col2 = st.columns(2)
    with col1:
        cards.metric_card("Score", f"{result['score']} / {result['total']}")
    with col2:
        cards.metric_card("Accuracy", f"{result['accuracy']}%")

    st.markdown("<div class='lm-spacer'></div>", unsafe_allow_html=True)
    st.markdown("### Concept-wise Performance")

    for concept, stats in result["concept_stats"].items():
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{concept}**")
            with col2:
                st.markdown(f"<div style='text-align:right;'>{stats['correct']}/{stats['total']} correct</div>", unsafe_allow_html=True)
            st.progress(stats["correct"] / stats["total"] if stats["total"] else 0)

    st.markdown("<div class='lm-spacer'></div>", unsafe_allow_html=True)
    st.markdown("### What LearnMind Learned")

    # This is a purely visual/frontend estimate — the real BKT mastery
    # update will come from the backend once /test/submit is wired up.
    main_concept = list(result["concept_stats"].keys())[0]
    mastery_before = mock_data.get_mock_mastery().get(main_concept, 50)
    mastery_after = min(100, mastery_before + result["accuracy"] // 10)

    with st.container(border=True):
        st.markdown(
            f"📈 Your **{main_concept}** mastery increased from **{mastery_before}% → {mastery_after}%**."
        )

    st.markdown("<div class='lm-spacer'></div>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("View My Mastery", use_container_width=True):
            st.session_state.page = "My Mastery"
            _reset_test()
            st.rerun()
    with col_b:
        if st.button("Take Another Test", type="primary", use_container_width=True):
            _reset_test()
            st.rerun()
