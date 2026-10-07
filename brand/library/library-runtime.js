// Shared runtime for the brand library pages. window.LIB comes from library.js, which
// `python3 scripts/brand_render.py book` generates from tokens.json, logos/, screenshots/ and
// visual-identity.md. This file draws the top navigation, loads the brand fonts and offers the
// helpers the pages use to build template previews.
(function () {
  const LIB = window.LIB || {};
  const root = document.documentElement.style;
  const c = LIB.colors || {};
  if (c.primary && c.accent) root.setProperty('--brand-gradient', `linear-gradient(90deg, ${c.primary}, ${c.accent})`);
  const fb = (LIB.fonts && LIB.fonts.fallback) || 'system-ui, -apple-system, sans-serif';
  const fam = (f) => (f ? `'${f}', ${fb}` : fb);
  root.setProperty('--font-display', fam(LIB.fonts && LIB.fonts.heading));
  root.setProperty('--font-body', fam(LIB.fonts && LIB.fonts.body));
  (LIB.fontFaces || []).forEach((f) => document.fonts.add(new FontFace(f.family, `url("${f.src}")`)));
  if (LIB.googleFonts) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = LIB.googleFonts;
    document.head.appendChild(link);
  }

  const PAGES = [['index.html', 'Overview'], ['logos.html', 'Logos'], ['colors.html', 'Color &amp; type'],
    ['banners.html', 'Banners'], ['posts.html', 'Social posts'], ['screenshots.html', 'Screenshots']];
  const here = location.pathname.split('/').pop() || 'index.html';
  const header = document.querySelector('header.top');
  if (header) {
    const brand = LIB.headerLogo ? `<img src="${LIB.headerLogo}" alt="${LIB.name || 'Brand'}">` : (LIB.name || 'Brand library');
    header.innerHTML = `<a class="brand" href="index.html">${brand}</a><nav>${PAGES.map(([href, label]) =>
      `<a href="${href}"${href === here ? ' aria-current="page"' : ''}>${label}</a>`).join('')}</nav>`;
  }
  document.querySelectorAll('[data-name]').forEach((el) => (el.textContent = LIB.name || 'our brand'));
  document.querySelectorAll('[data-regen]').forEach((el) => (el.textContent = LIB.regen || ''));

  // A template URL: the tokens query (precomputed per template) plus the content params.
  window.templateSrc = function (template, params) {
    const q = new URLSearchParams((LIB.query || {})[template] || '');
    Object.entries(params).forEach(([k, v]) => {
      if (v === undefined || v === null || v === '') return;
      q.set(k, k === 'shot' ? (LIB.shotBase || '../screenshots/') + v : v);
    });
    return `${LIB.templates || '../templates'}/${template}.html?${q}`;
  };

  // Scale every .ex preview to its column, stopping tall shapes at maxH.
  window.fitPreviews = function (container, maxH = 480) {
    const layout = () => container.querySelectorAll('.ex').forEach((el) => {
      const w = +el.dataset.w, h = +el.dataset.h;
      const scale = Math.min(el.clientWidth / w, maxH / h);
      el.querySelector('iframe').style.transform = `scale(${scale})`;
      const pv = el.querySelector('.preview');
      pv.style.height = h * scale + 'px';
      pv.style.width = w * scale + 'px';
    });
    new ResizeObserver(layout).observe(container);
  };

  window.esc = (s) => String(s).replace(/[&<>"]/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[ch]);
})();
