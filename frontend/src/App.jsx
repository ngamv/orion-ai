import Dashboard from "./Dashboard"
import { useState, useEffect, useRef } from "react"

const API = "http://127.0.0.1:8004"

export default function App() {
  const [agents, setAgents] = useState([])
  const [agent, setAgent] = useState(null)
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [memory, setMemory] = useState(null)
  const [autoRoute, setAutoRoute] = useState(false)
  const [showDashboard, setShowDashboard] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    fetch(`${API}/agents`)
      .then(r => r.json())
      .then(d => { setAgents(d.agents); setAgent(d.agents[0]) })
  }, [])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  async function refreshMemory() {
    const r = await fetch(`${API}/memory`)
    const d = await r.json()
    setMemory(d)
  }

  async function clearMemory() {
    if (!agent) return
    await fetch(`${API}/memory/${agent.id}`, { method: "DELETE" })
    setMessages([])
    refreshMemory()
  }

  async function send() {
    if (!input.trim() || loading || !agent) return
    const userMsg = { role: "user", content: input }
    setMessages(prev => [...prev, userMsg])
    const currentInput = input
    setInput("")
    setLoading(true)
    try {
const controller = new AbortController()
const timeoutId = setTimeout(() => controller.abort(), 600000)
const res = await fetch(`${API}/chat`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  signal: controller.signal,
  body: JSON.stringify({
          message: currentInput,
          agent: autoRoute ? null : agent.id
        })
      })
      const data = await res.json() 
      clearTimeout(timeoutId)
      setMessages(prev => [...prev, {
        role: "assistant",
        content: data.response,
        agent: data.agent,
        routed: data.routed_by === "auto"
      }])
      refreshMemory()
    } catch {
      setMessages(prev => [...prev, { role: "assistant", content: "❌ Erreur de connexion au backend" }])
    }
    setLoading(false)
  }

  if (!agent) return <div style={{ background: "#0f0f1a", color: "#fff", height: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>Chargement ORION AI...</div>
  if (showDashboard) return <Dashboard onBack={() => setShowDashboard(false)} />
  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "'Segoe UI', sans-serif", background: "#0f0f1a", color: "#fff" }}>

      {/* Sidebar */}
      <div style={{ width: 220, background: "#13132a", borderRight: "1px solid #2a2a3e", display: "flex", flexDirection: "column" }}>
        <div style={{ padding: "20px 16px", borderBottom: "1px solid #2a2a3e" }}>
          <div style={{ fontSize: 20, fontWeight: "bold", color: "#7c3aed" }}>🤖 ORION AI</div>
          <div style={{ fontSize: 11, color: "#555", marginTop: 4 }}>v1.0 • Qwen3:8b</div>
        </div>

        {/* Auto-route toggle */}
        <div style={{ padding: "12px 16px", borderBottom: "1px solid #2a2a3e" }}>
          <label style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer", fontSize: 12 }}>
            <input type="checkbox" checked={autoRoute} onChange={e => setAutoRoute(e.target.checked)} />
            <span style={{ color: autoRoute ? "#7c3aed" : "#666" }}>🔀 Router auto</span>
          </label>
        </div>

        {/* Agents list */}
        <div style={{ flex: 1, overflowY: "auto", padding: 8 }}>
          <div style={{ fontSize: 10, color: "#444", padding: "8px 8px 4px", letterSpacing: 1 }}>AGENTS</div>
          {agents.map(a => (
            <div
              key={a.id}
              onClick={() => { setAgent(a); setMessages([]) }}
              style={{
                padding: "10px 12px", marginBottom: 2, borderRadius: 8,
                cursor: "pointer", transition: "all 0.2s",
                background: agent.id === a.id ? "#7c3aed22" : "transparent",
                borderLeft: agent.id === a.id ? "3px solid #7c3aed" : "3px solid transparent"
              }}
            >
              <div style={{ fontSize: 13 }}>{a.emoji} {a.name}</div>
              <div style={{ fontSize: 10, color: "#555", marginTop: 2 }}>{a.team}</div>
            </div>
          ))}
        </div>

        {/* Memory status */}
        {memory && (
          <div style={{ padding: 12, borderTop: "1px solid #2a2a3e", fontSize: 11, color: "#555" }}>
            <div>🧠 Mémoire court terme : {memory.short_term_count}</div>
            <div>💾 Mémoire long terme : {memory.long_term_count}</div>
          </div>
        )}
      </div>

      {/* Main chat */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>

        {/* Header */}
        <div style={{ padding: "14px 24px", background: "#13132a", borderBottom: "1px solid #2a2a3e", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <div>
            <div style={{ fontSize: 16, fontWeight: "bold" }}>{agent.emoji} {agent.name}</div>
            <div style={{ fontSize: 11, color: "#7c3aed" }}>Équipe {agent.team} {autoRoute ? "• 🔀 Routage automatique actif" : ""}</div>
          </div>
          <button onClick={() => setShowDashboard(true)} style={{ padding: "6px 14px", borderRadius: 6, background: "#7c3aed", border: "none", color: "#fff", cursor: "pointer", fontSize: 12 }}>
            📊 Dashboard
          </button>
          <button onClick={clearMemory} style={{ padding: "6px 14px", borderRadius: 6, background: "#1a1a2e", border: "1px solid #2a2a3e", color: "#888", cursor: "pointer", fontSize: 12 }}>
            🗑️ Vider mémoire
          </button>
        </div>

        {/* Messages */}
        <div style={{ flex: 1, overflowY: "auto", padding: 24, display: "flex", flexDirection: "column", gap: 16 }}>
          {messages.length === 0 && (
            <div style={{ textAlign: "center", color: "#333", marginTop: 80 }}>
              <div style={{ fontSize: 56 }}>{agent.emoji}</div>
              <div style={{ fontSize: 20, marginTop: 12, color: "#555" }}>{agent.name}</div>
              <div style={{ fontSize: 13, color: "#333", marginTop: 6 }}>Agent {agent.team} • ORION AI</div>
            </div>
          )}
          {messages.map((m, i) => (
            <div key={i} style={{ display: "flex", justifyContent: m.role === "user" ? "flex-end" : "flex-start" }}>
              <div style={{
                maxWidth: "72%", padding: "12px 16px", borderRadius: 12,
                background: m.role === "user" ? "#7c3aed" : "#1a1a2e",
                border: m.role === "assistant" ? "1px solid #2a2a3e" : "none",
                lineHeight: 1.7, fontSize: 14
              }}>
                {m.routed && <div style={{ fontSize: 10, color: "#7c3aed", marginBottom: 6 }}>🔀 Routé vers {m.agent}</div>}
                {m.content}
              </div>
            </div>
          ))}
          {loading && (
            <div style={{ display: "flex", justifyContent: "flex-start" }}>
              <div style={{ padding: "12px 16px", borderRadius: 12, background: "#1a1a2e", border: "1px solid #2a2a3e", color: "#7c3aed", fontSize: 14 }}>
                ⏳ {agent.name} réfléchit...
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div style={{ padding: 16, background: "#13132a", borderTop: "1px solid #2a2a3e", display: "flex", gap: 12 }}>
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === "Enter" && send()}
            placeholder={autoRoute ? "Message... (routage automatique vers le bon agent)" : `Message à ${agent.name}...`}
            style={{
              flex: 1, padding: "12px 16px", borderRadius: 8,
              background: "#0f0f1a", border: "1px solid #2a2a3e",
              color: "#fff", fontSize: 14, outline: "none"
            }}
          />
          <button
            onClick={send}
            disabled={loading}
            style={{
              padding: "12px 24px", borderRadius: 8,
              background: loading ? "#333" : "#7c3aed",
              border: "none", color: "#fff",
              cursor: loading ? "not-allowed" : "pointer",
              fontSize: 14, fontWeight: "bold", transition: "background 0.2s"
            }}
          >
            {loading ? "⏳" : "Envoyer"}
          </button>
        </div>
      </div>
    </div>
  )
}
