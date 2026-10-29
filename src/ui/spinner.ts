import ora, { type Ora } from "ora";

export function startSpinner(text: string, enabled: boolean): Ora | null {
  if (!enabled) return null;
  return ora({ text, color: "cyan" }).start();
}
