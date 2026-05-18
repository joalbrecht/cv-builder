---
name: tailor-resume
description: Use when tailoring Jonas's resume to a specific job description. Reads master-timeline, decides which roles to include/omit/merge based on the role type, rewrites bullets to match, generates a tailored PDF into resumes/tailored/.
---

# Resume Tailoring Skill

Produces a tailored 1-page resume for a specific job by selectively drawing from the master timeline.
Core principle: **selective omission with timeline integrity** — never fabricate or alter dates, but
curate roles and reframe bullets to maximise relevance.

---

## When to Use

Trigger when the user provides:
- A job description (text or URL)
- A company name + role title
- "Tailor my CV for X"

---

## Step 0 — Parse the Job Description

Extract and record:

```
ROLE_TYPE:       [Senior DE / Platform Engineer / EM / Startup / Full-stack / Other]
COMPANY:         [name]
TITLE:           [exact job title]
KEY_SKILLS:      [top 6-8 skills/tools explicitly mentioned]
SENIORITY:       [IC / Lead / Manager]
DOMAIN:          [data / infra / product / fullstack / ML / other]
RED_FLAGS:       [anything Jonas clearly lacks — be honest]
TONE:            [startup-casual / enterprise-formal / research]
```

Present this parse to the user and ask: *"Does this look right? Anything to add?"*
Wait for confirmation before proceeding.

---

## Step 1 — Role Inclusion Strategy

Based on ROLE_TYPE, apply the following omission rules.
**Never alter dates. Never invent experience.**

### Senior Data Engineer / Platform Engineer
**Include:**
- Zalando SE (full, all bullets)
- scoutbee Data Engineer Oct 2021–Feb 2026 (merged, full)
- scoutbee Customer Insights Associate (1–2 bullets, show CRM/data quality breadth)
- KREATIZE (2 bullets max — keep if domain knowledge is relevant, else drop)

**Drop:** Working student, research assistant, innogy, Oschatz

**Gap strategy:** scoutbee spans Jun 2020–Feb 2026. No gap visible.

---

### Engineering Manager / Tech Lead
**Include:**
- Zalando SE (emphasise: led cross-team project, trained team, on-call, presentations)
- scoutbee Data Engineer (merged — show scale and ownership growth)
- KREATIZE (keep — shows customer/business fluency that distinguishes from pure ICs)
- scoutbee Customer Insights Associate (keep — shows CRM/commercial grounding)

**Drop:** Working student, research assistant, innogy, Oschatz

**Reframe summary:** Lead with breadth — "full-range engineer with commercial and technical depth"

---

### Startup / Founding Engineer
**Include:**
- Zalando SE
- scoutbee Data Engineer (merged)
- Sportellino + Pitch Wars (move to top of experience or dedicate a section directly after Zalando)
- KREATIZE (2 bullets — customer empathy angle)

**Drop:** Early internships, research assistant

**Reframe summary:** Lead with builder instinct — Pitch Wars, Sportellino, solo ownership

---

### Full-stack / Product Engineer
**Include:**
- Zalando SE
- scoutbee Data Engineer (merged, emphasise Superset, integrations, self-serve)
- Pitch Wars (full bullets — end-to-end product build)
- Sportellino (chatbot/product angle)
- Albrecht Indutherm (brief — shows full ownership)

**Drop:** Research assistant, innogy, Oschatz

---

### Default (unknown / general)
Include all roles from Jun 2020 onwards. Drop pre-2018 internships.
Use "Selected Experience" as section header.

---

## Step 2 — Bullet Rewriting

For each included role, rewrite bullets to:
1. **Front-load the keyword** from the JD's KEY_SKILLS where truthful
2. **Use the JD's vocabulary** — if they say "data mesh" use it if applicable, don't invent
3. **Max 5 bullets per role** — always
4. **Lead bullets with impact, not task** — "Improved X by Y" beats "Responsible for X"
5. **Keep 1 bullet per role that shows range** — a business/commercial bullet in a technical role, or vice versa

Show the rewritten bullets to the user before generating:
```
ROLE: [title] at [company]
KEPT: [bullet 1]
REWRITTEN: [bullet 2 — original → new]
DROPPED: [bullet 3 — reason: not relevant to JD]
```

Ask: *"Any changes before I generate the PDF?"*

---

## Step 3 — Summary Rewrite

Rewrite the Profile paragraph (3–4 sentences max) to:
- Open with the framing most relevant to the role type (technical depth / breadth / builder)
- Mention 2–3 of the JD's KEY_SKILLS naturally
- Do NOT say "intentional arc" or explain career transitions
- End with one line that signals fit for the specific role

---

## Step 4 — Generate PDF

1. Create output path: `resumes/tailored/{company}-{role-slug}-{YYYY-MM}.md` (markdown version)
2. Run: `~/.pyenv/versions/3.10.6/bin/python3 resumes/generate_tailored.py "{company}" "{title}" "{output_slug}"`
   — this script reads the tailored markdown and produces the PDF
3. Open the PDF for user review

If `generate_tailored.py` doesn't exist yet, produce the tailored markdown file and tell the user
to run the short PDF generator manually: `python3 resumes/generate_pdf.py`

---

## Step 5 — Gap Check

Before handing off, verify:
- No date gap larger than 3 months appears in the included roles
- If a gap exists, apply one of:
  - Extend adjacent role dates (only if truthful — ask user first)
  - Add "Additional earlier experience available on request" footnote
  - Use "Selected Experience" header to signal intentional curation

---

## Step 6 — Library Update (optional)

If the user approves the tailored resume, ask:
*"Save this as a reusable template for [ROLE_TYPE] roles? (Y/N)"*

If yes, save to `resumes/tailored/templates/{role-type}-template.md`

---

## Design Rules (always apply)

- Font: Merriweather
- Text: grey #4a5568, never black
- Company names: blue #2a52a0
- Section headers: teal #4a8b8c, uppercase, thin rule below
- Orange accent: name only
- Bullets: dots (·), max 5 per role
- No "this was intentional" framing anywhere
- 1-page output for tailored resumes

---

## Supporting Files

- `profile/master-timeline.md` — source of truth, all experience
- `resumes/generate_pdf.py` — PDF generator (short + full)
- `resumes/tailored/` — output directory
