import type { Book } from '../types/market'

const n = (value: number) => value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })
const age = (updated: number) => `${Math.max(0, Date.now() / 1000 - updated).toFixed(1)}s ago`

export function BookTable({ books, buy, sell }: { books: Book[]; buy?: string | null; sell?: string | null }) {
  return <section className="panel"><header className="panel__head"><div><p className="eyebrow">TOP OF BOOK</p><h2>Live exchange matrix</h2></div><span className="muted">BTC / USDT · public feeds</span></header>
    <div className="table-scroll"><table><thead><tr><th>Exchange</th><th>Bid</th><th>Bid Qty</th><th>Ask</th><th>Ask Qty</th><th>Status</th><th>Latency</th><th>Updated</th></tr></thead>
      <tbody>{books.map(book => <tr key={book.exchange} className={book.status === 'stale' ? 'is-stale' : ''}><td className="exchange">{book.exchange}</td><td className={book.exchange === sell ? 'price price--sell' : 'price'}>{n(book.bid)}</td><td>{n(book.bid_qty)}</td><td className={book.exchange === buy ? 'price price--buy' : 'price'}>{n(book.ask)}</td><td>{n(book.ask_qty)}</td><td><span className={`status status--${book.status}`}><i />{book.status}</span></td><td>{book.latency_ms.toFixed(0)} ms</td><td>{age(book.updated)}</td></tr>)}
      {!books.length && <tr><td colSpan={8} className="empty">Waiting for public exchange feeds…</td></tr>}</tbody></table></div>
  </section>
}
