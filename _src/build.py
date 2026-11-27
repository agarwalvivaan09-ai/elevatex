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
import subprocess
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

# The header shows the main pages; the phone menu and the footer also carry the rest.
NAV = [
    ('about.html', 'About', 'about'),
    ('welfare.html', 'Drives', 'drives'),
    ('fundraising.html', 'Events', 'events'),
    ('unnati.html', 'Unnati', 'unnati'),
    ('gallery.html', 'Gallery', 'gallery'),
    ('team.html', 'Team', 'team'),
]
NAV_MORE = [
    ('volunteer-hub.html', 'Hub', 'hub'),
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
        f'<a href="{href}"{" aria-current=page" if key == active else ""}>{label}</a>' for href, label, key in NAV + NAV_MORE
    )
    social = ''.join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SOCIAL[:3])
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap nav">
    <a href="index.html" class="brand"><img src="images/brand/logo-icon.png" alt="" width="38" height="38">ElevateX</a>
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
      <a href="index.html" class="brand"><img src="images/brand/logo-icon.png" alt="" width="38" height="38">ElevateX</a>
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
        <div class="footer-brand"><img src="images/brand/logo-icon.png" alt="" width="40" height="40" loading="lazy">ElevateX</div>
        <p>ElevateX (Elevate X) is a nonprofit run by school students in Kolkata. Drives, financial literacy classes, and the events that pay for them.</p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div>
        <h4>What we do</h4>
        <ul>
          <li><a href="welfare.html">Drives</a></li>
          <li><a href="unnati.html">Project Unnati</a></li>
          <li><a href="fundraising.html">Events &amp; fundraisers</a></li>
          <li><a href="gallery.html">Gallery</a></li>
          <li><a href="euphoria.html">Euphoria</a></li>
          <li><a href="timeline.html">Timeline</a></li>
        </ul>
      </div>
      <div>
        <h4>ElevateX</h4>
        <ul>
          <li><a href="about.html">About us</a></li>
          <li><a href="team.html">Team</a></li>
          <li><a href="volunteer-hub.html">Volunteer Hub</a></li>
          <li><a href="blog.html">Blog</a></li>
          <li><a href="resources.html">Resources</a></li>
          <li><a href="verify.html">Check a certificate</a></li>
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


# Structured data for the homepage: tells Google that "ElevateX" and "Elevate X" are the same
# organisation, and links the official social profiles to the website.
SCHEMA = """<script type="application/ld+json">
{"@context":"https://schema.org","@graph":[
{"@type":"NGO","@id":"https://elevate-x.in/#org","name":"ElevateX","alternateName":["Elevate X","ElevateX Kolkata","Elevate X Kolkata","ElevateX Nonprofit"],
"url":"https://elevate-x.in/","logo":"https://elevate-x.in/images/brand/logo-icon.png","foundingDate":"2025-03-08",
"founder":[{"@id":"https://elevate-x.in/team.html#vivaan"},{"@id":"https://elevate-x.in/team.html#devyansh"},{"@id":"https://elevate-x.in/team.html#samridh"}],
"description":"ElevateX is a nonprofit run by school students in Kolkata: welfare drives, Project Unnati financial literacy workshops, and fundraising events.",
"areaServed":"Kolkata, India","address":{"@type":"PostalAddress","addressLocality":"Kolkata","addressRegion":"West Bengal","addressCountry":"IN"},
"email":"elevate.x.20.25.ad@gmail.com",
"sameAs":["https://www.instagram.com/elevate.x._/","https://www.linkedin.com/company/elevat-ex/","https://x.com/elevatex182276","https://linktr.ee/elevate.x"]},
{"@type":"WebSite","@id":"https://elevate-x.in/#website","name":"ElevateX","alternateName":"Elevate X","url":"https://elevate-x.in/","publisher":{"@id":"https://elevate-x.in/#org"}}
]}
</script>"""

# People: tells Google who founded and runs ElevateX, so searches for their names connect to the
# organisation. Same names, roles, photos and links as the Team page.
FOUNDERS = [
    ('vivaan', 'Vivaan Agarwal', 'Founder, former CEO & Chairman', 'founder.html', 'images/team/elevatex-vivaan-agarwal.jpg',
     ['https://www.instagram.com/vivaan_agarwal__/', 'https://agarwalvivaan09-ai.github.io/vivaan-agarwal-website-3.0/']),
    ('devyansh', 'Devyansh Tolasaria', 'Founder, former COO & Vice Chairman', 'founder2.html', 'images/team/elevatex-devyansh-tolasaria.jpeg',
     ['https://www.instagram.com/devyanshtolasaria_7']),
    ('samridh', 'Samridh Sanganeria', 'Founder, former CFO', 'founder3.html', 'images/team/elevatex-samridh-sanganeria.jpeg',
     ['https://www.instagram.com/samridhsanganeria']),
]
ADVISORS = [
    ('krishank', 'Krishank Jain', 'Former CFO', 'images/team/elevatex-krishank-jain.jpg', ['https://www.instagram.com/krishankjain_']),
    ('kaschith', 'Kaschith Saraogi', 'Former Head of Drives', 'images/team/elevatex-kaschith-saraogi.jpg', ['https://www.instagram.com/kaschith_saraogi']),
    ('abhaay', 'Abhaay Jhawar', 'Former CMO & Head of Operations', 'images/team/elevatex-abhaay-jhawar.jpeg',
     ['https://www.instagram.com/abhaay09', 'https://www.linkedin.com/in/abhaay-jhawar-054734370']),
    ('pragya', 'Pragya Chharia', 'Chief Marketing Officer', 'images/team/elevatex-pragya-chharia.jpg', ['https://www.instagram.com/pragyachharia._']),
    ('nityam', 'Nityam Chaurasia', 'Director of Events', None, []),
    ('yaahvi', 'Yaahvi Kamalia', 'Director of Events', 'images/team/elevatex-yaahvi-kamalia.jpg', ['https://www.instagram.com/yaahvikamalia']),
]
ORG = {'@id': f'{SITE}/#org'}


def person(key, name, role, url, image, links):
    p = {'@type': 'Person', '@id': f'{SITE}/team.html#{key}', 'name': name, 'jobTitle': role,
         'worksFor': ORG, 'url': f'{SITE}/{url}'}
    if image:
        p['image'] = f'{SITE}/{image}'
    if links:
        p['sameAs'] = links
    return p


FOUNDER_NODES = {f[3]: person(f[0], f[1], f[2], f[3], f[4], f[5]) for f in FOUNDERS}
ADVISOR_NODES = [person(a[0], a[1], a[2], 'team.html', a[3], a[4]) for a in ADVISORS]


def ld(data):
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'


def people_schema(name):
    """Founders and advisors on the Team page; the founder on each founder's note."""
    if name == 'team.html':
        return ld({'@context': 'https://schema.org', '@type': 'NGO', '@id': ORG['@id'], 'name': 'ElevateX',
                   'founder': [{'@id': p['@id']} for p in FOUNDER_NODES.values()],
                   'member': list(FOUNDER_NODES.values()) + ADVISOR_NODES})
    if name in FOUNDER_NODES:
        return ld({'@context': 'https://schema.org', '@type': 'ProfilePage', 'mainEntity': FOUNDER_NODES[name]})
    return ''


# Breadcrumbs: the trail Google can show above a result (elevate-x.in › Blog › Post).
# Pages not listed here sit directly under the homepage.
PARENTS = {
    'blog1.html': ('Blog', 'blog.html'), 'blog2.html': ('Blog', 'blog.html'),
    'blog3.html': ('Blog', 'blog.html'), 'blog4.html': ('Blog', 'blog.html'),
    'founder.html': ('Team', 'team.html'), 'founder2.html': ('Team', 'team.html'),
    'founder3.html': ('Team', 'team.html'),
    'euphoria.html': ('Events & fundraisers', 'fundraising.html'),
    'verify.html': ('Resources', 'resources.html'),
}


def breadcrumbs(meta):
    name = meta['file']
    if name in ('index.html', '404.html'):
        return ''
    trail = [('ElevateX', f'{SITE}/')]
    if name in PARENTS:
        label, href = PARENTS[name]
        trail.append((label, f'{SITE}/{href}'))
    trail.append((meta['title'], f'{SITE}/{name}'))
    items = [{'@type': 'ListItem', 'position': i, 'name': label, 'item': url}
             for i, (label, url) in enumerate(trail, 1)]
    data = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'


def page(meta, body):
    name = meta['file']
    url = f'{SITE}/' if name == 'index.html' else f'{SITE}/{name}'
    title = meta['title']
    full_title = title if 'ElevateX' in title else f'{title} | ElevateX'
    image = meta.get('image', 'images/team/elevatex-team-kolkata.jpg')
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
{SCHEMA if name == 'index.html' else breadcrumbs(meta)}{people_schema(name)}
{meta.get('extra_head', '')}
<link rel="icon" type="image/png" href="images/brand/logo-icon.png">
<link rel="apple-touch-icon" href="images/brand/logo-icon.png">
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
  <h1>A note from {esc(who.split()[0])}, ElevateX co-founder</h1>
  <div class="text">{article_body(a, 'founder')}</div>
  <div class="article-foot"><a href="team.html" class="arrow-link">Meet the team</a><a href="blog.html" class="arrow-link">Read the blog</a></div>
</div></article>'''
        pages.append(({'file': f'{key}.html', 'title': f"A note from {who}", 'description': f"Why ElevateX exists, in {who.split()[0]}'s words. {who}: {role}.", 'nav': 'team', 'ogtype': 'article', 'image': 'images/team/elevatex-team-kolkata.jpg'}, body))
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
  <h1>The ElevateX blog: written by our members</h1>
  <p class="lede">What it has been like to build ElevateX, from the people doing it. Unedited, in their own words.</p>
</div></section>
<section class="section tight" style="padding-top:8px"><div class="wrap"><div class="post-list">{items}</div></div></section>'''
    pages.append(({'file': 'blog.html', 'title': 'Blog', 'description': 'Posts by ElevateX members about building a student-run nonprofit, running events and why financial literacy matters.', 'nav': 'blog'}, blog))
    return pages


GALLERY_GROUPS = [
    ('drives', 'Drives and Project Unnati', 'Out in Kolkata with food, water, umbrellas, saplings and rubbish bags, and in classrooms teaching money basics.'),
    ('events', 'Events', 'The fundraisers that pay for every drive.'),
]


def build_gallery():
    """The Gallery page (an album per drive or event) and one page per album.
    Albums and photos live in _src/gallery/albums.json; the first photo of each album is its cover."""
    albums = json.loads((SRC / 'gallery' / 'albums.json').read_text(encoding='utf-8'))
    total = sum(len(a['photos']) for a in albums)
    pages = []
    groups = []
    for key, title, lede in GALLERY_GROUPS:
        cards = ''.join(
            f'''
      <a class="card reveal" href="gallery-{a['slug']}.html"><div class="media"><img src="{a['photos'][0][0]}" alt="{esc(a['photos'][0][1])}"></div><div class="body"><h3>{esc(a['title'])}</h3><p>{esc(a['lede'])}</p><span class="chip">{len(a['photos'])} photo{'s' if len(a['photos']) != 1 else ''}</span></div></a>'''
            for a in albums if a['group'] == key)
        groups.append(f'''<section class="section tight" id="{key}">
  <div class="wrap">
    <div class="section-head">
      <h2>{esc(title)}</h2>
      <p>{esc(lede)}</p>
    </div>
    <div class="cards">{cards}
    </div>
  </div>
</section>''')
    index = f'''<section class="page-head">
  <div class="wrap">
    <span class="eyebrow">Gallery</span>
    <h1>ElevateX in photos</h1>
    <p class="lede">{total} photos from our drives, Project Unnati and the events that fund them. Pick an album to see all its photos.</p>
  </div>
</section>
''' + '\n'.join(groups)
    pages.append(({'file': 'gallery.html', 'title': 'Gallery', 'nav': 'gallery', 'image': albums[0]['photos'][0][0],
                   'description': f'Photos of ElevateX in Kolkata: clean-ups, food, umbrella and plantation drives, stray feeding, Project Unnati and our fundraising events. {total} photos.'}, index))
    for a in albums:
        figs = '\n'.join(
            f'      <figure><a href="{f}" target="_blank" rel="noopener"><img src="{f}" alt="{esc(alt)}"{" data-eager" if i == 0 else ""}></a></figure>'
            for i, (f, alt) in enumerate(a['photos']))
        others = [b for b in albums if b['slug'] != a['slug'] and b['group'] == a['group']][:3]
        more = ''.join(
            f'''
      <a class="card reveal" href="gallery-{b['slug']}.html"><div class="media"><img src="{b['photos'][0][0]}" alt="{esc(b['photos'][0][1])}"></div><div class="body"><h3>{esc(b['title'])}</h3><span class="chip">{len(b['photos'])} photo{'s' if len(b['photos']) != 1 else ''}</span></div></a>'''
            for b in others)
        more_section = f'''
<section class="section tight">
  <div class="wrap">
    <div class="section-head"><h2>More albums</h2></div>
    <div class="cards">{more}
    </div>
    <p style="margin-top:28px"><a href="gallery.html" class="arrow-link">All albums</a></p>
  </div>
</section>''' if others else ''
        body = f'''<section class="page-head">
  <div class="wrap">
    <a href="gallery.html" class="back-link">Gallery</a>
    <span class="eyebrow" style="display:flex;margin-top:22px">{len(a['photos'])} photos</span>
    <h1>{esc(a['title'])}</h1>
    <p class="lede">{esc(a['lede'])}</p>
  </div>
</section>

<section class="section tight" style="padding-top:8px">
  <div class="wrap">
    <div class="gallery">
{figs}
    </div>
  </div>
</section>{more_section}'''
        pages.append(({'file': f"gallery-{a['slug']}.html", 'title': f"{a['title']} photos", 'nav': 'gallery',
                       'image': a['photos'][0][0],
                       'description': f"{len(a['photos'])} photos of ElevateX {a['title'].lower()} in Kolkata. {a['lede']}"}, body))
        PARENTS[f"gallery-{a['slug']}.html"] = ('Gallery', 'gallery.html')
    return pages


REDIRECTS = {'impact.html': 'index.html', 'projects.html': 'index.html#what-we-do'}


def redirect_page(target):
    return f'''<!DOCTYPE html>
<html lang="en-IN"><head><meta charset="UTF-8"><title>ElevateX</title>
<meta name="robots" content="noindex"><link rel="canonical" href="{SITE}/{target.split('#')[0] if target != 'index.html' else ''}">
<meta http-equiv="refresh" content="0; url={target}"></head>
<body><p>This page has moved. <a href="{target}">Continue to ElevateX</a>.</p></body></html>
'''


def last_changed(file):
    """Date the page's source last changed in git (YYYY-MM-DD), or '' if unknown."""
    src = SRC / 'pages' / file
    target = src if src.exists() else SRC / 'articles' / 'articles.json'
    try:
        out = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', str(target)],
                             cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        out = ''
    return out


def sitemap_entry(path, file):
    lastmod = last_changed(file)
    tag = f'<lastmod>{lastmod}</lastmod>' if lastmod else ''
    return f'  <url><loc>{SITE}/{path}</loc>{tag}</url>'


def main():
    built = []
    for path in sorted((SRC / 'pages').glob('*.html')):
        meta, body = parse(path)
        meta['file'] = path.name
        built.append((meta, body))
    built += build_articles()
    built += build_gallery()
    for meta, body in built:
        (ROOT / meta['file']).write_text(fix_images(page(meta, body)), encoding='utf-8')
    for name, target in REDIRECTS.items():
        (ROOT / name).write_text(redirect_page(target), encoding='utf-8')
    urls = sorted(m['file'] for m, _ in built if m['file'] != '404.html')
    urls.remove('index.html')
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', sitemap_entry('', 'index.html')]
    sitemap += [sitemap_entry(u, u) for u in urls]
    sitemap.append('</urlset>')
    (ROOT / 'sitemap.xml').write_text('\n'.join(sitemap) + '\n', encoding='utf-8')
    print(f'Built {len(built)} pages, {len(REDIRECTS)} redirects, sitemap with {len(urls) + 1} URLs.')


if __name__ == '__main__':
    main()
