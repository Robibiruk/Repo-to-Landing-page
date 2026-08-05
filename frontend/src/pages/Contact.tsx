export default function Contact() {
  return (
    <div className="min-h-screen bg-[#020617] px-4 pt-32 pb-20 text-foreground">
      <div className="mx-auto max-w-3xl">
        <h1 className="mb-4 text-4xl font-extrabold tracking-tight">Contact</h1>
        <p className="mb-12 text-lg text-muted-foreground">Get in touch for support, partnerships, or feedback.</p>
        <div className="space-y-6">
          <a href="https://x.com/ynwrobii" target="_blank" rel="noopener noreferrer" className="glass-card block rounded-xl px-6 py-6 transition hover:ring-1 hover:ring-primary/40">
            <h3 className="font-semibold">X (Twitter)</h3>
            <p className="text-sm text-muted-foreground">@ynwrobii — DMs open</p>
          </a>
          <a href="https://www.linkedin.com/in/robel-biruk-5923101b5/" target="_blank" rel="noopener noreferrer" className="glass-card block rounded-xl px-6 py-6 transition hover:ring-1 hover:ring-primary/40">
            <h3 className="font-semibold">LinkedIn</h3>
            <p className="text-sm text-muted-foreground">Robel Biruk</p>
          </a>
          <a href="https://github.com/Robibiruk" target="_blank" rel="noopener noreferrer" className="glass-card block rounded-xl px-6 py-6 transition hover:ring-1 hover:ring-primary/40">
            <h3 className="font-semibold">GitHub</h3>
            <p className="text-sm text-muted-foreground">Robibiruk — open issues welcome</p>
          </a>
        </div>
      </div>
    </div>
  )
}
