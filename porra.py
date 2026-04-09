import streamlit as st

st.set_page_config(
    page_title="⚽ Porra Fútbol",
    page_icon="⚽",
    layout="centered"
)

st.markdown("""
<style>
    .stApp { background-color: #0f0f1a; }
    .partido-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── Datos reales ──────────────────────────────────────────────────────────────
PARTIDOS = {
    "🏆 Champions League": [
        {"id": "c1",  "home": "Real Madrid",      "away": "Bayern Munich",    "fecha": "Mar 7 Abr · FIN",        "estado": "final",      "score": (1, 2), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "c2",  "home": "Sporting CP",       "away": "Arsenal FC",       "fecha": "Mar 7 Abr · FIN",        "estado": "final",      "score": (0, 1), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "c3",  "home": "FC Barcelona",      "away": "Newcastle United", "fecha": "Mié 18 Mar · FIN",       "estado": "final",      "score": (7, 2), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "c4",  "home": "Tottenham",         "away": "Atlético Madrid",  "fecha": "Mié 18 Mar · FIN",       "estado": "final",      "score": (3, 2), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "c5",  "home": "Bayern Munich",     "away": "Atalanta BC",      "fecha": "Mié 18 Mar · FIN",       "estado": "final",      "score": (4, 1), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "c6",  "home": "Manchester City",   "away": "Real Madrid",      "fecha": "Mar 17 Mar · FIN",       "estado": "final",      "score": (1, 2), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "c7",  "home": "Chelsea FC",        "away": "PSG",              "fecha": "Mar 17 Mar · FIN",       "estado": "final",      "score": (0, 3), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "c8",  "home": "PSG",               "away": "Liverpool FC",     "fecha": "Hoy Mié 8 Abr · 21:00", "estado": "programado", "score": None,  "home_pct": 54.2, "draw_pct": 23.1, "away_pct": 22.7},
        {"id": "c9",  "home": "FC Barcelona",      "away": "Atlético Madrid",  "fecha": "Hoy Mié 8 Abr · 21:00", "estado": "programado", "score": None,  "home_pct": 63.6, "draw_pct": 18.7, "away_pct": 17.7},
        {"id": "c10", "home": "Liverpool FC",      "away": "PSG",              "fecha": "Mar 14 Abr · 21:00",    "estado": "programado", "score": None,  "home_pct": 24.5, "draw_pct": 23.0, "away_pct": 52.5},
        {"id": "c11", "home": "Atlético Madrid",   "away": "FC Barcelona",     "fecha": "Mar 14 Abr · 21:00",    "estado": "programado", "score": None,  "home_pct": 19.2, "draw_pct": 19.6, "away_pct": 61.2},
        {"id": "c12", "home": "Bayern Munich",     "away": "Real Madrid",      "fecha": "Mié 15 Abr · 21:00",   "estado": "programado", "score": None,  "home_pct": 60.8, "draw_pct": 19.2, "away_pct": 20.0},
        {"id": "c13", "home": "Arsenal FC",        "away": "Sporting CP",      "fecha": "Mié 15 Abr · 21:00",   "estado": "programado", "score": None,  "home_pct": 68.4, "draw_pct": 19.1, "away_pct": 12.5},
    ],
    "🇪🇸 LaLiga": [
        {"id": "l1",  "home": "Atlético Madrid",   "away": "FC Barcelona",     "fecha": "Sáb 4 Abr · FIN",       "estado": "final",      "score": (1, 2), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "l2",  "home": "Mallorca",           "away": "Real Madrid",      "fecha": "Sáb 4 Abr · FIN",       "estado": "final",      "score": (2, 1), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "l3",  "home": "Real Betis",         "away": "Espanyol",         "fecha": "Sáb 4 Abr · FIN",       "estado": "final",      "score": (0, 0), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "l4",  "home": "Getafe CF",          "away": "Athletic Bilbao",  "fecha": "Dom 5 Abr · FIN",       "estado": "final",      "score": (2, 0), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "l5",  "home": "Valencia CF",        "away": "Celta de Vigo",    "fecha": "Dom 5 Abr · FIN",       "estado": "final",      "score": (2, 3), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "l6",  "home": "Girona FC",          "away": "Villarreal CF",    "fecha": "Lun 6 Abr · FIN",       "estado": "final",      "score": (1, 0), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "l7",  "home": "Real Madrid",        "away": "Girona FC",        "fecha": "Vie 10 Abr · 21:00",   "estado": "programado", "score": None,  "home_pct": 75.0, "draw_pct": 14.6, "away_pct": 10.4},
        {"id": "l8",  "home": "Real Sociedad",      "away": "Dep. Alavés",      "fecha": "Sáb 11 Abr · 14:00",   "estado": "programado", "score": None,  "home_pct": 55.1, "draw_pct": 25.2, "away_pct": 19.7},
        {"id": "l9",  "home": "Elche CF",           "away": "Valencia CF",      "fecha": "Sáb 11 Abr · 16:15",   "estado": "programado", "score": None,  "home_pct": 38.9, "draw_pct": 28.7, "away_pct": 32.4},
        {"id": "l10", "home": "FC Barcelona",       "away": "Espanyol",         "fecha": "Sáb 11 Abr · 18:30",   "estado": "programado", "score": None,  "home_pct": 77.0, "draw_pct": 13.3, "away_pct":  9.7},
        {"id": "l11", "home": "Sevilla FC",         "away": "Atlético Madrid",  "fecha": "Sáb 11 Abr · 21:00",   "estado": "programado", "score": None,  "home_pct": 27.8, "draw_pct": 30.2, "away_pct": 42.0},
        {"id": "l12", "home": "Osasuna",            "away": "Real Betis",       "fecha": "Dom 12 Abr · 14:00",   "estado": "programado", "score": None,  "home_pct": 42.3, "draw_pct": 27.6, "away_pct": 30.1},
        {"id": "l13", "home": "Mallorca",           "away": "Rayo Vallecano",   "fecha": "Dom 12 Abr · 16:15",   "estado": "programado", "score": None,  "home_pct": 38.8, "draw_pct": 29.4, "away_pct": 31.8},
        {"id": "l14", "home": "Celta de Vigo",      "away": "Real Oviedo",      "fecha": "Dom 12 Abr · 18:30",   "estado": "programado", "score": None,  "home_pct": 57.8, "draw_pct": 24.0, "away_pct": 18.2},
        {"id": "l15", "home": "Athletic Bilbao",    "away": "Villarreal CF",    "fecha": "Dom 12 Abr · 21:00",   "estado": "programado", "score": None,  "home_pct": 42.0, "draw_pct": 27.2, "away_pct": 30.8},
        {"id": "l16", "home": "Levante UD",         "away": "Getafe CF",        "fecha": "Lun 13 Abr · 21:00",   "estado": "programado", "score": None,  "home_pct": 34.4, "draw_pct": 31.7, "away_pct": 33.9},
    ],
}

TODOS_PARTIDOS = [p for lista in PARTIDOS.values() for p in lista]

if "apuestas" not in st.session_state:
    st.session_state.apuestas = []

def get_partido(pid):
    return next((p for p in TODOS_PARTIDOS if p["id"] == pid), None)

def check_ganada(bet):
    partido = get_partido(bet["partido_id"])
    if not partido or partido["estado"] != "final" or not partido.get("score"):
        return None
    h, a = partido["score"]
    return bet["goles_home"] == h and bet["goles_away"] == a

# ── Header ────────────────────────────────────────────────────────────────────
st.title("⚽ Porra Fútbol")
st.caption("LaLiga · Champions League · Marcador exacto")

apuestas  = st.session_state.apuestas
total     = sum(b["cantidad"] for b in apuestas)
cobrado   = sum(b["cantidad"] for b in apuestas if b["pagado"])
pendiente = total - cobrado

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total", f"{total:.2f}€")
col2.metric("✅ Cobrado", f"{cobrado:.2f}€")
col3.metric("⏳ Pendiente", f"{pendiente:.2f}€")
if total > 0:
    st.progress(cobrado / total, text=f"{int(cobrado/total*100)}% cobrado")

st.divider()

tab_partidos, tab_apuestas = st.tabs(["🏟️ Partidos & Nueva apuesta", "📋 Mis Apuestas"])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — NUEVA APUESTA  (sin st.form para que el partido se actualice en vivo)
# ════════════════════════════════════════════════════════════════════════════
with tab_partidos:

    st.subheader("➕ Registrar apuesta")

    jugador     = st.text_input("👤 Nombre del apostador", key="jugador")
    cantidad    = st.number_input("💶 Cantidad (€)", min_value=0.5, value=10.0, step=0.5, key="cantidad")
    competicion = st.selectbox("🏆 Competición", list(PARTIDOS.keys()), key="competicion")

    partidos_comp = PARTIDOS[competicion]
    opciones = []
    for p in partidos_comp:
        if p["estado"] == "final":
            icono = "✅"
        elif "Hoy" in p["fecha"]:
            icono = "🔴 HOY"
        else:
            icono = "🕐"
        score_str = f" ({p['score'][0]}-{p['score'][1]})" if p.get("score") else ""
        opciones.append(f"{icono}  {p['home']} vs {p['away']}{score_str}  ·  {p['fecha']}")

    partido_sel = st.selectbox("⚽ Partido", opciones, key="partido_sel")
    partido_obj = partidos_comp[opciones.index(partido_sel)]

    # Marcador — se actualiza en tiempo real con el partido seleccionado
    st.markdown(f"**🎯 Marcador para: {partido_obj['home']} vs {partido_obj['away']}**")
    col_gh, col_sep, col_ga = st.columns([5, 1, 5])
    with col_gh:
        st.caption(partido_obj["home"])
        goles_home = st.number_input("gh", min_value=0, max_value=20, value=1, step=1,
                                     key="goles_home", label_visibility="collapsed")
    with col_sep:
        st.markdown("<div style='text-align:center;font-size:2em;font-weight:900;padding-top:16px'>-</div>",
                    unsafe_allow_html=True)
    with col_ga:
        st.caption(partido_obj["away"])
        goles_away = st.number_input("ga", min_value=0, max_value=20, value=0, step=1,
                                     key="goles_away", label_visibility="collapsed")

    st.markdown(
        f"<div style='text-align:center;font-size:2em;font-weight:900;color:#fbbf24;margin:8px 0'>"
        f"{goles_home} - {goles_away}</div>",
        unsafe_allow_html=True
    )

    if st.button("💾 Registrar apuesta", use_container_width=True, type="primary"):
        if not jugador.strip():
            st.error("⚠️ Escribe el nombre del apostador")
        else:
            st.session_state.apuestas.append({
                "jugador":     jugador.strip(),
                "partido_id":  partido_obj["id"],
                "competicion": competicion,
                "goles_home":  goles_home,
                "goles_away":  goles_away,
                "cantidad":    cantidad,
                "pagado":      False,
            })
            st.success(f"✅ **{jugador}** apuesta **{goles_home}-{goles_away}** → {cantidad:.2f}€")
            st.rerun()

    st.divider()

    # Lista de partidos
    for comp, lista in PARTIDOS.items():
        st.subheader(comp)

        hoy  = [p for p in lista if p["estado"] == "programado" and "Hoy" in p["fecha"]]
        prog = [p for p in lista if p["estado"] == "programado" and "Hoy" not in p["fecha"]]
        fin  = [p for p in lista if p["estado"] == "final"]

        if hoy:
            st.markdown("**🔴 HOY**")
            for p in hoy:
                st.markdown(f"""<div class="partido-card" style="border-color:rgba(239,68,68,0.6)">
                <small style="color:#ef4444;font-weight:700">🔴 HOY · {p['fecha']}</small><br>
                <b>{p['home']}</b> vs <b>{p['away']}</b></div>""", unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                c1.progress(p["home_pct"] / 100, text=f"Local {p['home_pct']}%")
                c2.progress(p["draw_pct"] / 100, text=f"Empate {p['draw_pct']}%")
                c3.progress(p["away_pct"] / 100, text=f"Visit. {p['away_pct']}%")

        if prog:
            st.markdown("**🕐 Próximos**")
            for p in prog:
                st.markdown(f"""<div class="partido-card">
                <small style="color:#fbbf24">{p['fecha']}</small><br>
                <b>{p['home']}</b> vs <b>{p['away']}</b></div>""", unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                c1.progress(p["home_pct"] / 100, text=f"Local {p['home_pct']}%")
                c2.progress(p["draw_pct"] / 100, text=f"Empate {p['draw_pct']}%")
                c3.progress(p["away_pct"] / 100, text=f"Visit. {p['away_pct']}%")

        if fin:
            with st.expander(f"✅ Resultados recientes ({len(fin)})"):
                for p in fin:
                    h, a = p["score"]
                    st.markdown(f"""<div class="partido-card">
                    <small style="color:#86efac">✓ FINALIZADO · {p['fecha']}</small><br>
                    <b {'style="color:#22c55e"' if h > a else ''}>{p['home']}</b>
                    &nbsp;<span style="font-size:1.3em;font-weight:900">{h} - {a}</span>&nbsp;
                    <b {'style="color:#22c55e"' if a > h else ''}>{p['away']}</b>
                    </div>""", unsafe_allow_html=True)
        st.markdown("")

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — APUESTAS  (sin HTML inline, todo con componentes nativos)
# ════════════════════════════════════════════════════════════════════════════
with tab_apuestas:

    if not apuestas:
        st.info("📭 Aún no hay apuestas. ¡Ve a Partidos para añadir la primera!")
    else:
        filtro = st.radio("Filtrar", ["Todas", "✅ Pagadas", "⏳ Pendientes"], horizontal=True)

        lista_filtrada = apuestas
        if filtro == "✅ Pagadas":
            lista_filtrada = [b for b in apuestas if b["pagado"]]
        elif filtro == "⏳ Pendientes":
            lista_filtrada = [b for b in apuestas if not b["pagado"]]

        if not lista_filtrada:
            st.info("No hay apuestas en esta categoría.")

        for bet in lista_filtrada:
            real_i  = apuestas.index(bet)
            partido = get_partido(bet["partido_id"])
            ganada  = check_ganada(bet)

            if ganada is None:
                estado_icon = "🕐"
                estado_txt  = "En juego"
            elif ganada:
                estado_icon = "🏆"
                estado_txt  = "¡Acertada!"
            else:
                estado_icon = "❌"
                estado_txt  = "Fallada"

            partido_str = f"{partido['home']} vs {partido['away']}" if partido else "?"
            comp_str    = bet.get("competicion", "")

            # Resultado real si está finalizado
            real_score_txt = ""
            if partido and partido["estado"] == "final" and partido.get("score"):
                rh, ra = partido["score"]
                real_score_txt = f"  ·  Real: {rh}-{ra}"

            # Color del contenedor
            color_border = "#22c55e" if bet["pagado"] else "#ef4444"
            color_bg     = "rgba(34,197,94,0.08)" if bet["pagado"] else "rgba(239,68,68,0.08)"
            badge_txt    = "✅ PAGADO" if bet["pagado"] else "⏳ PENDIENTE"

            st.markdown(
                f"""<div style="background:{color_bg};border:1.5px solid {color_border};
                border-radius:12px;padding:14px 18px;margin-bottom:4px">
                <div style="display:flex;justify-content:space-between">
                    <b style="font-size:1.1em">{bet['jugador']}</b>
                    <b style="color:{color_border}">{badge_txt}</b>
                </div>
                <div style="color:#9ca3af;font-size:0.82em">{comp_str}</div>
                <div style="color:#d1d5db;font-size:0.9em">⚽ {partido_str}</div>
                <div style="display:flex;justify-content:space-between;align-items:center;margin-top:8px">
                    <div>
                        <span style="font-size:1.8em;font-weight:900;color:#fbbf24">
                            {bet['goles_home']} - {bet['goles_away']}
                        </span>
                        <span style="color:#9ca3af;font-size:0.85em">{real_score_txt}</span>
                        <br>
                        <span style="font-size:0.95em">{estado_icon} {estado_txt}</span>
                    </div>
                    <span style="font-size:1.3em;font-weight:900;color:#fbbf24">{bet['cantidad']:.2f}€</span>
                </div>
                </div>""",
                unsafe_allow_html=True
            )

            col_chk, col_del = st.columns([3, 1])
            with col_chk:
                nuevo = st.checkbox(
                    "Marcar como pagado" if not bet["pagado"] else "Marcar como pendiente",
                    value=bet["pagado"],
                    key=f"chk_{real_i}"
                )
                if nuevo != bet["pagado"]:
                    st.session_state.apuestas[real_i]["pagado"] = nuevo
                    st.rerun()
            with col_del:
                if st.button("🗑️", key=f"del_{real_i}"):
                    st.session_state.apuestas.pop(real_i)
                    st.rerun()

        st.divider()
        st.markdown("**📊 Resumen**")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total", f"{total:.2f}€")
        c2.metric("✅ Cobrado", f"{cobrado:.2f}€")
        c3.metric("⏳ Pendiente", f"{pendiente:.2f}€")
        if total > 0:
            st.progress(cobrado / total, text=f"{int(cobrado/total*100)}% cobrado")
