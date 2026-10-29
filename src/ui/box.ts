import boxen from "boxen";
export function summaryBox(content: string, color = true, borderColor: "cyan" | "red" = "cyan"): string {
  return boxen(content, {
    padding: 1,
    margin: 1,
    borderStyle: "round",
    borderColor: color ? borderColor : undefined,
    title: "EXORCIST",
    titleAlignment: "center",
  });
}
