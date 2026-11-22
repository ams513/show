(function () {
  'use strict';
  var back = document.getElementById('back'), wl = null;
  function route() {
    var seg = (location.hash.slice(1).split('-')[0]) || 'home', views = document.querySelectorAll('.view'), found = false, i;
    for (i = 0; i < views.length; i++) if (views[i].id === seg) found = true;
    if (!found) seg = 'home';
    for (i = 0; i < views.length; i++) views[i].hidden = views[i].id !== seg;
    back.hidden = seg === 'home';
    if (location.hash.indexOf('-') < 0) window.scrollTo(0, 0);
    else { var t = document.getElementById(location.hash.slice(1)); if (t) t.scrollIntoView(); }
  }
  window.addEventListener('hashchange', route);
  route();
  Array.prototype.forEach.call(document.querySelectorAll('[data-gal]'), function (g) {
    var c = g.nextElementSibling, n = g.children.length;
    g.addEventListener('scroll', function () {
      var k = Math.round(g.scrollLeft / (g.scrollWidth / n)) + 1; if (c) c.textContent = k + ' / ' + n;
    }, { passive: true });
  });
  var box = document.getElementById('clipbox'), vid = document.getElementById('clipvid');
  Array.prototype.forEach.call(document.querySelectorAll('[data-clip]'), function (b) {
    b.addEventListener('click', function () { vid.src = b.getAttribute('data-clip'); if (box.showModal) box.showModal(); else box.setAttribute('open', ''); var p = vid.play(); if (p && p.catch) p.catch(function () {}); });
  });
  function shut() { try { vid.pause(); } catch (e) {} vid.removeAttribute('src'); vid.load(); if (box.close) box.close(); else box.removeAttribute('open'); }
  document.getElementById('clipclose').addEventListener('click', shut);
  box.addEventListener('close', function () { try { vid.pause(); } catch (e) {} });
  function keepAwake() { try { if (navigator.wakeLock && document.visibilityState === 'visible') navigator.wakeLock.request('screen').then(function (l) { wl = l; }, function () {}); } catch (e) {} }
  document.addEventListener('visibilitychange', keepAwake); keepAwake();
  if ('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js').catch(function () {});
})();
