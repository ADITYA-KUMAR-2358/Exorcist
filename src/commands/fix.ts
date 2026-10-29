import { Logger } from "../ui/logger.js";
import { summaryBox } from "../ui/box.js";

export async function fixCommand(logger: Logger, dryRun: boolean): Promise<void> {
  logger.info(dryRun ? "Dry run: preparing safe fix proposals..." : "Fix application is guarded behind explicit review.");
  logger.step("No files were changed.");
  logger.result(summaryBox("No files changed\n\nNext:  review the proposed diff", true));
}
