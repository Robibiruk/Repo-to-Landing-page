# 01 — Repo → Landing Page

**Pitch:** Paste any GitHub repo URL → get a beautiful marketing landing page generated from the README + code → deploy free in one click.

**Star loop:** Universal input (every repo is a candidate) → instant wow (your side project suddenly looks like a real product) → shareable deployed link. Low competition, tight loop.

**Target user:** Every open-source maintainer whose project deserves a homepage and doesn't have one.

---

## Tech stack

- **Frontend:** React + Vite + TypeScript (matches your PulseWatch stack), Tailwind CSS, shadcn/ui
- **Backend:** FastAPI
- **GitHub data:** Octokit (REST) — repo metadata, README, languages, stars, contributors
- **LLM:** Claude via OpenRouter — hero copy, tagline, feature extraction, section structure
- **Output:** Plain generated HTML + compiled CSS (no framework needed in the output site — keeps it fast and deployable anywhere)
- **Preview:** Sandboxed iframe live preview
- **Deploy:** Free tiers — Netlify Drop API / Vercel / Surge (one-click)
- **Storage:** Stateless for MVP (no DB) + small SQLite cache for rate-limit protection

---

## MVP features

1. Paste repo URL → fetch README + metadata (languages, stars, license, contributors)
2. LLM generates: hero section, tagline, 3-4 feature cards, install/usage snippet, footer, color palette derived from repo language/logo
3. Live preview in a sandboxed iframe, regenerable section-by-section
4. One-click deploy to a free host → shareable link
5. Download as a static zip (works offline / self-host)

## Cut for MVP

- Drag-and-drop editing canvas (later)
- Multi-page sites, custom domains, analytics (later)
- Push-back-to-GitHub (nice, but deploy-first is the demo)

---

## Why you win

Existing tools either charge or output generic templates. Yours is instant, free, and the output gets *shared* — that's the whole loop. The deployed link is the shareable artifact.
