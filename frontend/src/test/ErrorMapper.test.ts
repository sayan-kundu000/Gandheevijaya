import { describe, it, expect } from "vitest";
import { getErrorMessage } from "../utils/errorMapper";

describe("errorMapper Utility", () => {
  it("returns raw string error directly", () => {
    expect(getErrorMessage("Direct error message")).toBe("Direct error message");
  });

  it("handles FastAPI error message structure", () => {
    const errorObj = {
      response: {
        data: {
          error: {
            message: "Invalid login credentials.",
          },
        },
      },
    };
    expect(getErrorMessage(errorObj)).toBe("Invalid login credentials.");
  });

  it("handles HTTP status 401 session expiration", () => {
    const errorObj = { response: { status: 401 } };
    expect(getErrorMessage(errorObj)).toBe("Your session has expired. Please log in again.");
  });

  it("handles HTTP status 403 forbidden", () => {
    const errorObj = { response: { status: 403 } };
    expect(getErrorMessage(errorObj)).toBe("You do not have permission to access this resource.");
  });

  it("falls back to default message when error is unknown", () => {
    expect(getErrorMessage(null, "Fallback message")).toBe("Fallback message");
  });
});
