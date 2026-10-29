import { writeFile } from "node:fs/promises";
import type { Finding } from "./scanners.js";

export async function writeReport(path: string, findings: Finding[], root: string): Promise<void> {
  const rows = findings.map((finding) => `<li><strong>${finding.severity}</strong> ${finding.file}:${finding.line} - ${finding.detail}</li>`).join("");
  const html = `<!doctype html><meta charset="utf-8"><title>Exorcist report</title><style>body{background:#0b0d12;color:#e6e8ee;font:16px system-ui;max-width:900px;margin:40px auto}li{margin:12px 0}</style><h1>EXORCIST</h1><p>${root}</p><ul>${rows || "<li>Repository is quiet.</li>"}</ul>`;
  await writeFile(path, html, "utf8");
}
