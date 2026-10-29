export function isInteractive(): boolean {
  return Boolean(process.stdout.isTTY) && process.env.CI !== "true";
}

export function shouldAnimate(): boolean {
  return isInteractive() && process.env.NO_COLOR === undefined;
}
