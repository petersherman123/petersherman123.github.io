#!/usr/bin/env python3
"""Check generated pages and references, using only the Python standard library."""
import json
import runpy
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.ids = set()
        self.references = []
        self.headings = 0
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            assert a["id"] not in self.ids, f"Duplicate id in {self.path}: {a['id']}"
            self.ids.add(a["id"])
        if tag == "h1":
            self.headings += 1
        if tag in {"a", "img", "script", "link"}:
            ref = a.get("src") or a.get("href")
            if ref:
                self.references.append(ref)
        if tag == "img":
            assert "alt" in a, f"Image missing alt in {self.path}"
        if tag == "a" and a.get("target") == "_blank":
            assert "noopener" in a.get("rel", ""), f"Unsafe new-tab link in {self.path}"


def main():
    outputs = [ROOT / "index.html", ROOT / "publications/index.html", ROOT / "404.html"]
    outputs.extend(ROOT / name / "index.html" for name in ("projects", "resume", "about"))
    assets = [ROOT / 'assets/climate-stripes.svg', ROOT / 'assets/favicon.svg']
    before = {p: p.read_bytes() for p in [*outputs, *assets]}
    runpy.run_path(str(ROOT / "scripts/build.py"), run_name="__main__")
    assert all(p.read_bytes() == old for p, old in before.items()), "Generated files were stale. Commit rebuilt files."
    pages = {p: Page(p) for p in outputs}
    references = 0
    for p, page in pages.items():
        if p in outputs[:3]:
            assert page.headings == 1, f"Expected one main heading: {p}"
        for reference in page.references:
            url = urlsplit(reference)
            if url.scheme or url.netloc:
                continue
            target = ROOT / unquote(url.path).lstrip("/") if url.path.startswith("/") else p.parent / unquote(url.path)
            if not url.path:
                target = p
            if target.is_dir():
                target = target / "index.html"
            assert target.exists(), f"Broken reference in {p.name}: {reference}"
            if url.fragment and target.suffix == ".html":
                parsed = pages.get(target) or Page(target)
                assert unquote(url.fragment) in parsed.ids, f"Missing fragment: {reference}"
            references += 1
    papers = json.loads((ROOT / "data/publications.json").read_text())
    assert len({p["id"] for p in papers}) == len(papers)
    assert [p["year"] for p in papers] == sorted((p["year"] for p in papers), reverse=True)
    assert all(p["url"].startswith("https://") for p in papers)
    assert all(p["type"] in {"Journal article", "Conference abstract", "Preprint"} for p in papers)
    climate = json.loads((ROOT / 'data/climate-stripes.json').read_text())
    years = [row['year'] for row in climate['years']]
    assert years == list(range(years[0], years[-1] + 1)), 'Missing or duplicated stripe year.'
    assert all(isinstance(row['anomaly_c'], (int, float)) for row in climate['years'])
    profile = json.loads((ROOT / "data/profile.json").read_text())
    sports = {"Orlando Magic", "Philadelphia 76ers", "Los Angeles Dodgers", "Minnesota Timberwolves"}
    assert all(not x.get("description") for x in profile["experience"] if x["organization"] in sports)
    for p in [*outputs, ROOT / "scripts/build.py", ROOT / "data/profile.json"]:
        text = p.read_text().casefold()
        for restricted in ("pose data", "pose modeling", "player tracking", "player development", "forward kinematics", "inverse kinematics"):
            assert restricted not in text, f"Restricted sports detail in {p.name}"
    assert not (ROOT / "CNAME").exists(), "Unexpected inherited template domain."
    print(f"PASS: {len(outputs)} pages, {references} internal references, {len(papers)} publications, and sports-role privacy checks.")


if __name__ == "__main__":
    main()
