import { createContext, useContext, useEffect, useState, type ReactNode } from "react"

type Theme = "dark"

const ThemeCtx = createContext<{ theme: Theme; set: (t: Theme) => void }>({
  theme: "dark",
  set: () => {},
})

export function useTheme() {
  return useContext(ThemeCtx)
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme] = useState<Theme>("dark")

  useEffect(() => {
    document.documentElement.classList.add("dark")
  }, [])

  return (
    <ThemeCtx.Provider value={{ theme, set: () => {} }}>{children}</ThemeCtx.Provider>
  )
}
