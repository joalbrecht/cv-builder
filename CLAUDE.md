# CV Builder — Jonas Albrecht

AI-powered resume generation system. The flow: **master timeline → tailored CV output**.

## How It Works

```
profile/master-timeline.md   ← single source of truth (all experience, never cut)
         ↓
  resume-tailoring skill     ← reads master-timeline as library
         ↓
  resumes/                   ← generated outputs
    short/                   # 1-page resume
    full/                    # extensive / academic-style CV
    tailored/                # job-specific tailored resumes
```

## Usage

| Goal | How |
|------|-----|
| Tailor resume to a job | Provide job description or URL → skill auto-runs |
| Generate 1-page short CV | Ask: "generate a short 1-page resume from my timeline" |
| Generate extensive CV | Ask: "generate my full CV" |
| Update experience | Edit `profile/master-timeline.md` directly |

The skill reads `profile/master-timeline.md` as its resume library source.

## Repository Structure

```
profile/
  master-timeline.md    # Complete experience history — source of truth
resumes/
  short/                # 1-page resume outputs
  full/                 # Extensive CV outputs
  tailored/             # Job-tailored resume outputs (gitignored)
docs/                   # Research notes, job descriptions
.claude/
  skills/
    resume-tailoring/   # AI tailoring skill (varunr89/resume-tailoring-skill)
```

## Personal Info

- **Name:** Jonas Albrecht
- **Email:** jonas@jonas-albrecht.com
- **LinkedIn:** linkedin.com/in/albrechtjonas
- **GitHub:** github.com/joalbrecht
- **Location:** Germany

## Notes for AI

- Master timeline is at `profile/master-timeline.md` — point skill library path here
- `master-timeline.md` contains ALL experience including side projects and freelance work
- Never trim or summarize `master-timeline.md` — it is the raw input, not a resume
- Current primary role: Software Engineer at Zalando SE (Feb 2026–present)
- Parallel activities: Sportellino co-founder, Pitch Wars creator, IT admin for Albrecht Indutherm GmbH
- Background spans: mechanical engineering → sales engineering → data engineering → software engineering
- Two BSc degrees: Computer Science (HU Berlin, 2023) + Sales Engineering & Product Mgmt (RUB, 2018)
