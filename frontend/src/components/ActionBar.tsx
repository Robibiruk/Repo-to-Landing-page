import { Download, ExternalLink, Github, RefreshCw, Rocket } from "lucide-react"

import { exportUrl } from "@/api"
import { buttonVariants } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface Props {
  contentId: string | null
  theme: string
  html: string
  repoUrl: string
  repoName: string
  onRegenerate: () => void
  disabled: boolean
}

export function ActionBar({ contentId, theme, html, repoUrl, repoName, onRegenerate, disabled }: Props) {
  const openNewTab = () => {
    const blob = new Blob([html], { type: "text/html" })
    const url = URL.createObjectURL(blob)
    window.open(url, "_blank")
  }

  return (
    <div className="flex flex-wrap items-center gap-2">
      {contentId ? (
        <a
          href={exportUrl(contentId, theme)}
          className={cn(buttonVariants({ size: "sm" }), "gap-2")}
        >
          <Download className="size-4" />
          Download ZIP
        </a>
      ) : null}

      <button
        type="button"
        onClick={onRegenerate}
        disabled={disabled}
        className={cn(buttonVariants({ variant: "outline", size: "sm" }), "gap-2")}
      >
        <RefreshCw className={cn("size-4", disabled && "animate-spin")} />
        Regenerate
      </button>

      <button
        type="button"
        onClick={openNewTab}
        disabled={disabled}
        className={cn(buttonVariants({ variant: "outline", size: "sm" }), "gap-2")}
      >
        <ExternalLink className="size-4" />
        Open preview
      </button>

      <a
        href={repoUrl}
        target="_blank"
        rel="noopener noreferrer"
        className={cn(buttonVariants({ variant: "ghost", size: "sm" }), "gap-2")}
      >
        <Github className="size-4" />
        {repoName}
      </a>

      <button
        type="button"
        disabled
        title="Deploy to a free host is coming in the next phase"
        className={cn(buttonVariants({ size: "sm" }), "ml-auto gap-2 opacity-70")}
      >
        <Rocket className="size-4" />
        Deploy — coming soon
      </button>
    </div>
  )
}
