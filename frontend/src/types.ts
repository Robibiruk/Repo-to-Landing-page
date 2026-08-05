export interface FeatureCard {
  title: string
  blurb: string
  iconKey: string
}

export interface Brand {
  name: string
  tagline: string
  accent: string
  gradientFrom: string
  gradientTo: string
}

export interface Hero {
  headline: string
  subheadline: string
  cta: string
}

export interface InstallSection {
  heading: string
  commands: string[]
  snippet: string
}

export interface FooterLink {
  label: string
  url: string
}

export interface Footer {
  license: string
  links: FooterLink[]
}

export interface Seo {
  title: string
  description: string
  keywords: string[]
}

export interface LandingContent {
  brand: Brand
  hero: Hero
  problem: string
  solution: string
  features: FeatureCard[]
  install: InstallSection
  sections: string[]
  footer: Footer
  seo: Seo
}

export interface RepoInfo {
  full_name: string
  url: string
  description: string
  topics: string[]
  primary_language: string
  license: string
  stars: number
  forks: number
  contributors: string[]
  homepage: string
}

export interface GenerateResponse {
  content_id: string
  theme: string
  html: string
  content: LandingContent
  repo: RepoInfo
}

export interface PreviewResponse {
  html: string
  theme: string
}

export interface ThemeInfo {
  id: string
  label: string
}

export type PipelineStep = "idle" | "analyzing" | "generating" | "rendering" | "done" | "error"
