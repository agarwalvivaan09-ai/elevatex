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

// Photo viewer: on album pages, tapping a photo opens it large on the page, with previous/next.
// Without JavaScript the links still open the full-size photo.
(function () {
  const links = Array.from(document.querySelectorAll('.gallery a'));
  if (!links.length) return;
  const v = document.createElement('div');
  v.className = 'viewer';
  v.setAttribute('role', 'dialog');
  v.setAttribute('aria-modal', 'true');
  v.setAttribute('aria-label', 'Photo');
  v.innerHTML = '<img alt=""><button class="v-close" aria-label="Close">×</button>' +
    '<button class="v-prev" aria-label="Previous photo">‹</button><button class="v-next" aria-label="Next photo">›</button>' +
    '<div class="v-count" aria-live="polite"></div>';
  document.body.appendChild(v);
  const img = v.querySelector('img');
  const count = v.querySelector('.v-count');
  let i = 0;
  let opener = null;
  const show = (n) => {
    i = (n + links.length) % links.length;
    const a = links[i];
    img.src = a.getAttribute('href');
    img.alt = a.querySelector('img').alt;
    count.textContent = (i + 1) + ' of ' + links.length;
  };
  const close = () => { v.classList.remove('open'); document.body.classList.remove('menu-open'); if (opener) opener.focus(); };
  links.forEach((a, n) => a.addEventListener('click', (e) => {
    if (e.metaKey || e.ctrlKey || e.shiftKey) return;
    e.preventDefault();
    opener = a;
    show(n);
    v.classList.add('open');
    document.body.classList.add('menu-open');
    v.querySelector('.v-close').focus();
  }));
  v.querySelector('.v-close').addEventListener('click', close);
  v.querySelector('.v-prev').addEventListener('click', () => show(i - 1));
  v.querySelector('.v-next').addEventListener('click', () => show(i + 1));
  v.addEventListener('click', (e) => { if (e.target === v) close(); });
  document.addEventListener('keydown', (e) => {
    if (!v.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') show(i - 1);
    if (e.key === 'ArrowRight') show(i + 1);
  });
  let x0 = null;
  v.addEventListener('touchstart', (e) => { x0 = e.touches[0].clientX; }, { passive: true });
  v.addEventListener('touchend', (e) => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 40) show(dx < 0 ? i + 1 : i - 1);
    x0 = null;
  });
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
