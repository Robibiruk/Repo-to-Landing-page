from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

from .github_client import GitHubClient

MAX_README = 20_000
MAX_FILE = 4_000

# Primary language -> accent color (deterministic brand seed).
LANGUAGE_ACCENTS = {
    "rust": "#f97316",
    "python": "#22c55e",
    "typescript": "#eab308",
    "javascript": "#f59e0b",
    "go": "#06b6d4",
    "java": "#ef4444",
    "c": "#3b82f6",
    "c++": "#3b82f6",
    "c#": "#8b5cf6",
    "ruby": "#dc2626",
    "php": "#8b5cf6",
    "kotlin": "#f97316",
    "swift": "#f59e0b",
    "elixir": "#a855f7",
    "haskell": "#8b5cf6",
    "lua": "#3b82f6",
    "dart": "#06b6d4",
    "zig": "#eab308",
}

FRAMEWORK_HINTS = {
    "react": "React", "next": "Next.js", "vue": "Vue", "svelte": "Svelte",
    "angular": "Angular", "astro": "Astro", "solid": "Solid",
    "express": "Express", "fastify": "Fastify", "hono": "Hono",
    "django": "Django", "flask": "Flask", "fastapi": "FastAPI",
    "pytorch": "PyTorch", "tensorflow": "TensorFlow", "transformers": "Transformers",
    "langchain": "LangChain", "tauri": "Tauri", "electron": "Electron",
    "flask": "Flask", "gradio": "Gradio", "streamlit": "Streamlit",
}


@dataclass
class RepoAnalysis:
    owner: str
    repo: str
    full_name: str
    description: str
    homepage: str
    topics: list[str] = field(default_factory=list)
    primary_language: str = ""
    languages: dict[str, int] = field(default_factory=dict)
    license_name: str = ""
    stars: int = 0
    forks: int = 0
    contributors: list[str] = field(default_factory=list)
    latest_release: str = ""
    default_branch: str = "main"
    readme: str = ""
    package_json: dict[str, Any] = field(default_factory=dict)
    key_files: dict[str, str] = field(default_factory=dict)
    install_commands: list[str] = field(default_factory=list)
    frameworks: list[str] = field(default_factory=list)

    @property
    def accent_color(self) -> str:
        key = self.primary_language.lower()
        return LANGUAGE_ACCENTS.get(key, "#6366f1")

    @property
    def display_name(self) -> str:
        if self.package_json.get("name"):
            return str(self.package_json["name"]).replace("_", " ").title()
        return self.repo.replace("-", " ").title()

    def to_prompt_context(self) -> str:
        lines: list[str] = []
        lines.append(f"Repository: {self.full_name}")
        lines.append(f"Description: {self.description or '(none)'}")
        if self.topics:
            lines.append(f"Topics: {', '.join(self.topics)}")
        lines.append(f"Primary language: {self.primary_language or 'unknown'}")
        if self.languages:
            lines.append("Languages: " + ", ".join(f"{k} ({v})" for k, v in self.languages.items()))
        if self.frameworks:
            lines.append(f"Frameworks: {', '.join(self.frameworks)}")
        lines.append(f"Stars: {self.stars}, Forks: {self.forks}")
        if self.license_name:
            lines.append(f"License: {self.license_name}")
        if self.latest_release:
            lines.append(f"Latest release: {self.latest_release}")
        if self.homepage:
            lines.append(f"Homepage: {self.homepage}")
        if self.install_commands:
            lines.append("Install commands: " + " | ".join(self.install_commands))
        lines.append("\n--- README (truncated) ---")
        lines.append(self.readme or "(no README)")
        for name, content in self.key_files.items():
            lines.append(f"\n--- {name} (truncated) ---")
            lines.append(content)
        return "\n".join(lines)


async def analyze_repo(client: GitHubClient, owner: str, repo: str) -> RepoAnalysis:
    meta = await client.repo(owner, repo)
    analysis = RepoAnalysis(
        owner=owner,
        repo=repo,
        full_name=meta.get("full_name", f"{owner}/{repo}"),
        description=meta.get("description") or "",
        homepage=meta.get("homepage") or "",
        topics=meta.get("topics") or [],
        primary_language=meta.get("language") or "",
        license_name=(meta.get("license") or {}).get("spdx_id") or "",
        stars=meta.get("stargazers_count") or 0,
        forks=meta.get("forks_count") or 0,
        default_branch=meta.get("default_branch") or "main",
    )

    try:
        analysis.readme = (await client.readme(owner, repo))[:MAX_README]
    except Exception:
        pass

    key_names = {
        "package.json": "package.json",
        "cargo.toml": "Cargo.toml",
        "pyproject.toml": "pyproject.toml",
        "requirements.txt": "requirements.txt",
        "dockerfile": "Dockerfile",
        "license": "LICENSE",
        "contributing.md": "CONTRIBUTING.md",
        "changelog.md": "CHANGELOG.md",
    }
    try:
        root = await client.root_files(owner, repo)
        present = {item["name"].lower(): item["name"] for item in root}
        for lower, actual in key_names.items():
            if lower in present:
                try:
                    analysis.key_files[actual] = (await client.file(owner, repo, present[lower]))[:MAX_FILE]
                except Exception:
                    continue
    except Exception:
        pass

    try:
        analysis.languages = await client.languages(owner, repo)
    except Exception:
        pass

    try:
        analysis.contributors = [
            c.get("login", "") for c in (await client.contributors(owner, repo)) if c.get("login")
        ]
    except Exception:
        pass

    try:
        rel = await client.latest_release(owner, repo)
        if rel and rel.get("tag_name"):
            analysis.latest_release = rel["tag_name"]
    except Exception:
        pass

    analysis.package_json = _parse_package_json(analysis.key_files.get("package.json", ""))
    analysis.frameworks = _detect_frameworks(analysis.package_json)
    analysis.install_commands = _extract_install_commands(analysis.readme, analysis.package_json)
    return analysis


def _parse_package_json(text: str) -> dict[str, Any]:
    try:
        return json.loads(text)
    except Exception:
        return {}


def _detect_frameworks(pkg: dict[str, Any]) -> list[str]:
    deps = {}
    for section in ("dependencies", "devDependencies", "peerDependencies"):
        deps.update(pkg.get(section) or {})
    found: list[str] = []
    for dep in deps:
        for hint, label in FRAMEWORK_HINTS.items():
            if hint in dep.lower() and label not in found:
                found.append(label)
    return found[:5]


_INSTALL_RE = re.compile(
    r"(pip install [\S]+|npm install[^\n]*|npm i[^\n]*|yarn add[^\n]*|pnpm add[^\n]*"
    r"|cargo install [^\n]+|cargo add [^\n]+|go get [^\n]+|go install [^\n]+|brew install [^\n]+"
    r"|docker run[^\n]*|docker compose up[^\n]*|uv add[^\n]*|uv pip install[^\n]*|conda install[^\n]*)",
    re.IGNORECASE,
)


def _extract_install_commands(readme: str, pkg: dict[str, Any]) -> list[str]:
    commands: list[str] = []
    for match in _INSTALL_RE.findall(readme):
        cmd = match.strip()
        if cmd not in commands:
            commands.append(cmd)
        if len(commands) >= 4:
            break
    scripts = pkg.get("scripts") or {}
    if pkg and not commands:
        commands.append("npm install")
    if scripts.get("dev") and "npm install" not in commands:
        commands.insert(0, "npm install")
    return commands
