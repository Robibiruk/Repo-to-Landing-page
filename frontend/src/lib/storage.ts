import type { LandingContent } from "@/types"

const STORAGE_KEY = "repopages_projects"
const MAX_SAVED = 20

export interface SavedProject {
  id: string
  repoUrl: string
  repoName: string
  theme: string
  html: string
  content: LandingContent
  timestamp: number
}

export function saveProject(project: SavedProject): void {
  try {
    const existing = getProjects()
    // Remove duplicate of same repo
    const filtered = existing.filter((p) => p.repoUrl !== project.repoUrl)
    // Add to front, cap at MAX_SAVED
    const updated = [project, ...filtered].slice(0, MAX_SAVED)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated))
  } catch {
    // localStorage full or unavailable — silently fail
  }
}

export function getProjects(): SavedProject[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return []
    const parsed = JSON.parse(raw)
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

export function deleteProject(id: string): void {
  try {
    const existing = getProjects()
    localStorage.setItem(STORAGE_KEY, JSON.stringify(existing.filter((p) => p.id !== id)))
  } catch {
    // silently fail
  }
}

export function getProject(id: string): SavedProject | null {
  return getProjects().find((p) => p.id === id) ?? null
}
