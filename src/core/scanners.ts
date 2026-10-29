import { readFile, readdir } from "node:fs/promises";
import { join, relative } from "node:path";

export type Finding = {
  type: "secret" | "dependency" | "dead_code" | "zombie_job";
  file: string;
  line: number;
  severity: "low" | "medium" | "high" | "critical";
  detail: string;
};

const ignored = new Set([".git", "node_modules", ".venv", "dist", "__pycache__"]);

async function filesIn(root: string, current = root): Promise<string[]> {
  const entries = await readdir(current, { withFileTypes: true });
  const files: string[] = [];
  for (const entry of entries) {
    if (ignored.has(entry.name)) continue;
    const path = join(current, entry.name);
    if (entry.isDirectory()) files.push(...(await filesIn(root, path)));
    else files.push(path);
  }
  return files;
}

export async function scanRepository(root: string): Promise<Finding[]> {
  const findings: Finding[] = [];
  for (const file of await filesIn(root)) {
    let text: string;
    try {
      text = await readFile(file, "utf8");
    } catch {
      continue;
    }
    const lines = text.split(/\r?\n/);
    lines.forEach((line, index) => {
      if (/(AKIA[0-9A-Z]{16}|(?:secret|token|password)\s*=\s*['"][^'"]{8,})/i.test(line)) {
        findings.push({ type: "secret", file: relative(root, file), line: index + 1, severity: "critical", detail: "Possible hardcoded credential" });
      }
      if (/\bTODO\b|\bFIXME\b/.test(line)) {
        findings.push({ type: "dead_code", file: relative(root, file), line: index + 1, severity: "low", detail: "Review unfinished code marker" });
      }
    });
    if (/cron|schedule/i.test(file) && /[^\s]+\.sh/.test(text)) {
      findings.push({ type: "zombie_job", file: relative(root, file), line: 1, severity: "medium", detail: "Scheduled script should be verified" });
    }
  }
  return findings;
}
