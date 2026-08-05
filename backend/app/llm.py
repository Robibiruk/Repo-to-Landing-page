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
                "tagline": "Turn ideas into products, not READMEs.",
                "accent": accent,
                "gradientFrom": accent,
                "gradientTo": "#22d3ee",
            },
            "hero": {
                "headline": "Ship your project with a landing page that converts",
                "subheadline": "Paste your GitHub URL, get a branded product page with AI-written copy — live in seconds.",
                "cta": "Try it free",
            },
            "problem": "You built something great, but no one can figure out what it does or how to use it from your GitHub page alone.",
            "solution": "This turns your repository into a real product page — the kind that gets users, not just stars.",
            "features": [
                {"title": "Go live in seconds", "blurb": "Paste a URL, pick a theme, and your page is ready. No design skills needed.", "iconKey": "zap"},
                {"title": "AI writes your copy", "blurb": "Hero, features, FAQ — all generated from your actual codebase, not generic templates.", "iconKey": "spark"},
                {"title": "Looks like a million dollars", "blurb": "Premium themes with glass cards, smooth scroll, and dark mode. Your project deserves this.", "iconKey": "box"},
                {"title": "One-click deploy", "blurb": "Export or deploy instantly. Shareable link in under a minute.", "iconKey": "rocket"},
            ],
            "install": {
                "heading": "Get started in 3 steps",
                "commands": ["npm install", "npm run dev"],
                "snippet": "1. Paste your GitHub URL\n2. Pick a theme\n3. Share your new landing page",
            },
            "sections": ["stats"],
            "footer": {
                "license": "MIT",
                "links": [
                    {"label": "GitHub", "url": "https://github.com"},
                    {"label": "Docs", "url": "https://docs.example.com"},
                ],
            },
            "seo": {
                "title": f"{name} — launch faster",
                "description": f"{name}: turn your GitHub project into a landing page that users actually want to click.",
                "keywords": ["landing page", "developer tools", "product page", name],
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
