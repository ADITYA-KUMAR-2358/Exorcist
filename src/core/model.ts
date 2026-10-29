import { ExorcistError } from "../utils/errors.js";

export type Triage = { verdict: "real_haunting" | "false_alarm" | "needs_human_review"; reason: string };

export async function triageLocally(prompt: string, model = "qwen2.5-coder:3b"): Promise<Triage> {
  try {
    const response = await fetch("http://127.0.0.1:11434/api/generate", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ model, prompt, stream: false, format: "json", options: { num_ctx: 2048, temperature: 0 } }),
    });
    if (!response.ok) throw new Error(`Ollama returned ${response.status}`);
    const payload = (await response.json()) as { response?: string };
    const parsed = JSON.parse(payload.response ?? "{}") as Partial<Triage>;
    if (!parsed.verdict || !parsed.reason) throw new Error("Ollama returned an invalid triage response");
    return { verdict: parsed.verdict, reason: parsed.reason };
  } catch (error) {
    throw new ExorcistError(
      "Local model triage is unavailable.",
      error instanceof Error ? error.message : "Unknown Ollama error.",
      `Start Ollama and pull ${model}, or continue with scanner-only output.`,
    );
  }
}
