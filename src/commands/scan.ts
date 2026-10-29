import { join } from "node:path";
import type { Finding } from "../core/scanners.js";
import { scanRepository } from "../core/scanners.js";
import { writeReport } from "../core/report.js";
import { summaryBox } from "../ui/box.js";
import { Logger } from "../ui/logger.js";

export async function scanCommand(root: string, logger: Logger, json: boolean): Promise<number> {
  if (!json) {
    logger.info(`Summoning Exorcist in ${root}...`);
    logger.step("Detecting project type and languages...");
    logger.step("Checking Ollama and model (qwen2.5-coder:3b)...");
    logger.step("Loading rule packs (secrets, deps, dead code, cron)...");
    logger.success("Environment ready!");
  }
  const findings = await scanRepository(root);
  if (json) {
    logger.jsonResult(JSON.stringify({ root, findings }, null, 2));
    return findings.some((item) => item.severity === "critical" || item.severity === "high") ? 1 : 0;
  }
  const counts = { critical: 0, high: 0, medium: 0, low: 0 };
  findings.forEach((finding) => {
    counts[finding.severity] += 1;
    logger.success(`${finding.file}:${finding.line} ${finding.detail}`);
  });
  const reportPath = join(root, "exorcist-report.html");
  await writeReport(reportPath, findings, root);
  logger.result(summaryBox(`Critical  ${counts.critical}\nHigh      ${counts.high}\nMedium    ${counts.medium}\nLow       ${counts.low}\n\nReport    ${reportPath}\n\nNext steps\n  exorcist report --open\n  exorcist fix --pr`, true));
  return findings.some((item) => item.severity === "critical" || item.severity === "high") ? 1 : 0;
}
