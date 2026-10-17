// Builds the site, serves dist/ under BASE as GitHub Pages would, and rebuilds
// when content/, style.css, build.ts or data.json changes. Each build runs build.ts in a
// fresh process, so an edit to build.ts itself takes effect too.

import { watch } from "node:fs";
import { join } from "node:path";
import { BASE, OUT } from "./build";

const build = () => Bun.spawn(["bun", "build.ts"], { cwd: import.meta.dir, stdout: "inherit", stderr: "inherit" }).exited;

await build();

let timer: Timer | undefined;
const rebuild = () => {
  clearTimeout(timer);
  timer = setTimeout(build, 100);
};
watch(join(import.meta.dir, "content"), { recursive: true }, rebuild);
watch(join(import.meta.dir, "style.css"), rebuild);
watch(join(import.meta.dir, "build.ts"), rebuild);
watch(join(import.meta.dir, "data.json"), rebuild); // rewritten by tools/build.py

const server = Bun.serve({
  port: Number(process.env.PORT ?? 4321),
  async fetch(req) {
    const path = decodeURIComponent(new URL(req.url).pathname);
    if (!path.startsWith(BASE)) return Response.redirect(BASE);
    const rel = path.slice(BASE.length);
    if (rel.includes("..")) return new Response("bad path", { status: 400 });
    const file = Bun.file(join(OUT, rel.endsWith("/") || rel === "" ? `${rel}index.html` : rel));
    if (await file.exists()) return new Response(file);
    // a page asked for without its trailing slash
    if (await Bun.file(join(OUT, rel, "index.html")).exists()) return Response.redirect(`${path}/`);
    return new Response(Bun.file(join(OUT, "404.html")), { status: 404 });
  },
});

console.log(`serving on http://localhost:${server.port}${BASE}`);
