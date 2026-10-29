import { describe, expect, it } from "vitest";
import { EXORCIST_ART, renderBanner } from "../src/ui/banner.js";

describe("banner", () => {
  it("uses the requested block art and metadata", () => {
    expect(EXORCIST_ART).toContain("███████╗██╗  ██╗");
    expect(renderBanner(false)).toContain("@exorcist/cli v");
    expect(renderBanner(false)).toContain("scanners find  /  local Ollama triages  /  zero telemetry");
  });
});
