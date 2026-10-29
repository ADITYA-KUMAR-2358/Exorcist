import { describe, expect, it } from "vitest";
import { scanRepository } from "../src/core/scanners.js";

describe("scanner boundary", () => {
  it("returns JSON-safe findings without UI imports", async () => {
    const findings = await scanRepository("tests/cursed_repo");
    expect(Array.isArray(findings)).toBe(true);
    expect(JSON.stringify(findings)).not.toContain("\u001b[");
  });
});
