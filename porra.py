import streamlit as st
import requests
from datetime import datetime, timedelta, timezone

RAPIDAPI_KEY = st.secrets["rapidapi"]["key"]

# Endpoint directo de api-football.com (no RapidAPI)
HEADERS_API = {
    "x-apisports-key": RAPIDAPI_KEY
}
BASE_URL = "https://v3.football.api-sports.io"

st.title("🔧 Debug API Football")

hoy   = datetime.now(timezone.utc)
desde = (hoy - timedelta(days=3)).strftime("%Y-%m-%d")
hasta = (hoy + timedelta(days=7)).strftime("%Y-%m-%d")

st.write(f"Desde **{desde}** hasta **{hasta}**")

# Primero comprobar el estado de la cuenta
st.subheader("Estado de la cuenta")
r_status = requests.get(f"{BASE_URL}/status", headers=HEADERS_API, timeout=10)
st.write(f"Status code: {r_status.status_code}")
if r_status.ok:
    st.json(r_status.json())

st.divider()

for nombre, liga_id, season in [("LaLiga", 140, 2024), ("Champions", 2, 2024)]:
    st.subheader(nombre)
    try:
        r = requests.get(
            f"{BASE_URL}/fixtures",
            headers=HEADERS_API,
            params={
                "league": liga_id,
                "season": season,
                "from": desde,
                "to": hasta,
                "timezone": "Europe/Madrid"
            },
            timeout=15
        )
        st.write(f"Status: {r.status_code}")
        data = r.json()
        st.write(f"Partidos: {len(data.get('response', []))}")
        if data.get("errors"):
            st.error(f"Errores: {data['errors']}")
        if data.get("response"):
            st.json(data["response"][0])
    except Exception as e:
        st.error(f"Excepción: {e}")
