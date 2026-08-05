# RepoPages — Repo → Landing Page

Paste any GitHub repository URL and get a branded marketing landing page in seconds.
No coding, no design, no prompt writing.

> Vertical slice (`v0.1`): analyze → generate → preview → download ZIP. Deploy is stubbed.
> Full vision lives in [02-roadmap-and-ideas.md](./02-roadmap-and-ideas.md).

## Stack

- **Backend:** FastAPI, httpx (GitHub REST + OpenRouter), pydantic
- **Frontend:** React + Vite + TypeScript, Tailwind CSS v4, shadcn/ui-style components
- **LLM:** Claude via OpenRouter (default), with a `MockProvider` for keyless dev and a seam for a future self-hosted model

## Run it

**Backend** (needs Python 3.11+):

```bash
cd backend
python -m venv .venv
.venv/Scripts/activate            # Windows  |  source .venv/bin/activate  (mac/Linux)
pip install -r requirements.txt
cp .env.example .env              # add GITHUB_TOKEN + OPENROUTER_API_KEY
uvicorn app.main:app --reload --port 8000
```

No keys yet? Set `LLM_PROVIDER=mock` in `.env` — the full flow runs with sample copy.

**Frontend** (needs Node 18+):

```bash
cd frontend
npm install
npm run dev                       # http://localhost:5173
```

The Vite dev server proxies `/api` to the backend on port 8000.

## How it works

1. **Analyze** — reads the README, key files (`package.json`, `Cargo.toml`, `pyproject.toml`, …), topics, languages, stars, contributors.
2. **Generate** — one structured LLM call produces brand, hero, features, install, SEO.
3. **Render** — a standalone single-file HTML page in your chosen theme.
4. **Share** — preview in a sandboxed iframe, switch themes instantly, download as ZIP.

## Project layout

```
backend/app/          FastAPI: github_client, repo_analysis, llm, prompts, generator,
                      themes, render, zip_export, deploy (stub), main
frontend/src/         React app: api client, types, App + components
02-roadmap-and-ideas.md   living backlog (Phase 1–3, launch modes, viral features)
```

## Env vars

| Var | Purpose |
| --- | --- |
| `GITHUB_TOKEN` | GitHub PAT — higher rate limits + private repos |
| `OPENROUTER_API_KEY` | Required unless `LLM_PROVIDER=mock` |
| `OPENROUTER_MODEL` | Default `nvidia/nemotron-3-super-120b-a12b:free` (free tier). Swap for a paid model anytime. |
| `OPENROUTER_FALLBACK_MODELS` | Comma-separated free-model fallbacks for 429 rate limits |
| `QUALITY_GATE` | `true` (default) — critic scores copy and drives a targeted rewrite |
| `MAX_REFINE_ROUNDS` | `1` (default) — bounds refine latency on the free tier |
| `LLM_PROVIDER` | `openrouter` (default) or `mock` |
