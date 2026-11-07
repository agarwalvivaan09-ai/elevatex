// ElevateX website. Small and dependency-free.
document.documentElement.classList.add('js');

// Phone menu
(function () {
  const menu = document.getElementById('mobileMenu');
  const open = document.getElementById('menuToggle');
  if (!menu || !open) return;
  const close = () => {
    menu.classList.remove('open');
    document.body.classList.remove('menu-open');
    open.setAttribute('aria-expanded', 'false');
    open.focus();
  };
  open.addEventListener('click', () => {
    menu.classList.add('open');
    document.body.classList.add('menu-open');
    open.setAttribute('aria-expanded', 'true');
    menu.querySelector('.sheet-close').focus();
  });
  menu.querySelector('.sheet-close').addEventListener('click', close);
  menu.querySelector('.scrim').addEventListener('click', close);
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && menu.classList.contains('open')) close(); });
})();

// Header border once the page scrolls
(function () {
  const header = document.querySelector('.site-header');
  if (!header) return;
  const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 8);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
})();

// Fade sections in, and count numbers up, when they scroll into view
(function () {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const count = (el) => {
    const target = Number(el.dataset.count);
    const fmt = (n) => n.toLocaleString('en-IN');
    if (reduce || !target) { el.textContent = fmt(target); return; }
    const start = performance.now();
    const tick = (t) => {
      const p = Math.min((t - start) / 1100, 1);
      el.textContent = fmt(Math.round(target * (1 - Math.pow(1 - p, 3))));
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  if (!('IntersectionObserver' in window)) {
    document.querySelectorAll('.reveal').forEach((el) => el.classList.add('in'));
    return;
  }
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      e.target.querySelectorAll('[data-count]').forEach(count);
      io.unobserve(e.target);
    });
  }, { threshold: 0, rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('.reveal').forEach((el) => io.observe(el));
  // Safety net: anything already scrolled past (fast flicks, jumps) is shown too.
  let queued = false;
  window.addEventListener('scroll', () => {
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => {
      queued = false;
      document.querySelectorAll('.reveal:not(.in)').forEach((el) => {
        if (el.getBoundingClientRect().top < window.innerHeight) {
          el.classList.add('in');
          el.querySelectorAll('[data-count]').forEach(count);
          io.unobserve(el);
        }
      });
    });
  }, { passive: true });
})();

// Timeline progress line (Timeline page only)
(function () {
  const line = document.querySelector('.timeline');
  const bar = document.querySelector('.timeline .progress');
  if (!line || !bar) return;
  const update = () => {
    const r = line.getBoundingClientRect();
    const seen = Math.min(Math.max(window.innerHeight * 0.7 - r.top, 0), line.offsetHeight - 12);
    bar.style.height = seen + 'px';
  };
  update();
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
})();
