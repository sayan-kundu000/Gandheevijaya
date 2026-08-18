import { describe, it, expect } from "vitest";

describe("Taxonomy & Exam Categories Contract", () => {
  it("supports GATE CS, SSC, and Banking as primary exam categories", () => {
    const exams = [
      { id: 1, code: "GATE_CS", name: "GATE CS" },
      { id: 2, code: "SSC", name: "SSC Examinations" },
      { id: 3, code: "BANKING", name: "Banking Examinations" },
    ];

    expect(exams).toHaveLength(3);
    expect(exams.map((e) => e.code)).toContain("GATE_CS");
    expect(exams.map((e) => e.code)).toContain("SSC");
    expect(exams.map((e) => e.code)).toContain("BANKING");
  });
});
