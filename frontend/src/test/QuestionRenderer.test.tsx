import { describe, it, expect } from "vitest";
import { AttemptQuestionItem } from "../types";

describe("QuestionRenderer Contract & Data Transformation", () => {
  const mcqQuestion: AttemptQuestionItem = {
    id: "gcs-cprog-01",
    type: "MCQ",
    question_text: "What is the size of int pointer in 64-bit C environment?",
    options: {
      A: "4 bytes",
      B: "8 bytes",
      C: "2 bytes",
      D: "16 bytes",
    },
    marks: 1.0,
    negative_marks: 0.33,
  };

  it("extracts options list correctly from object payload", () => {
    const optionsObj = mcqQuestion.options;
    const entries = Object.entries(optionsObj);
    expect(entries).toHaveLength(4);
    expect(entries[1]).toEqual(["B", "8 bytes"]);
  });

  it("handles MSQ answer string splitting and joins", () => {
    const selected = ["A", "C"];
    const formatted = selected.sort().join(",");
    expect(formatted).toBe("A,C");

    const parsed = formatted.split(",").map((s) => s.trim());
    expect(parsed).toEqual(["A", "C"]);
  });
});
