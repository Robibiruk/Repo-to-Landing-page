# RepoPages

> **The publishing platform for open source.** Turn any GitHub repository into a beautiful product website in minutes.

[![Deploy on Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Robibiruk/Repo-to-Landing-page)

---

## What it does

Paste a GitHub URL. RepoPages:
1. **Analyzes** your README, package files, topics, and contributors
2. **Generates** AI-powered marketing copy tuned to your project
3. **Scores** the output with a quality gate (catches generic filler + invented features)
4. **Designs** a landing page with your brand colors, typography, and layout
5. **Deploys** as a static site — ZIP download or one-click deploy

No coding. No design. No prompt writing.

---

## Screenshots

<!-- Add screenshots here: paste your browser captures into frontend/public/screenshots/ -->

| Home | Generate | Preview |
|------|----------|---------|
| ![Home](frontend/public/screenshots/home.png) | ![Generate](frontend/public/screenshots/generate.png) | ![Preview](frontend/public/screenshots/preview.png) |

---

## Live demo

**Frontend:** [repo-to-landing-page.vercel.app](https://repo-to-landing-page.vercel.app)  
**Backend API:** [repo-to-landing-page-api.onrender.com/api/health](https://repo-to-landing-page-api.onrender.com/api/health)

---

## Tech stack

| Layer | Tech |
|-------|------|
| Frontend | React 19 + Vite + TypeScript + Tailwind CSS v4 |
| Routing | react-router-dom |
| Animations | Lenis (smooth scroll), Lightfall (WebGL hero), SpecularButton + SpecularBorder (glow), LogoLoop (scrolling marquee) |
| Backend | FastAPI + httpx + pydantic |
| LLM | Claude via OpenRouter (free open-source models by default) |
| Quality | Critic pass: scores truthfulness/specificity/hook → targeted rewrite |
| Hosting | Vercel (frontend) + Render (backend) |

---

## Quick start

### Backend (Python 3.11+)

```bash
cd backend
python -m venv .venv
.venv/Scripts/activate          # Windows  |  source .venv/bin/activate  (mac/Linux)
pip install -r requirements.txt
cp .env.example .env
# add GITHUB_TOKEN + OPENROUTER_API_KEY to .env
uvicorn app.main:app --reload --port 8000
```

No keys yet? Set `LLM_PROVIDER=mock` in `.env` — the full flow runs with sample copy.

### Frontend (Node 18+)

```bash
cd frontend
npm install
npm run dev                     # http://localhost:5173
```

---

## Environment variables

### Backend (`backend/.env`)

| Variable | Description | Default |
|----------|-------------|---------|
| `GITHUB_TOKEN` | GitHub PAT (Contents: read-only) | (empty) |
| `OPENROUTER_API_KEY` | Required unless `LLM_PROVIDER=mock` | (empty) |
| `OPENROUTER_MODEL` | LLM model ID | `nvidia/nemotron-3-super-120b-a12b:free` |
| `OPENROUTER_FALLBACK_MODELS` | Comma-separated fallback chain | `poolside/laguna-s-2.1:free,google/gemma-4-31b-it:free` |
| `LLM_PROVIDER` | `openrouter` or `mock` | `openrouter` |
| `QUALITY_GATE` | Enable critic + refine pass | `true` |
| `MAX_REFINE_ROUNDS` | Bounded refine iterations | `1` |
| `CORS_ORIGINS` | Comma-separated allowed origins | `http://localhost:5173,http://localhost:3000` |
| `REPOPAGES_URL` | Badge link target | (empty) |

### Frontend (`frontend/.env`)

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend URL (leave blank for local dev) | `/api` |

---

## How it works

### Pipeline

```
Paste GitHub URL
    ↓
Fetch repo (README, package.json, topics, languages, contributors)
    ↓
AI generates structured content (brand, hero, features, SEO)
    ↓
Critic scores: truthfulness / specificity / hook / clarity / SEO
    ↓
If score < threshold → targeted refine rewrite (bounded rounds)
    ↓
Renderer builds standalone HTML (no JS, fully sandboxed)
    ↓
Preview in iframe → switch themes → AI rewrite → Download ZIP
```

### LLM strategy

Free open-source models via OpenRouter — no monthly cost while unproven.
Default: **Nemotron 3 120B** (passes the critic at 1.0 truthfulness).

Fallback chain handles429 rate limits: Nemotron → Poolside → Gemma.
The seam is architected for self-hosted models — one adapter swap when you have cloud GPU budget.

### Themes (9 presets)

| Theme | Vibe |
|-------|------|
| Developer | Clean, modern dev tool |
| Minimal | Apple-like whitespace |
| Terminal | Dark monospace, green accents |
| Startup | Bold gradients, big type |
| Apple | SF Pro, pill buttons |
| Stripe | Purple→cyan, soft shadows |
| Linear | Dark, ink depth |
| GitHub | Light, familiar |
| Glassmorphism | Blur glass cards |

---

## Project structure

```
├── backend/               FastAPI backend
│   └── app/
│       ├── main.py        Routes + CORS + cache
│       ├── config.py      Settings from env
│       ├── github_client  GitHub REST API
│       ├── repo_analysis  Extract structured facts
│       ├── llm            Provider interface (OpenRouter + Mock + future self-hosted)
│       ├── prompts        System/user prompts + critic + refine
│       ├── generator      Analyze → write → critique → refine
│       ├── schemas        Pydantic models (LandingContent, Critique)
│       ├── render         Standalone HTML builder
│       ├── themes         9 theme presets
│       ├── rewrite        Per-block AI rewrite
│       ├── zip_export     Static ZIP builder
│       └── deploy         (stubbed for next phase)
├── frontend/              React + Vite + Tailwind
│   └── src/
│       ├── App.tsx         Home page + routing
│       ├── main.tsx        BrowserRouter + Lenis + ThemeProvider
│       ├── api.ts          Typed fetch wrappers
│       ├── components/     UI: UrlForm, PreviewFrame, SpecularButton, Lightfall, etc.
│       ├── pages/          Features, Gallery, Pricing, Docs, Blog, Changelog, About, Contact, Roadmap
│       └── types.ts        TypeScript interfaces
├── 01-repo-to-landing-page.md   Original MVP spec
├── 02-roadmap-and-ideas.md      Living backlog (Phase 1–3 + self-hosted LLM path)
├── render.yaml            Render deployment config
└── vercel.json            Vercel deployment config
```

---

## Deployment

### Backend → Render
1. Push to GitHub
2. Render → New Web Service → `Robibiruk/Repo-to-Landing-page`
3. Build: `cd backend && pip install -r requirements.txt`
4. Start: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add env vars (GITHUB_TOKEN, OPENROUTER_API_KEY, CORS_ORIGINS)

### Frontend → Vercel
1. Vercel → New Project → `Robibiruk/Repo-to-Landing-page`
2. Root directory: `frontend`
3. Add env var: `VITE_API_URL` = your Render backend URL

---

## Roadmap

- [ ] Phase 1: Deploy wiring, live GitHub widgets, before/after, AI rewrite improvements
- [ ] Phase 2: Gallery, custom domains, analytics, GitHub Action, browser extension
- [ ] Phase 3: Recruiter mode, hackathon mode, Product Hunt mode, launch kit
- [ ] Self-hosted LLM: provider adapter for vLLM/Ollama when GPU budget allows

See [02-roadmap-and-ideas.md](./02-roadmap-and-ideas.md) for the full backlog.

---

## Author

**Robel Biruk** — [@ynwrobii](https://x.com/ynwrobii) · [LinkedIn](https://www.linkedin.com/in/robel-biruk-5923101b5/) · [GitHub](https://github.com/Robibiruk)

---

## License

MIT
