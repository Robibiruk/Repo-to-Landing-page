import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import Lenis from "lenis"
import "lenis/dist/lenis.css"

import App from "./App"
import { ThemeProvider } from "./components/ThemeProvider"
import About from "./pages/About"
import Blog from "./pages/Blog"
import Changelog from "./pages/Changelog"
import Contact from "./pages/Contact"
import Docs from "./pages/Docs"
import Features from "./pages/Features"
import Gallery from "./pages/Gallery"
import Pricing from "./pages/Pricing"
import Roadmap from "./pages/Roadmap"
import "./index.css"

const lenis = new Lenis({ autoRaf: true })
requestAnimationFrame(function raf(time) {
  lenis.raf(time)
  requestAnimationFrame(raf)
})

document.addEventListener("DOMContentLoaded", () => {
  const observer = new IntersectionObserver(
    (entries) => entries.forEach((entry) => { if (entry.isIntersecting) entry.target.classList.add("visible") }),
    { threshold: 0.1 },
  )
  document.querySelectorAll(".fade-up").forEach((el) => observer.observe(el))
})

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ThemeProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="/features" element={<Features />} />
          <Route path="/gallery" element={<Gallery />} />
          <Route path="/pricing" element={<Pricing />} />
          <Route path="/docs" element={<Docs />} />
          <Route path="/blog" element={<Blog />} />
          <Route path="/changelog" element={<Changelog />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/roadmap" element={<Roadmap />} />
          <Route path="*" element={<div className="min-h-screen bg-[#020617] flex items-center justify-center text-muted-foreground text-lg">Page not found</div>} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  </StrictMode>,
)
