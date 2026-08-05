from __future__ import annotations

import asyncio
import json
from typing import Protocol

import httpx

from .config import settings

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class LLMError(Exception):
    pass


class LLMProvider(Protocol):
    name: str

    async def generate(self, system: str, user: str, hint: str = "") -> str: ...


class _Retryable(LLMError):
    """Rate limit (429) or upstream (5xx) failure — worth retrying, possibly on a fallback model."""


class OpenRouterProvider:
    """Default provider. Free open-source models are the default because they cost nothing;
    the model + a fallback chain are env-configurable, so a paid model (e.g. Claude) is one
    env change away. Retries transient 429/5xx with backoff, then moves down the fallback chain.
    """

    name = "openrouter"

    def __init__(self, api_key: str, model: str, fallbacks: list[str] | None = None):
        self.api_key = api_key
        self.model = model
        self.fallbacks = fallbacks or []

    async def generate(self, system: str, user: str, hint: str = "") -> str:
        if not self.api_key:
            raise LLMError("OPENROUTER_API_KEY is not set")
        models = [self.model, *self.fallbacks]
        last_error: LLMError | None = None
        for model in models:
            for attempt in range(3):
                try:
                    return await self._call(model, system, user)
                except _Retryable as exc:
                    last_error = exc
                    if attempt < 2:
                        await asyncio.sleep(2 * (attempt + 1))
                    else:
                        break
            # this model exhausted its retries — try the next fallback
        raise LLMError(f"All OpenRouter models failed. Last error: {last_error}")

    async def _call(self, model: str, system: str, user: str) -> str:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.7,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=180) as client:
            resp = await client.post(OPENROUTER_URL, json=payload, headers=headers)
            if resp.status_code == 429 or resp.status_code >= 500:
                raise _Retryable(f"OpenRouter {resp.status_code} for {model}: {resp.text[:300]}")
            if resp.status_code >= 400:
                raise LLMError(f"OpenRouter error {resp.status_code} for {model}: {resp.text[:500]}")
            data = resp.json()
        # OpenRouter sometimes returns HTTP 200 with an error body (upstream provider failure).
        if isinstance(data, dict) and data.get("error"):
            message = str(data["error"].get("message", ""))[:200].lower()
            transient = any(k in message for k in ("exhausted", "rate", "upstream", "timeout", "temporar", "overloaded"))
            if transient:
                raise _Retryable(f"OpenRouter upstream error for {model}: {str(data['error'])[:300]}")
            raise LLMError(f"OpenRouter error for {model}: {str(data['error'])[:300]}")
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMError(f"Unexpected OpenRouter response from {model}: {str(data)[:500]}") from exc


class MockProvider:
    """Deterministic sample output so the full flow runs with no API key."""

    name = "mock"

    async def generate(self, system: str, user: str, hint: str = "") -> str:
        name = hint or "Your Project"
        accent = "#6366f1"
        sample = {
            "brand": {
                "name": name,
                "tagline": "Ship it. Show it. Grow it.",
                "accent": accent,
                "gradientFrom": accent,
                "gradientTo": "#22d3ee",
            },
            "hero": {
                "headline": f"{name}: built by developers, loved by users",
                "subheadline": "The fastest way to turn a great idea into something the world can use. Open source, free, and ready in minutes.",
                "cta": "Get started",
            },
            "problem": "Great projects are everywhere, but most never get the presentation they deserve.",
            "solution": "This project fixes that with a focused, fast, and genuinely useful tool — no signup walls, no fluff.",
            "features": [
                {"title": "Lightning fast", "blurb": "Optimized from day one. Instant feedback, zero bloat.", "iconKey": "zap"},
                {"title": "Open source", "blurb": "MIT licensed and community-driven. Your data stays yours.", "iconKey": "code"},
                {"title": "Extensible", "blurb": "Clean APIs and clear docs make it trivial to build on.", "iconKey": "box"},
                {"title": "Built for developers", "blurb": "CLI-friendly, scriptable, and easy to self-host.", "iconKey": "terminal"},
            ],
            "install": {
                "heading": "Get started in seconds",
                "commands": ["npm install", "npm run dev"],
                "snippet": "import your_project from 'your-project'\n\n// ready to go\nyour_project.start()",
            },
            "sections": ["stats", "roadmap"],
            "footer": {
                "license": "MIT",
                "links": [
                    {"label": "GitHub", "url": "https://github.com"},
                    {"label": "Docs", "url": "https://docs.example.com"},
                ],
            },
            "seo": {
                "title": f"{name} — ship faster",
                "description": f"{name} is an open-source project that makes developers more productive.",
                "keywords": ["open source", "developer tools", name],
            },
        }
        return json.dumps(sample, indent=2)


def get_provider() -> LLMProvider:
    if settings.llm_provider == "mock":
        return MockProvider()
    fallbacks = [m.strip() for m in settings.openrouter_fallback_models.split(",") if m.strip()]
    return OpenRouterProvider(
        api_key=settings.openrouter_api_key,
        model=settings.openrouter_model,
        fallbacks=fallbacks,
    )
