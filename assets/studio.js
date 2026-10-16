(function () {
  const root = document.documentElement;
  const themeButton = document.querySelector('[data-theme-toggle]');
  const metaTheme = document.querySelector('meta[name="theme-color"]');

  function setTheme(theme, persist) {
    root.dataset.theme = theme;
    if (themeButton) {
      themeButton.setAttribute('aria-pressed', String(theme === 'night'));
      const label = themeButton.querySelector('span');
      if (label) label.textContent = theme === 'night' ? 'Lights on' : 'After dark';
    }
    if (metaTheme) metaTheme.setAttribute('content', theme === 'night' ? '#0B1020' : '#F5F2EB');
    if (persist) {
      try { localStorage.setItem('cc-theme', theme); } catch (_) {}
    }
  }

  let saved = null;
  try { saved = localStorage.getItem('cc-theme'); } catch (_) {}
  setTheme(saved === 'night' ? 'night' : 'day', false);

  if (themeButton) {
    themeButton.addEventListener('click', function () {
      setTheme(root.dataset.theme === 'night' ? 'day' : 'night', true);
    });
  }

  const revealItems = document.querySelectorAll('[data-reveal]');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion || !('IntersectionObserver' in window)) {
    revealItems.forEach((item) => item.classList.add('in'));
  } else {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('in');
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.14 });
    revealItems.forEach((item) => observer.observe(item));
  }
})();
