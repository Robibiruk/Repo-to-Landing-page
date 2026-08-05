export default function Features() {
  return (
    <div className="min-h-screen bg-[#020617] px-4 pt-32 pb-20 text-foreground">
      <div className="mx-auto max-w-5xl">
        <h1 className="mb-4 text-4xl font-extrabold tracking-tight">Features</h1>
        <p className="mb-12 max-w-2xl text-lg text-muted-foreground">
          Everything you need to turn any GitHub repository into a polished product page.
        </p>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {[
            { title: "Repository Intelligence", desc: "Reads your README, code, commits, and dependencies to understand what your project does." },
            { title: "AI Copy Generation", desc: "Hero, features, FAQ, SEO — all written by AI tuned to your repo's actual content." },
            { title: "Brand Design", desc: "Every repo gets a unique color palette, typography, and layout matched to its language and vibe." },
            { title: "9 Theme Presets", desc: "Developer, Minimal, Terminal, Startup, Apple, Stripe, Linear, GitHub, Glassmorphism." },
            { title: "Quality Gate", desc: "A critic scores every page for truthfulness, specificity, and hook — and rewrites weak spots." },
            { title: "AI Rewrite", desc: "Click any block to rewrite it in a different tone: professional, funny, startup, developer." },
            { title: "One-Click Deploy", desc: "Export as ZIP or deploy directly to Netlify, Vercel, or GitHub Pages." },
            { title: "SEO Engine", desc: "Auto-generated OpenGraph, Twitter Cards, title tags, and meta descriptions." },
            { title: "Live Preview", desc: "See your landing page in a sandboxed iframe before you export or deploy." },
          ].map((f) => (
            <div key={f.title} className="glass-card rounded-xl px-6 py-8">
              <h3 className="mb-2 font-semibold">{f.title}</h3>
              <p className="text-sm text-muted-foreground">{f.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
