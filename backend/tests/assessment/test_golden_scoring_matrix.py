import pytest
from backend.app.models.content import Question
from backend.app.services.scoring_service import ScoringService


def test_golden_scoring_calculation_matrix(db_session):
    """
    GOLDEN SCORING TEST: Verify server-side scoring accuracy across a fixed matrix
    of MCQ (+1.0 / -0.25), MSQ (+1.0 / 0.0), and NAT (+1.0 / 0.0) questions.
    """
    scorer = ScoringService()

    # 1. MCQ Test Cases
    q_mcq = Question(
        id="Q-GOLD-MCQ",
        topic_id=1,
        type="MCQ",
        difficulty="MEDIUM",
        question_text="What is 2+2?",
        options={"A": "3", "B": "4", "C": "5", "D": "6"},
        correct_answer="B",
        explanation="2+2=4",
    )

    # MCQ Correct -> +1.0
    res_mcq_correct = scorer.evaluate_question_response(
        q_mcq, selected_answer="B", marks_possible=1.0, negative_marks=0.25
    )
    assert res_mcq_correct.is_correct is True
    assert res_mcq_correct.marks_awarded == 1.0

    # MCQ Incorrect -> -0.25
    res_mcq_wrong = scorer.evaluate_question_response(
        q_mcq, selected_answer="A", marks_possible=1.0, negative_marks=0.25
    )
    assert res_mcq_wrong.is_correct is False
    assert res_mcq_wrong.marks_awarded == -0.25

    # MCQ Unanswered -> 0.0
    res_mcq_unans = scorer.evaluate_question_response(
        q_mcq, selected_answer=None, marks_possible=1.0, negative_marks=0.25
    )
    assert res_mcq_unans.is_correct is False
    assert res_mcq_unans.marks_awarded == 0.0

    # 2. MSQ Test Cases (Multiple Select)
    q_msq = Question(
        id="Q-GOLD-MSQ",
        topic_id=1,
        type="MSQ",
        difficulty="HARD",
        question_text="Select all even numbers",
        options={"A": "2", "B": "3", "C": "4", "D": "5"},
        correct_answer="A,C",
        explanation="2 and 4 are even",
    )

    # MSQ All Correct -> +1.0
    res_msq_correct = scorer.evaluate_question_response(
        q_msq, selected_answer="A,C", marks_possible=1.0, negative_marks=0.0
    )
    assert res_msq_correct.is_correct is True
    assert res_msq_correct.marks_awarded == 1.0

    # MSQ Partial/Wrong -> 0.0
    res_msq_partial = scorer.evaluate_question_response(
        q_msq, selected_answer="A", marks_possible=1.0, negative_marks=0.0
    )
    assert res_msq_partial.is_correct is False
    assert res_msq_partial.marks_awarded == 0.0

    # 3. NAT Test Cases (Numerical)
    q_nat = Question(
        id="Q-GOLD-NAT",
        topic_id=1,
        type="NAT",
        difficulty="EASY",
        question_text="Enter value of 5*5",
        options=None,
        correct_answer="25",
        explanation="5*5=25",
    )

    # NAT Correct -> +1.0
    res_nat_correct = scorer.evaluate_question_response(
        q_nat, selected_answer="25", marks_possible=1.0, negative_marks=0.0
    )
    assert res_nat_correct.is_correct is True
    assert res_nat_correct.marks_awarded == 1.0

    # NAT Wrong -> 0.0
    res_nat_wrong = scorer.evaluate_question_response(
        q_nat, selected_answer="24", marks_possible=1.0, negative_marks=0.0
    )
    assert res_nat_wrong.is_correct is False
    assert res_nat_wrong.marks_awarded == 0.0
