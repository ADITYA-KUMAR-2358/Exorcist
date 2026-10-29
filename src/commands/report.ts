import { join } from "node:path";
import { scanRepository } from "../core/scanners.js";
import { writeReport } from "../core/report.js";
import { Logger } from "../ui/logger.js";
import { summaryBox } from "../ui/box.js";

export async function reportCommand(root: string, output: string | undefined, logger: Logger): Promise<void> {
  const destination = output ?? join(root, "exorcist-report.html");
  logger.info(`Sealing an offline report for ${root}...`);
  logger.step("Reading scanner evidence...");
  await writeReport(destination, await scanRepository(root), root);
  logger.step("Writing self-contained HTML...");
  logger.success(`Report sealed at ${destination}`);
  logger.result(summaryBox(`Report    ${destination}\n\nNext:  exorcist report --open`, true));
}
