/* Couch Co-Op Studios: shared app-page motion. Phones cycle their screens while on
   screen, things with data-speed drift against the scroll, hero shapes lean toward
   the pointer, phone groups tilt toward it, and .rv items rise in once. */
(function () {
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO = 'IntersectionObserver' in window;

  var rv = document.querySelectorAll('.rv');
  if (!hasIO || reduce) rv.forEach(function (x) { x.classList.add('in'); });
  else {
    var rio = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); rio.unobserve(en.target); } });
    }, { threshold: .2 });
    rv.forEach(function (x) { rio.observe(x); });
  }
  if (reduce || !hasIO) return;

  // Cycle each phone's screens, only while it is on screen.
  var phones = [].slice.call(document.querySelectorAll('.iph')).filter(function (p) { return p.querySelectorAll('.scr img').length > 1; });
  var seen = new Set();
  var vio = new IntersectionObserver(function (es) {
    es.forEach(function (en) { en.isIntersecting ? seen.add(en.target) : seen.delete(en.target); });
  }, { threshold: .25 });
  phones.forEach(function (p) { vio.observe(p); });
  function step(p) {
    if (!seen.has(p) || document.hidden) return;
    var imgs = p.querySelectorAll('.scr img');
    var i = [].findIndex.call(imgs, function (x) { return x.classList.contains('on'); });
    imgs[i].classList.remove('on'); imgs[(i + 1) % imgs.length].classList.add('on');
  }
  phones.forEach(function (p, k) {
    setTimeout(function () { step(p); setInterval(function () { step(p); }, 3600); }, 2400 + (+p.dataset.delay || k * 700));
  });

  // Parallax.
  var par = [].slice.call(document.querySelectorAll('[data-speed]'));
  var px = 0, py = 0, tx = 0, ty = 0, ticking = false;
  function frame() {
    ticking = false;
    var vh = innerHeight;
    tx += (px - tx) * .08; ty += (py - ty) * .08;
    par.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.bottom < -400 || r.top > vh + 400) return;
      var y = ((r.top + r.height / 2) - vh / 2) * -(+el.dataset.speed);
      var d = +el.dataset.depth || 0;
      el.style.translate = (tx * d).toFixed(1) + 'px ' + (y + ty * d).toFixed(1) + 'px';
    });
    if (Math.abs(px - tx) > .002 || Math.abs(py - ty) > .002) request();
  }
  function request() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  addEventListener('scroll', request, { passive: true });
  addEventListener('resize', request);
  if (matchMedia('(pointer: fine)').matches) {
    addEventListener('pointermove', function (ev) { px = ev.clientX / innerWidth - .5; py = ev.clientY / innerHeight - .5; request(); }, { passive: true });
    document.querySelectorAll('.hfan,.vis').forEach(function (s) {
      s.addEventListener('pointermove', function (ev) {
        var r = s.getBoundingClientRect();
        s.style.setProperty('--ry', (((ev.clientX - r.left) / r.width - .5) * 14).toFixed(2) + 'deg');
        s.style.setProperty('--rx', (-((ev.clientY - r.top) / r.height - .5) * 10).toFixed(2) + 'deg');
      });
      s.addEventListener('pointerleave', function () { s.style.setProperty('--ry', '0deg'); s.style.setProperty('--rx', '0deg'); });
    });
  }
  request();
})();
