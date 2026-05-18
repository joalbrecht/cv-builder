"""Generate Jonas Albrecht CV PDFs — clean Rezi-inspired design with Merriweather."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, NextPageTemplate,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import Image as RLImage
import os

BASE  = os.path.dirname(os.path.abspath(__file__))
PHOTO = os.path.join(BASE, "../profile/photo-portrait.jpg")
PW, PH = A4

# ── Register Merriweather ─────────────────────────────────────────────────
FD = os.path.join(BASE, "fonts")
pdfmetrics.registerFont(TTFont("Merriweather",       os.path.join(FD, "Merriweather-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Merriweather-Bold",  os.path.join(FD, "Merriweather-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Merriweather-Italic",os.path.join(FD, "Merriweather-Italic.ttf")))
pdfmetrics.registerFontFamily("Merriweather",
    normal="Merriweather", bold="Merriweather-Bold",
    italic="Merriweather-Italic", boldItalic="Merriweather-Bold")

# ── Palette ───────────────────────────────────────────────────────────────
CHARCOAL = colors.HexColor("#2c3e50")   # headers, job titles
BODY     = colors.HexColor("#4a5568")   # body text — grey not black
TEAL     = colors.HexColor("#4a8b8c")   # section titles
BLUE     = colors.HexColor("#2a52a0")   # company names
ORANGE   = colors.HexColor("#e07b45")   # name accent only
RULE     = colors.HexColor("#d0d5d5")   # divider lines
SUBTLE   = colors.HexColor("#7a8c8c")   # dates, sub-lines
LBKG     = colors.HexColor("#f2f4f4")   # header background strip

# ── Styles ────────────────────────────────────────────────────────────────
def _s(name, **kw):
    d = dict(fontName="Merriweather", fontSize=9.5, textColor=BODY,
             leading=15, spaceAfter=0, spaceBefore=0,
             leftIndent=0, firstLineIndent=0)
    d.update(kw)
    return ParagraphStyle(name, **d)

S = {
    "sec":     _s("sec",  fontName="Merriweather-Bold", fontSize=7.8,
                  textColor=TEAL, leading=11, spaceBefore=12, spaceAfter=3),
    "job":     _s("job",  fontName="Merriweather-Bold", fontSize=10,
                  textColor=CHARCOAL, leading=14),
    "co":      _s("co",   fontName="Merriweather-Bold", fontSize=8.8,
                  textColor=BLUE, leading=12),
    "date":    _s("date", fontName="Merriweather", fontSize=8.2,
                  textColor=SUBTLE, leading=12, alignment=TA_RIGHT),
    "sub":     _s("sub",  fontName="Merriweather-Italic", fontSize=8.2,
                  textColor=SUBTLE, leading=11, spaceAfter=1),
    "bul":     _s("bul",  fontName="Merriweather", fontSize=8.8,
                  textColor=BODY, leading=13.5,
                  leftIndent=11, firstLineIndent=-9, spaceAfter=1.5),
    "body":    _s("body", fontName="Merriweather", fontSize=9,
                  textColor=BODY, leading=15, alignment=TA_JUSTIFY),
    "sk_cat":  _s("sk_cat", fontName="Merriweather-Bold", fontSize=8.8,
                  textColor=CHARCOAL, leading=13),
    "sk_val":  _s("sk_val", fontName="Merriweather", fontSize=8.8,
                  textColor=BODY, leading=13),
    "edu_deg": _s("edu_deg", fontName="Merriweather-Bold", fontSize=9,
                  textColor=CHARCOAL, leading=13),
    "edu_sch": _s("edu_sch", fontName="Merriweather", fontSize=8.5,
                  textColor=SUBTLE, leading=12),
    "small":   _s("small",   fontName="Merriweather", fontSize=8,
                  textColor=SUBTLE, leading=11),
    "proj_co": _s("proj_co", fontName="Merriweather-Bold", fontSize=8.8,
                  textColor=BLUE, leading=12),
}

# ── Helpers ───────────────────────────────────────────────────────────────

def rule():
    return HRFlowable(width="100%", thickness=0.6, color=RULE,
                      spaceBefore=2, spaceAfter=5)

def section(title):
    return [Paragraph(title.upper(), S["sec"]), rule()]

def bullet(text):
    return Paragraph(f"·  {text}", S["bul"])

def job_block(title, company, date_str, sub=None, bullets=None):
    """Max 5 bullets enforced."""
    if bullets and len(bullets) > 5:
        bullets = bullets[:5]
    header = Table(
        [[Paragraph(title, S["job"]), Paragraph(date_str, S["date"])]],
        colWidths=["*", 40*mm],
        style=TableStyle([
            ("LEFTPADDING",  (0,0), (-1,-1), 0),
            ("RIGHTPADDING", (0,0), (-1,-1), 0),
            ("TOPPADDING",   (0,0), (-1,-1), 0),
            ("BOTTOMPADDING",(0,0), (-1,-1), 1),
            ("VALIGN",       (0,0), (-1,-1), "BOTTOM"),
        ]),
    )
    rows = [header, Paragraph(company, S["co"])]
    if sub:
        rows.append(Paragraph(sub, S["sub"]))
    rows.append(Spacer(1, 3))
    if bullets:
        for b in bullets:
            rows.append(bullet(b))
    rows.append(Spacer(1, 9))
    return KeepTogether(rows)


# ══════════════════════════════════════════════════════════════════════════════
#  SHORT RESUME  — 1 page
# ══════════════════════════════════════════════════════════════════════════════

def build_short(out_path):
    LM = RM = 18*mm
    HEADER_H = 40*mm
    BM = 12*mm
    CW = PW - LM - RM

    def draw_page(canvas, doc):
        canvas.saveState()
        # Header strip
        canvas.setFillColor(LBKG)
        canvas.rect(0, PH - HEADER_H, PW, HEADER_H, fill=1, stroke=0)
        # Photo
        ps = 24*mm
        canvas.drawImage(PHOTO, LM, PH - HEADER_H + 8*mm, ps, ps,
                         preserveAspectRatio=True, mask="auto")
        # Name
        tx = LM + ps + 6*mm
        canvas.setFont("Merriweather-Bold", 22)
        canvas.setFillColor(CHARCOAL)
        canvas.drawString(tx, PH - 15*mm, "Jonas Albrecht")
        # Orange underline accent
        nw = canvas.stringWidth("Jonas Albrecht", "Merriweather-Bold", 22)
        canvas.setStrokeColor(ORANGE)
        canvas.setLineWidth(1.8)
        canvas.line(tx, PH - 16.8*mm, tx + nw, PH - 16.8*mm)
        # Tagline
        canvas.setFont("Merriweather", 8.5)
        canvas.setFillColor(SUBTLE)
        canvas.drawString(tx, PH - 22.5*mm,
                          "Software & Data Engineer  ·  Germany")
        # Contact
        canvas.setFont("Merriweather", 7.8)
        canvas.drawString(tx, PH - 28*mm,
                          "jonas@jonas-albrecht.com   ·   linkedin.com/in/albrechtjonas   ·   github.com/joalbrecht")
        # Teal rule below strip
        canvas.setStrokeColor(TEAL)
        canvas.setLineWidth(1.2)
        canvas.line(LM, PH - HEADER_H, PW - RM, PH - HEADER_H)
        canvas.restoreState()

    frame = Frame(LM, BM, CW, PH - HEADER_H - BM - 4*mm,
                  leftPadding=0, rightPadding=0, topPadding=6, bottomPadding=0)
    pt = PageTemplate(id="One", frames=[frame], onPage=draw_page)
    doc = BaseDocTemplate(out_path, pagesize=A4,
                          leftMargin=LM, rightMargin=RM,
                          topMargin=HEADER_H + 4*mm, bottomMargin=BM)
    doc.addPageTemplates([pt])

    story = []

    # Profile
    story += section("Profile")
    story.append(Paragraph(
        "Engineer with a full range of experience: from designing CRM systems and leading customer-facing "
        "business processes, to building large-scale data infrastructure and high-throughput pipelines as "
        "a technical individual contributor. Currently at Zalando SE across data platforms, DevOps, and "
        "cross-team technical projects. Early adopter of agentic AI development. "
        "Dual degree in Computer Science and Sales Engineering. Entrepreneur and builder on the side.",
        S["body"]))
    story.append(Spacer(1, 2))

    # Experience
    story += section("Experience")

    story.append(job_block(
        "Software Engineer", "Zalando SE", "Feb 2026 – Present",
        bullets=[
            "Designed and operated large-scale, high-throughput data pipelines with Airflow and Databricks, improving efficiency by up to 50%",
            "Led cross-team data foundation project for an applied science CRM initiative spanning 2 departments",
            "Engineered data platforms on AWS CloudFormation with IaC; established CI/CD pipelines increasing release velocity",
            "Early adopter of agentic AI workflows, measurably raising personal output; trained team on AI-assisted development practices",
            "On-call engineer 24/7; growing DevOps ownership across platform infrastructure",
        ]
    ))

    story.append(job_block(
        "Data Engineer", "scoutbee", "Oct 2021 – Feb 2026",
        sub="Part-time until Jun 2023, then full-time",
        bullets=[
            "Architected the company's AWS data platform (Airflow, S3, Lambda, SQS, Neo4j), scaling from initial setup to serving all departments",
            "Implemented Neo4j graph database layer modelling complex supplier networks; optimised query performance and data integrity",
            "Built self-serve analytics via Superset; published white papers from internal data analyses",
            "Administered Salesforce CRM, automated processes with Pardot, and visualised insights in Tableau",
            "Ensured data quality across all departments; connected external data sources to the central DWH",
        ]
    ))

    story.append(job_block(
        "Customer Success Engineer", "KREATIZE GmbH · Berlin", "Nov 2018 – Jun 2020",
        bullets=[
            "Technical consultant for a digital manufacturing platform, applying mechanical engineering domain knowledge to guide customers from RFQ through delivery",
            "Bridge between customer operations and technical product: diagnosed complex process issues and drove solutions",
            "Built Salesforce and Looker dashboards to surface process improvements for operations and sales leadership",
            "Presented at Hannover Messe and industry fairs to engineering-literate audiences",
        ]
    ))

    # Projects
    story += section("Projects & Ventures")
    for name, role, desc in [
        ("Sportellino", "Co-Founder & Board Member · Mar 2026–present · sportellino.it",
         "AI chatbot helping foreigners in Italy navigate bureaucracy (permits, healthcare, civil registration): leading QA and conversational development"),
        ("Pitch Wars", "Creator & Solo Developer · Mar 2026–present",
         "Built a full fantasy football manager game end-to-end: logic, backend, infra, and design, solo · pitch-wars.com"),
        ("Albrecht Indutherm GmbH", "IT Administrator (Freelance) · Feb 2025–present",
         "Sole IT responsible: Microsoft 365, web hosting, security management"),
    ]:
        story.append(KeepTogether([
            Table([[Paragraph(name, S["proj_co"]), Paragraph(role, S["date"])]],
                  colWidths=["*", 62*mm],
                  style=TableStyle([("LEFTPADDING",(0,0),(-1,-1),0),
                                    ("RIGHTPADDING",(0,0),(-1,-1),0),
                                    ("TOPPADDING",(0,0),(-1,-1),0),
                                    ("BOTTOMPADDING",(0,0),(-1,-1),1),
                                    ("VALIGN",(0,0),(-1,-1),"BOTTOM")])),
            Paragraph(desc, S["small"]),
            Spacer(1, 5),
        ]))

    # Skills
    story += section("Skills")
    for cat, val in [
        ("Engineering",       "Python · SQL · Apache Airflow · Databricks · Neo4j · CI/CD · DevOps"),
        ("Cloud & Infra",     "AWS (CloudFormation, S3, Lambda, SQS) · Infrastructure-as-Code"),
        ("Data & Analytics",  "ETL/ELT · Data Modeling · Superset · Tableau · Looker · BI"),
        ("AI & Agentic Dev",  "Agentic Workflows · Prompt Engineering · LLM Integration"),
        ("CRM & Platforms",   "Salesforce (Admin + App Builder certified) · Pardot · Microsoft 365"),
        ("Languages",         "German (native) · English (professional)"),
    ]:
        story.append(Table(
            [[Paragraph(cat, S["sk_cat"]), Paragraph(val, S["sk_val"])]],
            colWidths=[38*mm, "*"],
            style=TableStyle([("LEFTPADDING",(0,0),(-1,-1),0),
                              ("RIGHTPADDING",(0,0),(-1,-1),0),
                              ("TOPPADDING",(0,0),(-1,-1),1),
                              ("BOTTOMPADDING",(0,0),(-1,-1),2),
                              ("VALIGN",(0,0),(-1,-1),"TOP")])))

    story.append(Spacer(1, 2))

    # Education
    story += section("Education")
    for deg, school, year in [
        ("B.Sc. Computer Science", "Humboldt-Universität zu Berlin", "2023"),
        ("B.Sc. Sales Engineering & Product Management", "Ruhr University Bochum", "2018"),
    ]:
        story.append(Table(
            [[Paragraph(deg, S["edu_deg"]), Paragraph(year, S["date"])],
             [Paragraph(school, S["edu_sch"]), ""]],
            colWidths=["*", 20*mm],
            style=TableStyle([("LEFTPADDING",(0,0),(-1,-1),0),
                              ("RIGHTPADDING",(0,0),(-1,-1),0),
                              ("TOPPADDING",(0,0),(-1,-1),0),
                              ("BOTTOMPADDING",(0,0),(-1,-1),1)])))
        story.append(Spacer(1, 4))

    doc.build(story)
    print(f"✓ Short resume: {out_path}")


# ══════════════════════════════════════════════════════════════════════════════
#  FULL CV  — multi-page
# ══════════════════════════════════════════════════════════════════════════════

def build_full(out_path):
    LM = RM = 18*mm
    HEADER_H  = 42*mm
    BM = 14*mm
    CW = PW - LM - RM

    def draw_first(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(LBKG)
        canvas.rect(0, PH - HEADER_H, PW, HEADER_H, fill=1, stroke=0)
        ps = 26*mm
        canvas.drawImage(PHOTO, LM, PH - HEADER_H + 8*mm, ps, ps,
                         preserveAspectRatio=True, mask="auto")
        tx = LM + ps + 7*mm
        canvas.setFont("Merriweather-Bold", 23)
        canvas.setFillColor(CHARCOAL)
        canvas.drawString(tx, PH - 15*mm, "Jonas Albrecht")
        nw = canvas.stringWidth("Jonas Albrecht", "Merriweather-Bold", 23)
        canvas.setStrokeColor(ORANGE)
        canvas.setLineWidth(1.8)
        canvas.line(tx, PH - 17*mm, tx + nw, PH - 17*mm)
        canvas.setFont("Merriweather", 8.8)
        canvas.setFillColor(SUBTLE)
        canvas.drawString(tx, PH - 23*mm,
                          "Software & Data Engineer  ·  Germany  ·  June 2026")
        canvas.setFont("Merriweather", 8)
        canvas.drawString(tx, PH - 29.5*mm,
                          "jonas@jonas-albrecht.com   ·   linkedin.com/in/albrechtjonas   ·   github.com/joalbrecht")
        canvas.setStrokeColor(TEAL)
        canvas.setLineWidth(1.2)
        canvas.line(LM, PH - HEADER_H, PW - RM, PH - HEADER_H)
        canvas.restoreState()

    def draw_later(canvas, doc):
        canvas.saveState()
        canvas.setFont("Merriweather", 7.5)
        canvas.setFillColor(SUBTLE)
        canvas.drawCentredString(PW/2, 8*mm,
                                 f"Jonas Albrecht  ·  jonas@jonas-albrecht.com  ·  Page {doc.page}")
        canvas.restoreState()

    f_first = Frame(LM, BM, CW, PH - HEADER_H - BM - 4*mm,
                    leftPadding=0, rightPadding=0, topPadding=6, bottomPadding=0)
    f_later = Frame(LM, BM + 6*mm, CW, PH - 16*mm - BM - 6*mm,
                    leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    pt_first = PageTemplate(id="First", frames=[f_first], onPage=draw_first)
    pt_later = PageTemplate(id="Later", frames=[f_later], onPage=draw_later)

    doc = BaseDocTemplate(out_path, pagesize=A4,
                          leftMargin=LM, rightMargin=RM,
                          topMargin=HEADER_H + 4*mm, bottomMargin=BM)
    doc.addPageTemplates([pt_first, pt_later])

    story = [NextPageTemplate("Later")]

    # Profile
    story += section("Profile")
    story.append(Paragraph(
        "Engineer with a full range of experience: from designing CRM systems and leading "
        "customer-facing business processes, to building large-scale data infrastructure and "
        "high-throughput pipelines as a technical individual contributor. Currently at Zalando SE "
        "spanning data platform engineering, DevOps, and cross-team technical leadership. "
        "Early adopter of agentic AI development. Dual degree in Computer Science (HU Berlin) "
        "and Sales Engineering &amp; Product Management (RUB Bochum). "
        "Active entrepreneur and independent builder alongside professional work.",
        S["body"]))
    story.append(Spacer(1, 4))

    # Experience
    story += section("Professional Experience")

    story.append(job_block(
        "Software Engineer", "Zalando SE · Berlin/Remote", "Feb 2026 – Present",
        bullets=[
            "Designed, built, and operated large-scale, high-throughput data pipelines using Apache Airflow and Databricks, improving efficiency by up to 50% at scale",
            "Led cross-team data foundation project for an applied science CRM initiative spanning 2 departments and multiple teams",
            "Engineered secure data platforms on AWS CloudFormation with IaC; established end-to-end CI/CD pipelines increasing release reliability and velocity",
            "Early adopter of agentic AI workflows, significantly raising personal output; trained team on AI-assisted development, reducing worktime while maintaining output quality",
            "On-call engineer 24/7; onboarded teams onto Databricks Unity Catalog; delivered internal presentations at conferences and knowledge sharing forums",
        ]
    ))

    story.append(job_block(
        "Data Engineer", "scoutbee · Remote", "Oct 2021 – Feb 2026",
        sub="Part-time until Jun 2023, then full-time",
        bullets=[
            "Architected and maintained the company's core AWS data platform (Airflow, S3, Lambda, SQS), growing from initial data source connections to serving all departments at scale",
            "Implemented and optimised Neo4j graph databases representing complex supplier relationship networks; ensured data quality across all teams",
            "Built self-serve analytics stack via Apache Superset; connected external data sources to the DWH; published internal white papers from data analyses",
            "Administered Salesforce CRM, automated business processes with Pardot, and built data visualisations in Tableau to support commercial teams",
            "Established robust monitoring and alerting systems; continuously optimised pipelines for efficiency and cost-effectiveness",
        ]
    ))

    story.append(job_block(
        "Customer Insights & Analytics Associate", "scoutbee", "Oct 2020 – Dec 2021",
        bullets=[
            "Administered and configured Salesforce CRM; managed data quality across all CRM systems",
            "Automated business processes with Salesforce and Pardot; built data visualisations with Tableau",
            "Bridged commercial operations and the emerging data engineering function",
        ]
    ))

    story.append(job_block(
        "Customer Insights & Analytics (Working Student)", "scoutbee", "Jun 2020 – Sep 2020",
        bullets=[
            "First role at scoutbee; supported the customer insights and analytics team",
        ]
    ))

    story.append(job_block(
        "Customer Success Engineer", "KREATIZE GmbH · Berlin", "Nov 2018 – Jun 2020",
        bullets=[
            "Technical consultant for a digital manufacturing platform, applying mechanical engineering domain expertise to advise customers from RFQ through delivery",
            "Bridge between customer operations and technical product: diagnosed complex manufacturing process issues and drove solutions across teams",
            "Built data visualisations in Salesforce and Looker to surface process improvements for operations and sales leadership",
            "Presented at Hannover Messe and industry fairs to engineering-literate audiences",
        ]
    ))

    story.append(job_block(
        "Research Assistant", "Ruhr-Universität Bochum · Chair of Hydraulic Fluid Machines (HSM)", "Jan 2018 – Jan 2019",
        bullets=[
            "Evaluated computational fluid dynamics (CFD) data; developed visualisations with MATLAB",
            "Implemented grid designs in ANSYS ICEM; ran simulations with in-house software 'solver3D' and 'FLOAT'",
        ]
    ))

    story.append(job_block(
        "Working Student &amp; Intern, Key Account Sales", "innogy SE · Dortmund", "Sep 2017 – Dec 2017",
        bullets=[
            "Consulted customers on product decisions and contract design; supported customer acquisition in cooperation with product management",
        ]
    ))

    story.append(job_block(
        "Student Assistant", "Ruhr-Universität Bochum · Chair of Energy Systems (LEAT)", "Sep 2016 – Sep 2017",
        bullets=[
            "Budget planning and invoice control; collaborated with PhD researchers on department lab projects",
        ]
    ))

    story.append(job_block(
        "Intern", "Oschatz GmbH · Essen", "Sep 2015 – Oct 2015",
        bullets=[
            "Technical specification of industrial boilers; heat exchange and water circulation calculations for plant projects in Portugal and Turkey",
        ]
    ))

    # Entrepreneurship
    story += section("Entrepreneurship & Side Projects")

    story.append(job_block(
        "Co-Founder & Board Member", "Sportellino · sportellino.it", "Mar 2026 – Present",
        bullets=[
            "Co-founded an AI-powered chatbot helping foreigners in Italy navigate bureaucracy: residence permits, healthcare, civil registration",
            "Responsible for Quality Control and Conversational Analytics",
            "Leading chatbot development; product is free, anonymous, and available in multiple languages",
        ]
    ))

    story.append(job_block(
        "Creator & Solo Developer", "Pitch Wars · pitch-wars.com", "Mar 2026 – Present",
        bullets=[
            "Independently built and launched a full online fantasy football manager game end-to-end",
            "Sole developer and designer: game logic, backend, infrastructure, website, and creative assets",
        ]
    ))

    # Freelance
    story += section("Freelance & Consulting")

    story.append(job_block(
        "IT Administrator", "Albrecht Indutherm GmbH · albrecht-indutherm.com", "Feb 2025 – Present",
        bullets=[
            "Sole IT responsible: Microsoft 365 administration, website deployment and hosting, security management",
        ]
    ))

    # Education
    story += section("Education")
    for deg, school, year in [
        ("B.Sc. Computer Science (Informatik)", "Humboldt-Universität zu Berlin", "2023"),
        ("B.Sc. Sales Engineering & Product Management", "Ruhr University Bochum", "2018"),
    ]:
        story.append(Table(
            [[Paragraph(deg, S["edu_deg"]), Paragraph(year, S["date"])],
             [Paragraph(school, S["edu_sch"]), ""]],
            colWidths=["*", 22*mm],
            style=TableStyle([("LEFTPADDING",(0,0),(-1,-1),0),
                              ("RIGHTPADDING",(0,0),(-1,-1),0),
                              ("TOPPADDING",(0,0),(-1,-1),0),
                              ("BOTTOMPADDING",(0,0),(-1,-1),1)])))
        story.append(Spacer(1, 5))

    # Certifications
    story += section("Certifications")
    for cert, org, year in [
        ("CybSafe Certification in Security Awareness", "CybSafe", "2023"),
        ("Certified Platform App Builder (SP21)", "Salesforce", "2021"),
        ("Salesforce Certified Administrator (WI20)", "Salesforce", "2020"),
    ]:
        story.append(Table(
            [[Paragraph(f"<b>{cert}</b>", S["sk_val"]),
              Paragraph(f"{org} · {year}", S["date"])]],
            colWidths=["*", 34*mm],
            style=TableStyle([("LEFTPADDING",(0,0),(-1,-1),0),
                              ("RIGHTPADDING",(0,0),(-1,-1),0),
                              ("TOPPADDING",(0,0),(-1,-1),0),
                              ("BOTTOMPADDING",(0,0),(-1,-1),3),
                              ("VALIGN",(0,0),(-1,-1),"TOP")])))

    # Skills
    story += section("Skills")
    for cat, val in [
        ("Engineering & Pipelines",  "Python · SQL · Apache Airflow · Databricks · Databricks Unity Catalog · ETL/ELT · Data Modeling · Data Quality · Neo4j"),
        ("Cloud & Infrastructure",   "AWS (CloudFormation, S3, Lambda, SQS) · Infrastructure-as-Code · CI/CD · DevOps · Monitoring & Alerting"),
        ("AI & Agentic Development", "Agentic Workflows · Prompt Engineering · LLM Integration · AI-assisted Development"),
        ("Data & Analytics",         "Apache Superset · Tableau · Looker · Business Intelligence · Data-driven Decision Making"),
        ("CRM & Platforms",          "Salesforce (Admin + App Builder certified) · Pardot"),
        ("IT & Administration",      "Microsoft 365 · Web Hosting · Security Management"),
        ("Product & Design",         "Full-stack product development · Game design · Chatbot development · Website design"),
        ("Soft Skills",              "Cross-functional collaboration · Technical documentation · On-call operations · Public speaking"),
        ("Languages",                "German (native) · English (professional)"),
    ]:
        story.append(Table(
            [[Paragraph(cat, S["sk_cat"]), Paragraph(val, S["sk_val"])]],
            colWidths=[50*mm, "*"],
            style=TableStyle([("LEFTPADDING",(0,0),(-1,-1),0),
                              ("RIGHTPADDING",(0,0),(-1,-1),0),
                              ("TOPPADDING",(0,0),(-1,-1),1),
                              ("BOTTOMPADDING",(0,0),(-1,-1),2),
                              ("VALIGN",(0,0),(-1,-1),"TOP")])))
        story.append(HRFlowable(width="100%", thickness=0.3,
                                color=colors.HexColor("#e8ecec"),
                                spaceBefore=1, spaceAfter=1))

    doc.build(story)
    print(f"✓ Full CV: {out_path}")


if __name__ == "__main__":
    build_short(os.path.join(BASE, "short/resume-jun2026.pdf"))
    build_full(os.path.join(BASE, "full/cv-jun2026.pdf"))
