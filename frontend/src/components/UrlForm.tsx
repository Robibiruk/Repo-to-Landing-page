import { useState, type FormEvent } from "react"
import { Search } from "lucide-react"
import { Button } from "@/components/ui/button"
import SpecularBorder from "./SpecularBorder"

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
    <form
      onSubmit={submit}
      className="relative flex w-full items-center gap-3 rounded-2xl border border-white/[0.06] bg-[#0a0a12]/80 px-2 py-2 shadow-lg backdrop-blur-md"
      aria-label="Generate a landing page"
    >
      <SpecularBorder
        radius={14}
        lineColor="#ffffff"
        baseColor="#252347"
        intensity={1}
        shineSize={8}
        shineFade={45}
        thickness={0.8}
        speed={0.35}
        followMouse
        proximity={250}
        className="flex-1"
      >
        <div className="flex items-center">
          <Search className="ml-4 size-5 shrink-0 text-[#6b6b80]" />
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://github.com/owner/repo"
            disabled={disabled}
            className="hero-input"
            aria-label="GitHub repository URL"
          />
        </div>
      </SpecularBorder>
      <Button
        type="submit"
        disabled={disabled}
        className="h-14 rounded-xl bg-primary px-6 font-semibold text-primary-foreground shadow-lg shadow-primary/20 transition hover:bg-primary/90 active:scale-95"
      >
        Generate
      </Button>
      {error && (
        <p className="absolute -bottom-6 left-4 text-sm text-destructive">{error}</p>
      )}
    </form>
  )
}
