import { useState, useEffect } from "react";

const MATCHES = [
  { id: 1, home: "West Ham United", away: "Wolverhampton", homeAbbr: "WHU", awayAbbr: "WOL", date: "Vie 10 Abr · 21:00", status: "scheduled", score: null, homePct: 52.3, awayPct: 22.4, drawPct: 25.3 },
  { id: 2, home: "Arsenal FC", away: "AFC Bournemouth", homeAbbr: "ARS", awayAbbr: "BOU", date: "Sáb 11 Abr · 13:30", status: "scheduled", score: null, homePct: 66.3, awayPct: 14.2, drawPct: 19.5 },
  { id: 3, home: "Brentford FC", away: "Everton FC", homeAbbr: "BRE", awayAbbr: "EVE", date: "Sáb 11 Abr · 16:00", status: "scheduled", score: null, homePct: 44.3, awayPct: 27.7, drawPct: 28.0 },
  { id: 4, home: "Burnley FC", away: "Brighton & Hove", homeAbbr: "BUR", awayAbbr: "BRI", date: "Sáb 11 Abr · 16:00", status: "scheduled", score: null, homePct: 20.6, awayPct: 55.8, drawPct: 23.6 },
  { id: 5, home: "Liverpool FC", away: "Fulham FC", homeAbbr: "LFC", awayAbbr: "FUL", date: "Sáb 11 Abr · 18:30", status: "scheduled", score: null, homePct: 61.0, awayPct: 18.1, drawPct: 20.9 },
  { id: 6, home: "Crystal Palace", away: "Newcastle United", homeAbbr: "CRY", awayAbbr: "NEW", date: "Dom 12 Abr · 15:00", status: "scheduled", score: null, homePct: 32.5, awayPct: 40.8, drawPct: 26.7 },
  { id: 7, home: "Nottingham Forest", away: "Aston Villa", homeAbbr: "NFO", awayAbbr: "AVL", date: "Dom 12 Abr · 15:00", status: "scheduled", score: null, homePct: 36.1, awayPct: 35.7, drawPct: 28.2 },
  { id: 8, home: "Chelsea FC", away: "Manchester City", homeAbbr: "CFC", awayAbbr: "MCI", date: "Dom 12 Abr · 17:30", status: "scheduled", score: null, homePct: 30.7, awayPct: 44.7, drawPct: 24.6 },
  { id: 9, home: "Manchester United", away: "Leeds United", homeAbbr: "MUN", awayAbbr: "LEE", date: "Lun 13 Abr · 21:00", status: "scheduled", score: null, homePct: 60.7, awayPct: 17.4, drawPct: 21.9 },
  // Finalizados recientes
  { id: 10, home: "Brighton", away: "Liverpool FC", homeAbbr: "BRI", awayAbbr: "LFC", date: "Sáb 21 Mar · Finalizado", status: "final", score: { home: 2, away: 1 }, homePct: null, awayPct: null, drawPct: null },
  { id: 11, home: "Everton FC", away: "Chelsea FC", homeAbbr: "EVE", awayAbbr: "CFC", date: "Sáb 21 Mar · Finalizado", status: "final", score: { home: 3, away: 0 }, homePct: null, awayPct: null, drawPct: null },
  { id: 12, home: "Aston Villa", away: "West Ham United", homeAbbr: "AVL", awayAbbr: "WHU", date: "Dom 22 Mar · Finalizado", status: "final", score: { home: 2, away: 0 }, homePct: null, awayPct: null, drawPct: null },
];

const TEAM_COLORS = {
  WHU: "#7A1B3B", WOL: "#F9A11B", ARS: "#EF0107", BOU: "#DA291C",
  BRE: "#E30613", EVE: "#003399", BUR: "#6C1D45", BRI: "#0057B8",
  LFC: "#C8102E", FUL: "#000000", CRY: "#1B458F", NEW: "#241F20",
  NFO: "#DD0000", AVL: "#95BFE5", CFC: "#034694", MCI: "#6CABDD",
  MUN: "#DA291C", LEE: "#FFCD00", TOT: "#132257", SUN: "#EB172B",
};

const TEAM_EMOJIS = {
  WHU: "⚒️", WOL: "🐺", ARS: "🔴", BOU: "🍒", BRE: "🐝", EVE: "🔵",
  BUR: "🟤", BRI: "🔵", LFC: "🔴", FUL: "⚫", CRY: "🦅", NEW: "⚫",
  NFO: "🌳", AVL: "🦁", CFC: "🔵", MCI: "🩵", MUN: "😈", LEE: "🦚",
};

function ResultBadge({ result }) {
  const map = { home: "Local", away: "Visitante", draw: "Empate" };
  const colors = { home: "#3b82f6", away: "#f59e0b", draw: "#8b5cf6" };
  return (
    <span style={{
      background: colors[result], color: "#fff", borderRadius: 6,
      padding: "2px 10px", fontSize: 11, fontWeight: 700, letterSpacing: 1,
    }}>{map[result]}</span>
  );
}

function MatchCard({ match, onSelect, selected }) {
  const isFinal = match.status === "final";
  return (
    <div
      onClick={() => onSelect(match)}
      style={{
        background: selected ? "rgba(251,191,36,0.13)" : "rgba(255,255,255,0.04)",
        border: selected ? "1.5px solid #fbbf24" : "1.5px solid rgba(255,255,255,0.1)",
        borderRadius: 14, padding: "14px 18px", cursor: "pointer",
        transition: "all 0.2s", marginBottom: 10,
        boxShadow: selected ? "0 0 20px rgba(251,191,36,0.2)" : "none",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
        <span style={{ fontSize: 11, color: isFinal ? "#86efac" : "#fbbf24", fontWeight: 600, letterSpacing: 1 }}>
          {isFinal ? "✓ FINALIZADO" : "🕐 PROGRAMADO"}
        </span>
        <span style={{ fontSize: 11, color: "#9ca3af" }}>{match.date}</span>
      </div>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 10 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, flex: 1 }}>
          <span style={{ fontSize: 20 }}>{TEAM_EMOJIS[match.homeAbbr] || "⚽"}</span>
          <span style={{ fontWeight: 700, fontSize: 14, color: "#f3f4f6" }}>{match.home}</span>
        </div>
        {isFinal ? (
          <div style={{
            background: "rgba(0,0,0,0.4)", borderRadius: 8, padding: "4px 14px",
            fontFamily: "monospace", fontWeight: 900, fontSize: 18, color: "#fff", minWidth: 70, textAlign: "center"
          }}>
            {match.score.home} - {match.score.away}
          </div>
        ) : (
          <div style={{ color: "#6b7280", fontWeight: 700, fontSize: 15, minWidth: 30, textAlign: "center" }}>vs</div>
        )}
        <div style={{ display: "flex", alignItems: "center", gap: 8, flex: 1, justifyContent: "flex-end" }}>
          <span style={{ fontWeight: 700, fontSize: 14, color: "#f3f4f6" }}>{match.away}</span>
          <span style={{ fontSize: 20 }}>{TEAM_EMOJIS[match.awayAbbr] || "⚽"}</span>
        </div>
      </div>
      {!isFinal && (
        <div style={{ marginTop: 10, display: "flex", gap: 6 }}>
          {[
            { label: `Local ${match.homePct}%`, val: match.homePct, color: "#3b82f6" },
            { label: `Empate ${match.drawPct}%`, val: match.drawPct, color: "#8b5cf6" },
            { label: `Visitante ${match.awayPct}%`, val: match.awayPct, color: "#f59e0b" },
          ].map(({ label, val, color }) => (
            <div key={label} style={{ flex: 1 }}>
              <div style={{ fontSize: 10, color: "#9ca3af", marginBottom: 3, textAlign: "center" }}>{label}</div>
              <div style={{ height: 4, background: "rgba(255,255,255,0.1)", borderRadius: 4, overflow: "hidden" }}>
                <div style={{ width: `${val}%`, height: "100%", background: color, borderRadius: 4 }} />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function BetRow({ bet, index, onTogglePaid, onDelete }) {
  const match = MATCHES.find(m => m.id === bet.matchId);
  const paid = bet.paid;

  const getWinStatus = () => {
    if (!match || match.status !== "final") return "pending";
    const { home, away } = match.score;
    const actualResult = home > away ? "home" : away > home ? "away" : "draw";
    return bet.result === actualResult ? "won" : "lost";
  };
  const winStatus = getWinStatus();

  const statusColors = { pending: "#fbbf24", won: "#22c55e", lost: "#ef4444" };
  const statusLabels = { pending: "En juego", won: "¡Ganada! 🏆", lost: "Perdida" };

  return (
    <div style={{
      background: paid
        ? "linear-gradient(135deg, rgba(34,197,94,0.12), rgba(34,197,94,0.05))"
        : "linear-gradient(135deg, rgba(239,68,68,0.12), rgba(239,68,68,0.05))",
      border: paid ? "1.5px solid rgba(34,197,94,0.4)" : "1.5px solid rgba(239,68,68,0.4)",
      borderRadius: 14, padding: "14px 18px", marginBottom: 10,
      transition: "all 0.3s",
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 10 }}>
        <div style={{ flex: 1 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
            <span style={{
              width: 28, height: 28, borderRadius: "50%",
              background: paid ? "#22c55e" : "#ef4444",
              display: "flex", alignItems: "center", justifyContent: "center",
              fontSize: 14, fontWeight: 900, color: "#fff", flexShrink: 0,
            }}>{bet.player.charAt(0).toUpperCase()}</span>
            <span style={{ fontWeight: 700, fontSize: 15, color: "#f3f4f6" }}>{bet.player}</span>
            <span style={{
              background: paid ? "rgba(34,197,94,0.2)" : "rgba(239,68,68,0.2)",
              color: paid ? "#86efac" : "#fca5a5",
              borderRadius: 20, padding: "2px 10px", fontSize: 11, fontWeight: 700,
            }}>{paid ? "✓ PAGADO" : "✗ PENDIENTE"}</span>
          </div>
          <div style={{ fontSize: 12, color: "#9ca3af", marginBottom: 4 }}>
            ⚽ {match ? `${match.home} vs ${match.away}` : "Partido no encontrado"}
          </div>
          <div style={{ display: "flex", gap: 10, alignItems: "center", flexWrap: "wrap" }}>
            <ResultBadge result={bet.result} />
            <span style={{ fontSize: 12, color: statusColors[winStatus], fontWeight: 600 }}>
              {statusLabels[winStatus]}
            </span>
          </div>
        </div>
        <div style={{ textAlign: "right", flexShrink: 0 }}>
          <div style={{ fontSize: 22, fontWeight: 900, color: "#fbbf24" }}>
            {bet.amount}€
          </div>
          <div style={{ display: "flex", gap: 6, marginTop: 6, justifyContent: "flex-end" }}>
            <button
              onClick={() => onTogglePaid(index)}
              style={{
                background: paid ? "rgba(239,68,68,0.2)" : "rgba(34,197,94,0.2)",
                color: paid ? "#fca5a5" : "#86efac",
                border: "none", borderRadius: 8, padding: "4px 10px",
                fontSize: 11, cursor: "pointer", fontWeight: 700,
              }}
            >{paid ? "Desmarcar" : "Marcar pagado"}</button>
            <button
              onClick={() => onDelete(index)}
              style={{
                background: "rgba(107,114,128,0.2)", color: "#9ca3af",
                border: "none", borderRadius: 8, padding: "4px 10px",
                fontSize: 11, cursor: "pointer",
              }}
            >🗑️</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [bets, setBets] = useState([
    { player: "Carlos", matchId: 10, result: "home", amount: 20, paid: true },
    { player: "María", matchId: 11, result: "away", amount: 15, paid: false },
    { player: "Javi", matchId: 12, result: "home", amount: 50, paid: true },
  ]);
  const [selectedMatch, setSelectedMatch] = useState(null);
  const [form, setForm] = useState({ player: "", result: "home", amount: "" });
  const [tab, setTab] = useState("matches");
  const [filterPaid, setFilterPaid] = useState("all");
  const [showForm, setShowForm] = useState(false);

  const handleAdd = () => {
    if (!selectedMatch || !form.player.trim() || !form.amount) return;
    setBets(prev => [...prev, {
      player: form.player.trim(),
      matchId: selectedMatch.id,
      result: form.result,
      amount: parseFloat(form.amount),
      paid: false,
    }]);
    setForm({ player: "", result: "home", amount: "" });
    setSelectedMatch(null);
    setShowForm(false);
    setTab("bets");
  };

  const togglePaid = (idx) => setBets(prev => prev.map((b, i) => i === idx ? { ...b, paid: !b.paid } : b));
  const deleteBet = (idx) => setBets(prev => prev.filter((_, i) => i !== idx));

  const filtered = bets.filter(b => filterPaid === "all" ? true : filterPaid === "paid" ? b.paid : !b.paid);
  const totalPaid = bets.filter(b => b.paid).reduce((s, b) => s + b.amount, 0);
  const totalPending = bets.filter(b => !b.paid).reduce((s, b) => s + b.amount, 0);
  const totalAmount = bets.reduce((s, b) => s + b.amount, 0);

  const inputStyle = {
    background: "rgba(255,255,255,0.06)", border: "1.5px solid rgba(255,255,255,0.12)",
    borderRadius: 10, padding: "10px 14px", color: "#f3f4f6", fontSize: 14, width: "100%",
    outline: "none", boxSizing: "border-box",
  };

  return (
    <div style={{
      minHeight: "100vh", background: "linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #0f172a 100%)",
      fontFamily: "'Segoe UI', system-ui, sans-serif", color: "#f3f4f6",
    }}>
      {/* Header */}
      <div style={{
        background: "linear-gradient(90deg, rgba(251,191,36,0.15), rgba(251,191,36,0.05))",
        borderBottom: "1px solid rgba(251,191,36,0.2)", padding: "20px 20px 0",
        position: "sticky", top: 0, zIndex: 100, backdropFilter: "blur(20px)",
      }}>
        <div style={{ maxWidth: 700, margin: "0 auto" }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 16 }}>
            <div>
              <h1 style={{ margin: 0, fontSize: 22, fontWeight: 900, letterSpacing: -0.5 }}>
                ⚽ <span style={{ color: "#fbbf24" }}>BetZone</span>
              </h1>
              <p style={{ margin: "2px 0 0", fontSize: 11, color: "#6b7280" }}>Premier League · Jornada actual</p>
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              <div style={{ textAlign: "center", background: "rgba(34,197,94,0.1)", border: "1px solid rgba(34,197,94,0.3)", borderRadius: 10, padding: "8px 14px" }}>
                <div style={{ fontSize: 16, fontWeight: 900, color: "#22c55e" }}>{totalPaid.toFixed(0)}€</div>
                <div style={{ fontSize: 9, color: "#6b7280" }}>COBRADO</div>
              </div>
              <div style={{ textAlign: "center", background: "rgba(239,68,68,0.1)", border: "1px solid rgba(239,68,68,0.3)", borderRadius: 10, padding: "8px 14px" }}>
                <div style={{ fontSize: 16, fontWeight: 900, color: "#ef4444" }}>{totalPending.toFixed(0)}€</div>
                <div style={{ fontSize: 9, color: "#6b7280" }}>PENDIENTE</div>
              </div>
            </div>
          </div>

          <div style={{ display: "flex", gap: 4 }}>
            {[["matches", "🏟️ Partidos"], ["bets", `📋 Apuestas (${bets.length})`]].map(([key, label]) => (
              <button key={key} onClick={() => setTab(key)} style={{
                background: tab === key ? "#fbbf24" : "transparent",
                color: tab === key ? "#0f0f1a" : "#9ca3af",
                border: "none", borderRadius: "8px 8px 0 0", padding: "10px 20px",
                fontSize: 13, fontWeight: 700, cursor: "pointer", transition: "all 0.2s",
              }}>{label}</button>
            ))}
          </div>
        </div>
      </div>

      <div style={{ maxWidth: 700, margin: "0 auto", padding: "20px 16px" }}>
        {tab === "matches" && (
          <div>
            {/* Nueva apuesta form */}
            <button
              onClick={() => setShowForm(!showForm)}
              style={{
                width: "100%", background: showForm ? "rgba(239,68,68,0.2)" : "linear-gradient(135deg, #fbbf24, #f59e0b)",
                color: showForm ? "#fca5a5" : "#0f0f1a", border: "none", borderRadius: 12,
                padding: "13px", fontSize: 15, fontWeight: 800, cursor: "pointer", marginBottom: 16,
                boxShadow: showForm ? "none" : "0 4px 20px rgba(251,191,36,0.3)",
              }}
            >{showForm ? "✕ Cancelar" : "+ Nueva Apuesta"}</button>

            {showForm && (
              <div style={{
                background: "rgba(255,255,255,0.04)", border: "1.5px solid rgba(251,191,36,0.3)",
                borderRadius: 14, padding: 18, marginBottom: 20,
              }}>
                <p style={{ margin: "0 0 14px", fontWeight: 700, color: "#fbbf24", fontSize: 13 }}>
                  {selectedMatch ? `✓ ${selectedMatch.home} vs ${selectedMatch.away}` : "1. Selecciona un partido abajo"}
                </p>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginBottom: 10 }}>
                  <div>
                    <label style={{ fontSize: 11, color: "#9ca3af", display: "block", marginBottom: 4 }}>JUGADOR</label>
                    <input
                      placeholder="Nombre del apostador"
                      value={form.player}
                      onChange={e => setForm(p => ({ ...p, player: e.target.value }))}
                      style={inputStyle}
                    />
                  </div>
                  <div>
                    <label style={{ fontSize: 11, color: "#9ca3af", display: "block", marginBottom: 4 }}>CANTIDAD (€)</label>
                    <input
                      type="number" placeholder="0.00"
                      value={form.amount}
                      onChange={e => setForm(p => ({ ...p, amount: e.target.value }))}
                      style={inputStyle}
                    />
                  </div>
                </div>
                <div style={{ marginBottom: 12 }}>
                  <label style={{ fontSize: 11, color: "#9ca3af", display: "block", marginBottom: 6 }}>RESULTADO APOSTADO</label>
                  <div style={{ display: "flex", gap: 6 }}>
                    {[
                      { val: "home", label: selectedMatch ? selectedMatch.homeAbbr : "Local", color: "#3b82f6" },
                      { val: "draw", label: "Empate", color: "#8b5cf6" },
                      { val: "away", label: selectedMatch ? selectedMatch.awayAbbr : "Visitante", color: "#f59e0b" },
                    ].map(opt => (
                      <button
                        key={opt.val}
                        onClick={() => setForm(p => ({ ...p, result: opt.val }))}
                        style={{
                          flex: 1, padding: "10px 6px", borderRadius: 10, fontSize: 12, fontWeight: 700,
                          cursor: "pointer", transition: "all 0.2s",
                          background: form.result === opt.val ? opt.color : "rgba(255,255,255,0.05)",
                          color: form.result === opt.val ? "#fff" : "#9ca3af",
                          border: form.result === opt.val ? `2px solid ${opt.color}` : "2px solid transparent",
                        }}
                      >{opt.label}</button>
                    ))}
                  </div>
                </div>
                <button
                  onClick={handleAdd}
                  disabled={!selectedMatch || !form.player.trim() || !form.amount}
                  style={{
                    width: "100%", background: (!selectedMatch || !form.player.trim() || !form.amount)
                      ? "rgba(255,255,255,0.05)" : "linear-gradient(135deg, #22c55e, #16a34a)",
                    color: (!selectedMatch || !form.player.trim() || !form.amount) ? "#6b7280" : "#fff",
                    border: "none", borderRadius: 10, padding: 12, fontSize: 14, fontWeight: 800, cursor: "pointer",
                  }}
                >💾 Registrar Apuesta</button>
              </div>
            )}

            <p style={{ fontSize: 12, color: "#6b7280", margin: "0 0 10px" }}>
              {showForm ? "👆 Toca un partido para seleccionarlo" : "Partidos de la jornada"}
            </p>
            {MATCHES.map(m => (
              <MatchCard
                key={m.id}
                match={m}
                onSelect={showForm ? setSelectedMatch : () => {}}
                selected={selectedMatch?.id === m.id}
              />
            ))}
          </div>
        )}

        {tab === "bets" && (
          <div>
            <div style={{ display: "flex", gap: 6, marginBottom: 16 }}>
              {[["all", "Todas"], ["paid", "✓ Pagadas"], ["pending", "✗ Pendientes"]].map(([val, label]) => (
                <button
                  key={val}
                  onClick={() => setFilterPaid(val)}
                  style={{
                    flex: 1, padding: "9px 6px", borderRadius: 10, fontSize: 12, fontWeight: 700,
                    cursor: "pointer", border: "none",
                    background: filterPaid === val
                      ? val === "paid" ? "#22c55e" : val === "pending" ? "#ef4444" : "#fbbf24"
                      : "rgba(255,255,255,0.06)",
                    color: filterPaid === val ? (val === "all" ? "#0f0f1a" : "#fff") : "#9ca3af",
                  }}
                >{label}</button>
              ))}
            </div>

            {filtered.length === 0 ? (
              <div style={{ textAlign: "center", padding: 60, color: "#6b7280" }}>
                <div style={{ fontSize: 40, marginBottom: 12 }}>📭</div>
                <p style={{ margin: 0 }}>No hay apuestas aquí</p>
              </div>
            ) : (
              filtered.map((bet, idx) => (
                <BetRow
                  key={idx}
                  bet={bet}
                  index={bets.indexOf(bet)}
                  onTogglePaid={togglePaid}
                  onDelete={deleteBet}
                />
              ))
            )}

            <div style={{
              background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.1)",
              borderRadius: 14, padding: 16, marginTop: 8,
            }}>
              <div style={{ fontSize: 12, color: "#6b7280", marginBottom: 10, fontWeight: 700 }}>RESUMEN TOTAL</div>
              {[
                { label: "Total apostado", val: totalAmount, color: "#f3f4f6" },
                { label: "Cobrado ✓", val: totalPaid, color: "#22c55e" },
                { label: "Por cobrar ✗", val: totalPending, color: "#ef4444" },
              ].map(({ label, val, color }) => (
                <div key={label} style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
                  <span style={{ color: "#9ca3af", fontSize: 13 }}>{label}</span>
                  <span style={{ fontWeight: 800, color, fontSize: 14 }}>{val.toFixed(2)}€</span>
                </div>
              ))}
              <div style={{ height: 8, background: "rgba(255,255,255,0.08)", borderRadius: 4, overflow: "hidden", marginTop: 12 }}>
                <div style={{
                  width: totalAmount > 0 ? `${(totalPaid / totalAmount) * 100}%` : "0%",
                  height: "100%", background: "linear-gradient(90deg, #22c55e, #16a34a)", borderRadius: 4, transition: "width 0.5s",
                }} />
              </div>
              <div style={{ fontSize: 10, color: "#6b7280", marginTop: 4, textAlign: "right" }}>
                {totalAmount > 0 ? Math.round((totalPaid / totalAmount) * 100) : 0}% cobrado
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
