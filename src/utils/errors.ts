export class ExorcistError extends Error {
  constructor(
    message: string,
    readonly why: string,
    readonly howToFix: string,
  ) {
    super(message);
    this.name = "ExorcistError";
  }
}
