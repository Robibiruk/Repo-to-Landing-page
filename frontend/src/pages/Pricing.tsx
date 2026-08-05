export default function Pricing() {
  return (
    <div className="min-h-screen bg-[#020617] px-4 pt-32 pb-20 text-foreground">
      <div className="mx-auto max-w-4xl">
        <h1 className="mb-4 text-4xl font-extrabold tracking-tight">Pricing</h1>
        <p className="mb-12 max-w-2xl text-lg text-muted-foreground">
          Free for open source. Pro features for teams and businesses.
        </p>
        <div className="grid gap-6 sm:grid-cols-2">
          <div className="glass-card rounded-xl px-8 py-10">
            <h3 className="mb-1 text-lg font-semibold">Free</h3>
            <p className="mb-6 text-sm text-muted-foreground">For open-source projects</p>
            <ul className="mb-8 space-y-3 text-sm text-muted-foreground">
              <li>Unlimited page generations</li>
              <li>AI copy + quality gate</li>
              <li>9 theme presets</li>
              <li>ZIP export</li>
              <li>Community support</li>
            </ul>
            <div className="text-3xl font-bold">$0</div>
          </div>
          <div className="glass-card rounded-xl px-8 py-10 ring-2 ring-primary/40">
            <h3 className="mb-1 text-lg font-semibold">Pro</h3>
            <p className="mb-6 text-sm text-muted-foreground">For teams and businesses</p>
            <ul className="mb-8 space-y-3 text-sm text-muted-foreground">
              <li>Everything in Free</li>
              <li>One-click deploy</li>
              <li>Custom domains</li>
              <li>Analytics</li>
              <li>Priority support</li>
            </ul>
            <div className="text-3xl font-bold">Coming soon</div>
          </div>
        </div>
      </div>
    </div>
  )
}
