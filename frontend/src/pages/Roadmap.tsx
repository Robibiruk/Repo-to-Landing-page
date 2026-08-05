export default function Roadmap() {
  return (
    <div className="min-h-screen bg-[#020617] px-4 pt-32 pb-20 text-foreground">
      <div className="mx-auto max-w-3xl">
        <h1 className="mb-4 text-4xl font-extrabold tracking-tight">Roadmap</h1>
        <p className="mb-12 text-lg text-muted-foreground">What's planned for RepoPages.</p>
        <div className="space-y-8">
          {[
            { status: "done", title: "v0.1 — Vertical Slice", items: ["AI copy generation", "Quality gate", "9 themes", "AI rewrite", "ZIP export"] },
            { status: "next", title: "Phase 1 — Growth Features", items: ["Deploy wiring (Surge/Netlify)", "Live GitHub widgets", "Before/after preview", "More theme presets", "Share-loop badge"] },
            { status: "future", title: "Phase 2 — Platform", items: ["Gallery + community showcase", "Custom domains", "Analytics", "GitHub Action", "Browser extension"] },
          ].map((phase) => (
            <div key={phase.title} className="glass-card rounded-xl px-6 py-8">
              <div className="mb-4 flex items-center gap-2">
                <span className={`size-2.5 rounded-full ${phase.status === "done" ? "bg-green-500" : phase.status === "next" ? "bg-primary" : "bg-muted"}`} />
                <h3 className="font-semibold">{phase.title}</h3>
              </div>
              <ul className="space-y-1 text-sm text-muted-foreground">
                {phase.items.map((item) => (
                  <li key={item}>• {item}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
