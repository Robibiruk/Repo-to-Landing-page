export default function Blog() {
  return (
    <div className="min-h-screen bg-[#020617] px-4 pt-32 pb-20 text-foreground">
      <div className="mx-auto max-w-3xl">
        <h1 className="mb-4 text-4xl font-extrabold tracking-tight">Blog</h1>
        <p className="mb-12 text-lg text-muted-foreground">Product updates, launch articles, and case studies.</p>
        <div className="space-y-6">
          {[
            { date: "Aug 2026", title: "Introducing RepoPages", desc: "Turn any GitHub repository into a beautiful product website in minutes." },
            { date: "Aug 2026", title: "Free Models, Premium Results", desc: "How we use open-source LLMs with a quality gate to generate great copy for free." },
          ].map((b) => (
            <a key={b.title} href="#" className="glass-card block rounded-xl px-6 py-6 transition hover:ring-1 hover:ring-primary/40">
              <span className="font-mono text-xs text-muted-foreground">{b.date}</span>
              <h3 className="mt-1 font-semibold">{b.title}</h3>
              <p className="mt-1 text-sm text-muted-foreground">{b.desc}</p>
            </a>
          ))}
        </div>
      </div>
    </div>
  )
}
