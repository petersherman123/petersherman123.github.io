#!/usr/bin/env python3
"""Build a public CV without sports-work descriptions. Requires ReportLab."""
import json
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
profile = json.loads((ROOT / "data/profile.json").read_text())
papers = json.loads((ROOT / "data/publications.json").read_text())
INK = colors.HexColor("#203534")
MUTED = colors.HexColor("#5e6b66")
RUST = colors.HexColor("#a94b32")
styles = getSampleStyleSheet()
styles.add(ParagraphStyle("Name", fontName="Times-Roman", fontSize=30, leading=34, textColor=INK, spaceAfter=8))
styles.add(ParagraphStyle("Section", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=RUST, spaceBefore=18, spaceAfter=10))
styles.add(ParagraphStyle("Role", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=INK, spaceAfter=3))
styles.add(ParagraphStyle("Copy", fontName="Helvetica", fontSize=9, leading=13, textColor=INK, spaceAfter=4))
styles.add(ParagraphStyle("SmallCopy", fontName="Helvetica", fontSize=8, leading=11, textColor=MUTED, spaceAfter=3))
styles.add(ParagraphStyle("Paper", fontName="Helvetica", fontSize=9, leading=12, textColor=INK, spaceAfter=3))


def safe(text):
    return escape(str(text).replace("—", "-").replace("–", "-").replace("’", "'").replace("‘", "'").replace("…", "..."))


def para(text, style="Copy"):
    return Paragraph(text, styles[style])


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#d6dbd2"))
    canvas.line(48, 41, 564, 41)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(48, 28, "Peter Sherman | Public CV | October 2026")
    canvas.drawRightString(564, 28, str(doc.page))
    canvas.restoreState()


def build():
    # Fail closed if someone adds sports-work descriptions to the shared data.
    sports = {"Orlando Magic", "Philadelphia 76ers", "Los Angeles Dodgers", "Minnesota Timberwolves"}
    assert all(not x.get("description") for x in profile["experience"] if x["organization"] in sports)
    story = [para("Peter J. Sherman", "Name"),
             para(safe(profile["current_title"]) + " | Orlando Magic", "Copy"),
             para('<link href="mailto:petersherman@g.harvard.edu">petersherman@g.harvard.edu</link> | <link href="https://petersherman123.github.io/">petersherman123.github.io</link>', "SmallCopy"),
             para("EXPERIENCE", "Section")]
    for item in profile["experience"]:
        block = [para(safe(item["organization"]) + " - " + safe(item["dates"]), "Role"), para(safe(item["role"]), "Copy")]
        # Include descriptions for the three non-sports industry roles only.
        if item["organization"] in {"Ode Partners", "Climate Engine", "KPMG"}:
            block.append(para(safe(item["description"]), "SmallCopy"))
        block.append(Spacer(1, 5))
        story.append(KeepTogether(block))
    story.extend([para("EDUCATION", "Section"),
                  para("Harvard University - PhD, Earth and Planetary Sciences, 2022", "Role"),
                  para("Imperial College London - Master's degree in Physics, 2017", "Role"),
                  para("TEACHING AND MENTORSHIP", "Section"),
                  para("Harvard teaching and research mentorship, 2018-2022. Courses in climate change and Earth science; supervision of undergraduate and high-school research. Teaching recognized by the Derek Bok Center for Teaching and Learning.", "SmallCopy"),
                  PageBreak(), para("Research and skills", "Name"),
                  para("SELECTED PUBLICATIONS", "Section")])
    selected_ids = {"attribution-2025", "mangroves-2025", "offshore-grid-2023", "cooling-2022", "india-decarbonization-2022", "hydrogen-2021", "monsoon-2021", "wind-projections-2021", "india-renewables-2020", "greenland-2020", "offshore-wind-2020", "microplastics-2016"}
    for p in papers:
        if p["id"] not in selected_ids:
            continue
        block = [para(f'<b>{p["year"]}</b> | <link href="{escape(p["url"], quote=True)}">{safe(p["title"])}</link>', "Paper"),
                 para(safe(p["authors"]) + ". " + safe(p["venue"]) + "." + (" Conference abstract." if p["type"] == "Conference abstract" else ""), "SmallCopy"), Spacer(1, 8)]
        story.append(KeepTogether(block))
    story.extend([para('<link href="https://petersherman123.github.io/publications/">Full publication list: petersherman123.github.io/publications/</link>', "SmallCopy"),
                  para("COMPUTING AND MODELS", "Section"),
                  para("Python, PyTorch, SQL, R, Linux, AWS, GIS, Google Earth Engine, MLflow, Airflow, and Streamlit. Climate-model experience includes CESM, GEOS-Chem, and UKESM.", "SmallCopy")])
    doc = SimpleDocTemplate(str(ROOT / "images/Peter_Sherman_CV.pdf"), pagesize=(612, 792), rightMargin=48, leftMargin=48, topMargin=42, bottomMargin=54,
                            title="Peter Sherman - Public CV", author="Peter Sherman", subject="Public professional background and selected research")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("Built public CV from site content; sports roles contain titles and dates only.")


if __name__ == "__main__":
    build()
