export default function Docs() {
  return (
    <div className="min-h-screen bg-[#020617] px-4 pt-32 pb-20 text-foreground">
      <div className="mx-auto max-w-3xl">
        <h1 className="mb-4 text-4xl font-extrabold tracking-tight">Documentation</h1>
        <p className="mb-12 text-lg text-muted-foreground">Everything you need to get started with RepoPages.</p>
        <div className="space-y-6">
          {[
            { title: "Quick Start", desc: "Paste a GitHub URL, pick a theme, deploy in 30 seconds." },
            { title: "Themes & Customization", desc: "Choose from 9 presets or customize colors, fonts, and layout." },
            { title: "API Reference", desc: "Integrate RepoPages into your CI/CD pipeline with our REST API." },
            { title: "Deployment Guide", desc: "Deploy to Vercel, Netlify, GitHub Pages, or any static host." },
            { title: "GitHub Action", desc: "Auto-rebuild your landing page on every release." },
          ].map((d) => (
            <a key={d.title} href="#" className="glass-card block rounded-xl px-6 py-6 transition hover:ring-1 hover:ring-primary/40">
              <h3 className="mb-1 font-semibold">{d.title}</h3>
              <p className="text-sm text-muted-foreground">{d.desc}</p>
            </a>
          ))}
        </div>
      </div>
    </div>
  )
}
