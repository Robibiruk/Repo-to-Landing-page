import { useEffect, useRef, useState } from "react"
import {
  Brain,
  LayoutGrid,
  Rocket,
} from "lucide-react"

import { generate, getThemes, preview } from "./api"
import { ActionBar } from "./components/ActionBar"
import Lightfall from "./components/Lightfall"
import { PipelineSteps } from "./components/PipelineSteps"
import { RewritePanel } from "./components/RewritePanel"
import { ThemePicker } from "./components/ThemePicker"
import { UrlForm } from "./components/UrlForm"
import type { GenerateResponse, LandingContent, PipelineStep, ThemeInfo } from "./types"

const FEATURES = [
  {
    icon: Brain,
    title: "Repository Intelligence",
    body: "Our AI reads your codebase, README, and commits to truly understand your product's value proposition.",
  },
  {
    icon: LayoutGrid,
    title: "Bento Grid Designs",
    body: "Automatically maps your features into modern, high-converting layouts using premium UI components.",
  },
  {
    icon: Rocket,
    title: "One-Click Deploy",
    body: "Export to Netlify, Vercel, or deploy directly to GitHub with a single click. Fully customizable.",
  },
]

const TRUSTED_BY = [
  { name: "OpenSource", icon: Rocket },
  { name: "HackathonPro", icon: Rocket },
  { name: "API Builders", icon: LayoutGrid },
  { name: "DevTools Inc", icon: Brain },
]

const FOOTER_LINKS = [
  { heading: "Product", links: ["Features", "Gallery", "Templates", "Pricing"] },
  { heading: "Resources", links: ["Docs", "API", "Blog", "Changelog"] },
  { heading: "Community", links: ["GitHub", "Discord", "Twitter"] },
]

export default function App() {
  const [themes, setThemes] = useState<ThemeInfo[]>([])
  const [step, setStep] = useState<PipelineStep>("idle")
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<GenerateResponse | null>(null)
  const [theme, setTheme] = useState("developer")
  const [refreshing, setRefreshing] = useState(false)
  const resultRef = useRef<HTMLDivElement>(null)

  const themeRef = useRef(theme)
  useEffect(() => {
    themeRef.current = theme
  }, [theme])

  useEffect(() => {
    getThemes()
      .then(setThemes)
      .catch(() => setThemes([]))
  }, [])

  // Observe fade-up elements
  useEffect(() => {
    const els = document.querySelectorAll<HTMLElement>(".fade-up")
    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("visible")
          }
        })
      },
      { threshold: 0.1 },
    )
    els.forEach((el) => obs.observe(el))
    return () => els.forEach((el) => obs.unobserve(el))
  }, [step, result])

  const doGenerate = async (url: string) => {
    setStep("analyzing")
    setError(null)
    setResult(null)
    const timers = [
      window.setTimeout(() => setStep("generating"), 800),
      window.setTimeout(() => setStep("rendering"), 2000),
    ]
    try {
      const res = await generate(url, themeRef.current)
      timers.forEach(clearTimeout)
      setResult(res)
      setTheme(res.theme)
      setStep("done")
      setTimeout(() => {
        resultRef.current?.scrollIntoView({ behavior: "smooth", block: "start" })
      }, 100)
    } catch (e) {
      timers.forEach(clearTimeout)
      setError(e instanceof Error ? e.message : "Something went wrong")
      setStep("error")
    }
  }

  const handleTheme = async (id: string) => {
    setTheme(id)
    if (!result) return
    setRefreshing(true)
    try {
      const res = await preview(result.content_id, id)
      setResult((prev) => (prev ? { ...prev, html: res.html, theme: res.theme } : prev))
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to switch theme")
    } finally {
      setRefreshing(false)
    }
  }

  const handleRewrite = (html: string, content: LandingContent) => {
    setResult((prev) => (prev ? { ...prev, html, content } : prev))
  }

  const busy = step === "analyzing" || step === "generating" || step === "rendering"

  return (
    <div className="min-h-screen overflow-x-hidden">
      {/* ——— NAV ——— */}
      <nav className="glass-nav fixed top-4 left-1/2 z-50 flex w-[calc(100%-2rem)] max-w-3xl -translate-x-1/2 items-center justify-between gap-4 rounded-full px-5 py-3 shadow-lg shadow-primary/5">
        <div className="flex items-center gap-2 font-semibold">
          <img src="/favicon/icons8-web-windows-11-color-96.png" alt="" className="size-10" />
          RepoPages
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => {
              document.getElementById("hero-input")?.scrollIntoView({ behavior: "smooth" })
            }}
            className="rounded-full bg-primary px-5 py-2 text-sm font-semibold text-primary-foreground shadow-md shadow-primary/20 transition hover:bg-primary/90 active:scale-95"
          >
            Generate
          </button>
        </div>
      </nav>

      {/* ——— HERO ——— */}
      <section className="relative flex flex-col items-center overflow-hidden px-4 pt-32 pb-20 text-center">
        {/* Gradient backdrop — dark: Lightfall WebGL, light: CSS radial */}
        <div className="pointer-events-none absolute inset-0 -z-10" aria-hidden="true">
          <Lightfall
            className="absolute inset-0"
            colors={["#A6C8FF", "#5227FF", "#FF9FFC"]}
            backgroundColor="#020617"
            speed={0.4}
            streakCount={2}
            streakWidth={1.2}
            streakLength={1.1}
            glow={0.9}
            density={0.5}
            twinkle={0.8}
            zoom={3}
            backgroundGlow={0.4}
            opacity={1}
            mouseInteraction
            mouseStrength={0.4}
            mouseRadius={1.2}
            mixBlendMode="screen"
          />
          {/* Fade mask into next section */}
          <div
            className="absolute bottom-0 left-0 right-0 h-40"
            style={{
              background: "linear-gradient(to bottom, transparent 0%, #020617 100%)",
            }}
          />
        </div>

        <h1 className="mx-auto max-w-4xl text-5xl font-extrabold leading-[1.08] tracking-tight text-foreground sm:text-6xl md:text-7xl">
          Turn Any GitHub Repository Into a{" "}
          <span className="text-gradient">Beautiful Product Website</span>
        </h1>

        <p className="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground" style={{ lineHeight: 1.6 }}>
          Paste a GitHub URL. RepoPages understands your project, generates beautiful
          copy, designs a landing page, and lets you deploy it in minutes.
        </p>

        {/* Input pill */}
        <div id="hero-input" className="relative mt-10 w-full max-w-2xl">
          <UrlForm onGenerate={doGenerate} disabled={busy} />
        </div>

        {/* Working steps */}
        {busy && (
          <div className="mt-10 fade-up">
            <PipelineSteps step={step as "analyzing" | "generating" | "rendering"} />
          </div>
        )}

        {error && (
          <div className="mt-6 w-full max-w-2xl rounded-xl border border-destructive/40 bg-destructive/5 px-5 py-3 text-sm text-destructive">
            {error}
          </div>
        )}

        {/* Browser mockup / preview frame */}
        <div className="fade-up mx-auto mt-12 w-full max-w-4xl rounded-xl border border-border/60 bg-card/80 shadow-2xl shadow-primary/5 backdrop-blur-sm">
          <div className="flex items-center gap-1.5 border-b border-border/40 bg-muted/30 px-4 py-2.5">
            <span className="size-2.5 rounded-full bg-red-400" />
            <span className="size-2.5 rounded-full bg-yellow-400" />
            <span className="size-2.5 rounded-full bg-green-400" />
          </div>
          {result ? (
            <iframe
              title="Landing page preview"
              sandbox=""
              srcDoc={result.html}
              className="h-[60vh] w-full bg-white"
            />
          ) : (
            <div className="flex h-[60vh] items-center justify-center bg-gradient-to-br from-muted/20 to-muted/5">
              <p className="text-muted-foreground">
                Your generated landing page will appear here
              </p>
            </div>
          )}
        </div>
      </section>

      {/* ——— RESULT CONTROLS (only after generate) ——— */}
      {result && (
        <section ref={resultRef} className="mx-auto max-w-5xl space-y-5 px-4 py-12">
          <ThemePicker themes={themes} selected={theme} onChange={handleTheme} disabled={refreshing} />
          <ActionBar
            contentId={result.content_id}
            theme={result.theme}
            html={result.html}
            repoUrl={result.repo.url}
            repoName={result.repo.full_name}
            onRegenerate={() => doGenerate(result.repo.url)}
            disabled={refreshing}
          />
          <RewritePanel
            content={result.content}
            contentId={result.content_id}
            theme={result.theme}
            disabled={refreshing}
            onRewritten={handleRewrite}
          />
        </section>
      )}

      {/* ——— TRUSTED BY ——— */}
      <section className="fade-up border-y border-border/40 bg-card/50 py-12 text-center">
        <p className="mb-6 font-mono text-xs font-semibold uppercase tracking-[0.1em] text-muted-foreground">
          Trusted by hackathons & indie hackers
        </p>
        <div className="mx-auto flex max-w-2xl flex-wrap items-center justify-center gap-8 text-sm font-semibold text-muted-foreground">
          {TRUSTED_BY.map((t) => (
            <div key={t.name} className="flex items-center gap-2 opacity-50 grayscale transition hover:opacity-100 hover:grayscale-0">
              <t.icon className="size-4" />
              {t.name}
            </div>
          ))}
        </div>
      </section>

      {/* ——— FEATURES ——— */}
      <section className="fade-up px-4 py-32 text-center">
        <h2 className="text-gradient mx-auto mb-4 max-w-md text-3xl font-bold tracking-tight sm:text-4xl">
          AI-Powered Developer Experience
        </h2>
        <p className="mx-auto mb-16 max-w-xl text-lg text-muted-foreground" style={{ lineHeight: 1.6 }}>
          Everything you need to showcase your project, without writing a single line of marketing copy.
        </p>
        <div className="mx-auto grid max-w-5xl gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map((f) => (
            <div
              key={f.title}
              className="glass-card fade-up group rounded-xl px-8 py-10 text-left transition hover:-translate-y-1 hover:shadow-xl"
            >
              <div className="mb-5 flex size-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
                <f.icon className="size-6" />
              </div>
              <h3 className="mb-2 text-lg font-semibold">{f.title}</h3>
              <p className="text-sm leading-relaxed text-muted-foreground">{f.body}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ——— FOOTER ——— */}
      <footer className="border-t border-border/40 bg-card/30 px-4 py-16">
        <div className="mx-auto grid max-w-5xl gap-10 sm:grid-cols-2 md:grid-cols-4">
          {/* Brand */}
          <div>
            <div className="flex items-center gap-2 font-semibold">
              <img src="/favicon/icons8-web-windows-11-color-96.png" alt="" className="size-10" />
              RepoPages
            </div>
            <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
              Turn any open-source project into a polished product page.
            </p>
          </div>
          {FOOTER_LINKS.map((col) => (
            <div key={col.heading}>
              <h4 className="mb-4 text-sm font-semibold uppercase tracking-wide text-foreground">
                {col.heading}
              </h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                {col.links.map((link) => (
                  <li key={link}>
                    <a href="#" className="transition hover:text-primary">
                      {link}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className="mx-auto mt-12 max-w-5xl border-t border-border/40 pt-8 text-xs text-muted-foreground">
          © 2026 RepoPages. Built for developers.
        </div>
      </footer>
    </div>
  )
}
