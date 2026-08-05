import { Check, Loader2 } from "lucide-react"

import { cn } from "@/lib/utils"
import type { PipelineStep } from "@/types"

const STEPS: { id: "analyzing" | "generating" | "rendering"; label: string }[] = [
  { id: "analyzing", label: "Analyzing repository" },
  { id: "generating", label: "Generating brand & copy" },
  { id: "rendering", label: "Rendering page" },
]

interface Props {
  step: Extract<PipelineStep, "analyzing" | "generating" | "rendering">
}

export function PipelineSteps({ step }: Props) {
  const activeIdx = STEPS.findIndex((s) => s.id === step)
  return (
    <ol className="mx-auto flex max-w-md flex-col gap-3 text-sm">
      {STEPS.map((s, i) => {
        const done = i < activeIdx
        const active = i === activeIdx
        return (
          <li key={s.id} className="flex items-center gap-3">
            {done ? (
              <Check className="size-4 shrink-0 text-primary" />
            ) : active ? (
              <Loader2 className="size-4 shrink-0 animate-spin text-primary" />
            ) : (
              <span className="size-4 shrink-0 rounded-full border border-border" />
            )}
            <span className={cn("text-muted-foreground", active && "font-medium text-foreground")}>
              {s.label}
            </span>
          </li>
        )
      })}
    </ol>
  )
}
