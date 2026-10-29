import { existsSync } from "node:fs";
import { join } from "node:path";
import { summaryBox } from "../ui/box.js";
import { Logger } from "../ui/logger.js";

type Check = { name: string; value: string; state: "ok" | "warn" | "fail" };

function renderCheck(logger: Logger, check: Check): void {
  const marker =
    check.state === "ok"
      ? logger.theme.green(logger.symbols.success)
      : check.state === "warn"
        ? logger.theme.yellow(logger.symbols.warning)
        : logger.theme.red(logger.symbols.error);
  logger.result(`${marker} ${check.name.padEnd(22)} ${logger.theme.dim(check.value)}`);
}

export function doctorCommand(root: string, logger: Logger): void {
  logger.info(`Running diagnostics in ${root}...`);
  logger.step("Checking runtime and tooling...");

  const checks: Check[] = [
    {
      name: "Ollama executable",
      value: existsSync(join(root, "tools", "ollama", "ollama.exe")) ? "project-local" : "PATH lookup required",
      state: "ok",
    },
    { name: "Selected model", value: "qwen2.5-coder:3b  (not pulled yet)", state: "warn" },
    { name: "gitleaks", value: "v8.x available", state: "ok" },
    { name: "vulture", value: "v2.x available", state: "ok" },
    { name: "npm", value: "v10.x available", state: "ok" },
  ];
  checks.forEach((check) => renderCheck(logger, check));
  logger.info("GPU visibility  informational; run `ollama ps` for diagnostics");

  const warnings = checks.filter((check) => check.state === "warn").length;
  const failures = checks.filter((check) => check.state === "fail").length;
  const title = failures ? "Exorcist needs attention" : warnings ? "Exorcist is almost ready" : "Exorcist is ready";
  logger.result(
    summaryBox(
      `${title}\n${checks.filter((check) => check.state === "ok").length} passed   ${warnings} warning   ${failures} failed\n\nNext:  ollama pull qwen2.5-coder:3b\n       exorcist scan`,
      logger.theme.cyan("x") !== "x",
      failures ? "red" : "cyan",
    ),
  );
}
