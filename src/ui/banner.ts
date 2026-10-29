import gradient from "gradient-string";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { createTheme } from "./theme.js";

const moduleDirectory = dirname(fileURLToPath(import.meta.url));
const root = moduleDirectory.endsWith(`${join("src", "ui")}`)
  ? dirname(dirname(moduleDirectory))
  : dirname(moduleDirectory);

export const EXORCIST_ART = 
` ███████╗██╗  ██╗ ██████╗ ██████╗  ██████╗██╗███████╗████████╗
  ██╔════╝╚██╗██╔╝██╔═══██╗██╔══██╗██╔════╝██║██╔════╝╚══██╔══╝
  █████╗   ╚███╔╝ ██║   ██║██████╔╝██║     ██║███████╗   ██║
  ██╔══╝   ██╔██╗ ██║   ██║██╔══██╗██║     ██║╚════██║   ██║
  ███████╗██╔╝ ██╗╚██████╔╝██║  ██║╚██████╗██║███████║   ██║
 ╚══════╝╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝╚══════╝   ╚═╝`;

export function packageVersion(): string {
  const packagePath = join(root, "package.json");
  return JSON.parse(readFileSync(packagePath, "utf8")).version as string;
}

export function renderBanner(color = true): string {
  const theme = createTheme({ color });
  const title = EXORCIST_ART.split("\n")
    .map((line) => (color ? gradient("#22d3ee", "#14b8a6")(line) : line))
    .join("\n");
  return [
    "",
    title,
    "",
    theme.dim("  @exorcist/cli v" + packageVersion()),
    theme.dim("  Local-first code cleansing ritual"),
    theme.dim("  scanners find  /  local Ollama triages  /  zero telemetry"),
    theme.dim("  Created by Aditya Kumar <aditya.kumar2358@gmail.com>"),
    "",
  ].join("\n");
}
