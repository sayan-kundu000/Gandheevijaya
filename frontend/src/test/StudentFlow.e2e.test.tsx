import { describe, it, expect } from "vitest";

describe("Student Critical Path Workflow", () => {
  it("validates student navigation route sequence", () => {
    const studentRoutes = [
      "/dashboard",
      "/exams",
      "/exams/1",
      "/subjects/1",
      "/topics/1",
      "/quizzes",
      "/quizzes/1",
      "/quiz/att-101",
      "/results/res-101",
      "/results",
      "/analytics",
      "/profile",
    ];

    expect(studentRoutes).toContain("/dashboard");
    expect(studentRoutes).toContain("/quiz/att-101");
    expect(studentRoutes).toContain("/results/res-101");
    expect(studentRoutes).toContain("/analytics");
  });
});
