from .repo_analysis import RepoAnalysis

SYSTEM_PROMPT = """You are the product/marketing designer for open-source repositories.
Given a repository analysis, you produce a complete landing page in a single JSON object.
Voice: confident, concrete, developer-respectful. No fluff, no hype-words like "revolutionary" or "game-changing".
Be truthful to the actual repo — never invent features the analysis does not support.

Rules:
- accent, gradientFrom, gradientTo are hex colors (#rrggbb). Prefer the accent seeded by the repo's primary language when it fits.
- features: 3-4 cards. Each iconKey is one of: zap, code, terminal, shield, spark, chart, users, box.
- sections: pick only types that fit the repo, from: stats, examples, roadmap, pricing, faq, team, changelog.
- install: use commands actually present in the analysis when available.
- seo.title under 60 chars, seo.description under 160 chars.
- footer.license: the repo's license name, if any.
- Respond with ONLY the JSON object. No markdown fences, no commentary."""

SCHEMA_DESCRIPTION = """Output JSON shape:
{
  "brand": {"name": str, "tagline": str, "accent": str, "gradientFrom": str, "gradientTo": str},
  "hero": {"headline": str, "subheadline": str, "cta": str},
  "problem": str,
  "solution": str,
  "features": [{"title": str, "blurb": str, "iconKey": str}],
  "install": {"heading": str, "commands": [str], "snippet": str},
  "sections": [str],
  "footer": {"license": str, "links": [{"label": str, "url": str}]},
  "seo": {"title": str, "description": str, "keywords": [str]}
}"""


def build_user_prompt(analysis: RepoAnalysis) -> str:
    return (
        "Generate the landing page content for the repository below.\n\n"
        "Follow this schema exactly:\n"
        f"{SCHEMA_DESCRIPTION}\n\n"
        f"Suggested accent color to start from: {analysis.accent_color}\n\n"
        "Repository analysis:\n"
        f"{analysis.to_prompt_context()}"
    )


def build_repair_prompt(analysis: RepoAnalysis, raw: str, error: str) -> str:
    return (
        "The previous response was invalid JSON. Fix it so it parses and matches the schema.\n"
        f"Validation error: {error}\n\n"
        f"Previous response:\n{raw[:3000]}\n\n"
        "Return ONLY the corrected JSON object, matching this schema:\n"
        f"{SCHEMA_DESCRIPTION}"
    )
