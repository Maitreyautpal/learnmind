"""
backend/api_client.py

This is the ONLY file that should ever call your FastAPI backend.

HOW IT WORKS
------------
Every function below:
  1. Tries to call the real backend using `requests`.
  2. If the backend is unreachable, times out, or errors out, it silently
     falls back to mock data from `utils/mock_data.py`.
  3. Always returns a dictionary shaped like:
        {
            "success": True/False,
            "data": <the actual payload>,
            "source": "api" or "mock",
            "error": <error message, only if success is False>
        }

This means your Streamlit pages never crash, even if the backend is down.
They just check `result["source"]` and optionally show a
"Demo mode — backend not connected." message.

CONNECTING YOUR REAL BACKEND
-----------------------------
1. Change API_BASE_URL below (or set the LEARNMIND_API_URL environment variable).
2. Make sure your FastAPI endpoints match the paths used in this file
   (e.g. POST /ask, POST /test, POST /materials, GET /mastery, etc.)
   You can rename the paths here to match your actual backend instead.
3. Once a real request succeeds, "source" will automatically become "api"
   and the mock data will simply stop being used for that call.
"""

import os
import requests

# ---------------------------------------------------------------------------
# CONFIGURATION — change this one line (or set an env var) to point at your
# real FastAPI backend once it's ready.
# ---------------------------------------------------------------------------
API_BASE_URL = os.environ.get("LEARNMIND_API_URL", "http://localhost:8000")

REQUEST_TIMEOUT = 4  # seconds — keep short so the UI doesn't freeze in demo mode

from utils import mock_data


# ---------------------------------------------------------------------------
# INTERNAL HELPERS
# ---------------------------------------------------------------------------

def _success(data, source="api"):
    return {"success": True, "data": data, "source": source, "error": None}


def _failure(error_message):
    return {"success": False, "data": None, "source": "mock", "error": str(error_message)}


def check_backend_status():
    """
    Quick health check used by the sidebar to show 'Demo mode' banner.
    Returns True if the backend responds, False otherwise.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


# ---------------------------------------------------------------------------
# MATERIAL INGESTION
# ---------------------------------------------------------------------------

def upload_material(file_bytes, filename, material_type):
    """
    Uploads a PDF/TXT file to the backend.

    Expected real endpoint:
        POST /materials/upload   (multipart/form-data)

    Mock fallback:
        Pretends the upload succeeded and returns a fake material_id.
    """
    try:
        files = {"file": (filename, file_bytes)}
        data = {"type": material_type}
        response = requests.post(
            f"{API_BASE_URL}/materials/upload",
            files=files,
            data=data,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return _success(response.json())
    except requests.exceptions.RequestException as e:
        # Mock fallback
        fake_result = {"material_id": "mat_demo_001", "filename": filename}
        result = _failure(e)
        result["data"] = fake_result
        return result


def process_material(material_id=None, youtube_url=None, playlist_url=None, raw_text=None):
    """
    Tells the backend to extract text + identify concepts + build the
    knowledge base for a given material.

    Expected real endpoint:
        POST /materials/process
        Body: {"material_id": ..., "youtube_url": ..., "playlist_url": ..., "text": ...}

    Mock fallback:
        Returns a fixed list of "detected" concepts so the UI can render them.
    """
    payload = {
        "material_id": material_id,
        "youtube_url": youtube_url,
        "playlist_url": playlist_url,
        "text": raw_text,
    }
    try:
        response = requests.post(
            f"{API_BASE_URL}/materials/process",
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return _success(response.json())
    except requests.exceptions.RequestException as e:
        result = _failure(e)
        result["data"] = {"concepts": mock_data.get_mock_detected_concepts()}
        return result


def get_materials():
    """
    Fetches the list of materials the student has already added.

    Expected real endpoint:
        GET /materials
    """
    try:
        response = requests.get(f"{API_BASE_URL}/materials", timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return _success(response.json())
    except requests.exceptions.RequestException as e:
        result = _failure(e)
        result["data"] = mock_data.get_mock_materials()
        return result


# ---------------------------------------------------------------------------
# AI TUTOR
# ---------------------------------------------------------------------------

def ask_question(question, material_id=None):
    """
    Sends a student question to the RAG-powered AI tutor.

    Expected real endpoint:
        POST /ask
        Body: {"question": "...", "material_id": "..."}
        Response: {"answer": "...", "sources": [...]}
    """
    payload = {"question": question, "material_id": material_id}
    try:
        response = requests.post(
            f"{API_BASE_URL}/ask",
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return _success(response.json())
    except requests.exceptions.RequestException as e:
        result = _failure(e)
        result["data"] = mock_data.get_mock_ai_answer(question)
        return result


# ---------------------------------------------------------------------------
# PRACTICE TEST
# ---------------------------------------------------------------------------

def generate_test(material_id=None, concept=None, num_questions=10, difficulty="Adaptive"):
    """
    Requests a personalized test from the backend.

    Expected real endpoint:
        POST /test
        Body: {"material_id", "concept", "num_questions", "difficulty"}
        Response: {"questions": [{"id", "concept", "question", "options"}, ...]}
    """
    payload = {
        "material_id": material_id,
        "concept": concept,
        "num_questions": num_questions,
        "difficulty": difficulty,
    }
    try:
        response = requests.post(
            f"{API_BASE_URL}/test",
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return _success(response.json())
    except requests.exceptions.RequestException as e:
        result = _failure(e)
        result["data"] = {
            "questions": mock_data.get_mock_test_questions(concept or "Dynamic Programming", num_questions)
        }
        return result


def submit_test(test_id, questions, answers):
    """
    Submits student answers for scoring + BKT mastery update.

    Expected real endpoint:
        POST /test/submit
        Body: {"test_id", "answers": {question_id: selected_option}}
        Response: {"score", "total", "accuracy", "concept_stats", "mastery_updates"}
    """
    payload = {"test_id": test_id, "answers": answers}
    try:
        response = requests.post(
            f"{API_BASE_URL}/test/submit",
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return _success(response.json())
    except requests.exceptions.RequestException as e:
        result = _failure(e)
        result["data"] = mock_data.score_mock_test(questions, answers)
        return result


# ---------------------------------------------------------------------------
# PROGRESS / MASTERY / RECOMMENDATIONS
# ---------------------------------------------------------------------------

def get_progress():
    """
    Expected real endpoint: GET /progress
    Returns dashboard-level metrics (mastery, streak, questions attempted...).
    """
    try:
        response = requests.get(f"{API_BASE_URL}/progress", timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return _success(response.json())
    except requests.exceptions.RequestException as e:
        result = _failure(e)
        result["data"] = mock_data.get_mock_dashboard_metrics()
        return result


def get_mastery():
    """
    Expected real endpoint: GET /mastery
    Returns per-concept mastery percentages (produced by the BKT engine).
    """
    try:
        response = requests.get(f"{API_BASE_URL}/mastery", timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return _success(response.json())
    except requests.exceptions.RequestException as e:
        result = _failure(e)
        result["data"] = mock_data.get_mock_mastery()
        return result


def get_recommendations():
    """
    Expected real endpoint: GET /recommendations
    Returns ranked next-topic recommendations (BKT + forgetting + ranking).
    """
    try:
        response = requests.get(f"{API_BASE_URL}/recommendations", timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return _success(response.json())
    except requests.exceptions.RequestException as e:
        result = _failure(e)
        result["data"] = mock_data.get_mock_recommendations()
        return result
