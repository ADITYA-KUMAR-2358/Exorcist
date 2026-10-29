import { mkdir, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { Logger } from "../ui/logger.js";
import { isInteractive } from "../utils/env.js";
import { confirm } from "@clack/prompts";
import { summaryBox } from "../ui/box.js";

export async function initCommand(root: string, logger: Logger, yes = false): Promise<void> {
  logger.info(`Summoning Exorcist in ${root}...`);
  logger.step("Preparing local configuration...");
  await mkdir(join(root, ".exorcist"), { recursive: true });
  await writeFile(join(root, ".exorcist", "config.json"), JSON.stringify({ model: "qwen2.5-coder:3b", types: ["secrets", "deps", "dead_code", "cron"] }, null, 2) + "\n");
  if (!yes && isInteractive()) {
    await confirm({ message: "Would you like to pull the local model now?", initialValue: false });
  }
  logger.success("Environment ready!");
  logger.result(summaryBox("Configuration sealed\n\nNext:  exorcist scan", true));
}
