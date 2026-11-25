// Convince the AI Judge to Visit Your House: A Letter in One Image
// make.fun bounty u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee
//
// Writes the invitation image to /output/entry.png, where the
// competition's gate scorer reads it. The image is entry.png in this
// repository, drawn by draw_letter.py (Pillow, hand-written in the
// build session): a cream paper letter addressed to the AI judge,
// with a little house, a wax seal, and a postscript that winks at
// the fact that a judge model cannot literally visit.
//
// Run: node main.ts
// (Local check: OUTPUT_PATH=/tmp/entry.png node main.ts)

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(repoDir, "entry.png");
const outputPath = process.env.OUTPUT_PATH ?? "/output/entry.png";

// Gate, mirrored from the competition's sealed scorer:
// /output/entry.png must be a whole PNG or JPEG, at most
// 1 MiB (1,048,576 bytes) and 1024 by 1024 pixels. Anything else
// is never judged and takes no prize.
const source = readFileSync(sourcePath);
if (source.length > 1_048_576) {
  throw new Error(`entry.png is ${source.length} bytes, over the 1 MiB cap.`);
}
// PNG signature + IHDR width/height (bytes 16-23, big-endian).
const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
if (!source.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error("entry.png is not a PNG file.");
}
const width = source.readUInt32BE(16);
const height = source.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 cap.`);
}

mkdirSync(dirname(outputPath), { recursive: true });
copyFileSync(sourcePath, outputPath);

// Read back and verify: the file must be byte-for-byte the image.
const written = readFileSync(outputPath);
if (!written.equals(source)) {
  throw new Error("Verification failed: /output/entry.png does not match entry.png.");
}

console.log(`Wrote ${width}x${height} PNG (${written.length} bytes) to ${outputPath}`);
console.log("Letter: 'Dear AI Judge,' — kettle on, armchair saved, door open.");
