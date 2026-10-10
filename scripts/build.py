#!/usr/bin/env python3
"""Render the GitHub Pages site from small, editable JSON content files."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
profile = json.loads((ROOT / "data/profile.json").read_text())
papers = json.loads((ROOT / "data/publications.json").read_text())


def e(value):
    return escape(str(value), quote=True)


def arrow(direction="up"):
    path = "M5 19 19 5M5 5h14v14" if direction == "up" else "M4 12h16m-6-6 6 6-6 6"
    return f'<svg class="arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="{path}"/></svg>'


def external(url, label, css="text-link"):
    return f'<a class="{css}" href="{e(url)}" target="_blank" rel="noopener noreferrer">{label}{arrow()}</a>'


def header(library=False):
    return f'''<a class="skip-link" href="#main">Skip to content</a>
    <header class="site-header"><div class="header-inner">
      <a class="wordmark" href="/" aria-label="Peter Sherman home">peter sherman<span class="wordmark-dot">.</span></a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu <span aria-hidden="true">+</span></button>
      <nav id="site-nav" aria-label="Main navigation">
        <a href="/publications/"{' aria-current="page"' if library else ''}>Publications</a><a href="/#experience">Experience</a><a href="/#contact">Contact</a>
        <a class="nav-cv" href="/images/Peter_Sherman_CV.pdf" target="_blank" rel="noopener">CV {arrow()}</a>
      </nav>
    </div></header>'''


def footer():
    return f'''<footer class="site-footer"><div class="container footer-inner">
      <a class="wordmark" href="/">peter sherman<span class="wordmark-dot">.</span></a>
      <p>Peter Sherman · Data scientist</p>
      <a href="#top" class="back-top">Back to top <span aria-hidden="true">↑</span></a>
    </div></footer>'''


def shell(title, description, body, library=False):
    path = "/publications/" if library else "/"
    structured = {
        "@context": "https://schema.org", "@type": "Person", "name": profile["name"],
        "url": "https://petersherman123.github.io/", "jobTitle": profile["current_title"],
        "worksFor": {"@type": "Organization", "name": profile["current_organization"]},
        "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Harvard University"}, {"@type": "CollegeOrUniversity", "name": "Imperial College London"}],
        "sameAs": [profile["scholar"], profile["linkedin"], profile["github"]]
    }
    return f'''<!doctype html>
<html lang="en" id="top">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title><meta name="description" content="{e(description)}">
  <meta name="theme-color" content="#10151b"><meta name="color-scheme" content="dark"><link rel="canonical" href="https://petersherman123.github.io{path}">
  <meta property="og:type" content="{'profile' if not library else 'website'}"><meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}"><meta property="og:url" content="https://petersherman123.github.io{path}">
  <meta property="og:image" content="https://petersherman123.github.io/images/me.jpg"><meta property="og:image:alt" content="Peter Sherman">
  <meta name="twitter:card" content="summary"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/site.css"><script src="/assets/site.js" defer></script>
  <script type="application/ld+json">{json.dumps(structured).replace('<', chr(92) + 'u003c')}</script>
</head>
<body>{header(library)}<main id="main">{body}</main>{footer()}</body>
</html>
'''


def featured(paper, index):
    return f'''<article class="featured-paper">
      <div class="paper-index" aria-hidden="true">0{index}</div>
      <div class="featured-copy"><p class="eyebrow">{e(paper['topic'])}<span class="eyebrow-divider">/</span>{paper['year']}</p>
        <h3><a href="{e(paper['url'])}" target="_blank" rel="noopener noreferrer">{e(paper['title'])}{arrow()}</a></h3>
        <p class="paper-summary">{e(paper['summary'])}</p><p class="paper-venue">{e(paper['venue'])}<span> · {e(paper['type'])}</span></p>
      </div></article>'''


def experience(item):
    description = f'<p class="experience-description">{e(item["description"])}</p>' if item.get("description") else ""
    return f'''<article class="experience-row"><p class="experience-date">{e(item['dates'])}{'<span class="current-label">Current</span>' if item.get('current') else ''}</p>
      <div><h3>{e(item['organization'])}</h3><p class="experience-role">{e(item['role'])}</p>{description}</div></article>'''


def home():
    selected = "".join(featured(p, i + 1) for i, p in enumerate(p for p in papers if p.get("featured")))
    recent = "".join(experience(x) for x in profile["experience"][:3])
    earlier = "".join(experience(x) for x in profile["experience"][3:])
    return f'''
    <section class="hero container" aria-labelledby="hero-title">
      <div class="hero-copy"><p class="eyebrow hero-eyebrow">Data scientist · PhD</p>
        <h1 id="hero-title">Peter Sherman</h1>
        <p class="hero-role">{e(profile['current_title'])}<br><span>Orlando Magic</span></p>
        <p class="hero-intro">Associate Researcher at Harvard University. PhD in Earth and Planetary Sciences, Harvard, 2022.</p>
        <div class="hero-actions"><a class="button button-dark" href="/publications/">Publications {arrow('right')}</a><a class="text-link" href="/images/Peter_Sherman_CV.pdf" target="_blank" rel="noopener">CV {arrow()}</a></div>
      </div>
      <figure class="hero-portrait"><div class="portrait-frame"><img src="/images/me.jpg" width="2247" height="2247" alt="Portrait of Peter Sherman" fetchpriority="high"></div></figure>
    </section>

    <section id="research" class="research-section section" aria-labelledby="research-title"><div class="container">
      <div class="section-heading research-heading"><h2 id="research-title">Selected publications</h2>{external(profile['scholar'], 'Google Scholar')}</div>
      <div class="featured-list">{selected}</div><div class="research-bottom"><a class="button button-outline" href="/publications/">All publications {arrow('right')}</a></div>
    </div></section>

    <section id="experience" class="section container" aria-labelledby="experience-title"><span id="work" class="legacy-anchor" aria-hidden="true"></span><div class="experience-layout">
      <div class="section-heading experience-heading"><h2 id="experience-title">Experience</h2><a class="text-link" href="/images/Peter_Sherman_CV.pdf" target="_blank" rel="noopener">Download CV {arrow()}</a></div>
      <div class="experience-list">{recent}<details class="earlier-experience"><summary>Previous &amp; additional roles <span aria-hidden="true">+</span></summary>{earlier}</details></div>
    </div>
    <div class="education-grid"><div><h2>Education</h2><h3>Harvard University</h3><p>PhD, Earth and Planetary Sciences · 2022</p><h3>Imperial College London</h3><p>Master’s degree in Physics · 2017</p></div><div><h2>Teaching</h2><p class="teaching-dates">Harvard University · 2018–2022</p><p>Climate change and Earth science courses; undergraduate and high-school research supervision.</p><p class="muted">Teaching recognized by the Derek Bok Center for Teaching and Learning.</p></div></div>
    </section>

    <section class="press-section"><div class="container press-inner"><h2>Press</h2><div>{external('https://chinaproject.harvard.edu/news/peter-sherman', 'Harvard China Project · Researcher profile')}{external('https://www.seas.harvard.edu/news/2020/11/indias-renewable-future', 'Harvard SEAS · India’s renewable future')}{external('https://www.seas.harvard.edu/news/2020/02/opportunity-blows-offshore-wind-china-0', 'Harvard SEAS · Offshore wind in China')}</div></div></section>

    <section id="contact" class="contact-section" aria-labelledby="contact-title"><div class="container contact-inner"><h2 id="contact-title">Contact</h2><div class="contact-copy"><a class="contact-email" href="mailto:{e(profile['email'])}">{e(profile['email'])}{arrow()}</a><div class="contact-links">{external(profile['linkedin'], 'LinkedIn')}{external(profile['scholar'], 'Google Scholar')}{external(profile['github'], 'GitHub')}</div></div></div></section>
    '''


def publication_row(p):
    data = e(" ".join(str(p[k]) for k in ("title", "authors", "venue", "year", "topic", "type")).casefold())
    pdf = external(p["pdf"], "Open PDF", "publication-pdf") if p.get("pdf") else ""
    return f'''<article class="publication-row" data-search="{data}" data-type="{e(p['type'])}" data-topic="{e(p['topic'])}">
      <div class="publication-year">{p['year']}</div><div><p class="eyebrow publication-meta">{e(p['topic'])}<span class="type-tag">{e(p['type'])}</span></p>
        <h2><a href="{e(p['url'])}" target="_blank" rel="noopener noreferrer">{e(p['title'])}{arrow()}</a></h2><p class="publication-authors">{e(p['authors'])}</p><p class="publication-venue">{e(p['venue'])}</p>{pdf}</div></article>'''


def library():
    snapshot = profile["scholar_snapshot"]
    topics = "".join(f'<option>{e(t)}</option>' for t in sorted({p["topic"] for p in papers}))
    return f'''
    <section class="library-hero container"><a class="text-link library-back" href="/">← Back to home</a><p class="eyebrow">2016–2025</p><h1>Publications</h1><p class="library-intro">Climate dynamics, renewable energy, atmospheric science, and machine learning for the environment.</p>
      <div class="scholar-strip"><div><strong>{snapshot['citations']:,}</strong><span>Citations</span></div><div><strong>{snapshot['h_index']}</strong><span>h-index</span></div><p>Google Scholar snapshot<br>{e(snapshot['date'])}</p>{external(profile['scholar'], 'View current metrics')}</div>
    </section>
    <section class="container library-section" aria-label="Publication library"><div class="publication-controls" hidden>
      <div class="search-field"><label for="publication-search">Search publications</label><input id="publication-search" type="search" placeholder="Title, author, keyword, or year…" autocomplete="off"></div>
      <div class="topic-field"><label for="publication-topic">Research area</label><select id="publication-topic"><option value="">All areas</option>{topics}</select></div>
      <div class="type-filters" role="group" aria-label="Publication type">{''.join(f'<button type="button" data-filter="{e(t)}" aria-pressed="{str(i==0).lower()}">{e(label)}</button>' for i,(t,label) in enumerate([('', 'All'),('Journal article','Journal articles'),('Conference abstract','Conference abstracts'),('Preprint','Preprints')]))}</div>
    </div><p class="publication-count" role="status" aria-live="polite">{len(papers)} publications</p><div id="publication-list">{''.join(publication_row(p) for p in papers)}</div><div class="no-results" hidden><h2>No matching publications</h2><p>Try another keyword or research area.</p><button type="button" class="button button-outline" id="reset-filters">Clear filters {arrow('right')}</button></div>
    <p class="library-note">Includes journal articles, conference abstracts, and preprints. {external(profile['scholar'], 'Full Google Scholar profile')}</p></section>
    '''


def redirect(target, title):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="refresh" content="0;url={e(target)}"><link rel="canonical" href="https://petersherman123.github.io{e(target)}"><title>{e(title)} | Peter Sherman</title></head><body><p><a href="{e(target)}">{e(title)}</a></p></body></html>\n'


def write(path, content):
    destination = ROOT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content)


if __name__ == "__main__":
    write("index.html", shell("Peter Sherman", f"Peter Sherman, {profile['current_title']} at {profile['current_organization']} and Associate Researcher at Harvard University.", home()))
    write("publications/index.html", shell("Publications | Peter Sherman", "Research by Peter Sherman on climate dynamics, renewable energy, atmospheric science, geospatial machine learning, and marine microplastics.", library(), True))
    for legacy in ("projects",):
        write(f"{legacy}/index.html", redirect("/publications/", "Publications"))
    for legacy in ("resume",):
        write(f"{legacy}/index.html", redirect("/images/Peter_Sherman_CV.pdf", "View CV"))
    write("about/index.html", redirect("/", "About Peter Sherman"))
    write("404.html", shell("Page not found | Peter Sherman", "Return to Peter Sherman's website.", '<section class="container not-found"><p class="eyebrow">404</p><h1>Page not found</h1><p>This page may have moved.</p><a class="button button-dark" href="/">Return home →</a><a class="text-link" href="/publications/">Publications →</a></section>'))
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://petersherman123.github.io/</loc></url><url><loc>https://petersherman123.github.io/publications/</loc></url></urlset>\n')
    print(f"Built homepage, research library ({len(papers)} publications), legacy redirects, and 404 page.")
