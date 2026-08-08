export type Book = { exchange: string; bid: number; bid_qty: number; ask: number; ask_qty: number; updated: number; status: 'live' | 'stale'; latency_ms: number }
export type Opportunity = { buy_exchange: string; sell_exchange: string; buy_price: number; sell_price: number; spread: number; spread_percent: number }
export type MarketPayload = { summary: Opportunity | { buy_exchange: null; sell_exchange: null; buy_price: null; sell_price: null; spread: number; spread_percent: number }; books: Book[]; opportunities: Opportunity[]; updated_at: number }
