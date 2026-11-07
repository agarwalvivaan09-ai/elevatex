#!/usr/bin/env python3
"""
Builds the ElevateX website.

  Edit:   _src/pages/*.html      (page content, with a small header block at the top)
          _src/articles/articles.json  (founder notes and blog posts, word for word)
  Run:    python3 _src/build.py
  Output: the .html files in the repo root, plus sitemap.xml

Every page gets the same header, phone menu and footer written straight into the HTML
(so the menu appears instantly, with no flash), image width/height (no layout jumps) and
lazy loading for images below the first screen.

_src/ is ignored by GitHub Pages, so it is never published.
Needs Pillow for image sizes:  pip install pillow
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / '_src'
SITE = 'https://elevate-x.in'
HUB = 'https://hub.elevate-x.in'
APPLY = 'contact.html'
EMAIL = 'elevate.x.20.25.ad@gmail.com'

try:
    from PIL import Image
except ImportError:  # sizes are a nicety; the site still builds without Pillow
    Image = None

NAV = [
    ('about.html', 'About', 'about'),
    ('welfare.html', 'Drives', 'drives'),
    ('fundraising.html', 'Events', 'events'),
    ('unnati.html', 'Unnati', 'unnati'),
    ('team.html', 'Team', 'team'),
    ('timeline.html', 'Timeline', 'timeline'),
    ('blog.html', 'Blog', 'blog'),
    ('resources.html', 'Resources', 'resources'),
]

SOCIAL = [
    ('Instagram', 'https://www.instagram.com/elevate.x._/'),
    ('LinkedIn', 'https://www.linkedin.com/company/elevat-ex/'),
    ('X', 'https://x.com/elevatex182276?s=21'),
    ('WhatsApp', 'https://chat.whatsapp.com/F1YwvNztn4LJTFXM8NR43r?mode=hqctcli'),
    ('Linktree', 'https://linktr.ee/elevate.x'),
]


def esc(s):
    return html.escape(s, quote=True)


def header(active):
    links = ''.join(
        f'<a href="{href}"{" aria-current=page" if key == active else ""}>{label}</a>' for href, label, key in NAV
    )
    sheet = ''.join(
        f'<a href="{href}"{" aria-current=page" if key == active else ""}>{label}</a>' for href, label, key in NAV
    )
    social = ''.join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SOCIAL[:3])
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap nav">
    <a href="index.html" class="brand"><img src="logo-icon.png" alt="" width="38" height="38">ElevateX</a>
    <nav class="nav-links" aria-label="Main">{links}</nav>
    <div class="nav-actions">
      <a href="{APPLY}" class="btn btn-ghost">Apply</a>
      <a href="{HUB}" class="btn btn-primary">Volunteer login</a>
    </div>
    <button class="menu-btn" id="menuToggle" aria-label="Open menu" aria-expanded="false" aria-controls="mobileMenu"><span></span></button>
  </div>
</header>
<div class="mobile-menu" id="mobileMenu" role="dialog" aria-modal="true" aria-label="Menu">
  <div class="scrim"></div>
  <div class="sheet">
    <div class="sheet-top">
      <a href="index.html" class="brand"><img src="logo-icon.png" alt="" width="38" height="38">ElevateX</a>
      <button class="sheet-close" aria-label="Close menu">×</button>
    </div>
    <nav aria-label="Main">{sheet}</nav>
    <div class="sheet-actions">
      <a href="{APPLY}" class="btn btn-ghost">Apply to join</a>
      <a href="{HUB}" class="btn btn-primary">Volunteer login</a>
    </div>
    <div class="sheet-social">{social}</div>
  </div>
</div>'''


def footer():
    social = ''.join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in SOCIAL)
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <div class="footer-brand"><img src="logo-icon.png" alt="" width="40" height="40" loading="lazy">ElevateX</div>
        <p>A nonprofit run by school students in Kolkata. Drives, financial literacy classes, and the events that pay for them.</p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div>
        <h4>What we do</h4>
        <ul>
          <li><a href="welfare.html">Drives</a></li>
          <li><a href="unnati.html">Project Unnati</a></li>
          <li><a href="fundraising.html">Events &amp; fundraisers</a></li>
          <li><a href="euphoria.html">Euphoria</a></li>
          <li><a href="timeline.html">Timeline</a></li>
        </ul>
      </div>
      <div>
        <h4>ElevateX</h4>
        <ul>
          <li><a href="about.html">About us</a></li>
          <li><a href="team.html">Team</a></li>
          <li><a href="blog.html">Blog</a></li>
          <li><a href="resources.html">Certificates</a></li>
          <li><a href="{APPLY}">Apply to join</a></li>
          <li><a href="{HUB}">Volunteer login</a></li>
        </ul>
      </div>
      <div>
        <h4>Follow</h4>
        <ul>{social}</ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 ElevateX · Kolkata, India</span>
      <span>Website by Vivaan Agarwal</span>
    </div>
  </div>
</footer>'''


def page(meta, body):
    name = meta['file']
    url = f'{SITE}/' if name == 'index.html' else f'{SITE}/{name}'
    title = meta['title']
    full_title = title if 'ElevateX' in title else f'{title} | ElevateX'
    image = meta.get('image', 'image1ex.jpg')
    return f'''<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(meta['description'])}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(meta['description'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/{image}">
<meta property="og:type" content="{meta.get('ogtype', 'website')}">
<meta property="og:site_name" content="ElevateX">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1F3D2B">
{'<meta name="google-site-verification" content="BRuGEfzzq23Uh3XquKvL4vKrcuAyaFd01iYPJiQE5AU">' if name == 'index.html' else ''}
{meta.get('extra_head', '')}
<link rel="icon" type="image/png" href="logo-icon.png">
<link rel="apple-touch-icon" href="logo-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,600;1,9..144,600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>
{header(meta.get('nav', ''))}
<main id="main">
{body.strip()}
</main>
{footer()}
<script src="script.js" defer></script>
</body>
</html>
'''


_size_cache = {}


def fix_images(markup):
    """Add width/height (prevents layout jumps) and lazy loading (except images marked data-eager)."""
    def repl(m):
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag)
        if src and Image and 'width=' not in tag and not src.group(1).startswith('http'):
            f = ROOT / src.group(1)
            if f.exists():
                if f not in _size_cache:
                    with Image.open(f) as im:
                        _size_cache[f] = im.size
                w, h = _size_cache[f]
                tag = tag.replace('<img ', f'<img width="{w}" height="{h}" ', 1)
        if 'data-eager' in tag:
            tag = tag.replace(' data-eager', ' fetchpriority="high"')
        elif 'loading=' not in tag:
            tag = tag.replace('<img ', '<img loading="lazy" decoding="async" ', 1)
        if 'alt=' not in tag:
            tag = tag.replace('<img ', '<img alt="" ', 1)
        return tag
    return re.sub(r'<img\b[^>]*>', repl, markup)


def parse(path):
    text = path.read_text(encoding='utf-8')
    m = re.match(r'\s*<!--(.*?)-->', text, re.S)
    meta = {}
    for line in m.group(1).strip().splitlines():
        k, _, v = line.partition(':')
        meta[k.strip()] = v.strip()
    return meta, text[m.end():]


def article_body(a, kind):
    """Founder notes and blog posts: the author's words, unchanged."""
    paras = a['paras']
    sign = ''
    if kind == 'founder' and paras and paras[-1].startswith('Founder'):
        sign = paras[-2] + '\n' + paras[-1] if paras[-2].startswith('—') else paras[-1]
        paras = paras[:-2] if paras[-2].startswith('—') else paras[:-1]
    out = []
    for p in paras:
        if p.startswith('## '):
            out.append(f'<h2>{esc(p[3:])}</h2>')
        else:
            out.append('<p>' + esc(p).replace('\n', '<br>') + '</p>')
    if sign:
        out.append(f'<p class="sign">{esc(sign)}</p>')
    return '\n'.join(out)


def words(a):
    return sum(len(p.split()) for p in a['paras'])


def build_articles():
    data = json.loads((SRC / 'articles' / 'articles.json').read_text(encoding='utf-8'))
    founders = {
        'founder': ('Vivaan Agarwal', 'Founder, former CEO and Chairman'),
        'founder2': ('Devyansh Tolasaria', 'Founder, former COO and Vice Chairman'),
        'founder3': ('Samridh Sanganeria', 'Founder, former CFO'),
    }
    pages = []
    for key, (who, role) in founders.items():
        a = data[key]
        body = f'''<article class="article"><div class="wrap narrow">
  <a href="team.html" class="back-link">Team</a>
  <p class="meta" style="margin-top:22px">Founder's note · {esc(who)}, {esc(role)}</p>
  <h1>A note from {esc(who.split()[0])}</h1>
  <div class="text">{article_body(a, 'founder')}</div>
  <div class="article-foot"><a href="team.html" class="arrow-link">Meet the team</a><a href="blog.html" class="arrow-link">Read the blog</a></div>
</div></article>'''
        pages.append(({'file': f'{key}.html', 'title': f"A note from {who}", 'description': f"Why ElevateX exists, in {who.split()[0]}'s words. {who}: {role}.", 'nav': 'team', 'ogtype': 'article', 'image': 'image1ex.jpg'}, body))
    posts = []
    for key in ['blog4', 'blog1', 'blog2', 'blog3']:
        a = data[key]
        date, _, by = (a['meta'] or '').partition('•')
        by = by.replace('By', '').strip()
        mins = max(1, round(words(a) / 200))
        posts.append((key, a['title'], date.strip(), by, mins))
        body = f'''<article class="article"><div class="wrap narrow">
  <a href="blog.html" class="back-link">All posts</a>
  <p class="meta" style="margin-top:22px">{esc(date.strip())} · {esc(by)} · {mins} min read</p>
  <h1>{esc(a['title'])}</h1>
  <div class="text">{article_body(a, 'blog')}</div>
  <div class="article-foot"><a href="blog.html" class="arrow-link">More from the blog</a><a href="{APPLY}" class="arrow-link">Join ElevateX</a></div>
</div></article>'''
        first = a['paras'][0][:150].rsplit(' ', 1)[0] + '…'
        pages.append(({'file': f'{key}.html', 'title': a['title'], 'description': first, 'nav': 'blog', 'ogtype': 'article'}, body))
    items = ''.join(
        f'''<a class="post reveal" href="{k}.html"><div><div class="meta">{esc(d)} · {mins} min read</div><h3>{esc(t)}</h3><div class="meta">{esc(by)}</div></div><span class="go" aria-hidden="true">→</span></a>'''
        for k, t, d, by, mins in posts
    )
    blog = f'''<section class="page-head"><div class="wrap">
  <span class="eyebrow">Blog</span>
  <h1>Written by our members</h1>
  <p class="lede">What it has been like to build ElevateX, from the people doing it. Unedited, in their own words.</p>
</div></section>
<section class="section tight" style="padding-top:8px"><div class="wrap"><div class="post-list">{items}</div></div></section>'''
    pages.append(({'file': 'blog.html', 'title': 'Blog', 'description': 'Posts by ElevateX members about building a student-run nonprofit, running events and why financial literacy matters.', 'nav': 'blog'}, blog))
    return pages


REDIRECTS = {'impact.html': 'index.html', 'projects.html': 'index.html#what-we-do'}


def redirect_page(target):
    return f'''<!DOCTYPE html>
<html lang="en-IN"><head><meta charset="UTF-8"><title>ElevateX</title>
<meta name="robots" content="noindex"><link rel="canonical" href="{SITE}/{target.split('#')[0] if target != 'index.html' else ''}">
<meta http-equiv="refresh" content="0; url={target}"></head>
<body><p>This page has moved. <a href="{target}">Continue to ElevateX</a>.</p></body></html>
'''


def main():
    built = []
    for path in sorted((SRC / 'pages').glob('*.html')):
        meta, body = parse(path)
        meta['file'] = path.name
        built.append((meta, body))
    built += build_articles()
    for meta, body in built:
        (ROOT / meta['file']).write_text(fix_images(page(meta, body)), encoding='utf-8')
    for name, target in REDIRECTS.items():
        (ROOT / name).write_text(redirect_page(target), encoding='utf-8')
    urls = sorted(m['file'] for m, _ in built if m['file'] != '404.html')
    urls.remove('index.html')
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', f'  <url><loc>{SITE}/</loc></url>']
    sitemap += [f'  <url><loc>{SITE}/{u}</loc></url>' for u in urls]
    sitemap.append('</urlset>')
    (ROOT / 'sitemap.xml').write_text('\n'.join(sitemap) + '\n', encoding='utf-8')
    print(f'Built {len(built)} pages, {len(REDIRECTS)} redirects, sitemap with {len(urls) + 1} URLs.')


if __name__ == '__main__':
    main()
