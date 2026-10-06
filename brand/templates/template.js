// Shared runtime for banner.html, post.html, icon.html and shot.html. Everything comes from the
// query string, which scripts/brand_render.py builds from brand/tokens.json, the preset in
// sizes.json and the content params; `brand_render.py render ... --print-url` prints one to open
// in a browser. Sizes the canvas, applies the tokens, picks a layout, fits the headline, and sets
// document.title to "ready" when done.
//
// Size:     w, h, safe=t,r,b,l (px), debug=1 draws the safe area.
// Tokens:   c_bg, c_fg, c_primary, c_accent (hex without #), heading, body (font families),
//           heading_src, body_src (a font file relative to this folder; else the family loads
//           from Google Fonts), fallback (CSS stack), logo (an image relative to this folder).
// banner:   headline (one *gradient* phrase), theme=brand|inverse.
// post:     headline, stat (<= 6 chars, never with shot), shot (an image relative to this folder),
//           focus=x,y (0..1: zoom so that point of the screenshot sits at the frame's top-left).
// icon:     bg=brand|inverse|transparent|glow, pad (0..0.45 of the short side), radius (0..0.5).
// shot:     shot, fit=contain|cover, focus=x,y (cover only: the point kept at the centre).
// The rules for what goes in are brand/image-rules.md.

(function () {
  const q = new URLSearchParams(location.search);
  const get = (k, d = '') => q.get(k) ?? d;
  const w = +get('w', 1200);
  const h = +get('h', 630);
  const safe = get('safe').split(',').filter(Boolean).map(Number);
  const [st, sr, sb, sl] = safe.length === 4 ? safe : defaultSafe(w, h);
  const kind = document.body.dataset.template;
  const root = document.documentElement;
  const css = (k, v) => root.style.setProperty(k, v);

  function defaultSafe(w, h) {
    const v = Math.round(Math.min(w, h) * 0.075);
    return [v, Math.round(Math.max(v, w * 0.03)), v, Math.round(Math.max(v, w * 0.03))];
  }

  css('--w', w + 'px');
  css('--h', h + 'px');
  css('--safe-t', st + 'px');
  css('--safe-r', sr + 'px');
  css('--safe-b', sb + 'px');
  css('--safe-l', sl + 'px');
  if (get('debug') === '1') document.body.classList.add('debug');

  // Tokens. brand_render.py fills the neutral default when brand/tokens.json is empty.
  const hex = (k, d) => '#' + (/^[0-9a-fA-F]{6}$/.test(get('c_' + k)) ? get('c_' + k) : d);
  const rgba = (c, a) => `rgba(${parseInt(c.slice(1, 3), 16)}, ${parseInt(c.slice(3, 5), 16)}, ${parseInt(c.slice(5, 7), 16)}, ${a})`;
  const inverse = get('theme') === 'inverse' || get('bg') === 'inverse';
  const bg = hex(inverse ? 'fg' : 'bg', inverse ? 'F5F5F5' : '111111');
  const fg = hex(inverse ? 'bg' : 'fg', inverse ? '111111' : 'F5F5F5');
  const primary = hex('primary', '8B93A1');
  const accent = hex('accent', 'D4D8DE');
  css('--bg', bg);
  css('--fg', fg);
  css('--gradient', `linear-gradient(90deg, ${primary}, ${accent})`);
  css('--glow', `radial-gradient(closest-side, ${rgba(accent, 0.9)} 0%, ${rgba(primary, 0.45)} 50%, ${rgba(primary, 0)} 100%)`);
  css('--glow-lifted', `radial-gradient(closest-side, ${rgba(accent, 1)} 0%, ${rgba(primary, 0.6)} 55%, ${rgba(primary, 0)} 100%)`);
  const fallback = get('fallback', 'system-ui, -apple-system, sans-serif');
  const fonts = [];
  ['heading', 'body'].forEach((role) => {
    const family = get(role).replace(/["<>]/g, '');
    if (!family) return css('--font-' + role, fallback);
    css('--font-' + role, `"${family}", ${fallback}`);
    const src = get(role + '_src');
    if (src) {
      const face = new FontFace(family, `url("${encodeURI(src)}")`);
      document.fonts.add(face);
      fonts.push(face.load().catch(() => null));
    } else {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = 'https://fonts.googleapis.com/css2?family=' + encodeURIComponent(family).replace(/%20/g, '+') + ':wght@400;500;600;700&display=block';
      fonts.push(new Promise((r) => { link.onload = link.onerror = r; }).then(() => document.fonts.load(`500 40px "${family}"`)).catch(() => null));
      document.head.appendChild(link);
    }
  });
  const logo = get('logo');
  const focus = get('focus').split(',').map(Number);
  const validFocus = focus.length === 2 && focus.every((n) => n >= 0 && n <= 1);

  if (kind === 'shot') {
    const fit = get('fit', 'contain') === 'cover' ? 'cover' : 'contain';
    css('--pad', Math.round(Math.min(w, h) * 0.06) + 'px');
    document.body.dataset.fit = fit;
    const img = document.getElementById('shot');
    if (fit === 'cover' && validFocus) img.style.objectPosition = focus[0] * 100 + '% ' + focus[1] * 100 + '%';
    img.src = get('shot');
    return whenLoaded().then(done);
  }

  if (kind === 'icon') {
    const bgMode = get('bg', 'brand');
    const pad = Math.min(0.45, Math.max(0, +get('pad', 0.24)));
    document.body.dataset.bg = bgMode;
    css('--pad', Math.round(Math.min(w, h) * pad) + 'px');
    css('--radius', Math.round(Math.min(w, h) * +get('radius', 0)) + 'px');
    const mark = document.getElementById('mark');
    if (logo) mark.src = logo;
    else mark.remove();
    return whenLoaded().then(done);
  }

  // Banner and post
  const isPost = kind === 'post';
  const headline = get('headline');
  const ratio = w / h;
  const layout = isPost ? (ratio >= 1.4 ? 'post-wide' : 'post-tall')
    : !headline ? 'logo-only' : ratio > 4 ? 'ultra' : ratio >= 1.4 ? 'wide' : 'tall';
  const stat = isPost ? get('stat').slice(0, 6) : '';
  const shot = isPost && !stat ? get('shot') : '';
  const hasShot = !!shot;
  const hasFocus = hasShot && validFocus;

  Object.assign(document.body.dataset, {
    theme: inverse ? 'inverse' : 'brand', layout, shot: hasShot ? '1' : '0', stat: stat ? '1' : '0', focus: hasFocus ? '1' : '0',
  });

  if (isPost) {
    // Posts use one margin on every side, 7% of the width, and ignore the banner safe insets.
    const m = Math.round(w * 0.07);
    ['t', 'r', 'b', 'l'].forEach((s) => css('--safe-' + s, m + 'px'));
    const img = document.getElementById('shot');
    if (hasShot) img.src = shot;
    else img.parentElement.remove();
  }

  const lockup = document.getElementById('lockup');
  if (logo) lockup.src = logo;
  else lockup.remove();

  if (isPost) setText('stat', stat);
  setText('headline', headline, true);

  const safeH = h - st - sb;
  // Banners: one sizing rule for every shape. Type and logo scale with the width, capped by the
  // height so thin strips stay light; 68 px type and a 44 px logo on a 1200x630 card read at
  // thumbnail size. Posts must stop the scroll on a phone, so their type is sized by an ink
  // budget: the share of the safe area the text's line boxes may cover.
  const INK_BUDGET = {
    'post-tall': 0.28, 'post-tall-stat': 0.28, 'post-tall-shot': 0.19,
    'post-wide': 0.32, 'post-wide-stat': 0.32, 'post-wide-shot': 0.22,
  };
  const short = Math.min(w, h);
  const lockH = isPost ? w * 0.05 : layout === 'logo-only' ? short * 0.14
    : layout === 'ultra' ? Math.min(w * 0.037, safeH * 0.45) : Math.min(w * 0.037, safeH * 0.14);
  css('--lockup-h', Math.round(lockH) + 'px');
  // Post starts are ceilings for very short copy; the ink budget sets the real size.
  const start = layout === 'post-tall' ? w * (hasShot ? 0.11 : 0.16)
    : layout === 'post-wide' ? w * (hasShot ? 0.08 : 0.11)
    : layout === 'logo-only' ? 0
    : layout === 'ultra' ? Math.min(w * 0.057, safeH * 0.22) : Math.min(w * 0.057, safeH * 0.24);

  function setText(id, text, rich) {
    const el = document.getElementById(id);
    if (!el) return;
    if (!text) return el.remove();
    if (!rich) return (el.textContent = text);
    const esc = text.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
    el.innerHTML = esc.replace(/\*([^*]+)\*/g, '<span class="hl">$1</span>');
  }

  // Shrink the headline until the text block fits. Measures layout boxes, not scroll overflow,
  // because glyph descenders overflow the line box at tight leading.
  function fit() {
    const text = document.getElementById('text');
    const box = document.getElementById('safe');
    if (!text || !headline) return;
    const lock = document.getElementById('lockup');
    const lockSpace = lock && layout !== 'ultra' ? lock.offsetHeight * 1.8 : 0;
    const wrap = document.getElementById('shot-wrap');
    const room = layout === 'post-tall' && wrap ? wrap.offsetTop - box.offsetTop - w * 0.045 : box.clientHeight;
    const noWordOverflow = () => [...text.children].every((el) => el.scrollWidth <= el.clientWidth + 1);
    const budget = isPost ? INK_BUDGET[layout + (stat ? '-stat' : hasShot ? '-shot' : '')] * box.clientWidth * box.clientHeight : Infinity;
    const maxH = isPost && !hasShot ? box.clientHeight * (stat ? 0.5 : 0.36) : Infinity;
    const fits = () => lockSpace + text.offsetHeight <= room && noWordOverflow() && inkArea(text) <= budget
      && text.offsetHeight <= maxH;
    let size = start;
    css('--headline', size + 'px');
    while (!fits() && size > 10) {
      size *= 0.96;
      css('--headline', size + 'px');
    }
  }

  function inkArea(text) {
    let area = 0;
    for (const el of text.children) {
      const range = document.createRange();
      range.selectNodeContents(el);
      for (const r of range.getClientRects()) area += r.width * r.height;
    }
    return area;
  }

  // On a tall post the screenshot moves up to sit a fixed gap below the headline.
  function placeShot() {
    const wrap = document.getElementById('shot-wrap');
    const text = document.getElementById('text');
    if (layout !== 'post-tall' || !wrap || !text) return;
    const top = text.getBoundingClientRect().bottom + w * 0.065;
    wrap.style.top = Math.max(h * 0.3, Math.min(wrap.offsetTop, top)) + 'px';
  }

  // With focus, the enlarged screenshot shifts so the chosen point lands at the frame's
  // top-left corner, clamped so no empty edge shows.
  function zoomShot() {
    if (!hasFocus) return;
    const img = document.getElementById('shot');
    const wrap = img.parentElement;
    const x = Math.min(Math.max(0, img.offsetWidth - wrap.clientWidth), focus[0] * img.offsetWidth);
    const y = Math.min(Math.max(0, img.offsetHeight - wrap.clientHeight), focus[1] * img.offsetHeight);
    img.style.transform = `translate(${-x}px, ${-y}px)`;
  }

  whenLoaded().then(() => {
    fit();
    placeShot();
    zoomShot();
    done();
  });

  function whenLoaded() {
    const imgs = [...document.images].filter((i) => i.isConnected && i.getAttribute('src'));
    return Promise.all([
      ...fonts,
      ...imgs.map((i) => (i.complete ? null : new Promise((r) => (i.onload = i.onerror = r)))),
    ]).then(() => document.fonts.ready);
  }

  function done() {
    document.body.dataset.headlinePx = getComputedStyle(root).getPropertyValue('--headline');
    document.title = 'ready';
  }
})();
