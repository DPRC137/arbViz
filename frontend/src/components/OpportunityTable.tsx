import type { Opportunity } from '../types/market'

const money = (value: number) => value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })

export function OpportunityTable({ opportunities }: { opportunities: Opportunity[] }) {
  return <section className="panel opportunities"><header className="panel__head"><div><p className="eyebrow">RANKED PAIRS</p><h2>Positive cross-exchange spreads</h2></div><span className="muted">Top of book only</span></header>
    <div className="table-scroll"><table><thead><tr><th>Buy Exchange</th><th>Sell Exchange</th><th>Buy Ask</th><th>Sell Bid</th><th>Spread</th><th>Spread %</th></tr></thead><tbody>
      {opportunities.map(item => <tr key={`${item.buy_exchange}-${item.sell_exchange}`}><td className="buy-name">{item.buy_exchange}</td><td className="sell-name">{item.sell_exchange}</td><td>{money(item.buy_price)}</td><td>{money(item.sell_price)}</td><td className="positive">+{money(item.spread)} USDT</td><td className="positive">+{item.spread_percent.toFixed(3)}%</td></tr>)}
      {!opportunities.length && <tr><td colSpan={6} className="empty">No positive spread across currently live feeds.</td></tr>}</tbody></table></div>
  </section>
}
