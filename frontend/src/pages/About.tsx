export default function About() {
  return (
    <div className="min-h-screen bg-[#020617] px-4 pt-32 pb-20 text-foreground">
      <div className="mx-auto max-w-3xl">
        <h1 className="mb-4 text-4xl font-extrabold tracking-tight">About RepoPages</h1>
        <p className="mb-12 text-lg text-muted-foreground">The publishing platform for open source.</p>
        <div className="space-y-8 text-muted-foreground">
          <p>
            Developers spend months building projects and five minutes presenting them.
            Investors, recruiters, hackathon judges, and users judge the presentation before the code.
          </p>
          <p>
            RepoPages makes every GitHub repository instantly marketable. Paste a URL,
            get a branded landing page with AI-generated copy, deploy in seconds, and share it.
          </p>
          <p>
            Built by <a href="https://x.com/ynwrobii" className="text-primary hover:underline" target="_blank" rel="noopener noreferrer">Robel Biruk</a>.
          </p>
        </div>
      </div>
    </div>
  )
}
