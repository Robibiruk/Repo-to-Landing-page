<p align="center">
  <img src="frontend/public/favicon/icons8-web-windows-11-color-96.png" alt="RepoPages Logo" width="80" style="border-radius:16px" />
</p>

<h1 align="center">RepoPages</h1>

<p align="center">
  <strong>Turn any GitHub repository into a beautiful product website.</strong><br/>
  <em>Paste a URL. Get a branded landing page. Deploy in seconds.</em>
</p>

<p align="center">
  <a href="https://repo-to-landing-page.vercel.app/">
    <img src="https://img.shields.io/badge/Try%20It-Live-blueviolet?style=for-the-badge" alt="Try Live" />
  </a>
  <a href="https://repo-to-landing-page-api.onrender.com/api/health">
    <img src="https://img.shields.io/badge/API-Healthy-brightgreen?style=for-the-badge" alt="API Status" />
  </a>
  <a href="https://github.com/Robibiruk/Repo-to-Landing-page/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-gray?style=for-the-badge" alt="MIT License" />
  </a>
</p>

<p align="center">
  <a href="https://x.com/ynwrobii">
    <img src="https://img.shields.io/badge/Follow-%40ynwrobii-1DA1F2?style=flat-square&logo=x" alt="X/Twitter" />
  </a>
  <a href="https://www.linkedin.com/in/robel-biruk-5923101b5/">
    <img src="https://img.shields.io/badge/Connect-Robel%20Biruk-0A66C2?style=flat-square&logo=linkedin" alt="LinkedIn" />
  </a>
  <a href="https://github.com/Robibiruk">
    <img src="https://img.shields.io/badge/View-GitHub-181717?style=flat-square&logo=github" alt="GitHub" />
  </a>
</p>

---

## The Problem

Most GitHub repositories look like this:

```
README.md
├── Walls of text          ← no one reads
├── No screenshots         ← no visual context
├── No branding            ← default GitHub styling
├── No demo                ← impossible to understand
└── No CTA                 ← where do I even start?
```

**Developers spend months building projects and five minutes presenting them.**

Investors, recruiters, hackathon judges, and users judge the presentation *before* the code.

---

## The Solution

```
Paste Repo URL → AI Analyzes → Brand Generated → Landing Page → Deploy → Share
```

In **20 seconds**, you get:

```
┌─────────────────────────────────────────────┐
│  ✦  YourProject                              │
│                                              │
│  Hero headline that hooks                    │
│  Subheadline that explains                   │
│  [Get Started]                               │
│                                              │
│  ★ Stars  ⑂ Forks  ✓ MIT  v1.2.0           │
├─────────────────────────────────────────────┤
│  🧠 Feature 1    🎨 Feature 2   🚀 Feature 3│
│  Real copy      Real copy      Real copy     │
├─────────────────────────────────────────────┤
│  $ npm install your-project                  │
│  $ your-project start                        │
├─────────────────────────────────────────────┤
│  Footer · License · Docs · GitHub            │
│           ⚡ Built with RepoPages             │
└─────────────────────────────────────────────┘
```

No coding. No design. No prompt writing.

---

## How It Works

```
  Paste GitHub URL
         ↓
  ┌──────────────────┐
  │  📖 ANALYZE      │  README, package.json, topics,
  │                  │  languages, contributors
  └────────┬─────────┘
           ↓
  ┌──────────────────┐
  │  🤖 GENERATE     │  AI writes brand, hero, features,
  │                  │  SEO, and install instructions
  └────────┬─────────┘
           ↓
  ┌──────────────────┐
  │  🎯 CRITIC       │  Scores: truthfulness / specificity
  │                  │  Catches generic filler instantly
  └────────┬─────────┘
           ↓
  ┌──────────────────┐
  │  🎨 DESIGN       │  Theme + color palette
  │                  │  Matches language & vibe
  └────────┬─────────┘
           ↓
  ┌──────────────────┐
  │  📦 DEPLOY       │  Preview → ZIP → One-click
  │                  │  Shareable link in seconds
  └──────────────────┘
```

---

## Features

<table>
  <tr>
    <td width="50%" valign="top">

### 🧠 Repository Intelligence

Reads your **README**, `package.json`, `Cargo.toml`, `pyproject.toml`, topics, languages, and contributors to understand what your project *actually is* — not just what your README says.

    </td>
    <td width="50%" valign="top">

### 🎯 Quality Gate

A **critic agent** scores every page for truthfulness, specificity, and hook. Weak copy gets flagged and rewritten automatically. No generic filler survives.

    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">

### 🎨 9 Theme Presets

Developer · Minimal · Terminal · Startup · Apple · Stripe · Linear · GitHub · Glassmorphism — each with its own accent system and visual language.

    </td>
    <td width="50%" valign="top">

### ✍️ AI Rewrite

Don't like a block? Click **Rewrite** and choose a tone:
Professional · Funny · Startup · Developer · Concise · Inspiring

    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">

### 📦 One-Click Export

Download as a **static ZIP** (works offline, zero auth) or deploy directly to Vercel, Netlify, or GitHub Pages.

    </td>
    <td width="50%" valign="top">

### 🌙 Premium UI

**Lightfall** WebGL hero · **SpecularBorder** glow input · **LogoLoop** marquee · Lenis smooth scroll · Glass cards · Dark mode native.

    </td>
  </tr>
</table>

---

## Live Demo

**Try it now → [repo-to-landing-page.vercel.app](https://repo-to-landing-page.vercel.app/)**

Paste any public GitHub URL and see a branded landing page in seconds.

---

## Quick Start

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env         # add GITHUB_TOKEN + OPENROUTER_API_KEY
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev                  # http://localhost:5173
```

No API keys? Set `LLM_PROVIDER=mock` in `.env` and the full flow runs with sample copy.

---

## Tech Stack

| Layer | Stack |
|-------|-------|
| **Frontend** | React 19 · Vite · TypeScript · Tailwind CSS v4 |
| **Animations** | Lightfall · SpecularButton · LogoLoop · Lenis |
| **Backend** | FastAPI · httpx · pydantic |
| **AI** | OpenRouter (free models by default) · Quality gate with critic |
| **Deploy** | Vercel (frontend) · Render (backend) |

---

## Environment

| Variable | Default | Description |
|----------|---------|-------------|
| `GITHUB_TOKEN` | — | GitHub PAT (read-only Contents) |
| `OPENROUTER_API_KEY` | — | Required unless `LLM_PROVIDER=mock` |
| `OPENROUTER_MODEL` | `nvidia/nemotron-3-super-120b-a12b:free` | Free by default |
| `LLM_PROVIDER` | `openrouter` | `openrouter` or `mock` |
| `QUALITY_GATE` | `true` | Critic + targeted rewrite |
| `CORS_ORIGINS` | `localhost:5173` | Add your Vercel URL |

---

## Roadmap

| Phase | Status | What |
|-------|--------|------|
| **v0.1** | ✅ Shipped | AI copy · Quality gate · 9 themes · AI rewrite · ZIP export |
| **Phase 1** | 🔜 Next | Deploy wiring · Live widgets · Before/after · Share badge |
| **Phase 2** | 📋 Planned | Gallery · Custom domains · Analytics · GitHub Action |
| **Phase 3** | 💡 Future | Recruiter mode · Hackathon mode · Product Hunt mode |

Full backlog: [`02-roadmap-and-ideas.md`](./02-roadmap-and-ideas.md)

---

## Author

<p align="center">
  <a href="https://x.com/ynwrobii">
    <img src="https://github.com/Robibiruk.png" width="100" style="border-radius:50%" alt="Robel Biruk" />
  </a>
</p>

<h3 align="center">Robel Biruk</h3>

<p align="center">
  <a href="https://x.com/ynwrobii">X/Twitter</a> ·
  <a href="https://www.linkedin.com/in/robel-biruk-5923101b5/">LinkedIn</a> ·
  <a href="https://github.com/Robibiruk">GitHub</a>
</p>

---

## License

MIT — see [`LICENSE`](./LICENSE) for details.
