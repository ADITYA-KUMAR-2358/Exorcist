import { Chalk, type ChalkInstance } from "chalk";
import unicodeSupported from "is-unicode-supported";

export type ThemeOptions = { color?: boolean; ascii?: boolean };

export const supportsColor = process.env.NO_COLOR === undefined && Boolean(process.stdout.isTTY);
export function supportsUnicode(ascii = false): boolean {
  if (ascii || process.env.TERM === "dumb") return false;
  if (process.env.WT_SESSION || process.env.TERM_PROGRAM || process.env.TERM === "xterm-256color") return true;
  if (process.platform !== "win32") return true;
  return unicodeSupported() || process.platform === "win32";
}

export function getSymbols(ascii = false) {
  const unicode = supportsUnicode(ascii);
  return {
    info: unicode ? "ℹ" : "i",
    arrow: unicode ? "→" : "->",
    success: unicode ? "✔" : "√",
    warning: unicode ? "⚠" : "!",
    error: unicode ? "✖" : "x",
    prompt: "?",
  } as const;
}

export type Theme = {
  cyan: ChalkInstance;
  teal: ChalkInstance;
  green: ChalkInstance;
  yellow: ChalkInstance;
  red: ChalkInstance;
  magenta: ChalkInstance;
  dim: ChalkInstance;
  white: ChalkInstance;
};

export function createTheme(options: ThemeOptions = {}): Theme {
  const enabled = options.color ?? supportsColor;
  const base = new Chalk({ level: enabled ? 1 : 0 });
  return {
    cyan: base.cyan,
    teal: base.hex("#2dd4bf"),
    green: base.green,
    yellow: base.yellow,
    red: base.red,
    magenta: base.magenta,
    dim: base.dim,
    white: base.white,
  };
}
