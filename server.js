import { existsSync } from "node:fs";
import { mkdir, writeFile } from "node:fs/promises";
import { dirname, join, normalize, resolve, sep } from "node:path";

const PORT = Number(process.env.ANICALENDAR_PORT) || 7843;
const HOST = process.env.ANICALENDAR_HOST || "0.0.0.0";
const ROOT = import.meta.dir;
const LINKS_FILE = join(ROOT, "streaming_links.json");

const ROUTES = {
  "/": "anicalendar_dashboard.html",
  "/dashboard": "anicalendar_dashboard.html",
  "/links": "streaming_links.html",
};

const STATIC_ALLOWLIST = new Set([
  "/anicalendar_dashboard.html",
  "/streaming_links.html",
  "/manifest.webmanifest",
  "/service-worker.js",
]);

const STATIC_PREFIXES = ["/icons/"];

function resolveStaticPath(urlPath) {
  const normalized = normalize(urlPath).replaceAll("\\", "/");
  if (normalized.includes("..")) return null;
  if (!STATIC_ALLOWLIST.has(normalized) && !STATIC_PREFIXES.some(p => normalized.startsWith(p))) {
    return null;
  }
  const filePath = resolve(ROOT, "." + normalized);
  if (!filePath.startsWith(ROOT + sep) && filePath !== ROOT) return null;
  return filePath;
}

async function ensureLinksFile() {
  if (!existsSync(LINKS_FILE)) {
    await mkdir(dirname(LINKS_FILE), { recursive: true });
    await writeFile(LINKS_FILE, "{}\n", "utf8");
  }
}

async function readLinks() {
  await ensureLinksFile();
  const raw = await Bun.file(LINKS_FILE).text();
  try {
    const parsed = JSON.parse(raw);
    if (parsed === null || typeof parsed !== "object" || Array.isArray(parsed)) {
      return {};
    }
    return parsed;
  } catch {
    return {};
  }
}

async function writeLinks(data) {
  const serialized = JSON.stringify(data, null, 2) + "\n";
  await writeFile(LINKS_FILE, serialized, "utf8");
  return serialized;
}

function jsonResponse(body, init = {}) {
  return new Response(JSON.stringify(body), {
    ...init,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "no-store",
      ...(init.headers || {}),
    },
  });
}

function textResponse(body, status = 200) {
  return new Response(body, {
    status,
    headers: { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store" },
  });
}

async function handleLinksRoot(req) {
  if (req.method === "GET") {
    const raw = await Bun.file(LINKS_FILE).text().catch(() => "{}\n");
    return new Response(raw, {
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "Cache-Control": "no-store",
      },
    });
  }

  if (req.method === "PUT") {
    const body = await req.text();
    let parsed;
    try {
      parsed = JSON.parse(body);
    } catch (err) {
      return textResponse(`Invalid JSON: ${err.message}`, 400);
    }
    if (parsed === null || typeof parsed !== "object" || Array.isArray(parsed)) {
      return textResponse("Top-level value must be a JSON object.", 400);
    }
    const serialized = await writeLinks(parsed);
    return new Response(serialized, {
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "Cache-Control": "no-store",
      },
    });
  }

  return textResponse("Method Not Allowed", 405);
}

async function handleLinksEntry(req, id) {
  if (!id) return textResponse("Missing id", 400);
  const links = await readLinks();

  if (req.method === "DELETE") {
    delete links[id];
    await writeLinks(links);
    return jsonResponse({ ok: true });
  }

  if (req.method === "PUT" || req.method === "POST") {
    let payload;
    try {
      payload = await req.json();
    } catch (err) {
      return textResponse(`Invalid JSON: ${err.message}`, 400);
    }
    const url = typeof payload?.url === "string" ? payload.url.trim() : "";
    const title = typeof payload?.title === "string" ? payload.title.trim() : "";
    if (!url) return textResponse("Missing 'url' string.", 400);
    links[id] = title ? { title, url } : { url };
    await writeLinks(links);
    return jsonResponse({ ok: true, entry: links[id] });
  }

  return textResponse("Method Not Allowed", 405);
}

async function handleStatic(urlPath) {
  const filePath = resolveStaticPath(urlPath);
  if (!filePath) return null;
  const file = Bun.file(filePath);
  if (!(await file.exists())) return null;

  const headers = new Headers();
  if (urlPath === "/service-worker.js") {
    headers.set("Cache-Control", "no-cache");
    headers.set("Service-Worker-Allowed", "/");
  } else if (urlPath.startsWith("/icons/")) {
    headers.set("Cache-Control", "public, max-age=86400");
  } else {
    headers.set("Cache-Control", "no-cache");
  }
  return new Response(file, { headers });
}

async function handleRoute(routePath) {
  const target = ROUTES[routePath];
  if (!target) return null;
  const filePath = join(ROOT, target);
  const file = Bun.file(filePath);
  if (!(await file.exists())) return null;
  return new Response(file, {
    headers: {
      "Content-Type": "text/html; charset=utf-8",
      "Cache-Control": "no-cache",
    },
  });
}

await ensureLinksFile();

Bun.serve({
  port: PORT,
  hostname: HOST,
  development: false,
  async fetch(req) {
    const url = new URL(req.url);
    const pathname = url.pathname;

    if (pathname === "/api/links") {
      return handleLinksRoot(req);
    }
    if (pathname.startsWith("/api/links/")) {
      const id = decodeURIComponent(pathname.slice("/api/links/".length));
      return handleLinksEntry(req, id);
    }

    if (req.method !== "GET" && req.method !== "HEAD") {
      return textResponse("Method Not Allowed", 405);
    }

    const routed = await handleRoute(pathname);
    if (routed) return routed;

    const staticResp = await handleStatic(pathname);
    if (staticResp) return staticResp;

    return textResponse("Not Found", 404);
  },
  error(err) {
    console.error("Server error:", err);
    return textResponse("Internal Server Error", 500);
  },
});

console.log(`AniCalendar listening on http://${HOST}:${PORT}`);
console.log(`  Dashboard: http://${HOST}:${PORT}/`);
console.log(`  Links editor: http://${HOST}:${PORT}/links`);
console.log(`  Data file: ${LINKS_FILE}`);
