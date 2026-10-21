// App preview loops: silent, play only while on screen, never on their own under reduced motion, and always pausable.
// Without JavaScript the video keeps the browser's own controls.
(function () {
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  [].forEach.call(document.querySelectorAll('.pvw'), function (w) {
    var ph = w.querySelector('.pv'), v = w.querySelector('video'), b = w.querySelector('.pv-btn'), t = b.querySelector('span');
    var name = w.getAttribute('data-name'), chose = false;
    v.removeAttribute('controls');
    b.hidden = false;
    v.muted = true;
    function sync() {
      var on = !v.paused;
      ph.classList.toggle('playing', on);
      if (on) ph.classList.remove('idle');
      t.textContent = on ? 'Pause' : 'Play';
      b.setAttribute('aria-label', (on ? 'Pause' : 'Play') + ' the ' + name + ' preview');
    }
    function toggle() { chose = true; if (v.paused) { v.play().catch(function () {}); } else { v.pause(); } }
    b.addEventListener('click', toggle);
    v.addEventListener('click', toggle);
    v.addEventListener('play', sync);
    v.addEventListener('pause', sync);
    if (w.hasAttribute('data-auto') && !reduce && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (en) {
          if (chose) return;
          if (en.isIntersecting) { v.play().catch(function () {}); } else { v.pause(); }
        });
      }, { threshold: 0.5 }).observe(v);
    }
    sync();
  });
})();
