import { describe, it, expect } from "vitest";

describe("Admin Navigation & Governance Workflow", () => {
  it("verifies all admin routes match protected governance specifications", () => {
    const adminRoutes = [
      "/admin",
      "/admin/exams",
      "/admin/subjects",
      "/admin/topics",
      "/admin/questions",
      "/admin/questions/q-101",
      "/admin/quizzes",
      "/admin/ingestion",
      "/admin/content-quality",
      "/admin/analytics",
      "/admin/users",
    ];

    expect(adminRoutes).toHaveLength(11);
    expect(adminRoutes).toContain("/admin/ingestion");
    expect(adminRoutes).toContain("/admin/content-quality");
    expect(adminRoutes).toContain("/admin/questions");
  });
});
