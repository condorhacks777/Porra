import streamlit as st
import requests

SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# ── Auth helpers ──────────────────────────────────────────────────────────────
def auth_headers(token):
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

def registrar(email, password, nombre):
    r = requests.post(
        f"{SUPABASE_URL}/auth/v1/signup",
        headers=HEADERS,
        json={"email": email, "password": password, "data": {"nombre": nombre}},
        timeout=10
    )
    return r.json()

def login(email, password):
    r = requests.post(
        f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
        headers=HEADERS,
        json={"email": email, "password": password},
        timeout=10
    )
    return r.json()

# ── DB helpers ────────────────────────────────────────────────────────────────
def crear_grupo(nombre, user_id, token):
    r = requests.post(
        f"{SUPABASE_URL}/rest/v1/grupos",
        headers=auth_headers(token),
        json={"nombre": nombre, "creador_id": user_id},
        timeout=10
    )
    data = r.json()
    if isinstance(data, list) and data:
        grupo = data[0]
        # Añadir creador como miembro
        requests.post(
            f"{SUPABASE_URL}/rest/v1/miembros",
            headers=auth_headers(token),
            json={"grupo_id": grupo["id"], "user_id": user_id},
            timeout=10
        )
        return grupo
    return None

def unirse_grupo(codigo, user_id, token):
    # Buscar grupo por código
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/grupos?codigo=eq.{codigo}&select=*",
        headers=auth_headers(token),
        timeout=10
    )
    grupos = r.json()
    if not grupos:
        return None, "Código de invitación no válido"
    grupo = grupos[0]
    # Unirse
    r2 = requests.post(
        f"{SUPABASE_URL}/rest/v1/miembros",
        headers=auth_headers(token),
        json={"grupo_id": grupo["id"], "user_id": user_id},
        timeout=10
    )
    if r2.status_code in [200, 201]:
        return grupo, None
    elif "unique" in r2.text.lower():
        return grupo, "Ya eres miembro de este grupo"
    return None, "Error al unirse al grupo"

def get_mis_grupos(user_id, token):
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/miembros?user_id=eq.{user_id}&select=grupo_id,grupos(*)",
        headers=auth_headers(token),
        timeout=10
    )
    data = r.json()
    return [d["grupos"] for d in data if d.get("grupos")] if isinstance(data, list) else []

def cargar_apuestas(grupo_id, token):
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/apuestas?grupo_id=eq.{grupo_id}&order=id.asc",
        headers=auth_headers(token),
        timeout=10
    )
    return r.json() if r.ok else []

def guardar_apuesta(apuesta, token):
    requests.post(
        f"{SUPABASE_URL}/rest/v1/apuestas",
        headers=auth_headers(token),
        json=apuesta,
        timeout=10
    )

def actualizar_pagado(apuesta_id, pagado, token):
    requests.patch(
        f"{SUPABASE_URL}/rest/v1/apuestas?id=eq.{apuesta_id}",
        headers=auth_headers(token),
        json={"pagado": pagado},
        timeout=10
    )

def eliminar_apuesta(apuesta_id, token):
    requests.delete(
        f"{SUPABASE_URL}/rest/v1/apuestas?id=eq.{apuesta_id}",
        headers=auth_headers(token),
        timeout=10
    )

# ── Datos partidos ────────────────────────────────────────────────────────────
PARTIDOS = {
    "🏆 Champions League": [
        {"id": "c1",  "home": "Real Madrid",      "away": "Bayern Munich",    "fecha": "Mar 7 Abr · FIN",      "estado": "final",      "score": (1, 2), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "c2",  "home": "Sporting CP",       "away": "Arsenal FC",       "fecha": "Mar 7 Abr · FIN",      "estado": "final",      "score": (0, 1), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "c3",  "home": "FC Barcelona",      "away": "Newcastle United", "fecha": "Mié 18 Mar · FIN",     "estado": "final",      "score": (7, 2), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "c4",  "home": "Tottenham",         "away": "Atlético Madrid",  "fecha": "Mié 18 Mar · FIN",     "estado": "final",      "score": (3, 2), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "c5",  "home": "Bayern Munich",     "away": "Atalanta BC",      "fecha": "Mié 18 Mar · FIN",     "estado": "final",      "score": (4, 1), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "c6",  "home": "Manchester City",   "away": "Real Madrid",      "fecha": "Mar 17 Mar · FIN",     "estado": "final",      "score": (1, 2), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "c7",  "home": "Chelsea FC",        "away": "PSG",              "fecha": "Mar 17 Mar · FIN",     "estado": "final",      "score": (0, 3), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "c8",  "home": "PSG",               "away": "Liverpool FC",     "fecha": "Mié 8 Abr · 21:00",   "estado": "programado", "score": None,   "home_pct": 54.2, "draw_pct": 23.1, "away_pct": 22.7},
        {"id": "c9",  "home": "FC Barcelona",      "away": "Atlético Madrid",  "fecha": "Mié 8 Abr · 21:00",   "estado": "programado", "score": None,   "home_pct": 63.6, "draw_pct": 18.7, "away_pct": 17.7},
        {"id": "c10", "home": "Liverpool FC",      "away": "PSG",              "fecha": "Mar 14 Abr · 21:00",  "estado": "programado", "score": None,   "home_pct": 24.5, "draw_pct": 23.0, "away_pct": 52.5},
        {"id": "c11", "home": "Atlético Madrid",   "away": "FC Barcelona",     "fecha": "Mar 14 Abr · 21:00",  "estado": "programado", "score": None,   "home_pct": 19.2, "draw_pct": 19.6, "away_pct": 61.2},
        {"id": "c12", "home": "Bayern Munich",     "away": "Real Madrid",      "fecha": "Mié 15 Abr · 21:00",  "estado": "programado", "score": None,   "home_pct": 60.8, "draw_pct": 19.2, "away_pct": 20.0},
        {"id": "c13", "home": "Arsenal FC",        "away": "Sporting CP",      "fecha": "Mié 15 Abr · 21:00",  "estado": "programado", "score": None,   "home_pct": 68.4, "draw_pct": 19.1, "away_pct": 12.5},
    ],
    "🇪🇸 LaLiga": [
        {"id": "l1",  "home": "Atlético Madrid",   "away": "FC Barcelona",     "fecha": "Sáb 4 Abr · FIN",     "estado": "final",      "score": (1, 2), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "l2",  "home": "Mallorca",           "away": "Real Madrid",      "fecha": "Sáb 4 Abr · FIN",     "estado": "final",      "score": (2, 1), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "l3",  "home": "Real Betis",         "away": "Espanyol",         "fecha": "Sáb 4 Abr · FIN",     "estado": "final",      "score": (0, 0), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "l4",  "home": "Getafe CF",          "away": "Athletic Bilbao",  "fecha": "Dom 5 Abr · FIN",     "estado": "final",      "score": (2, 0), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "l5",  "home": "Valencia CF",        "away": "Celta de Vigo",    "fecha": "Dom 5 Abr · FIN",     "estado": "final",      "score": (2, 3), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "l6",  "home": "Girona FC",          "away": "Villarreal CF",    "fecha": "Lun 6 Abr · FIN",     "estado": "final",      "score": (1, 0), "home_pct": None, "draw_pct": None, "away_pct": None},
        {"id": "l7",  "home": "Real Madrid",        "away": "Girona FC",        "fecha": "Vie 10 Abr · 21:00",  "estado": "programado", "score": None,   "home_pct": 75.0, "draw_pct": 14.6, "away_pct": 10.4},
        {"id": "l8",  "home": "Real Sociedad",      "away": "Dep. Alavés",      "fecha": "Sáb 11 Abr · 14:00",  "estado": "programado", "score": None,   "home_pct": 55.1, "draw_pct": 25.2, "away_pct": 19.7},
        {"id": "l9",  "home": "Elche CF",           "away": "Valencia CF",      "fecha": "Sáb 11 Abr · 16:15",  "estado": "programado", "score": None,   "home_pct": 38.9, "draw_pct": 28.7, "away_pct": 32.4},
        {"id": "l10", "home": "FC Barcelona",       "away": "Espanyol",         "fecha": "Sáb 11 Abr · 18:30",  "estado": "programado", "score": None,   "home_pct": 77.0, "draw_pct": 13.3, "away_pct":  9.7},
        {"id": "l11", "home": "Sevilla FC",         "away": "Atlético Madrid",  "fecha": "Sáb 11 Abr · 21:00",  "estado": "programado", "score": None,   "home_pct": 27.8, "draw_pct": 30.2, "away_pct": 42.0},
        {"id": "l12", "home": "Osasuna",            "away": "Real Betis",       "fecha": "Dom 12 Abr · 14:00",  "estado": "programado", "score": None,   "home_pct": 42.3, "draw_pct": 27.6, "away_pct": 30.1},
        {"id": "l13", "home": "Mallorca",           "away": "Rayo Vallecano",   "fecha": "Dom 12 Abr · 16:15",  "estado": "programado", "score": None,   "home_pct": 38.8, "draw_pct": 29.4, "away_pct": 31.8},
        {"id": "l14", "home": "Celta de Vigo",      "away": "Real Oviedo",      "fecha": "Dom 12 Abr · 18:30",  "estado": "programado", "score": None,   "home_pct": 57.8, "draw_pct": 24.0, "away_pct": 18.2},
        {"id": "l15", "home": "Athletic Bilbao",    "away": "Villarreal CF",    "fecha": "Dom 12 Abr · 21:00",  "estado": "programado", "score": None,   "home_pct": 42.0, "draw_pct": 27.2, "away_pct": 30.8},
        {"id": "l16", "home": "Levante UD",         "away": "Getafe CF",        "fecha": "Lun 13 Abr · 21:00",  "estado": "programado", "score": None,   "home_pct": 34.4, "draw_pct": 31.7, "away_pct": 33.9},
    ],
}

TODOS_PARTIDOS = [p for lista in PARTIDOS.values() for p in lista]

def get_partido(pid):
    return next((p for p in TODOS_PARTIDOS if p["id"] == pid), None)

def check_ganada(bet):
    partido = get_partido(bet["partido_id"])
    if not partido or partido["estado"] != "final" or not partido.get("score"):
        return None
    h, a = partido["score"]
    return bet["goles_home"] == h and bet["goles_away"] == a

# ── Estilos ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0f0f1a; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "token" not in st.session_state:
    st.session_state.token = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "nombre" not in st.session_state:
    st.session_state.nombre = None
if "grupo" not in st.session_state:
    st.session_state.grupo = None

# ── Capturar código de invitación desde URL ───────────────────────────────────
params = st.query_params
invite_code = params.get("invite", None)

# ════════════════════════════════════════════════════════════════════════════
# PANTALLA LOGIN / REGISTRO
# ════════════════════════════════════════════════════════════════════════════
if not st.session_state.token:
    st.title("⚽ Porra Fútbol")

    if invite_code:
        st.info(f"🎉 Has sido invitado a unirte a un grupo. Regístrate o inicia sesión para continuar.")

    tab_login, tab_reg = st.tabs(["🔑 Iniciar sesión", "📝 Registrarse"])

    with tab_login:
        email    = st.text_input("Email", key="login_email")
        password = st.text_input("Contraseña", type="password", key="login_pass")
        if st.button("Entrar", use_container_width=True, type="primary"):
            res = login(email, password)
            if "access_token" in res:
                st.session_state.token   = res["access_token"]
                st.session_state.user_id = res["user"]["id"]
                st.session_state.nombre  = res["user"].get("user_metadata", {}).get("nombre", email)
                st.rerun()
            else:
                msg = res.get("error_description", res.get("msg", "Error al iniciar sesión"))
                st.error(f"❌ {msg}")

    with tab_reg:
        nombre   = st.text_input("Tu nombre", key="reg_nombre")
        email    = st.text_input("Email", key="reg_email")
        password = st.text_input("Contraseña", type="password", key="reg_pass")
        if st.button("Crear cuenta", use_container_width=True, type="primary"):
            res = registrar(email, password, nombre)
            if "id" in res or ("user" in res and res["user"]):
                st.success("✅ Cuenta creada. Ya puedes iniciar sesión.")
            else:
                msg = res.get("error_description", res.get("msg", str(res)))
                st.error(f"❌ {msg}")

    st.stop()

# ════════════════════════════════════════════════════════════════════════════
# USUARIO LOGUEADO — SELECCIÓN DE GRUPO
# ════════════════════════════════════════════════════════════════════════════
token   = st.session_state.token
user_id = st.session_state.user_id
nombre  = st.session_state.nombre

# Si viene con código de invitación, unirse automáticamente
if invite_code and not st.session_state.grupo:
    grupo, err = unirse_grupo(invite_code, user_id, token)
    if grupo:
        st.session_state.grupo = grupo
        st.query_params.clear()
        st.rerun()

if not st.session_state.grupo:
    st.title("⚽ Porra Fútbol")
    st.markdown(f"Hola, **{nombre}** 👋")
    st.divider()

    mis_grupos = get_mis_grupos(user_id, token)

    tab_mis, tab_crear, tab_unir = st.tabs(["📋 Mis grupos", "➕ Crear grupo", "🔗 Unirse con código"])

    with tab_mis:
        if not mis_grupos:
            st.info("Aún no perteneces a ningún grupo. Crea uno o únete con un código.")
        for g in mis_grupos:
            col1, col2 = st.columns([3, 1])
            col1.markdown(f"**{g['nombre']}**")
            if col2.button("Entrar", key=f"entrar_{g['id']}"):
                st.session_state.grupo = g
                st.rerun()

    with tab_crear:
        nombre_grupo = st.text_input("Nombre del grupo (ej: Peñas del Bar)")
        if st.button("Crear grupo", use_container_width=True, type="primary"):
            if not nombre_grupo.strip():
                st.error("Escribe un nombre para el grupo")
            else:
                grupo = crear_grupo(nombre_grupo.strip(), user_id, token)
                if grupo:
                    st.session_state.grupo = grupo
                    st.rerun()
                else:
                    st.error("Error al crear el grupo")

    with tab_unir:
        codigo = st.text_input("Código de invitación")
        if st.button("Unirse", use_container_width=True, type="primary"):
            grupo, err = unirse_grupo(codigo.strip(), user_id, token)
            if grupo:
                st.session_state.grupo = grupo
                st.rerun()
            else:
                st.error(f"❌ {err}")

    st.stop()

# ════════════════════════════════════════════════════════════════════════════
# APP PRINCIPAL — DENTRO DEL GRUPO
# ════════════════════════════════════════════════════════════════════════════
grupo   = st.session_state.grupo
apuestas = cargar_apuestas(grupo["id"], token)

# Header
col_t, col_out = st.columns([4, 1])
col_t.title("⚽ Porra Fútbol")
col_t.caption(f"Grupo: **{grupo['nombre']}** · {nombre}")
if col_out.button("Salir", key="logout"):
    st.session_state.token   = None
    st.session_state.user_id = None
    st.session_state.nombre  = None
    st.session_state.grupo   = None
    st.rerun()

# Link de invitación
app_url = st.secrets.get("app_url", "https://tu-app.streamlit.app")
invite_url = f"{app_url}?invite={grupo['codigo']}"
with st.expander("🔗 Invitar al grupo"):
    st.markdown(f"Comparte este enlace con tus amigos:")
    st.code(invite_url)
    st.caption(f"O el código: **{grupo['codigo']}**")

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

tab_partidos, tab_apuestas = st.tabs(["🏟️ Partidos & Nueva apuesta", "📋 Apuestas del grupo"])

# ── TAB 1 — NUEVA APUESTA ─────────────────────────────────────────────────────
with tab_partidos:
    st.subheader("➕ Registrar apuesta")

    jugador     = st.text_input("👤 Nombre del apostador", value=nombre, key="jugador")
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
        f"{goles_home} - {goles_away}</div>", unsafe_allow_html=True)

    if st.button("💾 Registrar apuesta", use_container_width=True, type="primary"):
        if not jugador.strip():
            st.error("⚠️ Escribe el nombre del apostador")
        else:
            guardar_apuesta({
                "jugador":     jugador.strip(),
                "partido_id":  partido_obj["id"],
                "competicion": competicion,
                "goles_home":  int(goles_home),
                "goles_away":  int(goles_away),
                "cantidad":    float(cantidad),
                "pagado":      False,
                "grupo_id":    grupo["id"],
                "user_id":     user_id,
            }, token)
            st.success(f"✅ **{jugador}** apuesta **{goles_home}-{goles_away}** → {cantidad:.2f}€")
            st.rerun()

    st.divider()

    for comp, lista in PARTIDOS.items():
        st.subheader(comp)
        hoy  = [p for p in lista if p["estado"] == "programado" and "Hoy" in p["fecha"]]
        prog = [p for p in lista if p["estado"] == "programado" and "Hoy" not in p["fecha"]]
        fin  = [p for p in lista if p["estado"] == "final"]

        if hoy:
            st.markdown("**🔴 HOY**")
            for p in hoy:
                st.markdown(f"""<div style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.5);
                border-radius:10px;padding:12px;margin-bottom:8px">
                <small style="color:#ef4444;font-weight:700">🔴 HOY · {p['fecha']}</small><br>
                <b>{p['home']}</b> vs <b>{p['away']}</b></div>""", unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                c1.progress(p["home_pct"] / 100, text=f"Local {p['home_pct']}%")
                c2.progress(p["draw_pct"] / 100, text=f"Empate {p['draw_pct']}%")
                c3.progress(p["away_pct"] / 100, text=f"Visit. {p['away_pct']}%")

        if prog:
            st.markdown("**🕐 Próximos**")
            for p in prog:
                st.markdown(f"""<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);
                border-radius:10px;padding:12px;margin-bottom:8px">
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
                    st.markdown(f"""<div style="background:rgba(34,197,94,0.06);border:1px solid rgba(34,197,94,0.2);
                    border-radius:10px;padding:12px;margin-bottom:6px">
                    <small style="color:#86efac">✓ FINALIZADO · {p['fecha']}</small><br>
                    <b {'style="color:#22c55e"' if h > a else ''}>{p['home']}</b>
                    &nbsp;<span style="font-size:1.3em;font-weight:900">{h} - {a}</span>&nbsp;
                    <b {'style="color:#22c55e"' if a > h else ''}>{p['away']}</b>
                    </div>""", unsafe_allow_html=True)
        st.markdown("")

# ── TAB 2 — APUESTAS DEL GRUPO ────────────────────────────────────────────────
with tab_apuestas:
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
            partido = get_partido(bet["partido_id"])
            ganada  = check_ganada(bet)

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
                    actualizar_pagado(bet["id"], nuevo, token)
                    st.rerun()
            with col_del:
                if st.button("🗑️", key=f"del_{bet['id']}"):
                    eliminar_apuesta(bet["id"], token)
                    st.rerun()

        st.divider()
        st.markdown("**📊 Resumen del grupo**")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total", f"{total:.2f}€")
        c2.metric("✅ Cobrado", f"{cobrado:.2f}€")
        c3.metric("⏳ Pendiente", f"{pendiente:.2f}€")
        if total > 0:
            st.progress(cobrado / total, text=f"{int(cobrado/total*100)}% cobrado")
