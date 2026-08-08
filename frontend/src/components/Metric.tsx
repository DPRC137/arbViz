import type { ReactNode } from 'react'

export function Metric({ label, value, accent, detail }: { label: string; value: ReactNode; accent?: 'buy' | 'sell'; detail?: string }) {
  return <article className={`metric metric--${accent ?? 'neutral'}`}>
    <span className="metric__label">{label}</span>
    <strong className="metric__value">{value}</strong>
    {detail && <span className="metric__detail">{detail}</span>}
  </article>
}
