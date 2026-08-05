from __future__ import annotations

import json

from .llm import LLMProvider, get_provider
from .repo_analysis import RepoAnalysis
from .schemas import FeatureCard, LandingContent

TONES = ["professional", "funny", "startup", "developer", "concise", "inspiring"]

BLOCK_LABELS = {
    "brand.tagline": "Tagline",
    "hero.headline": "Hero headline",
    "hero.subheadline": "Hero subheadline",
    "hero.cta": "CTA button",
    "problem": "Problem",
    "solution": "Solution",
    "seo.title": "SEO title",
    "seo.description": "SEO description",
    "features.title": "Feature title",
    "features.blurb": "Feature description",
    "install.heading": "Install heading",
}

REWRITE_SYSTEM = """You are the marketing designer for an open-source project's landing page.
You rewrite a single block of copy into a new tone. Keep it truthful to the repository —
never invent features, never contradict the facts. A rewrite can be shorter or longer than the
original. Return ONLY the plain rewritten block text: no quotes, no JSON, no label, no explanation."""


def extract_block(content: LandingContent, block_type: str, index: int) -> str:
    if block_type == "brand.tagline":
        return content.brand.tagline
    if block_type == "hero.headline":
        return content.hero.headline
    if block_type == "hero.subheadline":
        return content.hero.subheadline
    if block_type == "hero.cta":
        return content.hero.cta
    if block_type == "problem":
        return content.problem
    if block_type == "solution":
        return content.solution
    if block_type == "seo.title":
        return content.seo.title
    if block_type == "seo.description":
        return content.seo.description
    if block_type == "install.heading":
        return content.install.heading
    if block_type in ("features.title", "features.blurb") and index < len(content.features):
        f = content.features[index]
        return f.title if block_type == "features.title" else f.blurb
    return ""


def update_block(content: LandingContent, block_type: str, index: int, text: str) -> LandingContent:
    b = content.brand
    if block_type == "brand.tagline":
        return content.model_copy(update={"brand": b.model_copy(update={"tagline": text})})
    h = content.hero
    if block_type == "hero.headline":
        return content.model_copy(update={"hero": h.model_copy(update={"headline": text})})
    if block_type == "hero.subheadline":
        return content.model_copy(update={"hero": h.model_copy(update={"subheadline": text})})
    if block_type == "hero.cta":
        return content.model_copy(update={"hero": h.model_copy(update={"cta": text})})
    if block_type == "problem":
        return content.model_copy(update={"problem": text})
    if block_type == "solution":
        return content.model_copy(update={"solution": text})
    s = content.seo
    if block_type == "seo.title":
        return content.model_copy(update={"seo": s.model_copy(update={"title": text})})
    if block_type == "seo.description":
        return content.model_copy(update={"seo": s.model_copy(update={"description": text})})
    if block_type == "install.heading":
        return content.model_copy(update={"install": content.install.model_copy(update={"heading": text})})
    if block_type in ("features.title", "features.blurb") and index < len(content.features):
        features = list(content.features)
        f = features[index]
        fields: dict = {}
        if block_type == "features.title":
            fields["title"] = text
        else:
            fields["blurb"] = text
        features[index] = f.model_copy(update=fields)
        return content.model_copy(update={"features": features})
    return content


async def rewrite_block(
    analysis: RepoAnalysis,
    content: LandingContent,
    block_type: str,
    index: int,
    tone: str,
    provider: LLMProvider | None = None,
) -> tuple[LandingContent, str]:
    provider = provider or get_provider()
    current = extract_block(content, block_type, index)
    label = BLOCK_LABELS.get(block_type, block_type)
    user = (
        "Repository facts:\n"
        f"{analysis.to_prompt_context()[:4000]}\n\n"
        f"Block to rewrite: {label}\n"
        f"Current text: {current or '(empty)'}\n"
        f"New tone: {tone}\n\n"
        "Rewrite ONLY this block in the requested tone. Return just the rewritten text."
    )
    raw = await provider.generate(REWRITE_SYSTEM, user, hint="rewrite")
    text = _extract_rewrite(raw)
    if not text:
        text = current
    return update_block(content, block_type, index, text), text


def _extract_rewrite(raw: str) -> str:
    """Free models are inconsistent about output framing — unwrap JSON dicts/strings and stray
    quotes so we always get plain text."""
    text = raw.strip()
    if not text:
        return ""
    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            values = [str(v) for v in obj.values() if str(v).strip()]
            if values:
                return values[0]
            keys = [str(k) for k in obj.keys() if str(k).strip()]
            return keys[0] if keys else ""
        if isinstance(obj, str):
            return obj.strip()
    except (ValueError, json.JSONDecodeError):
        pass
    return text.strip('"').strip("'").strip()
