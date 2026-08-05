import { useState, type FormEvent } from "react"
import { Search } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

interface Props {
  onGenerate: (url: string) => void
  disabled: boolean
  pill?: boolean
}

export function UrlForm({ onGenerate, disabled, pill }: Props) {
  const [url, setUrl] = useState("")
  const [error, setError] = useState("")

  const submit = (e: FormEvent) => {
    e.preventDefault()
    const trimmed = url.trim()
    if (!trimmed) {
      setError("Paste a GitHub repository URL first.")
      return
    }
    setError("")
    onGenerate(trimmed)
  }

  return (
    <form
      onSubmit={submit}
      className={
        pill
          ? "relative flex w-full items-center gap-2 rounded-full border border-border/60 bg-card/80 px-2 py-2 shadow-lg shadow-primary/5 backdrop-blur-sm"
          : "w-full space-y-2"
      }
      aria-label="Generate a landing page"
    >
      <Input
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="https://github.com/owner/repo"
        disabled={disabled}
        className={
          pill
            ? "h-10 flex-1 border-0 bg-transparent text-base shadow-none focus-visible:ring-0"
            : "h-11 flex-1"
        }
        aria-label="GitHub repository URL"
      />
      <Button
        type="submit"
        disabled={disabled}
        className={pill ? "h-10 gap-2 rounded-full px-5" : "h-11 gap-2 px-6"}
      >
        <Search className="size-4" />
        Generate
      </Button>
      {error && !pill && <p className="text-sm text-destructive">{error}</p>}
      {error && pill && (
        <p className="absolute -bottom-6 left-4 text-xs text-destructive">{error}</p>
      )}
    </form>
  )
}
