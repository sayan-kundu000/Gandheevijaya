import { describe, it, expect } from "vitest";
import { THEME_CONFIGS, ThemeMode } from "../context/ThemeContext";

describe("5-Mode Theme System Suite", () => {
  it("defines all 5 required theme modes with icons and descriptions", () => {
    expect(THEME_CONFIGS).toHaveLength(5);
    const themeIds = THEME_CONFIGS.map((t) => t.id);
    expect(themeIds).toEqual(["dark", "light", "pink-neon", "blue-neon", "supernatural"]);
  });

  it("has custom names and icons for Pink Neon, Blue Neon, and Supernatural Mode", () => {
    const pinkConfig = THEME_CONFIGS.find((t) => t.id === "pink-neon");
    expect(pinkConfig?.name).toContain("Pink Neon");
    expect(pinkConfig?.icon).toBe("💖");

    const blueConfig = THEME_CONFIGS.find((t) => t.id === "blue-neon");
    expect(blueConfig?.name).toContain("Blue Neon");
    expect(blueConfig?.icon).toBe("⚡");

    const superConfig = THEME_CONFIGS.find((t) => t.id === "supernatural");
    expect(superConfig?.name).toContain("Supernatural Mode");
    expect(superConfig?.icon).toBe("🔯");
  });
});
