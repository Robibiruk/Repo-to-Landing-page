interface Props {
  html: string
  repoName: string
}

export function PreviewFrame({ html, repoName }: Props) {
  return (
    <div className="overflow-hidden rounded-xl border bg-muted/30 shadow-sm">
      <div className="flex items-center gap-1.5 border-b bg-muted/40 px-4 py-2.5">
        <span className="size-2.5 rounded-full bg-red-400" />
        <span className="size-2.5 rounded-full bg-yellow-400" />
        <span className="size-2.5 rounded-full bg-green-400" />
        <span className="ml-2 truncate font-mono text-xs text-muted-foreground">
          {repoName} — landing page preview
        </span>
      </div>
      <iframe
        title="Landing page preview"
        sandbox=""
        srcDoc={html}
        className="h-[70vh] w-full bg-white"
      />
    </div>
  )
}
