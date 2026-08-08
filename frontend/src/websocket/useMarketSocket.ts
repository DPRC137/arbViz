import { useEffect, useRef, useState } from 'react'
import type { MarketPayload } from '../types/market'

const websocketUrl = () => {
  const base = import.meta.env.VITE_API_URL || window.location.origin
  return `${base.replace(/^http/, 'ws')}/ws`
}

export function useMarketSocket() {
  const [payload, setPayload] = useState<MarketPayload | null>(null)
  const retry = useRef(1000)

  useEffect(() => {
    let socket: WebSocket | undefined
    let timer: number | undefined
    let disposed = false
    const open = () => {
      socket = new WebSocket(websocketUrl())
      socket.onopen = () => { retry.current = 1000 }
      socket.onmessage = event => setPayload(JSON.parse(event.data) as MarketPayload)
      socket.onclose = () => {
        if (!disposed) { timer = window.setTimeout(open, retry.current); retry.current = Math.min(retry.current * 2, 16000) }
      }
      socket.onerror = () => socket?.close()
    }
    open()
    return () => { disposed = true; if (timer) clearTimeout(timer); socket?.close() }
  }, [])
  return { payload }
}
