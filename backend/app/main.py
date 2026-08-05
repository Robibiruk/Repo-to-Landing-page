import uuid
from collections import OrderedDict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from .config import settings
from .generator import generate_content
from .github_client import GitHubClient, RepoNotFound, parse_repo_url
from .llm import LLMError
from .render import render_landing
from .repo_analysis import RepoAnalysis, analyze_repo
from .rewrite import TONES, rewrite_block
from .schemas import LandingContent
from .themes import THEMES
from .zip_export import build_zip

app = FastAPI(title="RepoPages", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Small in-memory caches. Stateless by design; cleared on restart.
_CONTENT: "OrderedDict[str, dict]" = OrderedDict()
_HTML: "OrderedDict[tuple[str, str], str]" = OrderedDict()
_MAX_ITEMS = 32


class GenerateRequest(BaseModel):
    repo_url: str
    theme: str = Field(default="developer")


class PreviewRequest(BaseModel):
    content_id: str
    theme: str = Field(default="developer")


class RewriteRequest(BaseModel):
    content_id: str
    block_type: str
    index: int = Field(default=0)
    tone: str = Field(default="professional")
    theme: str = Field(default="developer")


def _cache_get(cache, key):
    if key in cache:
        cache.move_to_end(key)
        return cache[key]
    return None


def _cache_put(cache, key, value):
    cache[key] = value
    cache.move_to_end(key)
    while len(cache) > _MAX_ITEMS:
        cache.popitem(last=False)


def _repo_info(analysis: RepoAnalysis) -> dict:
    return {
        "full_name": analysis.full_name,
        "url": f"https://github.com/{analysis.owner}/{analysis.repo}",
        "description": analysis.description,
        "topics": analysis.topics,
        "primary_language": analysis.primary_language,
        "license": analysis.license_name,
        "stars": analysis.stars,
        "forks": analysis.forks,
        "contributors": analysis.contributors,
        "homepage": analysis.homepage,
    }


@app.get("/api/health")
async def health():
    return {"status": "ok", "provider": settings.llm_provider, "model": settings.openrouter_model}


@app.get("/api/themes")
async def themes():
    return [{"id": t.id, "label": t.label} for t in THEMES.values()]


@app.post("/api/generate")
async def generate(req: GenerateRequest):
    try:
        owner, repo = parse_repo_url(req.repo_url)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    client = GitHubClient(token=settings.github_token)
    try:
        analysis = await analyze_repo(client, owner, repo)
        content = await generate_content(
            analysis,
            quality_gate=settings.quality_gate,
            max_refine_rounds=settings.max_refine_rounds,
        )
    except RepoNotFound as exc:
        raise HTTPException(status_code=404, detail=f"Repository not found: {exc.path}")
    except (LLMError, Exception) as exc:
        if isinstance(exc, LLMError):
            raise HTTPException(status_code=502, detail=str(exc))
        raise HTTPException(status_code=502, detail=f"Failed to analyze repository: {exc}")

    content_id = uuid.uuid4().hex[:12]
    theme = req.theme if req.theme in THEMES else "developer"
    html = render_landing(analysis, content, theme, settings.repopages_url)
    _cache_put(_CONTENT, content_id, {"analysis": analysis, "content": content})
    _cache_put(_HTML, (content_id, theme), html)

    return {
        "content_id": content_id,
        "theme": theme,
        "html": html,
        "content": content.model_dump(),
        "repo": _repo_info(analysis),
    }


@app.post("/api/preview")
async def preview(req: PreviewRequest):
    entry = _cache_get(_CONTENT, req.content_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="No generated content for this id. Generate first.")
    theme = req.theme if req.theme in THEMES else "developer"
    html = _cache_get(_HTML, (req.content_id, theme))
    if html is None:
        html = render_landing(entry["analysis"], entry["content"], theme, settings.repopages_url)
        _cache_put(_HTML, (req.content_id, theme), html)
    return {"html": html, "theme": theme}


@app.post("/api/rewrite")
async def rewrite(req: RewriteRequest):
    entry = _cache_get(_CONTENT, req.content_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="No generated content for this id. Generate first.")
    if req.tone not in TONES:
        raise HTTPException(status_code=422, detail=f"Unknown tone. Choose from: {', '.join(TONES)}")
    try:
        content, block_text = await rewrite_block(
            entry["analysis"], entry["content"], req.block_type, req.index, req.tone
        )
    except LLMError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    entry["content"] = content
    theme = req.theme if req.theme in THEMES else "developer"
    html = render_landing(entry["analysis"], content, theme, settings.repopages_url)
    _cache_put(_HTML, (req.content_id, theme), html)
    return {"html": html, "content": content.model_dump(), "block_text": block_text}


@app.get("/api/export")
async def export(content_id: str, theme: str = "developer"):
    entry = _cache_get(_CONTENT, content_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="No generated content for this id. Generate first.")
    theme = theme if theme in THEMES else "developer"
    html = _cache_get(_HTML, (content_id, theme))
    if html is None:
        html = render_landing(entry["analysis"], entry["content"], theme, settings.repopages_url)
        _cache_put(_HTML, (content_id, theme), html)
    zip_bytes = build_zip(html)
    name = entry["analysis"].repo or "repopages"
    return StreamingResponse(
        iter([zip_bytes]),
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{name}-landing.zip"'},
    )
