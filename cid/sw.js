// Offline cache for the static (phone) build. Each deploy replaces BUILD, so a new
// worker precaches the whole app + question bank as one consistent set and the old
// cache is dropped only after the new one is complete.
const BUILD = '__BUILD__';
const CACHE = 'fde-cid-' + BUILD;
const FILES = [
  './', 'index.html', 'manifest.webmanifest',
  'src/app.js', 'src/core.js', 'src/store.js', 'src/device-db.js', 'src/styles.css',
  'data/questions.json', 'data/manifest.json', 'data/notes.json',
  'icons/apple-touch-icon.png', 'icons/icon-192.png', 'icons/icon-512.png', 'icons/icon-maskable-512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE)
    .then(cache => cache.addAll(FILES.map(f => new Request(f, {cache: 'reload'}))))
    .then(() => self.skipWaiting()));
});

self.addEventListener('activate', event => {
  event.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k.startsWith('fde-cid-') && k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', event => {
  const request = event.request;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin || url.pathname.includes('/api/')) return;
  event.respondWith(
    caches.open(CACHE).then(cache =>
      cache.match(request, {ignoreSearch: true}).then(hit =>
        hit || fetch(request).catch(() =>
          request.mode === 'navigate' ? cache.match('index.html') : Response.error())))
  );
});
