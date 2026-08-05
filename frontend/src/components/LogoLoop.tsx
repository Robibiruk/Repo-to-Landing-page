import React, { useCallback, useEffect, useMemo, useRef, useState } from "react"

export type LogoItem =
  | { node: React.ReactNode; href?: string; title?: string; ariaLabel?: string }
  | { src: string; alt?: string; href?: string; title?: string; width?: number; height?: number }

export interface LogoLoopProps {
  logos: LogoItem[]
  speed?: number
  direction?: "left" | "right" | "up" | "down"
  width?: number | string
  logoHeight?: number
  gap?: number
  pauseOnHover?: boolean
  hoverSpeed?: number
  fadeOut?: boolean
  fadeOutColor?: string
  scaleOnHover?: boolean
  renderItem?: (item: LogoItem, key: React.Key) => React.ReactNode
  ariaLabel?: string
  className?: string
}

const ANIMATION_CONFIG = { SMOOTH_TAU: 0.25, MIN_COPIES: 2, COPY_HEADROOM: 2 } as const
const toCssLength = (v?: number | string) => (typeof v === "number" ? `${v}px` : v ?? undefined)
const cx = (...p: Array<string | false | null | undefined>) => p.filter(Boolean).join(" ")

const useAnimationLoop = (
  trackRef: React.RefObject<HTMLDivElement | null>,
  targetVelocity: number,
  seqSize: number,
  isHovered: boolean,
  hoverSpeed: number | undefined,
  isVertical: boolean,
) => {
  const rafRef = useRef<number | null>(null)
  const lastRef = useRef<number | null>(null)
  const offsetRef = useRef(0)
  const velRef = useRef(0)

  useEffect(() => {
    const track = trackRef.current
    if (!track) return
    const reduced = window.matchMedia?.("(prefers-reduced-motion: reduce)").matches
    if (reduced || seqSize <= 0) return () => { lastRef.current = null }

    const animate = (ts: number) => {
      rafRef.current = requestAnimationFrame(animate)
      if (lastRef.current === null) lastRef.current = ts
      const dt = Math.min((ts - lastRef.current) / 1000, 0.05)
      lastRef.current = ts
      const target = isHovered && hoverSpeed !== undefined ? hoverSpeed : targetVelocity
      velRef.current += (target - velRef.current) * (1 - Math.exp(-dt / ANIMATION_CONFIG.SMOOTH_TAU))
      offsetRef.current = ((offsetRef.current + velRef.current * dt) % seqSize + seqSize) % seqSize
      track.style.transform = isVertical
        ? `translate3d(0,${-offsetRef.current}px,0)`
        : `translate3d(${-offsetRef.current}px,0,0)`
    }
    rafRef.current = requestAnimationFrame(animate)
    return () => { if (rafRef.current != null) cancelAnimationFrame(rafRef.current); lastRef.current = null }
  }, [targetVelocity, seqSize, isHovered, hoverSpeed, isVertical, trackRef])
}

export const LogoLoop = React.memo<LogoLoopProps>(
  ({ logos, speed = 120, direction = "left", width = "100%", logoHeight = 28, gap = 32, pauseOnHover, hoverSpeed, fadeOut, fadeOutColor, scaleOnHover, renderItem, ariaLabel = "Logos", className }) => {
    const containerRef = useRef<HTMLDivElement>(null)
    const trackRef = useRef<HTMLDivElement>(null)
    const seqRef = useRef<HTMLUListElement>(null)
    const [seqSize, setSeqSize] = useState(0)
    const [copyCount, setCopyCount] = useState<number>(ANIMATION_CONFIG.MIN_COPIES)
    const [isHovered, setIsHovered] = useState(false)

    const effectiveHoverSpeed = useMemo(() => hoverSpeed ?? (pauseOnHover === true ? 0 : pauseOnHover === false ? undefined : 0), [hoverSpeed, pauseOnHover])
    const isVertical = direction === "up" || direction === "down"
    const targetVelocity = useMemo(() => {
      const mag = Math.abs(speed)
      const dirMul = isVertical ? (direction === "up" ? 1 : -1) : (direction === "left" ? 1 : -1)
      return mag * dirMul * (speed < 0 ? -1 : 1)
    }, [speed, direction, isVertical])

    const updateDims = useCallback(() => {
      const cw = containerRef.current?.clientWidth ?? 0
      const seq = seqRef.current?.getBoundingClientRect()
      const s = isVertical ? seq?.height ?? 0 : seq?.width ?? 0
      if (s > 0) {
        setSeqSize(Math.ceil(s))
        const n = Math.ceil((isVertical ? (containerRef.current?.clientHeight ?? s) : cw) / s) + ANIMATION_CONFIG.COPY_HEADROOM
        setCopyCount(Math.max(ANIMATION_CONFIG.MIN_COPIES, n))
      }
    }, [isVertical])

    useEffect(() => {
      const els = [containerRef, seqRef].filter((r) => r.current).map((r) => r.current!)
      const obs = els.map((el) => { const o = new ResizeObserver(updateDims); o.observe(el); return o })
      updateDims()
      return () => obs.forEach((o) => o.disconnect())
    }, [logos, gap, logoHeight, isVertical, updateDims])

    useAnimationLoop(trackRef, targetVelocity, seqSize, isHovered, effectiveHoverSpeed, isVertical)

    const cssVars = useMemo(() => ({ "--logoloop-gap": `${gap}px`, "--logoloop-logoHeight": `${logoHeight}px`, ...(fadeOutColor && { "--logoloop-fadeColor": fadeOutColor }) }) as React.CSSProperties, [gap, logoHeight, fadeOutColor])

    const rootCls = useMemo(() => cx("relative group", isVertical ? "overflow-hidden h-full inline-block" : "overflow-x-hidden", scaleOnHover && "py-[calc(var(--logoloop-logoHeight)*0.1)]", className), [isVertical, scaleOnHover, className])

    const renderLogoItem = useCallback((item: LogoItem, key: React.Key) => {
      const isNode = "node" in item
      const content = isNode ? (
        <span className={cx("inline-flex items-center", scaleOnHover && "transition-transform duration-300 group-hover/item:scale-120")} aria-hidden={!!(item as any).href && !(item as any).ariaLabel}>{(item as any).node}</span>
      ) : (
        <img className={cx("h-[var(--logoloop-logoHeight)] w-auto block object-contain pointer-events-none", scaleOnHover && "transition-transform duration-300 group-hover/item:scale-120")} src={(item as any).src} alt={(item as any).alt ?? ""} title={(item as any).title} loading="lazy" decoding="async" draggable={false} />
      )
      const inner = (item as any).href ? (
        <a className="inline-flex items-center no-underline rounded transition-opacity duration-200 hover:opacity-80" href={(item as any).href} target="_blank" rel="noreferrer noopener">{content}</a>
      ) : content
      return (
        <li key={key} role="listitem" className={cx("flex-none text-[length:var(--logoloop-logoHeight)] leading-[1]", isVertical ? "mb-[var(--logoloop-gap)]" : "mr-[var(--logoloop-gap)]", scaleOnHover && "overflow-visible group/item")}>
          {inner}
        </li>
      )
    }, [isVertical, scaleOnHover, renderItem])

    const lists = useMemo(() => Array.from({ length: copyCount }, (_, ci) => (
      <ul className={cx("flex items-center", isVertical && "flex-col")} key={`c${ci}`} role="list" aria-hidden={ci > 0} ref={ci === 0 ? seqRef : undefined}>
        {logos.map((item, ii) => renderLogoItem(item, `${ci}-${ii}`))}
      </ul>
    )), [copyCount, logos, renderLogoItem, isVertical])

    return (
      <div ref={containerRef} className={rootCls} style={{ width: toCssLength(width), ...cssVars }} role="region" aria-label={ariaLabel}>
        {fadeOut && !isVertical && (
          <>
            <div aria-hidden className="pointer-events-none absolute inset-y-0 left-0 z-10 w-[clamp(24px,8%,120px)] bg-[linear-gradient(to_right,var(--logoloop-fadeColor,var(--logoloop-fadeColorAuto))_0%,rgba(0,0,0,0)_100%)]" />
            <div aria-hidden className="pointer-events-none absolute inset-y-0 right-0 z-10 w-[clamp(24px,8%,120px)] bg-[linear-gradient(to_left,var(--logoloop-fadeColor,var(--logoloop-fadeColorAuto))_0%,rgba(0,0,0,0)_100%)]" />
          </>
        )}
        <div className={cx("flex will-change-transform select-none relative z-0", isVertical ? "flex-col h-max w-full" : "flex-row w-max")} ref={trackRef} onMouseEnter={() => { if (effectiveHoverSpeed !== undefined) setIsHovered(true) }} onMouseLeave={() => { if (effectiveHoverSpeed !== undefined) setIsHovered(false) }}>
          {lists}
        </div>
      </div>
    )
  },
)
LogoLoop.displayName = "LogoLoop"
export default LogoLoop
