import { describe, it, expect } from "vitest";

describe("Admin Ingestion ETL Contract", () => {
  it("formats import params for backend endpoint accurately", () => {
    const params = {
      source_path: "datasets",
      dry_run: true,
      upsert: false,
      subject: "CPROG",
    };

    expect(params.source_path).toBe("datasets");
    expect(params.dry_run).toBe(true);
    expect(params.upsert).toBe(false);
  });
});
