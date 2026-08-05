# 02 — Roadmap & Ideas (living backlog)

Everything beyond the vertical slice lives here. This is the long-term vision
("the publishing platform for open source") chopped into phases we can actually ship.
Tick things off as they land. Add freely.

**Thesis:** the product is a **developer growth tool** — making every GitHub repo
instantly marketable. The landing page is the output; the share loop is the product.

---

## ✅ Vertical slice (shipped — `v0.1`)

- [x] Paste repo URL → fetch README + key files + metadata + stats (GitHub token)
- [x] One structured LLM call → brand, hero, features, install, SEO (OpenRouter, configurable model)
- [x] Standalone single-file HTML render, 4 themes (developer / minimal / terminal / startup)
- [x] Sandboxed iframe live preview, theme switching without re-running the LLM
- [x] Download ZIP (works offline, zero auth)
- [x] Deploy = stubbed interface
- [x] `LLMProvider` seam: OpenRouter (default) + Mock (no-key dev)
- [x] **Critic/quality-gate pass** — copy is scored (truthfulness/specificity/hook/…) and driven through a targeted rewrite when weak (bounded `MAX_REFINE_ROUNDS`)
- [x] **Free-model A/B** (2026-08-05) — winner: `nvidia/nemotron-3-super-120b-a12b:free`; fallbacks `poolside/laguna-s-2.1`, `google/gemma-4-31b-it`; provider retries + walks the chain on 429/upstream errors

---

## Phase 1 — make it a *growth tool*, not a generator

- [ ] **Live GitHub widgets** — stars / forks / contributors / latest release auto-refreshed on the page
- [ ] **Share loop badge** — "Built with RepoPages" links to the product / gallery once live
- [ ] **Deploy wiring** — Surge first (token-only, no OAuth), then Netlify Drop / Vercel
- [ ] **Before vs after** — one screenshot slider: README vs landing page
- [ ] **Public gallery** — browse recently generated pages ("Best of RepoPages")
- [ ] **AI rewrite** — redo any copy block with a tone (professional / funny / startup / developer)
- [ ] **Auto theme engine** — one-click presets: Apple, Stripe, Vercel, Linear, GitHub, Glassmorphism, Retro, Brutalist

## Phase 2 — deeper understanding

- [ ] **Richer analysis** — Dockerfile/CI, commit history, releases, issues, PRs, wiki, CHANGELOG
- [ ] **Feature detection** — detect auth, payments, API, AI, chat, dark mode, Docker, tests → auto feature cards
- [ ] **Smart demo detection** — auto-embed YouTube / Loom / GIF / Live Demo / CodeSandbox from the README
- [ ] **Repository visualizer** — folder structure → architecture diagram
- [ ] **README improver** — generate badges, install docs, FAQ, contributing, roadmap back to the repo
- [ ] **Logo / icon generator** — SVG logo, favicon, social icon, PWA icon when missing

## Phase 3 — editing + SEO + analytics

- [ ] **Inline editing** — click any block, edit or rewrite with AI (no drag-drop canvas yet)
- [ ] **SEO engine** — Schema.org, sitemap, robots.txt, canonical, OG/Twitter previews (partially there)
- [ ] **Landing page score** — design / SEO / readability / accessibility / performance
- [ ] **Analytics** — views, countries, referrers, click → star/conversion rates
- [ ] Multi-page sites, custom domains

## Launch modes (the monetizable tail)

- [ ] **Recruiter mode** — portfolio view: problem, architecture, challenges, impact, resume bullets
- [ ] **Hackathon mode** — pitch, demo page, judging criteria, innovation section, timeline
- [ ] **Product Hunt mode** — tagline, launch description, gallery, maker comment, social assets
- [ ] **Indie hacker mode** — pricing section, roadmap, email waitlist, newsletter, testimonial placeholders

## Viral features

- [ ] **"Generate my repo"** viral share buttons on every page
- [ ] **Remix this design** — reuse another project's theme
- [ ] **Launch kit** — landing page + README refresh + Product Hunt copy + X thread + LinkedIn post in one click
- [ ] **Browser extension** — "Generate landing page" button on GitHub repo pages
- [ ] **GitHub Action** — rebuild + redeploy after every release (live repo sync)

## Alternative exports

- [ ] React / Next.js / Astro / Vue / Svelte / Markdown / PDF export
- [ ] Screenshot generator (laptop + phone mockups) when the repo has no images

---

## Personal / self-hosted LLM path

**Goal:** run our own open-weight model instead of paying per-token. Currently
architected-for, not built: `backend/app/llm.py` exposes an `LLMProvider` protocol,
so a self-hosted model is **one adapter swap**, not a rewrite.

**Why we're not building it yet (honest assessment):**
- **Frontier quality is the product.** Marketing copy from a 7–13B model reads as
  generic filler. The "instant wow" loop depends on Claude-class copy.
- **Latency.** A full page is 3–6k tokens. ~20–50 tok/s on a consumer GPU = 1–3 min
  per page vs 10–30 s via API. Breaks the "20 seconds" promise.
- **Hardware.** No local GPU today → self-hosting means renting (RunPod / Vast.ai /
  Lambda), which costs more than the API at MVP traffic.

**When to build it:**
1. You rent cloud GPU (a real server, not a dev machine).
2. A model + serving stack is chosen (vLLM or llama.cpp, e.g. Qwen/Llama/Mistral 14–70B).
3. Traffic justifies it (self-host wins on $/token at scale) **or** privacy
   requirements make it mandatory (repo contents never leave your infra).

**When we do:** add `SelfHostedProvider` → points at any OpenAI-compatible endpoint
(`/v1/chat/completions`), e.g. `http://localhost:11434/v1` (Ollama) or a vLLM box.
Set `LLM_PROVIDER=selfhosted` + `SELFHOSTED_BASE_URL` + `SELFHOSTED_MODEL`. Nothing
else changes.

**Open questions to revisit:**
- [ ] Confirm the self-host target: cost-at-scale vs privacy vs independence
- [ ] Pick model class + quant size + VRAM budget for the target GPU
- [ ] Decide who owns inference ops (uptime, driver updates, security)
