"""
utils/mock_data.py

All fake/demo data lives here.

WHY THIS FILE EXISTS
---------------------
Your FastAPI backend (ML models, RAG pipeline, BKT engine) is not ready yet.
So instead of the frontend crashing or showing empty screens, every page can
import functions from this file and get realistic-looking data.

WHEN YOUR BACKEND IS READY
---------------------------
You do NOT need to delete this file. The `backend/api_client.py` file already
falls back to these functions automatically whenever the real API call fails
or is unavailable. You can keep this file forever as a "demo mode" data source.
"""

import random
from datetime import datetime, timedelta


# ---------------------------------------------------------------------------
# CONCEPTS + MASTERY
# ---------------------------------------------------------------------------

def get_mock_mastery():
    """Returns a dict of {concept_name: mastery_percentage}."""
    return {
        "Python Basics": 91,
        "Functions": 82,
        "Recursion": 61,
        "Dynamic Programming": 43,
        "Graphs": 72,
        "Trees": 55,
    }


def get_mock_overall_mastery():
    mastery = get_mock_mastery()
    return round(sum(mastery.values()) / len(mastery))


def get_mock_weak_concepts(top_n=3):
    """Returns the weakest concepts sorted ascending by mastery."""
    mastery = get_mock_mastery()
    sorted_concepts = sorted(mastery.items(), key=lambda x: x[1])

    status_map = {}
    for concept, score in sorted_concepts:
        if score < 50:
            status_map[concept] = "Needs revision"
        elif score < 70:
            status_map[concept] = "Improving"
        else:
            status_map[concept] = "Solid"

    result = []
    for concept, score in sorted_concepts[:top_n]:
        result.append({
            "concept": concept,
            "mastery": score,
            "status": status_map[concept],
        })
    return result


def get_mock_concepts_to_improve():
    """Concept-wise breakdown used on the 'My Mastery' page."""
    mastery = get_mock_mastery()
    last_practiced_days = {
        "Python Basics": 1,
        "Functions": 2,
        "Recursion": 4,
        "Dynamic Programming": 3,
        "Graphs": 6,
        "Trees": 5,
    }

    rows = []
    for concept, score in mastery.items():
        if score < 50:
            risk = "High"
        elif score < 75:
            risk = "Medium"
        else:
            risk = "Low"

        days = last_practiced_days.get(concept, 3)
        rows.append({
            "concept": concept,
            "mastery": score,
            "risk": risk,
            "last_practiced": f"{days} days ago" if days > 1 else "1 day ago",
        })

    # Weakest first
    rows.sort(key=lambda x: x["mastery"])
    return rows


def get_mock_detected_concepts():
    """Concepts 'extracted' after processing a new material."""
    return ["Variables", "Functions", "Recursion", "Stack", "Dynamic Programming"]


# ---------------------------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------------------------

def get_mock_dashboard_metrics():
    return {
        "overall_mastery": get_mock_overall_mastery(),
        "concepts_learned": len(get_mock_mastery()),
        "questions_attempted": 148,
        "current_streak": 6,
    }


def get_mock_continue_learning():
    return [
        {"topic": "Python Functions", "mastery": 82},
        {"topic": "Recursion", "mastery": 61},
        {"topic": "Dynamic Programming", "mastery": 43},
        {"topic": "Graph Algorithms", "mastery": 72},
    ]


def get_mock_recommendation_highlight():
    return {
        "text": "Revise Dynamic Programming basics before attempting advanced DP questions.",
        "concept": "Dynamic Programming",
    }


# ---------------------------------------------------------------------------
# MATERIALS ("My Learning")
# ---------------------------------------------------------------------------

def get_mock_materials():
    """Simulates materials the student has already added to LearnMind."""
    today = datetime.now()
    return [
        {
            "id": "mat_001",
            "title": "Python DSA Lecture",
            "type": "Video",
            "icon": "🎥",
            "concepts": 12,
            "date_added": (today - timedelta(days=5)).strftime("%d %b %Y"),
            "progress": 65,
            "status": "In Progress",
        },
        {
            "id": "mat_002",
            "title": "Dynamic Programming Notes",
            "type": "PDF",
            "icon": "📄",
            "concepts": 8,
            "date_added": (today - timedelta(days=3)).strftime("%d %b %Y"),
            "progress": 43,
            "status": "Needs Revision",
        },
        {
            "id": "mat_003",
            "title": "Graph Algorithms Playlist",
            "type": "Playlist",
            "icon": "🎞️",
            "concepts": 15,
            "date_added": (today - timedelta(days=10)).strftime("%d %b %Y"),
            "progress": 72,
            "status": "In Progress",
        },
        {
            "id": "mat_004",
            "title": "Python Basics — Handwritten Notes",
            "type": "TXT",
            "icon": "📝",
            "concepts": 6,
            "date_added": (today - timedelta(days=20)).strftime("%d %b %Y"),
            "progress": 91,
            "status": "Mastered",
        },
    ]


# ---------------------------------------------------------------------------
# AI TUTOR (CHAT)
# ---------------------------------------------------------------------------

_MOCK_ANSWERS = [
    (
        "Based on your lecture, memoization solves subproblems top-down using "
        "recursion plus a cache, while tabulation solves them bottom-up using "
        "an iterative table. Memoization is often easier to write, tabulation "
        "is usually more memory-efficient."
    ),
    (
        "A recursive function is one that calls itself. It needs a base case "
        "(to stop) and a recursive case (to make progress toward the base case). "
        "Your notes cover this in the 'Recursion Basics' section."
    ),
    (
        "In your Dynamic Programming notes, the key idea is 'optimal substructure' "
        "— a problem can be solved using solutions to its smaller subproblems, "
        "and 'overlapping subproblems' — the same subproblem is solved multiple times."
    ),
    (
        "A stack follows Last-In-First-Out (LIFO) order. It's commonly used to "
        "implement recursion internally, undo operations, and to convert "
        "recursive algorithms into iterative ones."
    ),
]


def get_mock_ai_answer(question: str):
    """Fakes a RAG-based answer + sources for the AI Tutor page."""
    answer = random.choice(_MOCK_ANSWERS)
    sources = [
        {"material": "Dynamic Programming Lecture", "concept": "Memoization"},
        {"material": "Python DSA Lecture", "concept": "Recursion"},
    ]
    return {"answer": answer, "sources": sources}


# ---------------------------------------------------------------------------
# PRACTICE TEST
# ---------------------------------------------------------------------------

_QUESTION_BANK = {
    "Dynamic Programming": [
        "What is the main difference between memoization and tabulation?",
        "Which of the following problems is a classic DP problem?",
        "What does 'optimal substructure' mean?",
        "What is the time complexity of the naive Fibonacci recursion?",
        "Which technique avoids recomputation of overlapping subproblems?",
    ],
    "Recursion": [
        "What is a base case in recursion?",
        "What happens if a recursive function has no base case?",
        "Which data structure is used internally to manage recursive calls?",
        "What is tail recursion?",
    ],
    "Graphs": [
        "Which algorithm is used to find the shortest path in an unweighted graph?",
        "What is a cycle in a graph?",
        "Which traversal uses a queue?",
        "What is the difference between BFS and DFS?",
    ],
    "Functions": [
        "What is a pure function?",
        "What is the purpose of a return statement?",
        "What is a default argument?",
    ],
}

_OPTION_SETS = [
    ["Option A", "Option B", "Option C", "Option D"],
    ["True", "False", "Depends on input", "Cannot be determined"],
    ["O(1)", "O(n)", "O(2^n)", "O(n log n)"],
]


def get_mock_test_questions(concept: str, num_questions: int = 5):
    """Generates fake multiple-choice questions for a given concept."""
    pool = _QUESTION_BANK.get(concept, _QUESTION_BANK["Dynamic Programming"])
    questions = []
    for i in range(num_questions):
        q_text = pool[i % len(pool)]
        options = random.choice(_OPTION_SETS)
        questions.append({
            "id": i + 1,
            "concept": concept,
            "question": q_text,
            "options": options,
            "correct_option": options[0],  # mock "correct" answer
        })
    return questions


def score_mock_test(questions, answers):
    """
    Very simple mock scoring so the UI has something to show.
    In the real backend, correctness + scoring will come from the API response.
    """
    total = len(questions)
    correct = 0
    concept_stats = {}

    for q in questions:
        user_answer = answers.get(q["id"])
        is_correct = random.random() < 0.7  # simulate realistic performance
        if is_correct:
            correct += 1

        stats = concept_stats.setdefault(q["concept"], {"correct": 0, "total": 0})
        stats["total"] += 1
        if is_correct:
            stats["correct"] += 1

    accuracy = round((correct / total) * 100) if total else 0
    return {
        "score": correct,
        "total": total,
        "accuracy": accuracy,
        "concept_stats": concept_stats,
    }


# ---------------------------------------------------------------------------
# RECOMMENDATIONS
# ---------------------------------------------------------------------------

def get_mock_recommendations():
    return [
        {
            "priority": "High Priority",
            "emoji": "🔴",
            "concept": "Dynamic Programming",
            "mastery": 43,
            "reason": "Low mastery + high recent error rate.",
            "action_label": "Revise Concept",
        },
        {
            "priority": "Medium Priority",
            "emoji": "🟡",
            "concept": "Recursion",
            "mastery": 61,
            "reason": "Some forgetting detected.",
            "action_label": "Practice",
        },
        {
            "priority": "Next Challenge",
            "emoji": "🟢",
            "concept": "Graphs",
            "mastery": 72,
            "reason": "You're ready for harder questions.",
            "action_label": "Take Advanced Test",
        },
    ]
