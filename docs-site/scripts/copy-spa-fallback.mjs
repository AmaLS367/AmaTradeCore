import { copyFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const currentDirectory = path.dirname(fileURLToPath(import.meta.url));
const docsSiteRoot = path.resolve(currentDirectory, "..");
const distDirectory = path.join(docsSiteRoot, "dist");
const indexHtmlPath = path.join(distDirectory, "index.html");
const fallbackHtmlPath = path.join(distDirectory, "404.html");
const noJekyllPath = path.join(distDirectory, ".nojekyll");

await copyFile(indexHtmlPath, fallbackHtmlPath);
await writeFile(noJekyllPath, "", "utf8");
