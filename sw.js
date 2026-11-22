/* Stark Showcase service worker: caches only this folder's own files. */
const V = "show-wm20261122", FILES = ['./', 'index.html', 'css/show.css', 'js/show.js', 'img/eyes.jpg', 'img/cov-patients.png', 'img/cov-chart.png', 'img/cov-emergency.png', 'img/cov-emergency-phone.png', 'img/cov-outcomes.png', 'img/cov-todo.png', 'img/cov-safety.png', 'clips/math-sim.mp4', 'clips/warden-call.mp4'];
self.addEventListener("install", e => { self.skipWaiting(); e.waitUntil(caches.open(V).then(c => Promise.all(FILES.map(f => c.add(f).catch(() => 0))))); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(k => Promise.all(k.filter(x => x !== V).map(x => caches.delete(x)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", e => {
  const r = e.request, u = new URL(r.url);
  if (r.method !== "GET" || u.origin !== self.location.origin) return;
  e.respondWith(caches.open(V).then(async c => {
    if (r.mode === "navigate") { try { const n = await fetch(r, { cache: "no-cache" }); if (n.ok) { c.put(r, n.clone()); return n; } } catch (x) {} }
    let m = await c.match(r, { ignoreSearch: true });
    if (!m) { try { m = await fetch(r); if (m.ok && m.status === 200) c.put(r, m.clone()); return m; } catch (x) { return (await c.match("index.html")) || Response.error(); } }
    const rg = r.headers.get("range");
    if (!rg) return m;
    const b = await m.blob(), mm = /bytes=(\d*)-(\d*)/.exec(rg), s = mm[1] ? +mm[1] : 0, en = mm[2] ? Math.min(+mm[2], b.size - 1) : b.size - 1;
    return new Response(b.slice(s, en + 1), { status: 206, headers: { "Content-Type": m.headers.get("Content-Type") || "video/mp4", "Content-Range": `bytes ${s}-${en}/${b.size}`, "Content-Length": en + 1 - s } });
  }));
});
