import { BookTable } from './components/BookTable'
import { Metric } from './components/Metric'
import { OpportunityTable } from './components/OpportunityTable'
import { useMarketSocket } from './websocket/useMarketSocket'

const money = (value: number | null) => value == null ? '—' : value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })

export default function App() {
  const { payload } = useMarketSocket()
  const summary = payload?.summary
  const hasSummary = summary && summary.buy_exchange !== null
  const updated = payload?.updated_at ? new Date(payload.updated_at * 1000).toLocaleTimeString() : '—'
  return <main className="app-shell">
    <section className="intro"><div><a className="hero-brand" href="/"><img className="hero-brand__mark" src="/logo.png" alt="arbViz logo" /><span>arbViz</span></a><p className="eyebrow">REAL-TIME SPOT ARBITRAGE</p><h1>Watch the gap. <span>Not the noise.</span></h1><p className="lede">Public order books, normalized at the top of the market. No accounts, no execution, no stale signals.</p></div><aside className="feed-note"><span className="pulse" />8 exchange feeds<br /><small>stale after 3 seconds</small></aside></section>
    <section className="metrics">
      <Metric label="Best buy" value={hasSummary ? <>{summary.buy_exchange}<em>{money(summary.buy_price)} USDT</em></> : '—'} accent="buy" />
      <Metric label="Best sell" value={hasSummary ? <>{summary.sell_exchange}<em>{money(summary.sell_price)} USDT</em></> : '—'} accent="sell" />
      <Metric label="Spread" value={hasSummary ? `+${money(summary.spread)}` : '—'} detail="USDT" />
      <Metric label="Spread %" value={hasSummary ? `+${summary.spread_percent.toFixed(3)}%` : '—'} detail="cross-venue gross" />
      <Metric label="Last update" value={updated} detail="websocket broadcast" />
    </section>
    <BookTable books={payload?.books ?? []} buy={summary?.buy_exchange} sell={summary?.sell_exchange} />
    <OpportunityTable opportunities={payload?.opportunities ?? []} />
    <footer><strong>Pricing is observation, not instruction.</strong><span>arbViz uses public websocket feeds only. Network, transfer, fee, and execution risks are not modeled.</span></footer>
  </main>
}
