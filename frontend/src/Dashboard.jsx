import { useState, useEffect } from "react"

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8004"

export default function Dashboard({ onBack }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${API}/dashboard`)
      .then(r => r.json())
      .then(d => { setData(d); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  const refresh = () => {
    setLoading(true)
    fetch(`${API}/dashboard`)
      .then(r => r.json())
      .then(d => { setData(d); setLoading(false) })
  }

  if (loading) return (
    <div style={{ background: "#0f0f1a", color: "#fff", height: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div>Chargement du dashboard...</div>
    </div>
  )

  return (
    <div style={{ background: "#0f0f1a", color: "#fff", minHeight: "100vh", fontFamily: "'Segoe UI', sans-serif" }}>
      
      {/* Header */}
      <div style={{ background: "#13132a", borderBottom: "1px solid #2a2a3e", padding: "16px 32px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div style={{ fontSize: 20, fontWeight: "bold", color: "#7c3aed" }}>📊 ORION AI — Dashboard</div>
        <div style={{ display: "flex", gap: 12 }}>
          <button onClick={refresh} style={{ padding: "8px 16px", borderRadius: 8, background: "#2a2a3e", border: "none", color: "#fff", cursor: "pointer" }}>
            🔄 Actualiser
          </button>
          <button onClick={onBack} style={{ padding: "8px 16px", borderRadius: 8, background: "#7c3aed", border: "none", color: "#fff", cursor: "pointer" }}>
            💬 Chat
          </button>
        </div>
      </div>

      <div style={{ padding: 32 }}>

        {/* Stats globales */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16, marginBottom: 32 }}>
          {[
            { label: "Total Agents", value: data?.total_agents || 0, emoji: "🤖" },
            { label: "Agents Actifs", value: data?.active_agents || 0, emoji: "✅" },
            { label: "Messages Total", value: data?.total_messages || 0, emoji: "💬" },
            { label: "Mémoire Long Terme", value: data?.memory?.long_term_count || 0, emoji: "🧠" },
          ].map((stat, i) => (
            <div key={i} style={{ background: "#13132a", borderRadius: 12, padding: 20, border: "1px solid #2a2a3e", textAlign: "center" }}>
              <div style={{ fontSize: 32 }}>{stat.emoji}</div>
              <div style={{ fontSize: 28, fontWeight: "bold", color: "#7c3aed", marginTop: 8 }}>{stat.value}</div>
              <div style={{ fontSize: 12, color: "#555", marginTop: 4 }}>{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Agents */}
        <div style={{ marginBottom: 24, fontSize: 16, fontWeight: "bold", color: "#888" }}>
          🤖 Agents
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12 }}>
          {data?.agents?.map(agent => (
            <div key={agent.id} style={{
              background: "#13132a", borderRadius: 12, padding: 16,
              border: `1px solid ${agent.active ? "#7c3aed44" : "#2a2a3e"}`,
            }}>
              <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
                <div style={{ fontSize: 28 }}>{agent.emoji}</div>
                <div>
                  <div style={{ fontWeight: "bold" }}>{agent.name}</div>
                  <div style={{ fontSize: 11, color: "#555" }}>{agent.team}</div>
                </div>
                <div style={{ marginLeft: "auto", fontSize: 10, padding: "3px 8px", borderRadius: 20, background: agent.active ? "#7c3aed22" : "#2a2a3e", color: agent.active ? "#7c3aed" : "#555" }}>
                  {agent.active ? "Actif" : "Inactif"}
                </div>
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
                <div style={{ background: "#0f0f1a", borderRadius: 8, padding: 10, textAlign: "center" }}>
                  <div style={{ fontSize: 18, fontWeight: "bold", color: "#7c3aed" }}>{agent.messages_count}</div>
                  <div style={{ fontSize: 10, color: "#555" }}>Messages</div>
                </div>
                <div style={{ background: "#0f0f1a", borderRadius: 8, padding: 10, textAlign: "center" }}>
                  <div style={{ fontSize: 18, fontWeight: "bold", color: "#7c3aed" }}>{agent.events_count}</div>
                  <div style={{ fontSize: 10, color: "#555" }}>Événements</div>
                </div>
              </div>
              {agent.last_active && (
                <div style={{ fontSize: 10, color: "#444", marginTop: 8 }}>
                  Dernière activité : {new Date(agent.last_active).toLocaleString("fr-FR")}
                </div>
              )}
            </div>
          ))}
        </div>

      </div>
    </div>
  )
}