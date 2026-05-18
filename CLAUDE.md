# CV Builder — Jonas Albrecht

This repository contains Jonas's resume library and AI-powered resume tailoring setup.

## Purpose

Generate tailored, job-specific resumes using the `resume-tailoring` skill. Resumes are stored in `resumes/` as markdown files and used as the source library.

## Repository Structure

```
resumes/          # Markdown resume library (source of truth for experience)
  base-resume.md  # Full master resume — all experience, never cut
  tailored/       # Job-specific tailored resumes (generated output)
docs/             # Supporting research, notes
.claude/
  skills/
    resume-tailoring/  # AI resume tailoring skill
```

## How to Use

To tailor a resume for a job:
1. Provide the job description (text or URL)
2. Run `/resume-tailoring` (or just describe the job — the skill auto-triggers)
3. Follow the guided workflow: research → template → discovery → generate

The skill reads from `resumes/` as its library. Always keep `base-resume.md` complete.

## Personal Info

- **Name:** Jonas Albrecht
- **Email:** jonas.albrecht@rub.de
- **LinkedIn:** linkedin.com/in/albrechtjonas
- **GitHub:** github.com/joalbrecht
- **Location:** Germany

## Notes for AI

- Resume library is in `resumes/` — default skill path
- `base-resume.md` is the master source with ALL experience; never trim it
- Tailored outputs go in `resumes/tailored/`
- Jonas has a dual background: mechanical/sales engineering + computer science + data engineering
- Current role at scoutbee needs updated dates (resume is from Dec 2024; today is May 2026)
