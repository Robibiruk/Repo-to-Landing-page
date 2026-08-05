from dataclasses import dataclass, field

THEME_IDS = ["developer", "minimal", "terminal", "startup", "apple", "stripe", "linear", "github", "glass"]


@dataclass
class Theme:
    id: str
    label: str
    vars: dict[str, str]
    font: str
    extra_css: str = ""


BASE_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#ffffff;--surface:#ffffff;--text:#0a0a0a;--muted:#6b7280;--border:#e5e7eb;
  --accent:#6366f1;--grad-a:#6366f1;--grad-b:#22d3ee;--radius:12px;--maxw:1080px;
}
html{scroll-behavior:smooth}
body{font-family:var(--font);background:var(--bg);color:var(--text);line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 24px}
header{position:sticky;top:0;z-index:10;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--border)}
.nav{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px 0}
.logo{display:flex;align-items:center;gap:10px;font-weight:700;font-size:1.05rem}
.logo-mark{width:26px;height:26px;border-radius:7px;background:linear-gradient(135deg,var(--grad-a),var(--grad-b));display:inline-flex;align-items:center;justify-content:center;color:#fff;font-size:13px}
.btn{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--border);border-radius:var(--radius);padding:9px 16px;font-size:.9rem;font-weight:600;text-decoration:none;color:var(--text);background:var(--surface);transition:.15s}
.btn:hover{border-color:var(--accent);color:var(--accent)}
.btn.primary{background:linear-gradient(135deg,var(--grad-a),var(--grad-b));color:#fff;border:none}
.btn.primary:hover{filter:brightness(1.08);color:#fff}
.hero{padding:96px 0 72px;text-align:center}
.eyebrow{display:inline-block;font-size:.8rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);border:1px solid color-mix(in srgb,var(--accent) 35%,transparent);border-radius:999px;padding:5px 14px;margin-bottom:22px}
h1{font-size:clamp(2.2rem,5vw,3.6rem);line-height:1.1;letter-spacing:-.02em;font-weight:800;margin-bottom:18px}
.hero p{font-size:clamp(1.05rem,2vw,1.3rem);color:var(--muted);max-width:640px;margin:0 auto 30px}
.cta-row{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.stats{display:flex;gap:0;justify-content:center;margin-top:56px;border:1px solid var(--border);border-radius:var(--radius);overflow:hidden}
.stat{flex:1;min-width:120px;padding:18px 10px;text-align:center}
.stat+.stat{border-left:1px solid var(--border)}
.stat b{display:block;font-size:1.35rem;font-weight:800}
.stat span{font-size:.78rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
section{padding:72px 0}
section h2{font-size:clamp(1.6rem,3vw,2.2rem);letter-spacing:-.02em;font-weight:800;margin-bottom:14px}
.lead{color:var(--muted);max-width:680px;font-size:1.08rem}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px;margin-top:34px}
.card{border:1px solid var(--border);border-radius:var(--radius);padding:24px;background:var(--surface)}
.card .icon{width:40px;height:40px;border-radius:10px;background:color-mix(in srgb,var(--accent) 12%,transparent);display:flex;align-items:center;justify-content:center;font-size:20px;margin-bottom:14px}
.card h3{font-size:1.05rem;font-weight:700;margin-bottom:6px}
.card p{color:var(--muted);font-size:.92rem}
.code-block{background:#0b1020;color:#d6e2f4;border-radius:var(--radius);padding:20px 22px;overflow-x:auto;margin-top:20px;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.9rem}
.code-block .cmt{color:#64748b}
code.inline{background:color-mix(in srgb,var(--muted) 14%,transparent);border:1px solid var(--border);border-radius:6px;padding:2px 8px;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.85em}
.install-cmds{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}
.split{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}
@media(max-width:760px){.split{grid-template-columns:1fr}.hero{padding:64px 0 48px}}
footer{border-top:1px solid var(--border);padding:40px 0 56px}
.foot{display:flex;flex-wrap:wrap;gap:18px;align-items:center;justify-content:space-between;color:var(--muted);font-size:.9rem}
.foot a{color:var(--muted);text-decoration:none}
.foot a:hover{color:var(--accent)}
.badge{display:inline-flex;align-items:center;gap:7px;border:1px solid var(--border);border-radius:999px;padding:5px 12px;font-size:.78rem}
.badge b{color:var(--accent)}
a{color:var(--accent)}
"""

THEMES: dict[str, Theme] = {
    "developer": Theme(
        id="developer",
        label="Developer",
        font="Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
        vars={
            "--bg": "#ffffff", "--surface": "#ffffff", "--text": "#0a0a0a",
            "--muted": "#6b7280", "--border": "#e5e7eb", "--radius": "12px",
        },
    ),
    "minimal": Theme(
        id="minimal",
        label="Minimal",
        font="Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
        vars={
            "--bg": "#fafafa", "--surface": "#ffffff", "--text": "#111111",
            "--muted": "#888888", "--border": "#e8e8e8", "--radius": "16px",
        },
        extra_css="h1,h2{font-weight:600;letter-spacing:-.03em}.card{box-shadow:none}",
    ),
    "terminal": Theme(
        id="terminal",
        label="Terminal",
        font="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace",
        vars={
            "--bg": "#0d1117", "--surface": "#161b22", "--text": "#e6edf3",
            "--muted": "#8b949e", "--border": "#30363d", "--radius": "8px",
            "--accent": "#3fb950",
        },
        extra_css=".btn.primary{background:#238636}.hero h1{letter-spacing:-.01em}.eyebrow{text-transform:none;letter-spacing:.02em}",
    ),
    "startup": Theme(
        id="startup",
        label="Startup",
        font="ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
        vars={
            "--bg": "#0b0b12", "--surface": "#14141f", "--text": "#f5f5ff",
            "--muted": "#9a9ab0", "--border": "#262636", "--radius": "14px",
        },
        extra_css="h1{background:linear-gradient(135deg,var(--grad-a),var(--grad-b));-webkit-background-clip:text;background-clip:text;color:transparent}.btn{border-radius:999px}",
    ),
    "apple": Theme(
        id="apple",
        label="Apple",
        font='-apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", system-ui, sans-serif',
        vars={
            "--bg": "#ffffff", "--surface": "#ffffff", "--text": "#1d1d1f",
            "--muted": "#86868b", "--border": "#e8e8ed", "--radius": "18px",
            "--accent": "#0071e3", "--grad-a": "#0071e3", "--grad-b": "#2997ff",
        },
        extra_css="h1{letter-spacing:-.03em;font-weight:700}section h2{letter-spacing:-.02em}.btn.primary{border-radius:980px}.badge{border-radius:980px}",
    ),
    "stripe": Theme(
        id="stripe",
        label="Stripe",
        font='Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif',
        vars={
            "--bg": "#ffffff", "--surface": "#ffffff", "--text": "#1a1f36",
            "--muted": "#697386", "--border": "#e6ebf1", "--radius": "10px",
            "--accent": "#635bff", "--grad-a": "#635bff", "--grad-b": "#00d4ff",
        },
        extra_css=".card{box-shadow:0 1px 2px rgba(18,25,45,.06),0 6px 24px rgba(18,25,45,.06)}.btn.primary{box-shadow:0 2px 8px rgba(99,91,255,.4)}",
    ),
    "linear": Theme(
        id="linear",
        label="Linear",
        font='Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif',
        vars={
            "--bg": "#0d0d12", "--surface": "#17171f", "--text": "#f7f8f8",
            "--muted": "#8b8d98", "--border": "#26262f", "--radius": "8px",
            "--accent": "#5e6ad2", "--grad-a": "#5e6ad2", "--grad-b": "#8b5cf6",
        },
        extra_css=".card{background:linear-gradient(180deg,#17171f,#15151c)}.logo-mark{border-radius:6px}",
    ),
    "github": Theme(
        id="github",
        label="GitHub",
        font='-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif',
        vars={
            "--bg": "#ffffff", "--surface": "#ffffff", "--text": "#1f2328",
            "--muted": "#59636e", "--border": "#d1d9e0", "--radius": "6px",
            "--accent": "#0969da", "--grad-a": "#0969da", "--grad-b": "#1f883d",
        },
        extra_css=".card{box-shadow:0 1px 0 rgba(31,35,40,.04)}.btn{font-weight:600}",
    ),
    "glass": Theme(
        id="glass",
        label="Glassmorphism",
        font="Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif",
        vars={
            "--bg": "#f5f5ff", "--surface": "rgba(255,255,255,.55)", "--text": "#1a1a2e",
            "--muted": "#5a5a76", "--border": "rgba(255,255,255,.6)", "--radius": "16px",
        },
        extra_css=(
            "body{background:radial-gradient(at 20% 10%,rgba(99,102,241,.20),transparent 50%),"
            "radial-gradient(at 80% 20%,rgba(34,211,238,.18),transparent 50%),"
            "radial-gradient(at 50% 100%,rgba(244,114,182,.14),transparent 55%),#f5f5ff}"
            ".card{backdrop-filter:blur(14px);box-shadow:0 8px 32px rgba(31,38,135,.10)}"
            ".btn{backdrop-filter:blur(8px)}"
        ),
    ),
}


def get_theme(theme_id: str) -> Theme:
    if theme_id not in THEMES:
        theme_id = "developer"
    return THEMES[theme_id]


# Section type -> (heading, blurb). Rendered generically from real repo data or an honest pointer.
SECTION_FALLBACKS: dict[str, tuple[str, str]] = {
    "stats": ("Project health", "Live numbers straight from GitHub."),
    "roadmap": ("Roadmap", "Upcoming work is tracked openly on the GitHub issues and milestones pages."),
    "examples": ("Examples", "Real usage examples live in the repository docs and README."),
    "faq": ("FAQ", "Common questions are answered in the repository wiki and issue discussions."),
    "team": ("Team", "Meet the contributors on the repository's contributors page."),
    "changelog": ("Changelog", "Release history is published on the repository's releases page."),
    "pricing": ("Pricing", "Open source and free. See the repository for licensing details."),
}


def section_fallback(section_id: str) -> tuple[str, str]:
    return SECTION_FALLBACKS.get(section_id, (section_id.title(), "See the repository for more."))
