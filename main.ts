// makefun-news-20261126 - entrypoint (Node 22, standard library only).
//
// The image is drawn at build time by draw.py (Python + Pillow) and ships
// in this repository as entry.png. This program only copies that image
// into the grader's output directory, so both runs write byte-identical
// files. It never deletes anything, never touches the network, and reads
// nothing but the entry.png shipped beside it.
//
// Run locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(
  new URL('./entry.png', import.meta.url),
  join(outDir, 'entry.png'),
);
