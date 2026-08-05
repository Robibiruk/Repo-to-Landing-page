export default function Gallery() {
  return (
    <div className="min-h-screen bg-[#020617] px-4 pt-32 pb-20 text-foreground">
      <div className="mx-auto max-w-5xl">
        <h1 className="mb-4 text-4xl font-extrabold tracking-tight">Gallery</h1>
        <p className="mb-12 max-w-2xl text-lg text-muted-foreground">
          Community-generated landing pages. Browse what others have built with RepoPages.
        </p>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="glass-card flex aspect-video items-center justify-center rounded-xl">
              <span className="text-sm text-muted-foreground">Coming soon</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
