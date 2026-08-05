from __future__ import annotations

from html import escape as esc

from .repo_analysis import RepoAnalysis
from .schemas import LandingContent
from .themes import BASE_CSS, Theme, get_theme, section_fallback

ICON_PATHS: dict[str, str] = {
    "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    "code": '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
    "terminal": '<polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "chart": '<line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/>',
    "spark": '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
    "box": '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>',
}


def _icon(key: str) -> str:
    path = ICON_PATHS.get(key, ICON_PATHS["spark"])
    return f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{path}</svg>'


def _count(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}k"
    return str(n)


def render_landing(analysis: RepoAnalysis, content: LandingContent, theme_id: str = "developer") -> str:
    theme = get_theme(theme_id)
    repo_url = f"https://github.com/{analysis.owner}/{analysis.repo}"
    accent = content.brand.accent or analysis.accent_color
    ga, gb = content.brand.gradientFrom or accent, content.brand.gradientTo or "#22d3ee"

    vars_css = "\n".join(f"{k}:{v};" for k, v in theme.vars.items())
    vars_css += f"\n--accent:{esc(accent, quote=True)};--grad-a:{esc(ga, quote=True)};--grad-b:{esc(gb, quote=True)};--font:{theme.font};"
    css = f":root{{{vars_css}}}\n{BASE_CSS}\n{theme.extra_css}"

    brand_name = content.brand.name or analysis.display_name
    stat_items = [
        ("Stars", _count(analysis.stars)),
        ("Forks", _count(analysis.forks)),
        ("Contributors", str(len(analysis.contributors))),
        ("License", esc(analysis.license_name or "—")),
    ]
    stats_html = ""
    if analysis.stars or analysis.forks or analysis.contributors:
        cells = "".join(
            f'<div class="stat"><b>{val}</b><span>{label}</span></div>' for label, val in stat_items
        )
        stats_html = f'<div class="stats">{cells}</div>'

    feature_cards = "".join(
        f'<div class="card"><div class="icon">{_icon(f.iconKey)}</div><h3>{esc(f.title)}</h3><p>{esc(f.blurb)}</p></div>'
        for f in content.features
    )

    install_html = ""
    if content.install.heading or content.install.commands or content.install.snippet:
        chips = "".join(
            f'<code class="inline">{esc(c)}</code>' for c in content.install.commands[:6]
        )
        snippet_html = ""
        if content.install.snippet:
            snippet_html = (
                '<div class="code-block" style="white-space:pre">'
                f'<span class="cmt"># {esc(content.install.heading or "Quick start")}</span>\n'
                f"{esc(content.install.snippet)}</div>"
            )
        install_html = (
            "<section id=\"install\"><div class=\"wrap\">"
            f"<h2>{esc(content.install.heading or 'Get started')}</h2>"
            f'<div class="install-cmds">{chips}</div>{snippet_html}</div></section>'
        )

    extra_sections = ""
    for sid in content.sections:
        heading, blurb = section_fallback(sid)
        body = f"<p class=\"lead\">{esc(blurb)}</p>"
        if sid == "stats":
            body = _render_stats_body(analysis)
        elif sid == "team" and analysis.contributors:
            body = "<p class=\"lead\">" + ", ".join(esc(u) for u in analysis.contributors) + "</p>"
        extra_sections += (
            f'<section id="{esc(sid)}"><div class="wrap"><h2>{esc(heading)}</h2>{body}</div></section>'
        )

    foot_links = "".join(
        f'<a href="{esc(l.url, quote=True)}">{esc(l.label)}</a>' for l in content.footer.links[:5]
    )
    cta_target = analysis.homepage or repo_url

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{esc(content.seo.title)}</title>
<meta name="description" content="{esc(content.seo.description, quote=True)}"/>
<meta name="keywords" content="{esc(', '.join(content.seo.keywords), quote=True)}"/>
<meta property="og:title" content="{esc(content.seo.title, quote=True)}"/>
<meta property="og:description" content="{esc(content.seo.description, quote=True)}"/>
<meta property="og:type" content="website"/>
<meta name="twitter:card" content="summary"/>
<style>{css}</style>
</head>
<body>
<header><div class="wrap nav">
  <div class="logo"><span class="logo-mark">{esc(brand_name[:1].upper())}</span>{esc(brand_name)}</div>
  <a class="btn" href="{esc(repo_url, quote=True)}" target="_blank" rel="noopener">★ {_count(analysis.stars)} · View on GitHub</a>
</div></header>

<section class="hero"><div class="wrap">
  <span class="eyebrow">{esc(content.brand.tagline)}</span>
  <h1>{esc(content.hero.headline)}</h1>
  <p>{esc(content.hero.subheadline)}</p>
  <div class="cta-row">
    <a class="btn primary" href="{esc(cta_target, quote=True)}" target="_blank" rel="noopener">{esc(content.hero.cta)}</a>
    <a class="btn" href="{esc(repo_url, quote=True)}" target="_blank" rel="noopener">Explore the code</a>
  </div>
  {stats_html}
</div></section>

<section id="problem"><div class="wrap"><div class="split">
  <div><h2>The problem</h2><p class="lead">{esc(content.problem)}</p></div>
  <div><h2>The solution</h2><p class="lead">{esc(content.solution)}</p></div>
</div></div></section>

<section id="features"><div class="wrap">
  <h2>Why {esc(brand_name)}</h2>
  <div class="grid">{feature_cards}</div>
</div></section>

{install_html}
{extra_sections}

<footer><div class="wrap foot">
  <div>© {esc(brand_name)} · {esc(analysis.license_name or content.footer.license)}</div>
  <div class="foot-links">{foot_links}</div>
  <span class="badge">⚡ Built with <b>RepoPages</b></span>
</div></footer>
</body>
</html>"""
    return html


def _render_stats_body(analysis: RepoAnalysis) -> str:
    parts: list[str] = []
    if analysis.languages:
        total = sum(analysis.languages.values()) or 1
        top = sorted(analysis.languages.items(), key=lambda kv: kv[1], reverse=True)[:5]
        chips = "".join(
            f'<code class="inline">{esc(name)} {round(v / total * 100)}%</code>' for name, v in top
        )
        parts.append(f'<div class="install-cmds">{chips}</div>')
    if analysis.contributors:
        parts.append(
            '<p class="lead" style="margin-top:14px">Top contributors: '
            + ", ".join(esc(u) for u in analysis.contributors)
            + "</p>"
        )
    return "".join(parts) or '<p class="lead">Live numbers straight from GitHub.</p>'
