import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(
    page_title="⚽ Porra Fútbol",
    page_icon="⚽",
    layout="centered"
)

# ── Estilos ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0f0f1a; }
    h1, h2, h3 { color: #fbbf24; }
    .pagado {
        background: rgba(34,197,94,0.15);
        border: 1.5px solid rgba(34,197,94,0.5);
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }
    .pendiente {
        background: rgba(239,68,68,0.15);
        border: 1.5px solid rgba(239,68,68,0.5);
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }
    .partido {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 8px;
    }
    .badge-pagado { color: #22c55e; font-weight: bold; }
    .badge-pendiente { color: #ef4444; font-weight: bold; }
    .euro { color: #fbbf24; font-size: 1.2em; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ── Partidos Premier League (datos reales jornada actual) ─────────────────────
PARTIDOS = [
    {"id": 1, "home": "West Ham United",     "away": "Wolverhampton",     "fecha": "Vie 10 Abr · 21:00", "estado": "programado", "score": None,        "home_pct": 52.3, "draw_pct": 25.3, "away_pct": 22.4},
    {"id": 2, "home": "Arsenal FC",           "away": "AFC Bournemouth",   "fecha": "Sáb 11 Abr · 13:30", "estado": "programado", "score": None,        "home_pct": 66.3, "draw_pct": 19.5, "away_pct": 14.2},
    {"id": 3, "home": "Brentford FC",         "away": "Everton FC",        "fecha": "Sáb 11 Abr · 16:00", "estado": "programado", "score": None,        "home_pct": 44.3, "draw_pct": 28.0, "away_pct": 27.7},
    {"id": 4, "home": "Burnley FC",           "away": "Brighton & Hove",   "fecha": "Sáb 11 Abr · 16:00", "estado": "programado", "score": None,        "home_pct": 20.6, "draw_pct": 23.6, "away_pct": 55.8},
    {"id": 5, "home": "Liverpool FC",         "away": "Fulham FC",         "fecha": "Sáb 11 Abr · 18:30", "estado": "programado", "score": None,        "home_pct": 61.0, "draw_pct": 20.9, "away_pct": 18.1},
    {"id": 6, "home": "Crystal Palace",       "away": "Newcastle United",  "fecha": "Dom 12 Abr · 15:00", "estado": "programado", "score": None,        "home_pct": 32.5, "draw_pct": 26.7, "away_pct": 40.8},
    {"id": 7, "home": "Nottingham Forest",    "away": "Aston Villa",       "fecha": "Dom 12 Abr · 15:00", "estado": "programado", "score": None,        "home_pct": 36.1, "draw_pct": 28.2, "away_pct": 35.7},
    {"id": 8, "home": "Chelsea FC",           "away": "Manchester City",   "fecha": "Dom 12 Abr · 17:30", "estado": "programado", "score": None,        "home_pct": 30.7, "draw_pct": 24.6, "away_pct": 44.7},
    {"id": 9, "home": "Manchester United",    "away": "Leeds United",      "fecha": "Lun 13 Abr · 21:00", "estado": "programado", "score": None,        "home_pct": 60.7, "draw_pct": 21.9, "away_pct": 17.4},
    # Finalizados
    {"id": 10, "home": "Brighton",            "away": "Liverpool FC",      "fecha": "Sáb 21 Mar · FIN",   "estado": "final",      "score": (2, 1),      "home_pct": None, "draw_pct": None, "away_pct": None},
    {"id": 11, "home": "Everton FC",          "away": "Chelsea FC",        "fecha": "Sáb 21 Mar · FIN",   "estado": "final",      "score": (3, 0),      "home_pct": None, "draw_pct": None, "away_pct": None},
    {"id": 12, "home": "Aston Villa",         "away": "West Ham United",   "fecha": "Dom 22 Mar · FIN",   "estado": "final",      "score": (2, 0),      "home_pct": None, "draw_pct": None, "away_pct": None},
]

# ── Estado de sesión ──────────────────────────────────────────────────────────
if "apuestas" not in st.session_state:
    st.session_state.apuestas = [
        {"jugador": "Carlos",  "partido_id": 10, "resultado": "Local",     "cantidad": 20.0, "pagado": True},
        {"jugador": "María",   "partido_id": 11, "resultado": "Visitante", "cantidad": 15.0, "pagado": False},
        {"jugador": "Javi",    "partido_id": 12, "resultado": "Local",     "cantidad": 50.0, "pagado": True},
    ]

def get_partido(pid):
    return next((p for p in PARTIDOS if p["id"] == pid), None)

def resultado_real(partido):
    if partido["estado"] != "final" or not partido["score"]:
        return None
    h, a = partido["score"]
    if h > a: return "Local"
    if a > h: return "Visitante"
    return "Empate"

# ── Header ────────────────────────────────────────────────────────────────────
st.title("⚽ Porra Fútbol")
st.caption("Premier League · Jornada actual")

apuestas = st.session_state.apuestas
total = sum(b["cantidad"] for b in apuestas)
cobrado = sum(b["cantidad"] for b in apuestas if b["pagado"])
pendiente = total - cobrado

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total apostado", f"{total:.2f}€")
col2.metric("✅ Cobrado", f"{cobrado:.2f}€")
col3.metric("⏳ Pendiente", f"{pendiente:.2f}€")

if total > 0:
    st.progress(cobrado / total, text=f"{int(cobrado/total*100)}% cobrado")

st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["🏟️ Partidos", "📋 Apuestas"])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — PARTIDOS
# ════════════════════════════════════════════════════════════════════════════
with tab1:

    st.subheader("➕ Nueva apuesta")
    with st.form("form_apuesta", clear_on_submit=True):
        jugador = st.text_input("👤 Nombre del apostador")

        opciones_partidos = []
        for p in PARTIDOS:
            estado = "✅" if p["estado"] == "final" else "🕐"
            score_str = f" ({p['score'][0]}-{p['score'][1]})" if p["score"] else ""
            opciones_partidos.append(f"{estado} {p['home']} vs {p['away']}{score_str} · {p['fecha']}")

        partido_sel = st.selectbox("⚽ Partido", opciones_partidos)
        idx_partido = opciones_partidos.index(partido_sel)
        partido_obj = PARTIDOS[idx_partido]

        col_r, col_c = st.columns(2)
        with col_r:
            resultado = st.radio(
                "🎯 Apuesta por",
                ["Local", "Empate", "Visitante"],
                captions=[partido_obj["home"], "Empate", partido_obj["away"]],
                horizontal=False
            )
        with col_c:
            cantidad = st.number_input("💶 Cantidad (€)", min_value=0.5, value=10.0, step=0.5)

        submitted = st.form_submit_button("💾 Registrar apuesta", use_container_width=True, type="primary")
        if submitted:
            if not jugador.strip():
                st.error("⚠️ Escribe el nombre del apostador")
            else:
                st.session_state.apuestas.append({
                    "jugador": jugador.strip(),
                    "partido_id": partido_obj["id"],
                    "resultado": resultado,
                    "cantidad": cantidad,
                    "pagado": False,
                })
                st.success(f"✅ Apuesta de {jugador} registrada ({cantidad}€ a {resultado})")
                st.rerun()

    st.divider()
    st.subheader("📅 Partidos de la jornada")

    prog = [p for p in PARTIDOS if p["estado"] == "programado"]
    fin  = [p for p in PARTIDOS if p["estado"] == "final"]

    st.markdown("**🕐 Próximos partidos**")
    for p in prog:
        with st.container():
            st.markdown(f"""
            <div class="partido">
            <small style="color:#fbbf24">🕐 PROGRAMADO · {p['fecha']}</small><br>
            <b>{p['home']}</b> &nbsp;vs&nbsp; <b>{p['away']}</b>
            </div>
            """, unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            c1.progress(p["home_pct"] / 100, text=f"Local {p['home_pct']}%")
            c2.progress(p["draw_pct"] / 100, text=f"Empate {p['draw_pct']}%")
            c3.progress(p["away_pct"] / 100, text=f"Visit. {p['away_pct']}%")

    st.markdown("**✅ Finalizados**")
    for p in fin:
        h, a = p["score"]
        st.markdown(f"""
        <div class="partido">
        <small style="color:#86efac">✓ FINALIZADO · {p['fecha']}</small><br>
        <b>{p['home']}</b> &nbsp; <span style="font-size:1.3em;font-weight:900">{h} - {a}</span> &nbsp; <b>{p['away']}</b>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — APUESTAS
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("📋 Lista de apuestas")

    filtro = st.radio("Filtrar", ["Todas", "✅ Pagadas", "⏳ Pendientes"], horizontal=True)

    apuestas_filtradas = apuestas
    if filtro == "✅ Pagadas":
        apuestas_filtradas = [b for b in apuestas if b["pagado"]]
    elif filtro == "⏳ Pendientes":
        apuestas_filtradas = [b for b in apuestas if not b["pagado"]]

    if not apuestas_filtradas:
        st.info("No hay apuestas en esta categoría.")

    for i, bet in enumerate(apuestas_filtradas):
        real_i = apuestas.index(bet)
        partido = get_partido(bet["partido_id"])
        res_real = resultado_real(partido) if partido else None

        if res_real is None:
            estado_str = "🕐 En juego"
        elif res_real == bet["resultado"]:
            estado_str = "🏆 ¡Ganada!"
        else:
            estado_str = "❌ Perdida"

        clase = "pagado" if bet["pagado"] else "pendiente"
        badge = "✅ PAGADO" if bet["pagado"] else "⏳ PENDIENTE"
        color_badge = "#22c55e" if bet["pagado"] else "#ef4444"

        partido_str = f"{partido['home']} vs {partido['away']}" if partido else "?"

        st.markdown(f"""
        <div class="{clase}">
            <div style="display:flex;justify-content:space-between;align-items:center">
                <div>
                    <b style="font-size:1.1em">{bet['jugador']}</b>
                    &nbsp;<span style="color:{color_badge};font-weight:700">{badge}</span>
                </div>
                <span style="color:#fbbf24;font-size:1.3em;font-weight:900">{bet['cantidad']:.2f}€</span>
            </div>
            <div style="color:#9ca3af;font-size:0.85em;margin-top:4px">⚽ {partido_str}</div>
            <div style="margin-top:4px">
                🎯 Apuesta: <b>{bet['resultado']}</b> &nbsp;·&nbsp; {estado_str}
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_p, col_d = st.columns([2, 1])
        with col_p:
            nuevo_estado = st.checkbox(
                "Marcar como pagado" if not bet["pagado"] else "Marcar como pendiente",
                value=bet["pagado"],
                key=f"chk_{real_i}"
            )
            if nuevo_estado != bet["pagado"]:
                st.session_state.apuestas[real_i]["pagado"] = nuevo_estado
                st.rerun()
        with col_d:
            if st.button("🗑️ Eliminar", key=f"del_{real_i}"):
                st.session_state.apuestas.pop(real_i)
                st.rerun()

        st.markdown("")
