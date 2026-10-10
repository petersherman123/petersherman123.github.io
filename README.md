# Peter Sherman's website

Personal website at https://petersherman123.github.io/. A static site with no client-side framework, external fonts, analytics, or build dependencies. The HTML is committed so GitHub Pages can serve the repository root directly.

The site uses a dark charcoal theme with muted blue links. The homepage lists roles, selected publications, experience, education, and contact information. The publications page includes search and topic/type filters. Keep headings factual and avoid taglines or descriptions of confidential work.

Author lists highlight Peter Sherman. Publication-type counts reflect the current search and research area, so readers can see the available results before switching types. The contact section includes a copy-email button with an announced success message and manual-selection fallback when clipboard access is unavailable.

## Edit and preview

- `data/profile.json`: public role titles, dates, contact links, and dated Scholar metrics.
- `data/publications.json`: publication metadata, links, summaries, and homepage selections.
- `scripts/build.py`: page templates and compatibility redirects.
- `assets/site.css` and `assets/site.js`: layout, mobile navigation, and publication filters.
- `scripts/build_public_cv.py`: a separate public CV generated from approved site content. Requires ReportLab.

After editing content or templates:

```sh
python3 scripts/build.py
python3 scripts/check_site.py
python3 -m http.server 8765 --bind 127.0.0.1
```

Open http://127.0.0.1:8765/. Styles and browser JavaScript can be edited directly; reload to see changes.

The production site is published from the root of `master`. Changes on a feature branch do not publish until merged. Historical `/projects`, `/resume`, and `/about` URLs have static redirects; the custom 404 page also redirects mixed-case variants such as `/Projects` and `/Resume` with JavaScript.

## Content sources and privacy

Content was reconciled on October 10, 2026 against the June 2026 CV, LinkedIn, Google Scholar, and publisher records. LinkedIn provides the more recent employment titles and dates. Journal publication years take precedence over preprint dates; conference abstracts and preprints are labeled. Scholar counts are a dated snapshot, with a link to live metrics.

Sports roles include only public organizations, titles, and dates. Do not add descriptions of work at the Orlando Magic, or copy a private CV into this repository. The downloadable CV is a separate public summary; the original CV in Documents is not a site asset.

## Verification

`scripts/check_site.py` checks generated pages, internal links and fragments, publication metadata, and the sports-role content restriction. Browser checks cover mobile navigation, publication search, combined filters, empty states, and the CV download. The site content and navigation remain available without JavaScript; filtering, the small-screen menu toggle, and the copy-email control use it.

Run `node scripts/check_interactions.cjs` to check filter counts, combined filters, reset behavior, and email-copy success and failure in a DOM harness. This does not replace browser layout or real clipboard checks. Without JavaScript, the email link and complete publication list remain available.
