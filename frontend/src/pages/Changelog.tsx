export default function Changelog() {
  return (
    <div className="min-h-screen bg-[#020617] px-4 pt-32 pb-20 text-foreground">
      <div className="mx-auto max-w-3xl">
        <h1 className="mb-4 text-4xl font-extrabold tracking-tight">Changelog</h1>
        <p className="mb-12 text-lg text-muted-foreground">Release history and what's new.</p>
        <div className="space-y-8 border-l border-border/40 pl-6">
          <div className="relative">
            <span className="absolute -left-[31px] top-1 size-3 rounded-full bg-primary" />
            <span className="font-mono text-xs text-muted-foreground">Aug 5, 2026</span>
            <h3 className="mt-1 font-semibold">v0.1 — Vertical Slice</h3>
            <ul className="mt-2 space-y-1 text-sm text-muted-foreground">
              <li>• Repository analysis (README, package files, topics, contributors)</li>
              <li>• AI copy generation with free open-source models</li>
              <li>• Quality gate: critic scores + targeted rewrite</li>
              <li>• 9 theme presets</li>
              <li>• AI rewrite with 6 tone presets</li>
              <li>• ZIP export, live preview</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
