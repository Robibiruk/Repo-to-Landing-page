"""Deploy is stubbed for the vertical slice.

The generated site is a single self-contained HTML file, so any static host works.
Planned providers (see 02-roadmap-and-ideas.md, Phase 2):
- Surge   (surge.sh)  - token-based, simplest to automate, no OAuth
- Netlify (drop/netlify-cli)
- Vercel  (vercel CLI/token)
- GitHub Pages (via the repo itself)

Each will implement a small interface like:

    class DeployProvider(Protocol):
        async def deploy(self, html: str) -> DeployResult: ...   # returns a public URL

Until then the frontend shows the action as "coming soon".
"""
