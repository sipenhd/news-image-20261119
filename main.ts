// News in one image — make.fun bounty news-image-20261119
// Node.js 22.18+ compatible. Standard library only.
// No network, no installs, runs offline in the sandbox.
// Copies entry.png (the 19 November 2026 world news front page,
// 1024x1024 PNG) to /output/entry.png so the bounty judge can read it.
// The copy is byte-for-byte, so two runs write identical bytes.
//
// Run: node main.ts
// (Node 22.18+ strips types natively; this file uses no
//  TypeScript-only syntax, so it also works as plain JS.)

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = process.env.MAKEFUN_BOT_DIR
  ? process.env.MAKEFUN_BOT_DIR
  : dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outputDir, "entry.png");

if (!existsSync(source)) {
  throw new Error("entry.png not found next to main.ts: " + source);
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(source, target);

console.log("Copied entry.png to " + target);
