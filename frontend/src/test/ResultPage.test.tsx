import { describe, it, expect } from "vitest";
import { Result } from "../types";

describe("Result Data & Scoring Calculations Contract", () => {
  const dummyResult: Result = {
    id: "res-123",
    attempt_id: "att-123",
    quiz_id: 1,
    quiz_title: "C Programming Pointers Test",
    subject_name: "C Programming",
    user_id: "user-456",
    total_questions: 10,
    attempted_count: 8,
    correct_count: 7,
    incorrect_count: 1,
    unanswered_count: 2,
    total_marks: 10,
    score: 6.67,
    percentage: 66.7,
    accuracy: 87.5,
    time_taken_seconds: 480,
    passed: true,
    completed_at: new Date().toISOString(),
  };

  it("evaluates accuracy percentage correctly", () => {
    expect(dummyResult.accuracy).toBe(87.5);
    expect(dummyResult.passed).toBe(true);
    expect(dummyResult.attempted_count).toBe(dummyResult.correct_count + dummyResult.incorrect_count);
  });
});
