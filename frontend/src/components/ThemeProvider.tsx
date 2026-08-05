import { createContext, useContext, useEffect, useState, type ReactNode } from "react"

type Theme = "light" | "dark" | "system"

const ThemeCtx = createContext<{ theme: Theme; set: (t: Theme) => void }>({
  theme: "system",
  set: () => {},
})

export function useTheme() {
  return useContext(ThemeCtx)
}

function applyTheme(theme: Theme) {
  const root = document.documentElement
  const prefersDark =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-color-scheme: dark)").matches

  if (theme === "dark" || (theme === "system" && prefersDark)) {
    root.classList.add("dark")
  } else {
    root.classList.remove("dark")
  }
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>(() => {
    try {
      return (localStorage.getItem("rp-theme") as Theme) || "system"
    } catch {
      return "system"
    }
  })

  useEffect(() => {
    try {
      localStorage.setItem("rp-theme", theme)
    } catch {}
    applyTheme(theme)
  }, [theme])

  // Listen for system color-scheme changes when in system mode
  useEffect(() => {
    if (theme !== "system") return
    const mq = window.matchMedia("(prefers-color-scheme: dark)")
    const handler = () => applyTheme("system")
    mq.addEventListener("change", handler)
    return () => mq.removeEventListener("change", handler)
  }, [theme])

  // Apply on mount
  useEffect(() => {
    applyTheme(theme)
  }, [])

  return (
    <ThemeCtx.Provider value={{ theme, set: setTheme }}>{children}</ThemeCtx.Provider>
  )
}
