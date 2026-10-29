import { describe, expect, it } from "vitest";
import { createTheme, getSymbols, supportsUnicode } from "../src/ui/theme.js";

describe("theme", () => {
  it("strips ANSI styles when color is disabled", () => {
    expect(createTheme({ color: false }).cyan("info")).toBe("info");
  });

  it("exposes stable status symbols", () => {
    const symbols = getSymbols();
    expect(symbols.info).toBe("ℹ");
    expect(symbols.arrow).toBe("→");
    expect(symbols.success).toBe("✔");
  });

  it("only switches to ASCII when explicitly requested", () => {
    expect(supportsUnicode(true)).toBe(false);
    expect(getSymbols(true)).toMatchObject({ info: "i", arrow: "->", success: "√", warning: "!", error: "x" });
  });
});
