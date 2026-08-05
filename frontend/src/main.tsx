import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import Lenis from "lenis"
import "lenis/dist/lenis.css"

import App from "./App"
import { ThemeProvider } from "./components/ThemeProvider"
import "./index.css"

// Smooth scroll
const lenis = new Lenis({ autoRaf: true })

requestAnimationFrame(function raf(time) {
  lenis.raf(time)
  requestAnimationFrame(raf)
})

// IntersectionObserver for fade-up reveals on DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible")
        }
      })
    },
    { threshold: 0.1 },
  )
  document.querySelectorAll(".fade-up").forEach((el) => observer.observe(el))
})

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </StrictMode>,
)
