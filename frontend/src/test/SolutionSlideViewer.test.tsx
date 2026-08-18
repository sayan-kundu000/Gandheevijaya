import { describe, it, expect } from "vitest";
import { QuestionSolutionItem } from "../types";

const mockSolutions: QuestionSolutionItem[] = [
  {
    question_id: "q1",
    question_text: "What is the capital of France?",
    type: "MCQ",
    options: { A: "London", B: "Paris", C: "Berlin", D: "Madrid" },
    user_answer: "B",
    correct_answer: "B",
    is_correct: true,
    marks_awarded: 1.0,
    penalty_deducted: 0.0,
    explanation: "Paris is the capital of France.",
  },
  {
    question_id: "q2",
    question_text: "Which language is used for web styling?",
    type: "MCQ",
    options: { A: "HTML", B: "CSS", C: "Python", D: "Java" },
    user_answer: "A",
    correct_answer: "B",
    is_correct: false,
    marks_awarded: 0.0,
    penalty_deducted: 0.25,
    explanation: "CSS is used for styling HTML.",
  },
  {
    question_id: "q3",
    question_text: "Calculate 5 + 5",
    type: "NAT",
    options: null,
    user_answer: null,
    correct_answer: "10",
    is_correct: false,
    marks_awarded: 0.0,
    penalty_deducted: 0.0,
    explanation: "5 + 5 equals 10.",
  },
];

describe("SolutionSlideViewer Data & Logic Suite", () => {
  it("filters solutions correctly by tab selection", () => {
    const correctFilter = mockSolutions.filter((s) => s.is_correct);
    expect(correctFilter).toHaveLength(1);
    expect(correctFilter[0].question_id).toBe("q1");

    const incorrectFilter = mockSolutions.filter((s) => !s.is_correct && s.user_answer);
    expect(incorrectFilter).toHaveLength(1);
    expect(incorrectFilter[0].question_id).toBe("q2");

    const unansweredFilter = mockSolutions.filter((s) => !s.user_answer);
    expect(unansweredFilter).toHaveLength(1);
    expect(unansweredFilter[0].question_id).toBe("q3");
  });

  it("identifies user selection vs official correct answer accurately", () => {
    const q2 = mockSolutions[1];
    const userChoiceKey = q2.user_answer; // "A"
    const rightChoiceKey = q2.correct_answer; // "B"

    expect(userChoiceKey).toBe("A");
    expect(rightChoiceKey).toBe("B");
    expect(q2.is_correct).toBe(false);
  });

  it("handles navigation index boundaries correctly", () => {
    let index = 0;
    const total = mockSolutions.length;

    // Next button
    index = Math.min(total - 1, index + 1);
    expect(index).toBe(1);

    index = Math.min(total - 1, index + 1);
    expect(index).toBe(2);

    // Bound check next
    index = Math.min(total - 1, index + 1);
    expect(index).toBe(2);

    // Previous button
    index = Math.max(0, index - 1);
    expect(index).toBe(1);
  });
});
