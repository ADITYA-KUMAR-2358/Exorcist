import { describe, expect, it } from "vitest";
import { isInteractive, shouldAnimate } from "../src/utils/env.js";

describe("environment detection", () => {
  it("disables interactive output in the test runner", () => {
    expect(isInteractive()).toBe(false);
    expect(shouldAnimate()).toBe(false);
  });
});
