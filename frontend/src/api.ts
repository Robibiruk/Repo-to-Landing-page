import type { GenerateResponse, PreviewResponse, ThemeInfo } from "./types"

const BASE = "/api"

async function read<T>(res: Response): Promise<T> {
  const data = await res.json().catch(() => null)
  if (!res.ok) {
    const detail = data && typeof data.detail === "string" ? data.detail : `Request failed (${res.status})`
    throw new Error(detail)
  }
  return data as T
}

export async function getThemes(): Promise<ThemeInfo[]> {
  const res = await fetch(`${BASE}/themes`)
  return read<ThemeInfo[]>(res)
}

export async function generate(repoUrl: string, theme: string): Promise<GenerateResponse> {
  const res = await fetch(`${BASE}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ repo_url: repoUrl, theme }),
  })
  return read<GenerateResponse>(res)
}

export async function preview(contentId: string, theme: string): Promise<PreviewResponse> {
  const res = await fetch(`${BASE}/preview`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content_id: contentId, theme }),
  })
  return read<PreviewResponse>(res)
}

export function exportUrl(contentId: string, theme: string): string {
  return `${BASE}/export?content_id=${encodeURIComponent(contentId)}&theme=${encodeURIComponent(theme)}`
}
