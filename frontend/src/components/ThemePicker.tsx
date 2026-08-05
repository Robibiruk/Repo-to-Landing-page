import { cn } from "@/lib/utils"
import type { ThemeInfo } from "@/types"

interface Props {
  themes: ThemeInfo[]
  selected: string
  onChange: (id: string) => void
  disabled: boolean
}

export function ThemePicker({ themes, selected, onChange, disabled }: Props) {
  return (
    <div className="flex flex-wrap items-center gap-2">
      <span className="text-sm text-muted-foreground">Theme</span>
      {themes.map((t) => {
        const active = t.id === selected
        return (
          <button
            key={t.id}
            type="button"
            onClick={() => onChange(t.id)}
            disabled={disabled}
            className={cn(
              "rounded-full border px-3.5 py-1.5 text-sm font-medium transition-colors",
              active
                ? "border-primary bg-primary text-primary-foreground"
                : "border-input bg-background text-muted-foreground hover:text-foreground",
              disabled && "opacity-50",
            )}
          >
            {t.label}
          </button>
        )
      })}
    </div>
  )
}
