import { Command } from "commander";
import { renderBanner, packageVersion } from "./ui/banner.js";
import { Logger } from "./ui/logger.js";
import { initCommand } from "./commands/init.js";
import { scanCommand } from "./commands/scan.js";
import { reportCommand } from "./commands/report.js";
import { fixCommand } from "./commands/fix.js";
import { doctorCommand } from "./commands/doctor.js";
import { checkForUpdates } from "./utils/updates.js";

const program = new Command();
if (process.platform === "win32") process.stdout.setDefaultEncoding("utf8");
checkForUpdates();
program.name("exorcist").description("Local-first AI code exorcism").version(packageVersion());
program
  .option("--no-color", "disable color output")
  .option("--ascii", "use ASCII status symbols")
  .option("--verbose", "show detailed errors")
  .option("--quiet", "suppress human-readable output")
  .option("--json", "machine-readable output")
  .option("-y, --yes", "skip prompts")
  .option("--dry-run", "preview changes without writing");

function loggerFor(options: ReturnType<typeof program.opts>): Logger {
  return new Logger({
    color: options.color && !options.json && !options.quiet && process.env.NO_COLOR === undefined,
    quiet: options.quiet,
    json: options.json,
    ascii: options.ascii,
  });
}

function showBanner(options: ReturnType<typeof program.opts>): void {
  if (!options.json && !options.quiet && process.stdout.isTTY && !process.env.CI) {
    console.log(renderBanner(options.color));
  }
}

program
  .command("init [path]")
  .description("prepare a repository for local scanning")
  .action(async (path = ".") => {
    const options = program.opts();
    const logger = loggerFor(options);
    showBanner(options);
    await initCommand(path, logger, Boolean(options.yes));
  });

program
  .command("scan [path]")
  .description("scan for possessed code")
  .action(async (path = ".") => {
    const options = program.opts();
    const logger = loggerFor(options);
    showBanner(options);
    process.exitCode = await scanCommand(path, logger, Boolean(options.json));
  });

program
  .command("report [path]")
  .option("-o, --out <file>", "report output path")
  .description("generate an offline HTML report")
  .action(async (path = ".", commandOptions) => {
    const options = program.opts();
    showBanner(options);
    await reportCommand(path, commandOptions.out, loggerFor(options));
  });

program
  .command("fix")
  .description("preview or apply safe fixes")
  .action(async () => {
    const options = program.opts();
    showBanner(options);
    await fixCommand(loggerFor(options), options.dryRun !== false);
  });

program
  .command("doctor")
  .description("check local tools and Ollama")
  .action(() => {
    const options = program.opts();
    showBanner(options);
    doctorCommand(process.cwd(), loggerFor(options));
  });

program.parseAsync().catch((error: unknown) => {
  const options = program.opts();
  const logger = loggerFor(options);
  logger.error(error instanceof Error ? error.message : "Exorcism failed.");
  if (options.verbose && error instanceof Error) console.error(error.stack);
  process.exitCode = 2;
});
