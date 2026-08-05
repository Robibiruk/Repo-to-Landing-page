import { useEffect, useRef, useState } from "react"
import { Code2, Share2, Sparkles } from "lucide-react"

import { generate, getThemes, preview } from "./api"
import { ActionBar } from "./components/ActionBar"
import { PipelineSteps } from "./components/PipelineSteps"
import { PreviewFrame } from "./components/PreviewFrame"
import { ThemePicker } from "./components/ThemePicker"
import { UrlForm } from "./components/UrlForm"
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card"
import type { GenerateResponse, PipelineStep, ThemeInfo } from "./types"

const HOW_IT_WORKS = [
  {
    icon: Sparkles,
    title: "Analyze",
    body: "We read the README, package files, topics, languages, and stats to understand what the repo actually is.",
  },
  {
    icon: Code2,
    title: "Generate",
    body: "An AI writes the brand, hero, features, and copy — tuned to the repo's language and vibe.",
  },
  {
    icon: Share2,
    title: "Share",
    body: "Preview it, pick a theme, download the static site, and deploy it anywhere for free.",
  },
]

export default function App() {
  const [themes, setThemes] = useState<ThemeInfo[]>([])
  const [step, setStep] = useState<PipelineStep>("idle")
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<GenerateResponse | null>(null)
  const [theme, setTheme] = useState("developer")
  const [refreshing, setRefreshing] = useState(false)

  const themeRef = useRef(theme)
  useEffect(() => {
    themeRef.current = theme
  }, [theme])

  useEffect(() => {
    getThemes()
      .then(setThemes)
      .catch(() => setThemes([]))
  }, [])

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

  const busy = step === "analyzing" || step === "generating" || step === "rendering"

  return (
    <div className="min-h-screen bg-background text-foreground">
      <header className="border-b">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-4">
          <div className="flex items-center gap-2 font-semibold">
            <span className="flex size-7 items-center justify-center rounded-lg bg-gradient-to-br from-indigo-500 to-cyan-400 text-sm font-bold text-white">
              R
            </span>
            RepoPages
          </div>
          <span className="hidden text-sm text-muted-foreground sm:block">
            GitHub repository → landing page
          </span>
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-4 py-14">
        <section className="mb-12 text-center">
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
            Turn any GitHub repo into a landing page
          </h1>
          <p className="mx-auto mt-4 max-w-2xl text-lg text-muted-foreground">
            Paste a repository URL. Get a branded, shareable marketing page in seconds.
          </p>
          <div className="mx-auto mt-8 max-w-2xl">
            <UrlForm onGenerate={doGenerate} disabled={busy} />
          </div>
        </section>

        {busy && (
          <section className="my-10">
            <PipelineSteps
              step={step === "analyzing" || step === "generating" || step === "rendering" ? step : "analyzing"}
            />
          </section>
        )}

        {error && (
          <section className="my-6">
            <div className="rounded-lg border border-destructive/40 bg-destructive/5 p-4 text-sm text-destructive">
              {error}
            </div>
          </section>
        )}

        {result && (
          <section className="space-y-4">
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
            <PreviewFrame html={result.html} repoName={result.repo.full_name} />
          </section>
        )}

        {!result && !busy && (
          <section className="mt-24 grid gap-4 sm:grid-cols-3">
            {HOW_IT_WORKS.map((item) => (
              <Card key={item.title}>
                <CardHeader>
                  <item.icon className="mb-2 size-6 text-primary" />
                  <CardTitle>{item.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">{item.body}</p>
                </CardContent>
              </Card>
            ))}
          </section>
        )}
      </main>

      <footer className="mt-24 border-t">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-6 text-sm text-muted-foreground">
          <span>Built with RepoPages</span>
          <span>Open source publishing — coming soon</span>
        </div>
      </footer>
    </div>
  )
}
