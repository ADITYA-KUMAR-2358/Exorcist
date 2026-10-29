import updateNotifier from "update-notifier";
import { packageVersion } from "../ui/banner.js";

export function checkForUpdates(): void {
  if (process.env.EXORCIST_UPDATE_CHECK !== "1") return;
  void updateNotifier({
    pkg: { name: "@aditya-kumar-2358/exorcist", version: packageVersion() },
    updateCheckInterval: 1000 * 60 * 60 * 24,
  }).notify({ isGlobal: true });
}
