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
        <a href="/#work">Work</a><a href="/publications/"{' aria-current="page"' if library else ''}>Research</a><a href="/#experience">Experience</a><a href="/#contact">Contact</a>
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
  <meta name="theme-color" content="#f6f5f0"><link rel="canonical" href="https://petersherman123.github.io{path}">
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
      <div class="hero-copy"><p class="eyebrow hero-eyebrow"><span class="small-cross" aria-hidden="true">✳</span> Peter Sherman, PhD</p>
        <h1 id="hero-title">Data science,<br>climate <em>&amp; sport.</em></h1>
        <p class="hero-intro">I’m Peter Sherman, a data scientist with a PhD in Earth and Planetary Sciences from Harvard. I work at the Orlando Magic and am an Associate Researcher at Harvard.</p>
        <div class="hero-actions"><a class="button button-dark" href="#work">Explore my work {arrow('right')}</a><a class="text-link" href="/publications/">Browse research {arrow()}</a></div>
      </div>
      <figure class="hero-portrait"><div class="portrait-frame"><img src="/images/me.jpg" width="2247" height="2247" alt="Portrait of Peter Sherman" fetchpriority="high"></div>
        <figcaption><span>Peter Sherman</span><span class="portrait-mark">PhD · Harvard University</span></figcaption>
      </figure>
    </section>
    <div class="current-bar"><div class="container current-inner"><span class="eyebrow">Currently</span><p><span class="status-dot" aria-hidden="true"></span>{e(profile['current_title'])} <span class="current-at">at</span> <strong>Orlando Magic</strong></p><a href="#experience" aria-label="View my experience">{arrow('right')}</a></div></div>

    <section id="work" class="section container" aria-labelledby="work-title">
      <div class="section-heading"><p class="eyebrow"><span class="section-number">01</span> Professional work</p><h2 id="work-title">Data science &amp;<br><em>applied research.</em></h2><p class="section-lede">My background spans professional sports, environmental AI, and climate and energy research.</p></div>
      <div class="work-grid">
        <article class="work-card sport-card"><div class="work-card-top"><span class="eyebrow">01 / Sport</span><span class="work-caption">Orlando Magic</span></div>
          <div class="court" aria-hidden="true"><svg viewBox="0 0 660 330" fill="none"><rect x="30" y="20" width="600" height="290" rx="2"/><path d="M330 20v290M30 65h170v200H30m600-200H460v200h170"/><circle cx="330" cy="165" r="45"/><circle cx="200" cy="165" r="55"/><circle cx="460" cy="165" r="55"/><path d="M30 40h50a145 145 0 0 1 0 250H30m600-250h-50a145 145 0 0 0 0 250h50"/></svg></div>
          <div class="work-card-copy"><h3>Orlando Magic.</h3><p>{e(profile['current_title'])}. Previously, I worked with the Philadelphia 76ers, Los Angeles Dodgers, and Minnesota Timberwolves.</p></div>
        </article>
        <article class="work-card environment-card"><div class="work-card-top"><span class="eyebrow">02 / Applied AI</span><span class="work-caption">Previously at Ode</span></div>
          <div class="work-card-copy"><span class="field-symbol" aria-hidden="true">↗</span><h3>Environmental AI.</h3><p>At Ode Partners, I worked on climate and environmental projects using geospatial foundation models, retrieval-augmented generation, and AI research tools.</p><div class="tags"><span>Geospatial ML</span><span>RAG</span><span>Python & PyTorch</span></div></div>
        </article>
        <article class="work-card climate-card"><div><p class="eyebrow">03 / Climate & energy</p><h3>Climate &amp; energy.</h3><p>My research covers climate variability, extreme weather, and renewable energy systems. I have also worked on physical and transition risk at Climate Engine and KPMG.</p></div><a class="round-link" href="/publications/" aria-label="Explore climate and energy research">{arrow()}</a></article>
      </div>
    </section>

    <section id="research" class="research-section section" aria-labelledby="research-title"><div class="container">
      <div class="section-heading research-heading"><div><p class="eyebrow"><span class="section-number">02</span> Research</p><h2 id="research-title">Selected<br><em>publications.</em></h2></div><div class="research-heading-aside"><p>Recent work on extreme weather attribution and geospatial ML, alongside earlier research on energy systems.</p>{external(profile['scholar'], 'Google Scholar')}</div></div>
      <div class="featured-list">{selected}</div><div class="research-bottom"><p>Journal articles, conference abstracts, and preprints — clearly labeled.</p><a class="button button-outline" href="/publications/">All publications {arrow('right')}</a></div>
    </div></section>

    <section id="experience" class="section container" aria-labelledby="experience-title"><div class="experience-layout">
      <div class="section-heading experience-heading"><p class="eyebrow"><span class="section-number">03</span> Background</p><h2 id="experience-title">Experience &amp;<br><em>education.</em></h2><a class="text-link" href="/images/Peter_Sherman_CV.pdf" target="_blank" rel="noopener">Download CV {arrow()}</a><span class="cv-date">PDF · Public version</span></div>
      <div class="experience-list">{recent}<details class="earlier-experience"><summary>Earlier & additional experience <span aria-hidden="true">+</span></summary>{earlier}</details></div>
    </div>
    <div class="education-grid"><div><p class="eyebrow">Education</p><h3>Harvard University</h3><p>PhD, Earth and Planetary Sciences · 2022</p><p class="muted">Climate change and green technology</p><h3>Imperial College London</h3><p>Master’s degree in Physics · 2017</p></div><div><p class="eyebrow">Teaching</p><h3>Teaching &amp; mentorship.</h3><p>At Harvard, I taught courses on climate change and Earth science and supervised undergraduate and high-school research. My teaching was recognized by the Derek Bok Center for Teaching and Learning.</p><p class="muted">Teaching & research mentorship · 2018–2022</p></div></div>
    </section>

    <section class="press-section"><div class="container press-inner"><p class="eyebrow">Research in the news</p><div>{external('https://chinaproject.harvard.edu/news/peter-sherman', 'Harvard China Project · Researcher profile')}{external('https://www.seas.harvard.edu/news/2020/11/indias-renewable-future', 'Harvard SEAS · India’s renewable future')}{external('https://www.seas.harvard.edu/news/2020/02/opportunity-blows-offshore-wind-china-0', 'Harvard SEAS · Offshore wind in China')}</div></div></section>

    <section id="contact" class="contact-section" aria-labelledby="contact-title"><div class="container contact-inner"><div><p class="eyebrow"><span class="section-number">04</span> Get in touch</p><h2 id="contact-title">Contact<em>.</em></h2></div><div class="contact-copy"><p>For research questions or professional inquiries, you can reach me by email or LinkedIn.</p><a class="contact-email" href="mailto:{e(profile['email'])}">{e(profile['email'])}{arrow()}</a><div class="contact-links">{external(profile['linkedin'], 'LinkedIn')}{external(profile['scholar'], 'Google Scholar')}{external(profile['github'], 'GitHub')}</div></div></div></section>
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
    <section class="library-hero container"><a class="text-link library-back" href="/">← Back to home</a><p class="eyebrow">Research library / 2016–2025</p><h1>Research &amp;<br><em>publications.</em></h1><p class="library-intro">Climate dynamics, renewable energy, atmospheric science, and machine learning for the environment.</p>
      <div class="scholar-strip"><div><strong>{snapshot['citations']:,}</strong><span>Citations</span></div><div><strong>{snapshot['h_index']}</strong><span>h-index</span></div><p>Google Scholar snapshot<br>{e(snapshot['date'])}</p>{external(profile['scholar'], 'View current metrics')}</div>
    </section>
    <section class="container library-section" aria-label="Publication library"><div class="publication-controls" hidden>
      <div class="search-field"><label for="publication-search">Search publications</label><input id="publication-search" type="search" placeholder="Title, author, keyword, or year…" autocomplete="off"></div>
      <div class="topic-field"><label for="publication-topic">Research area</label><select id="publication-topic"><option value="">All areas</option>{topics}</select></div>
      <div class="type-filters" role="group" aria-label="Publication type">{''.join(f'<button type="button" data-filter="{e(t)}" aria-pressed="{str(i==0).lower()}">{e(label)}</button>' for i,(t,label) in enumerate([('', 'All work'),('Journal article','Journal articles'),('Conference abstract','Conference abstracts'),('Preprint','Preprints')]))}</div>
    </div><p class="publication-count" role="status" aria-live="polite">{len(papers)} publications</p><div id="publication-list">{''.join(publication_row(p) for p in papers)}</div><div class="no-results" hidden><h2>No matching publications.</h2><p>Try another keyword or research area.</p><button type="button" class="button button-outline" id="reset-filters">Clear filters {arrow('right')}</button></div>
    <p class="library-note">Conference abstracts and preprints are listed separately from journal articles. Earlier versions of published papers are not duplicated. {external(profile['scholar'], 'Full Google Scholar profile')}</p></section>
    '''


def redirect(target, title):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="refresh" content="0;url={e(target)}"><link rel="canonical" href="https://petersherman123.github.io{e(target)}"><title>{e(title)} | Peter Sherman</title></head><body><p><a href="{e(target)}">{e(title)}</a></p></body></html>\n'


def write(path, content):
    destination = ROOT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content)


if __name__ == "__main__":
    write("index.html", shell("Peter Sherman | Data Science, Climate & Sport", "Peter Sherman is a quantitative researcher and data scientist at the Orlando Magic, with a Harvard PhD and research in climate, energy, and applied machine learning.", home()))
    write("publications/index.html", shell("Research & Publications | Peter Sherman", "Research by Peter Sherman on climate dynamics, renewable energy, atmospheric science, geospatial machine learning, and marine microplastics.", library(), True))
    for legacy in ("projects",):
        write(f"{legacy}/index.html", redirect("/publications/", "Explore publications"))
    for legacy in ("resume",):
        write(f"{legacy}/index.html", redirect("/images/Peter_Sherman_CV.pdf", "View CV"))
    write("about/index.html", redirect("/", "About Peter Sherman"))
    write("404.html", shell("Page not found | Peter Sherman", "Return to Peter Sherman's website.", '<section class="container not-found"><p class="eyebrow">404</p><h1>Page not found<em>.</em></h1><p>This page may have moved.</p><a class="button button-dark" href="/">Return home →</a><a class="text-link" href="/publications/">Browse publications →</a></section>'))
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://petersherman123.github.io/</loc></url><url><loc>https://petersherman123.github.io/publications/</loc></url></urlset>\n')
    print(f"Built homepage, research library ({len(papers)} publications), legacy redirects, and 404 page.")
