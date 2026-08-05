from __future__ import annotations

import json
import re

from . import prompts
from .llm import LLMError, LLMProvider, get_provider
from .repo_analysis import RepoAnalysis
from .schemas import LandingContent

_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


def _clean_json(raw: str) -> str:
    return _FENCE_RE.sub("", raw).strip()


async def generate_content(analysis: RepoAnalysis, provider: LLMProvider | None = None) -> LandingContent:
    provider = provider or get_provider()
    system = prompts.SYSTEM_PROMPT
    user = prompts.build_user_prompt(analysis)

    raw = await provider.generate(system, user, hint=analysis.display_name)
    try:
        return _parse(raw)
    except (ValueError, json.JSONDecodeError) as first_error:
        repair = prompts.build_repair_prompt(analysis, raw, str(first_error))
        repaired = await provider.generate(system, repair)
        try:
            return _parse(repaired)
        except (ValueError, json.JSONDecodeError) as exc:
            raise LLMError(f"LLM returned invalid content twice: {exc}") from exc


def _parse(raw: str) -> LandingContent:
    cleaned = _clean_json(raw)
    data = json.loads(cleaned)
    return LandingContent.model_validate(data)
