# arbViz

Real-time BTC-USDT spot top-of-book arbitrage visualizer. It uses only public exchange WebSockets and never places orders.

## Run locally

Start the backend in one terminal:

```bash
cd backend
python3 -m pip install .
uvicorn app.main:app --reload
```

Start the frontend in another:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. The backend is available at http://localhost:8000, its health endpoint is `/api/health`, and market updates stream at `/ws`.

## Docker

```bash
docker compose up --build
```

## Notes

- Supported spot pairs are BTC-USDT only: Binance, Bybit, OKX, Kraken, KuCoin, Gate.io, Bitget, and MEXC.
- A feed is excluded after three seconds without a top-of-book update.
- Rankings are gross top-of-book differences only; they intentionally exclude fees, transfers, settlement, and execution risk.
