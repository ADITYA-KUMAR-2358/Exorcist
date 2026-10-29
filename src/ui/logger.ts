import { createTheme, getSymbols, type Theme } from "./theme.js";

export type LoggerOptions = { color?: boolean; quiet?: boolean; json?: boolean; ascii?: boolean };

export class Logger {
  readonly theme: Theme;
  readonly json: boolean;
  readonly quiet: boolean;
  readonly symbols: ReturnType<typeof getSymbols>;

  constructor(options: LoggerOptions = {}) {
    this.theme = createTheme({ color: options.color });
    this.json = options.json ?? false;
    this.quiet = options.quiet ?? false;
    this.symbols = getSymbols(options.ascii);
  }

  private write(line: string): void {
    if (!this.quiet && !this.json) process.stdout.write(line + "\n");
  }

  info(message: string): void {
    this.write(`${this.theme.cyan(this.symbols.info)} ${message}`);
  }

  step(message: string): void {
    this.write(`  ${this.theme.cyan(this.symbols.arrow)} ${message}`);
  }

  success(message: string): void {
    this.write(`${this.theme.green(this.symbols.success)} ${message}`);
  }

  warning(message: string): void {
    this.write(`${this.theme.yellow(this.symbols.warning)} ${message}`);
  }

  error(message: string): void {
    process.stderr.write(`${this.theme.red(this.symbols.error)} ${message}\n`);
  }

  result(message: string): void {
    if (!this.quiet && !this.json) process.stdout.write(message + "\n");
  }

  jsonResult(message: string): void {
    if (!this.quiet && this.json) process.stdout.write(message + "\n");
  }
}
