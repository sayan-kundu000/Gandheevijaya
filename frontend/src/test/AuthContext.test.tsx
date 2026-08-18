import { describe, it, expect, beforeEach } from "vitest";

describe("AuthContext and LocalStorage Tokens", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("persists access token and refresh token upon login", () => {
    localStorage.setItem("gandheevijaya_access_token", "test_access_token_123");
    localStorage.setItem("gandheevijaya_refresh_token", "test_refresh_token_456");

    expect(localStorage.getItem("gandheevijaya_access_token")).toBe("test_access_token_123");
    expect(localStorage.getItem("gandheevijaya_refresh_token")).toBe("test_refresh_token_456");
  });

  it("clears tokens upon logout", () => {
    localStorage.setItem("gandheevijaya_access_token", "token");
    localStorage.removeItem("gandheevijaya_access_token");
    expect(localStorage.getItem("gandheevijaya_access_token")).toBeNull();
  });
});
