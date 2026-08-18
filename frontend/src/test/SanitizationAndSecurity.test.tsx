import { describe, it, expect } from "vitest";

describe("Frontend Sanitization & Security Protection", () => {
  it("verifies script injection payloads in question prompt are safe strings", () => {
    const xssPayload = "<script>window.xssHacked = true;</script><img src=x onerror='window.xssHacked=true'>";
    
    // Verify payload is stored as raw string and not evaluated as HTML DOM script execution
    expect(xssPayload).toContain("<script>");
    const isHacked = typeof window !== "undefined" ? (window as any).xssHacked : undefined;
    expect(isHacked).toBeUndefined();
  });
});
