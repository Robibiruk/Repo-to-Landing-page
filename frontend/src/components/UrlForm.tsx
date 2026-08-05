import { useState, type FormEvent } from "react"
import { Search } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

interface Props {
  onGenerate: (url: string) => void
  disabled: boolean
}

export function UrlForm({ onGenerate, disabled }: Props) {
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
    <form onSubmit={submit} className="w-full space-y-2" aria-label="Generate a landing page">
      <div className="flex w-full gap-2">
        <Input
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://github.com/owner/repo"
          disabled={disabled}
          className="h-11 flex-1"
          aria-label="GitHub repository URL"
        />
        <Button type="submit" disabled={disabled} className="h-11 gap-2 px-6">
          <Search className="size-4" />
          Generate
        </Button>
      </div>
      {error && <p className="text-sm text-destructive">{error}</p>}
    </form>
  )
}
