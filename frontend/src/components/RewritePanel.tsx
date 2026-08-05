import { useState } from "react"
import { Wand2 } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { LandingContent, Tone } from "@/types"

const TONES: Tone[] = ["professional", "funny", "startup", "developer", "concise", "inspiring"]

interface BlockDef {
  key: string
  index: number
  label: string
  text: string
}

function buildBlocks(content: LandingContent): BlockDef[] {
  const blocks: BlockDef[] = [
    { key: "brand.tagline", index: 0, label: "Tagline", text: content.brand.tagline },
    { key: "hero.headline", index: 0, label: "Hero headline", text: content.hero.headline },
    { key: "hero.subheadline", index: 0, label: "Hero subheadline", text: content.hero.subheadline },
    { key: "hero.cta", index: 0, label: "CTA button", text: content.hero.cta },
    { key: "problem", index: 0, label: "Problem", text: content.problem },
    { key: "solution", index: 0, label: "Solution", text: content.solution },
    ...content.features.map((f, i) => ({
      key: "features.blurb" as const,
      index: i,
      label: `Feature · ${f.title}`,
      text: f.blurb,
    })),
    { key: "seo.title", index: 0, label: "SEO title", text: content.seo.title },
    { key: "seo.description", index: 0, label: "SEO description", text: content.seo.description },
  ]
  return blocks.filter((b) => b.text.trim())
}

interface Props {
  content: LandingContent
  contentId: string
  theme: string
  disabled: boolean
  onRewritten: (html: string, content: LandingContent) => void
}

export function RewritePanel({ content, contentId, theme, disabled, onRewritten }: Props) {
  const [tone, setTone] = useState<Tone>("professional")
  const [busyKey, setBusyKey] = useState<string | null>(null)
  const [error, setError] = useState("")

  const blocks = buildBlocks(content)

  const doRewrite = async (block: BlockDef) => {
    setBusyKey(block.key + block.index)
    setError("")
    try {
      const res = await import("@/api").then((m) =>
        m.rewrite(contentId, block.key, block.index, tone, theme),
      )
      onRewritten(res.html, res.content)
    } catch (e) {
      setError(e instanceof Error ? e.message : "Rewrite failed")
    } finally {
      setBusyKey(null)
    }
  }

  return (
    <Card>
      <CardHeader className="flex-row items-center justify-between space-y-0 pb-3">
        <CardTitle className="flex items-center gap-2 text-base">
          <Wand2 className="size-4 text-primary" />
          AI rewrite
        </CardTitle>
        <div className="flex items-center gap-2">
          <span className="text-sm text-muted-foreground">Tone</span>
          <select
            value={tone}
            onChange={(e) => setTone(e.target.value as Tone)}
            disabled={disabled}
            className="h-9 rounded-md border border-input bg-background px-2 text-sm"
            aria-label="Rewrite tone"
          >
            {TONES.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </div>
      </CardHeader>
      <CardContent className="space-y-2">
        {blocks.map((b) => (
          <div
            key={b.key + b.index}
            className="flex items-center gap-3 rounded-lg border px-3 py-2"
          >
            <div className="min-w-0 flex-1">
              <div className="text-xs font-medium text-muted-foreground">{b.label}</div>
              <div className="truncate text-sm">{b.text}</div>
            </div>
            <Button
              variant="outline"
              size="sm"
              disabled={disabled || busyKey === b.key + b.index}
              onClick={() => doRewrite(b)}
            >
              {busyKey === b.key + b.index ? "Rewriting…" : "Rewrite"}
            </Button>
          </div>
        ))}
        {error && <p className="pt-1 text-sm text-destructive">{error}</p>}
      </CardContent>
    </Card>
  )
}
