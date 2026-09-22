// Letter Dispatcher Sync — minimal offline service worker.
//
// Two jobs:
//  1. Cache the app shell so the page still opens (from cache) with no
//     network — the app's own data lives in the browser's localStorage, not
//     on a server, so caching just this one HTML file is enough.
//  2. Simply existing as a registered service worker with a fetch handler
//     is one of the conditions Chrome/Edge/Android require before they will
//     ever fire the `beforeinstallprompt` event — the app's "Install"
//     button needs that event to trigger the native
//     "add to home screen / desktop" flow directly.
//
// Strategy: network-first, falling back to the cache when offline. That way
// anyone online always gets the current file (no manual cache-busting to
// remember when this file is updated later), and offline visitors get the
// last copy that was successfully fetched.
//
// Cache name is namespaced "...-sync-..." (distinct from the LIGHT edition's
// "letter-dispatcher-shell-v1") purely for clarity when debugging — the two
// editions live on separate origins/repos, so there is no actual collision
// risk either way.

const CACHE_NAME = "letter-dispatcher-sync-shell-v1";
const APP_SHELL = ["./", "./index.html"];

self.addEventListener("install", (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(APP_SHELL))
      .catch(() => {})
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((names) => Promise.all(names.filter((n) => n !== CACHE_NAME).map((n) => caches.delete(n))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;

  event.respondWith(
    fetch(event.request)
      .then((response) => {
        const copy = response.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy)).catch(() => {});
        return response;
      })
      .catch(() => caches.match(event.request).then((cached) => cached || caches.match("./index.html")))
  );
});
