import json
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, List, Optional, Tuple, Union

from backend.app.models.content import Question
from backend.app.models.quiz import QuizQuestion
from backend.app.schemas.quiz import QuestionReviewItem


class ScoringEvaluationResult:
    def __init__(
        self,
        is_correct: bool,
        marks_awarded: float,
        penalty_deducted: float,
        review_item: QuestionReviewItem,
    ):
        self.is_correct = is_correct
        self.marks_awarded = marks_awarded
        self.penalty_deducted = penalty_deducted
        self.review_item = review_item


class ScoringService:
    """
    Server-authoritative scoring engine supporting MCQ, MSQ, and NAT questions
    with fractional marking precision, configurable negative marking, and performance metrics.
    """

    @staticmethod
    def evaluate_mcq(
        question: Question,
        selected_answer: Optional[str],
        marks_possible: float,
        negative_marks: float,
    ) -> Tuple[bool, float, float]:
        """
        MCQ Evaluation:
        - Correct option: +marks_possible
        - Wrong option: -abs(negative_marks)
        - Unanswered: 0.0
        """
        if not selected_answer or not str(selected_answer).strip():
            return False, 0.0, 0.0

        correct_target = str(question.correct_answer).strip().lower()
        submitted_target = str(selected_answer).strip().lower()

        if correct_target == submitted_target:
            return True, float(marks_possible), 0.0
        else:
            penalty = float(abs(negative_marks))
            return False, -penalty, penalty

    @staticmethod
    def evaluate_msq(
        question: Question,
        selected_answer: Optional[str],
        marks_possible: float,
        negative_marks: float,
    ) -> Tuple[bool, float, float]:
        """
        MSQ Evaluation (All-or-Nothing policy as standard per GATE CS rules):
        - 100% exact set match: +marks_possible
        - Incorrect set: -abs(negative_marks) or 0 (configurable)
        - Unanswered: 0.0
        """
        if not selected_answer or not str(selected_answer).strip():
            return False, 0.0, 0.0

        # Parse target correct set
        try:
            if str(question.correct_answer).startswith("["):
                correct_set = set(json.loads(str(question.correct_answer)))
            else:
                correct_set = {s.strip().lower() for s in str(question.correct_answer).split(",")}
        except Exception:
            correct_set = {str(question.correct_answer).strip().lower()}

        # Parse submitted set
        try:
            if str(selected_answer).startswith("["):
                submitted_set = set(json.loads(str(selected_answer)))
            else:
                submitted_set = {s.strip().lower() for s in str(selected_answer).split(",")}
        except Exception:
            submitted_set = {str(selected_answer).strip().lower()}

        if correct_set == submitted_set:
            return True, float(marks_possible), 0.0
        else:
            penalty = float(abs(negative_marks))
            return False, -penalty, penalty

    @staticmethod
    def evaluate_nat(
        question: Question,
        selected_answer: Optional[str],
        marks_possible: float,
        tolerance: float = 0.01,
    ) -> Tuple[bool, float, float]:
        """
        NAT (Numerical Answer Type) Evaluation:
        - Match within tolerance: +marks_possible
        - Incorrect numeric value: 0.0 (No negative marking for NAT per GATE CS standards)
        - Unanswered: 0.0
        """
        if not selected_answer or not str(selected_answer).strip():
            return False, 0.0, 0.0

        try:
            submitted_val = float(str(selected_answer).strip())
            correct_val = float(str(question.correct_answer).strip())

            if abs(submitted_val - correct_val) <= tolerance:
                return True, float(marks_possible), 0.0
            else:
                return False, 0.0, 0.0
        except ValueError:
            return False, 0.0, 0.0

    def evaluate_question_response(
        self,
        question: Question,
        selected_answer: Optional[str],
        marks_possible: float,
        negative_marks: float,
    ) -> ScoringEvaluationResult:
        """
        Dispatches scoring evaluation based on Question.question_type.
        """
        raw_type = getattr(question, "type", None) or getattr(question, "question_type", "MCQ")
        q_type = str(raw_type or "MCQ").upper()

        if q_type == "MSQ":
            is_correct, score_change, penalty = self.evaluate_msq(
                question, selected_answer, marks_possible, negative_marks
            )
        elif q_type in ("NAT", "NUMERICAL"):
            is_correct, score_change, penalty = self.evaluate_nat(
                question, selected_answer, marks_possible
            )
        else:  # MCQ default
            is_correct, score_change, penalty = self.evaluate_mcq(
                question, selected_answer, marks_possible, negative_marks
            )

        review_item = QuestionReviewItem(
            question_id=question.id,
            question_text=question.question_text,
            options=question.options,
            selected_answer=selected_answer,
            correct_answer=question.correct_answer,
            is_correct=is_correct,
            marks_awarded=score_change,
            penalty_deducted=penalty,
            marks_possible=marks_possible,
            explanation=question.explanation,
        )

        return ScoringEvaluationResult(
            is_correct=is_correct,
            marks_awarded=score_change,
            penalty_deducted=penalty,
            review_item=review_item,
        )

    @staticmethod
    def calculate_summary_stats(
        total_questions: int,
        correct_count: int,
        incorrect_count: int,
        unanswered_count: int,
        total_score: float,
        total_possible_marks: float,
    ) -> Dict[str, float]:
        """
        Calculates percentage, accuracy, and score metrics avoiding division by zero.
        """
        attempted_count = correct_count + incorrect_count
        percentage = (
            round((total_score / total_possible_marks) * 100.0, 2)
            if total_possible_marks > 0
            else 0.0
        )
        accuracy = (
            round((correct_count / attempted_count) * 100.0, 2)
            if attempted_count > 0
            else 0.0
        )

        return {
            "percentage": percentage,
            "accuracy": accuracy,
            "attempted_count": attempted_count,
        }
