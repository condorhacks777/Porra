import streamlit as st
import requests
import hashlib
from datetime import datetime, timedelta, timezone

SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]
RAPIDAPI_KEY = st.secrets["rapidapi"]["key"]

HEADERS_SB = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

HEADERS_API = {
    "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
    "x-rapidapi-key": RAPIDAPI_KEY
}

# ── API Football ──────────────────────────────────────────────────────────────
# Liga IDs: LaLiga=140, Champions=2
LIGAS = {
    "🇪🇸 LaLiga": {"id": 140, "season": 2025},
    "🏆 Champions League": {"id": 2, "season": 2025},
}

def fetch_partidos_api():
    """Carga partidos de los próximos 7 días y últimos 3 días de LaLiga y Champions."""
    partidos = {}
    hoy = datetime.now(timezone.utc)
    desde = (hoy - timedelta(days=3)).strftime("%Y-%m-%d")
    hasta = (hoy + timedelta(days=7)).strftime("%Y-%m-%d")

    for comp, info in LIGAS.items():
        try:
            r = requests.get(
                "https://api-football-v1.p.rapidapi.com/v3/fixtures",
                headers=HEADERS_API,
                params={
                    "league": info["id"],
                    "season": info["season"],
                    "from": desde,
                    "to": hasta,
                    "timezone": "Europe/Madrid"
                },
                timeout=15
            )
            data = r.json()
            lista = []
            for f in data.get("response", []):
                fixture  = f["fixture"]
                teams    = f["teams"]
                goals    = f["goals"]
                status   = fixture["status"]["short"]
                date_str = fixture["date"]  # ISO string

                # Parsear fecha
                try:
                    dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                    dt_madrid = dt + timedelta(hours=2)  # CEST
                    fecha_fmt = dt_madrid.strftime("%a %d %b · %H:%M")
                except:
                    fecha_fmt = date_str[:10]

                if status in ["FT", "AET", "PEN"]:
                    estado = "final"
                    score  = (goals["home"] or 0, goals["away"] or 0)
                    home_pct = draw_pct = away_pct = None
                elif status in ["1H", "HT", "2H", "ET", "BT", "P", "SUSP", "INT", "LIVE"]:
                    estado = "en_vivo"
                    score  = (goals["home"] or 0, goals["away"] or 0)
                    home_pct = draw_pct = away_pct = None
                else:
                    estado = "programado"
                    score  = None
                    home_pct = draw_pct = away_pct = None

                lista.append({
                    "id":       f"f{fixture['id']}",
                    "home":     teams["home"]["name"],
                    "away":     teams["away"]["name"],
                    "fecha":    fecha_fmt,
                    "estado":   estado,
                    "score":    score,
                    "home_pct": home_pct,
                    "draw_pct": draw_pct,
                    "away_pct": away_pct,
                    "ts":       fixture["date"],
                })
            # Ordenar por fecha
            lista.sort(key=lambda x: x["ts"])
            partidos[comp] = lista
        except Exception as e:
            partidos[comp] = []

    return partidos

@st.cache_data(ttl=86400)  # Cache 24 horas
def get_partidos():
    return fetch_partidos_api()

# ── Auth helpers ──────────────────────────────────────────────────────────────
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def registrar(nombre, password):
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/usuarios?nombre=eq.{nombre}&select=id",
        headers=HEADERS_SB, timeout=10
    )
    if r.ok and r.json():
        return None, "Ya existe un usuario con ese nombre"
    r2 = requests.post(
        f"{SUPABASE_URL}/rest/v1/usuarios",
        headers=HEADERS_SB,
        json={"nombre": nombre, "password": hash_password(password)},
        timeout=10
    )
    if r2.ok and r2.json():
        return r2.json()[0], None
    return None, "Error al crear el usuario"

def login(nombre, password):
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/usuarios?nombre=eq.{nombre}&password=eq.{hash_password(password)}&select=*",
        headers=HEADERS_SB, timeout=10
    )
    if r.ok and r.json():
        return r.json()[0], None
    return None, "Nombre o contraseña incorrectos"

# ── Grupos ────────────────────────────────────────────────────────────────────
def crear_grupo(nombre_grupo, user_id):
    r = requests.post(
        f"{SUPABASE_URL}/rest/v1/grupos",
        headers=HEADERS_SB,
        json={"nombre": nombre_grupo, "creador_id": user_id},
        timeout=10
    )
    if r.ok and r.json():
        grupo = r.json()[0]
        requests.post(
            f"{SUPABASE_URL}/rest/v1/miembros",
            headers=HEADERS_SB,
            json={"grupo_id": grupo["id"], "user_id": user_id},
            timeout=10
        )
        return grupo, None
    return None, "Error al crear el grupo"

def unirse_grupo(codigo, user_id):
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/grupos?codigo=eq.{codigo}&select=*",
        headers=HEADERS_SB, timeout=10
    )
    if not r.ok or not r.json():
        return None, "Código no válido"
    grupo = r.json()[0]
    r_check = requests.get(
        f"{SUPABASE_URL}/rest/v1/miembros?grupo_id=eq.{grupo['id']}&user_id=eq.{user_id}&select=id",
        headers=HEADERS_SB, timeout=10
    )
    if r_check.ok and r_check.json():
        return grupo, "ya_miembro"
    r2 = requests.post(
        f"{SUPABASE_URL}/rest/v1/miembros",
        headers=HEADERS_SB,
        json={"grupo_id": grupo["id"], "user_id": user_id},
        timeout=10
    )
    if r2.status_code in [200, 201]:
        return grupo, None
    return None, "Error al unirse"

def get_mis_grupos(user_id):
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/miembros?user_id=eq.{user_id}&select=grupo_id",
        headers=HEADERS_SB, timeout=10
    )
    if not r.ok or not r.json():
        return []
    grupo_ids = [d["grupo_id"] for d in r.json()]
    if not grupo_ids:
        return []
    ids_str = ",".join(f'"{g}"' for g in grupo_ids)
    r2 = requests.get(
        f"{SUPABASE_URL}/rest/v1/grupos?id=in.({ids_str})&select=*",
        headers=HEADERS_SB, timeout=10
    )
    return r2.json() if r2.ok else []

def borrar_grupo(grupo_id):
    requests.delete(f"{SUPABASE_URL}/rest/v1/apuestas?grupo_id=eq.{grupo_id}", headers=HEADERS_SB, timeout=10)
    requests.delete(f"{SUPABASE_URL}/rest/v1/miembros?grupo_id=eq.{grupo_id}", headers=HEADERS_SB, timeout=10)
    requests.delete(f"{SUPABASE_URL}/rest/v1/grupos?id=eq.{grupo_id}", headers=HEADERS_SB, timeout=10)

def salir_grupo(grupo_id, user_id):
    requests.delete(
        f"{SUPABASE_URL}/rest/v1/miembros?grupo_id=eq.{grupo_id}&user_id=eq.{user_id}",
        headers=HEADERS_SB, timeout=10
    )

# ── Apuestas ──────────────────────────────────────────────────────────────────
def cargar_apuestas(grupo_id):
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/apuestas?grupo_id=eq.{grupo_id}&order=id.asc",
        headers=HEADERS_SB, timeout=10
    )
    return r.json() if r.ok else []

def guardar_apuesta(apuesta):
    r = requests.post(
        f"{SUPABASE_URL}/rest/v1/apuestas",
        headers=HEADERS_SB, json=apuesta, timeout=10
    )
    return r.ok

def actualizar_pagado(apuesta_id, pagado):
    requests.patch(
        f"{SUPABASE_URL}/rest/v1/apuestas?id=eq.{apuesta_id}",
        headers=HEADERS_SB, json={"pagado": pagado}, timeout=10
    )

def eliminar_apuesta(apuesta_id):
    requests.delete(
        f"{SUPABASE_URL}/rest/v1/apuestas?id=eq.{apuesta_id}",
        headers=HEADERS_SB, timeout=10
    )

def get_partido_por_id(pid, partidos):
    for lista in partidos.values():
        for p in lista:
            if p["id"] == pid:
                return p
    return None

def check_ganada(bet, partidos):
    partido = get_partido_por_id(bet["partido_id"], partidos)
    if not partido or partido["estado"] not in ["final"] or not partido.get("score"):
        return None
    h, a = partido["score"]
    return bet["goles_home"] == h and bet["goles_away"] == a

# ── Estilos ───────────────────────────────────────────────────────────────────
st.markdown("<style>.stApp { background-color: #0f0f1a; }</style>", unsafe_allow_html=True)

for key in ["user", "grupo", "confirmar_borrar"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ════════════════════════════════════════════════════════════════════════════
# LOGIN / REGISTRO
# ════════════════════════════════════════════════════════════════════════════
if not st.session_state.user:
    st.title("⚽ Porra Fútbol")
    tab_login, tab_reg = st.tabs(["🔑 Iniciar sesión", "📝 Registrarse"])

    with tab_login:
        nombre_l   = st.text_input("Nombre de usuario", key="l_nombre")
        password_l = st.text_input("Contraseña", type="password", key="l_pass")
        if st.button("Entrar", use_container_width=True, type="primary", key="btn_login"):
            if nombre_l.strip() and password_l:
                user, err = login(nombre_l.strip(), password_l)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error(f"❌ {err}")
            else:
                st.error("Rellena todos los campos")

    with tab_reg:
        nombre_r    = st.text_input("Elige un nombre de usuario", key="r_nombre")
        password_r  = st.text_input("Contraseña", type="password", key="r_pass")
        password_r2 = st.text_input("Repite la contraseña", type="password", key="r_pass2")
        if st.button("Crear cuenta", use_container_width=True, type="primary", key="btn_reg"):
            if not nombre_r.strip() or not password_r:
                st.error("Rellena todos los campos")
            elif password_r != password_r2:
                st.error("Las contraseñas no coinciden")
            else:
                user, err = registrar(nombre_r.strip(), password_r)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error(f"❌ {err}")
    st.stop()

# ════════════════════════════════════════════════════════════════════════════
# SELECCIÓN DE GRUPO
# ════════════════════════════════════════════════════════════════════════════
user = st.session_state.user

if not st.session_state.grupo:
    st.title("⚽ Porra Fútbol")
    col1, col2 = st.columns([3, 1])
    col1.markdown(f"Hola, **{user['nombre']}** 👋")
    if col2.button("Cerrar sesión"):
        st.session_state.user  = None
        st.session_state.grupo = None
        st.rerun()

    st.divider()
    mis_grupos = get_mis_grupos(user["id"])

    tab_mis, tab_crear, tab_unir = st.tabs(["📋 Mis grupos", "➕ Crear grupo", "🔗 Unirse con código"])

    with tab_mis:
        if not mis_grupos:
            st.info("Aún no perteneces a ningún grupo. Crea uno o pide el código a alguien.")
        for g in mis_grupos:
            es_creador = g.get("creador_id") == user["id"]
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.markdown(f"**{g['nombre']}**" + (" 👑" if es_creador else ""))
            if col2.button("Entrar", key=f"entrar_{g['id']}"):
                st.session_state.grupo = g
                st.session_state.confirmar_borrar = None
                st.rerun()
            if es_creador:
                if col3.button("🗑️", key=f"del_g_{g['id']}", help="Borrar grupo"):
                    st.session_state.confirmar_borrar = g["id"]
            else:
                if col3.button("🚪", key=f"salir_{g['id']}", help="Salir del grupo"):
                    salir_grupo(g["id"], user["id"])
                    st.rerun()

            if st.session_state.confirmar_borrar == g["id"]:
                st.warning(f"⚠️ ¿Borrar **{g['nombre']}** y todas sus apuestas?")
                c1, c2 = st.columns(2)
                if c1.button("✅ Sí, borrar", key=f"confirm_{g['id']}", type="primary"):
                    borrar_grupo(g["id"])
                    st.session_state.confirmar_borrar = None
                    st.rerun()
                if c2.button("❌ Cancelar", key=f"cancel_{g['id']}"):
                    st.session_state.confirmar_borrar = None
                    st.rerun()

    with tab_crear:
        nombre_grupo = st.text_input("Nombre del grupo (ej: Peñas del Bar)")
        if st.button("Crear grupo", use_container_width=True, type="primary"):
            if not nombre_grupo.strip():
                st.error("Escribe un nombre")
            else:
                grupo, err = crear_grupo(nombre_grupo.strip(), user["id"])
                if grupo:
                    st.session_state.grupo = grupo
                    st.rerun()
                else:
                    st.error(f"❌ {err}")

    with tab_unir:
        st.markdown("Pide el código al administrador del grupo:")
        codigo = st.text_input("Código del grupo")
        if st.button("Unirse", use_container_width=True, type="primary"):
            if not codigo.strip():
                st.error("Escribe el código")
            else:
                grupo, err = unirse_grupo(codigo.strip(), user["id"])
                if grupo:
                    st.session_state.grupo = grupo
                    st.rerun()
                elif err == "ya_miembro":
                    st.session_state.grupo = grupo
                    st.rerun()
                else:
                    st.error(f"❌ {err}")
    st.stop()

# ════════════════════════════════════════════════════════════════════════════
# CARGAR PARTIDOS (cache 24h)
# ════════════════════════════════════════════════════════════════════════════
with st.spinner("Cargando partidos..."):
    PARTIDOS = get_partidos()

# ════════════════════════════════════════════════════════════════════════════
# APP PRINCIPAL
# ════════════════════════════════════════════════════════════════════════════
grupo      = st.session_state.grupo
apuestas   = cargar_apuestas(grupo["id"])
es_creador = grupo.get("creador_id") == user["id"]

col_t, col_out = st.columns([4, 1])
col_t.title("⚽ Porra Fútbol")
col_t.caption(f"Grupo: **{grupo['nombre']}** · {user['nombre']}" + (" 👑" if es_creador else ""))
if col_out.button("← Grupos"):
    st.session_state.grupo = None
    st.rerun()

with st.expander("🔑 Código de invitación"):
    st.markdown("Comparte este código con tus amigos:")
    st.code(grupo["codigo"], language=None)

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

tab_partidos, tab_apuestas_tab = st.tabs(["🏟️ Partidos & Nueva apuesta", "📋 Apuestas del grupo"])

# ── TAB 1 ─────────────────────────────────────────────────────────────────────
with tab_partidos:
    st.subheader("➕ Registrar apuesta")

    jugador     = st.text_input("👤 Nombre del apostador", value=user["nombre"], key="jugador")
    cantidad    = st.number_input("💶 Cantidad (€)", min_value=0.5, value=10.0, step=0.5, key="cantidad")
    competicion = st.selectbox("🏆 Competición", list(PARTIDOS.keys()), key="competicion")

    partidos_comp = PARTIDOS.get(competicion, [])

    if not partidos_comp:
        st.warning("No hay partidos disponibles para esta competición.")
    else:
        opciones = []
        for p in partidos_comp:
            if p["estado"] == "final":
                icono = "✅"
            elif p["estado"] == "en_vivo":
                icono = "🔴 EN VIVO"
            else:
                icono = "🕐"
            score_str = f" ({p['score'][0]}-{p['score'][1]})" if p.get("score") else ""
            opciones.append(f"{icono}  {p['home']} vs {p['away']}{score_str}  ·  {p['fecha']}")

        partido_sel = st.selectbox("⚽ Partido", opciones, key="partido_sel")
        partido_obj = partidos_comp[opciones.index(partido_sel)]

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

        st.markdown(f"<div style='text-align:center;font-size:2em;font-weight:900;color:#fbbf24;margin:8px 0'>"
                    f"{goles_home} - {goles_away}</div>", unsafe_allow_html=True)

        if st.button("💾 Registrar apuesta", use_container_width=True, type="primary"):
            if not jugador.strip():
                st.error("⚠️ Escribe el nombre")
            else:
                ok = guardar_apuesta({
                    "jugador":     jugador.strip(),
                    "partido_id":  partido_obj["id"],
                    "competicion": competicion,
                    "goles_home":  int(goles_home),
                    "goles_away":  int(goles_away),
                    "cantidad":    float(cantidad),
                    "pagado":      False,
                    "grupo_id":    grupo["id"],
                    "user_id":     int(user["id"]),
                })
                if ok:
                    st.success(f"✅ **{jugador}** apuesta **{goles_home}-{goles_away}** → {cantidad:.2f}€")
                    st.rerun()
                else:
                    st.error("❌ Error al guardar la apuesta")

    st.divider()

    # Mostrar partidos
    for comp, lista in PARTIDOS.items():
        st.subheader(comp)
        if not lista:
            st.info("No hay partidos disponibles.")
            continue

        en_vivo  = [p for p in lista if p["estado"] == "en_vivo"]
        prog     = [p for p in lista if p["estado"] == "programado"]
        fin      = [p for p in lista if p["estado"] == "final"]

        if en_vivo:
            st.markdown("**🔴 EN VIVO**")
            for p in en_vivo:
                h, a = p["score"]
                st.markdown(f"""<div style="background:rgba(239,68,68,0.12);border:2px solid rgba(239,68,68,0.7);
                border-radius:10px;padding:12px;margin-bottom:8px">
                <small style="color:#ef4444;font-weight:700">🔴 EN VIVO · {p['fecha']}</small><br>
                <b>{p['home']}</b>
                &nbsp;<span style="font-size:1.3em;font-weight:900;color:#fff">{h} - {a}</span>&nbsp;
                <b>{p['away']}</b></div>""", unsafe_allow_html=True)

        if prog:
            st.markdown("**🕐 Próximos**")
            for p in prog:
                st.markdown(f"""<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);
                border-radius:10px;padding:12px;margin-bottom:8px">
                <small style="color:#fbbf24">{p['fecha']}</small><br>
                <b>{p['home']}</b> vs <b>{p['away']}</b></div>""", unsafe_allow_html=True)

        if fin:
            with st.expander(f"✅ Resultados recientes ({len(fin)})"):
                for p in fin:
                    h, a = p["score"]
                    st.markdown(f"""<div style="background:rgba(34,197,94,0.06);border:1px solid rgba(34,197,94,0.2);
                    border-radius:10px;padding:12px;margin-bottom:6px">
                    <small style="color:#86efac">✓ FINALIZADO · {p['fecha']}</small><br>
                    <b {'style="color:#22c55e"' if h > a else ''}>{p['home']}</b>
                    &nbsp;<span style="font-size:1.3em;font-weight:900">{h} - {a}</span>&nbsp;
                    <b {'style="color:#22c55e"' if a > h else ''}>{p['away']}</b>
                    </div>""", unsafe_allow_html=True)
        st.markdown("")

# ── TAB 2 ─────────────────────────────────────────────────────────────────────
with tab_apuestas_tab:
    if not apuestas:
        st.info("📭 Aún no hay apuestas en este grupo.")
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
            partido = get_partido_por_id(bet["partido_id"], PARTIDOS)
            ganada  = check_ganada(bet, PARTIDOS)

            if ganada is None:
                estado_icon, estado_txt = "🕐", "En juego"
            elif ganada:
                estado_icon, estado_txt = "🏆", "¡Acertada!"
            else:
                estado_icon, estado_txt = "❌", "Fallada"

            partido_str    = f"{partido['home']} vs {partido['away']}" if partido else "?"
            comp_str       = bet.get("competicion", "")
            real_score_txt = ""
            if partido and partido["estado"] == "final" and partido.get("score"):
                rh, ra = partido["score"]
                real_score_txt = f"  ·  Real: {rh}-{ra}"

            color_border = "#22c55e" if bet["pagado"] else "#ef4444"
            color_bg     = "rgba(34,197,94,0.08)" if bet["pagado"] else "rgba(239,68,68,0.08)"
            badge_txt    = "✅ PAGADO" if bet["pagado"] else "⏳ PENDIENTE"

            st.markdown(f"""
            <div style="background:{color_bg};border:1.5px solid {color_border};
            border-radius:12px;padding:14px 18px;margin-bottom:4px">
                <div style="display:flex;justify-content:space-between">
                    <b style="font-size:1.1em">{bet['jugador']}</b>
                    <b style="color:{color_border}">{badge_txt}</b>
                </div>
                <div style="color:#9ca3af;font-size:0.82em">{comp_str}</div>
                <div style="color:#d1d5db;font-size:0.9em">⚽ {partido_str}</div>
                <div style="display:flex;justify-content:space-between;align-items:center;margin-top:8px">
                    <div>
                        <span style="font-size:1.8em;font-weight:900;color:#fbbf24">{bet['goles_home']} - {bet['goles_away']}</span>
                        <span style="color:#9ca3af;font-size:0.85em">{real_score_txt}</span><br>
                        <span>{estado_icon} {estado_txt}</span>
                    </div>
                    <span style="font-size:1.3em;font-weight:900;color:#fbbf24">{bet['cantidad']:.2f}€</span>
                </div>
            </div>""", unsafe_allow_html=True)

            col_chk, col_del = st.columns([3, 1])
            with col_chk:
                nuevo = st.checkbox(
                    "Marcar como pagado" if not bet["pagado"] else "Marcar como pendiente",
                    value=bet["pagado"],
                    key=f"chk_{bet['id']}"
                )
                if nuevo != bet["pagado"]:
                    actualizar_pagado(bet["id"], nuevo)
                    st.rerun()
            with col_del:
                if st.button("🗑️", key=f"del_{bet['id']}"):
                    eliminar_apuesta(bet["id"])
                    st.rerun()

        st.divider()
        st.markdown("**📊 Resumen del grupo**")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total", f"{total:.2f}€")
        c2.metric("✅ Cobrado", f"{cobrado:.2f}€")
        c3.metric("⏳ Pendiente", f"{pendiente:.2f}€")
        if total > 0:
            st.progress(cobrado / total, text=f"{int(cobrado/total*100)}% cobrado")
