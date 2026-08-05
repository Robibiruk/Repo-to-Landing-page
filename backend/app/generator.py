from __future__ import annotations

import json
import re

from . import prompts
from .llm import LLMError, LLMProvider, get_provider
from .repo_analysis import RepoAnalysis
from .schemas import Critique, LandingContent

_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


def _clean_json(raw: str) -> str:
    return _FENCE_RE.sub("", raw).strip()


def _parse(raw: str) -> LandingContent:
    cleaned = _clean_json(raw)
    data = json.loads(cleaned)
    return LandingContent.model_validate(data)


async def generate_content(
    analysis: RepoAnalysis,
    provider: LLMProvider | None = None,
    quality_gate: bool = True,
    max_refine_rounds: int = 1,
) -> LandingContent:
    """Analyze -> write -> critique -> refine. The critic is what lets weaker (free) models
    punch above their weight: it catches generic filler and invented features, then drives a
    targeted rewrite. Refine rounds are bounded so latency stays sane on the free tier."""
    provider = provider or get_provider()
    system = prompts.SYSTEM_PROMPT
    user = prompts.build_user_prompt(analysis)

    raw = await _generate_valid_json(provider, system, user, analysis)
    content = _parse(raw)

    if quality_gate and provider.name != "mock":
        refined = 0
        while refined <= max_refine_rounds:
            critique = await _critique(provider, analysis, content)
            if critique.passed:
                break
            if refined == max_refine_rounds:
                break
            content = await _refine(provider, analysis, content, critique.feedback)
            refined += 1
    return content


async def _generate_valid_json(provider: LLMProvider, system: str, user: str, analysis: RepoAnalysis) -> str:
    raw = await provider.generate(system, user, hint=analysis.display_name)
    try:
        _parse(raw)
        return raw
    except (ValueError, json.JSONDecodeError) as first_error:
        repair = prompts.build_repair_prompt(analysis, raw, str(first_error))
        repaired = await provider.generate(system, repair)
        try:
            _parse(repaired)
            return repaired
        except (ValueError, json.JSONDecodeError) as exc:
            raise LLMError(f"LLM returned invalid content twice: {exc}") from exc


async def _critique(provider: LLMProvider, analysis: RepoAnalysis, content: LandingContent) -> Critique:
    content_json = content.model_dump_json()
    raw = await provider.generate(
        prompts.CRITIC_SYSTEM_PROMPT,
        prompts.build_critic_prompt(analysis, content_json),
        hint="critique",
    )
    try:
        return Critique.model_validate(json.loads(_clean_json(raw)))
    except (ValueError, json.JSONDecodeError):
        # A malformed critique shouldn't sink the page — treat it as a pass.
        return Critique(passed=True, scores={}, feedback="")


async def _refine(provider: LLMProvider, analysis: RepoAnalysis, content: LandingContent, feedback: str) -> LandingContent:
    content_json = content.model_dump_json()
    raw = await provider.generate(
        prompts.REFINE_SYSTEM_PROMPT,
        prompts.build_refine_prompt(analysis, content_json, feedback),
        hint=analysis.display_name,
    )
    try:
        return _parse(raw)
    except (ValueError, json.JSONDecodeError):
        # If the rewrite is invalid, keep the previous draft rather than regress.
        return content
