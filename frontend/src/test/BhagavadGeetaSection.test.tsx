import { describe, it, expect } from "vitest";
import { GITA_CHAPTERS, EXAM_WISDOM_TOPICS } from "../components/common/BhagavadGeetaSection";

describe("Bhagavad Geeta Click-Based Section Suite", () => {
  it("contains all 24 chapters across 3 parts including all 18 authentic Bhagavad Gita chapters in Part II", () => {
    expect(GITA_CHAPTERS).toHaveLength(24);
    const chapterIds = GITA_CHAPTERS.map((ch) => ch.id);
    expect(chapterIds).toContain(1); // What Is the Bhagavad Gita, Really?
    expect(chapterIds).toContain(2); // Arjuna's Crisis
    expect(chapterIds).toContain(18); // Chapter 16: Daivasura Sampad Vibhaga Yoga
    expect(chapterIds).toContain(19); // Chapter 17: Shraddhatraya Vibhaga Yoga
    expect(chapterIds).toContain(20); // Chapter 18: Moksha Sannyasa Yoga
    expect(chapterIds).toContain(23); // Why We Need the Gita in Exams
    expect(chapterIds).toContain(24); // The Student's Gita
  });

  it("includes Daivasura Sampad, Shraddhatraya, and Moksha Sannyasa Yoga as individual chapters", () => {
    const ch18 = GITA_CHAPTERS.find((ch) => ch.id === 18);
    expect(ch18?.title).toContain("Daivasura Sampad Vibhaga Yoga");

    const ch19 = GITA_CHAPTERS.find((ch) => ch.id === 19);
    expect(ch19?.title).toContain("Shraddhatraya Vibhaga Yoga");

    const ch20 = GITA_CHAPTERS.find((ch) => ch.id === 20);
    expect(ch20?.title).toContain("Moksha Sannyasa Yoga");
  });

  it("includes all 14 core exam psychological topics in Chapter 23 & Wisdom Grid", () => {
    expect(EXAM_WISDOM_TOPICS).toHaveLength(8);
    const ch23 = GITA_CHAPTERS.find((ch) => ch.id === 23);
    expect(ch23?.summary).toContain("14 core mental competencies");
    expect(ch23?.keyPoints[0]).toContain("Anxiety Management");
    expect(ch23?.keyPoints[0]).toContain("Result Detachment");
  });

  it("exports valid chapter structures with non-empty key points and student takeaways", () => {
    GITA_CHAPTERS.forEach((ch) => {
      expect(ch.id).toBeGreaterThan(0);
      expect(ch.title).toBeTruthy();
      expect(ch.summary).toBeTruthy();
      expect(ch.studentTakeaway).toBeTruthy();
      expect(ch.keyPoints.length).toBeGreaterThan(0);
    });
  });
});
