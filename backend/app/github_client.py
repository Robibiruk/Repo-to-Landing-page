from __future__ import annotations

import re
from typing import Any

import httpx

ACCEPT_JSON = "application/vnd.github+json"
ACCEPT_RAW = "application/vnd.github.raw+json"


def parse_repo_url(url: str) -> tuple[str, str]:
    """Extract (owner, repo) from a github.com URL, tolerating .git, trailing slashes,
    tree/blob/fragment suffixes, and shorthand 'owner/repo'."""
    url = url.strip()
    m = re.match(r"^(?:https?://)?(?:www\.)?github\.com/([^/]+)/([^/#?]+)", url)
    if m:
        owner, repo = m.group(1), m.group(2)
    elif "/" in url and not url.startswith("http"):
        parts = url.split("/")
        if len(parts) == 2:
            owner, repo = parts[0], parts[1]
        else:
            raise ValueError(f"Not a valid GitHub repo reference: {url!r}")
    else:
        raise ValueError(f"Not a valid GitHub repo reference: {url!r}")
    if repo.endswith(".git"):
        repo = repo[:-4]
    return owner, repo


class GitHubClient:
    def __init__(self, token: str = "", base: str = "https://api.github.com"):
        self.base = base.rstrip("/")
        self.headers = {
            "Accept": ACCEPT_JSON,
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    async def _get_json(self, path: str, **params: Any) -> Any:
        async with httpx.AsyncClient(timeout=25) as client:
            resp = await client.get(f"{self.base}{path}", headers=self.headers, params=params or None)
            if resp.status_code == 404:
                raise RepoNotFound(path)
            resp.raise_for_status()
            return resp.json()

    async def _get_raw(self, path: str) -> str:
        headers = {**self.headers, "Accept": ACCEPT_RAW}
        async with httpx.AsyncClient(timeout=25) as client:
            resp = await client.get(f"{self.base}{path}", headers=headers)
            if resp.status_code == 404:
                raise RepoNotFound(path)
            resp.raise_for_status()
            return resp.text

    async def repo(self, owner: str, repo: str) -> dict:
        return await self._get_json(f"/repos/{owner}/{repo}")

    async def readme(self, owner: str, repo: str) -> str:
        return await self._get_raw(f"/repos/{owner}/{repo}/readme")

    async def root_files(self, owner: str, repo: str) -> list[dict]:
        return await self._get_json(f"/repos/{owner}/{repo}/contents")

    async def file(self, owner: str, repo: str, path: str) -> str:
        return await self._get_raw(f"/repos/{owner}/{repo}/contents/{path}")

    async def languages(self, owner: str, repo: str) -> dict[str, int]:
        return await self._get_json(f"/repos/{owner}/{repo}/languages")

    async def contributors(self, owner: str, repo: str, per_page: int = 5) -> list[dict]:
        return await self._get_json(f"/repos/{owner}/{repo}/contributors", per_page=per_page)

    async def latest_release(self, owner: str, repo: str) -> dict | None:
        try:
            return await self._get_json(f"/repos/{owner}/{repo}/releases/latest")
        except RepoNotFound:
            return None


class RepoNotFound(Exception):
    def __init__(self, path: str):
        self.path = path
        super().__init__(f"GitHub resource not found: {path}")
