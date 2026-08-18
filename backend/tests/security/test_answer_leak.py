from backend.app.schemas.user import QuestionForAdmin, QuestionForQuizStudent


def test_question_schema_for_student_strips_sensitive_answers():
    raw_question = {
        "id": "q_1001",
        "topic_id": 1,
        "subtopic_id": 2,
        "difficulty": "MEDIUM",
        "type": "SINGLE_CHOICE",
        "question_text": "What is the capital of India?",
        "options": [
            {"id": "opt_a", "text": "Mumbai"},
            {"id": "opt_b", "text": "New Delhi"},
            {"id": "opt_c", "text": "Kolkata"},
        ],
        "correct_answer": "opt_b",  # Highly sensitive content!
        "explanation": "New Delhi is the official capital of India.",  # Highly sensitive content!
        "tags": ["GATE", "GK"],
    }

    # Deserialize into student-facing Pydantic model
    student_q = QuestionForQuizStudent.model_validate(raw_question)
    dumped = student_q.model_dump()

    # Assert correct_answer and explanation are completely stripped from student payload
    assert "correct_answer" not in dumped
    assert "explanation" not in dumped
    assert dumped["id"] == "q_1001"
    assert dumped["question_text"] == "What is the capital of India?"


def test_question_schema_for_admin_includes_full_answer_key():
    raw_question = {
        "id": "q_1001",
        "topic_id": 1,
        "subtopic_id": 2,
        "difficulty": "MEDIUM",
        "type": "SINGLE_CHOICE",
        "question_text": "What is the capital of India?",
        "options": [
            {"id": "opt_a", "text": "Mumbai"},
            {"id": "opt_b", "text": "New Delhi"},
            {"id": "opt_c", "text": "Kolkata"},
        ],
        "correct_answer": "opt_b",
        "explanation": "New Delhi is the official capital of India.",
        "tags": ["GATE", "GK"],
    }

    admin_q = QuestionForAdmin.model_validate(raw_question)
    dumped = admin_q.model_dump()

    assert dumped["correct_answer"] == "opt_b"
    assert dumped["explanation"] == "New Delhi is the official capital of India."
