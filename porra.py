import streamlit as st
import requests
from datetime import datetime, timedelta, timezone

RAPIDAPI_KEY = st.secrets["rapidapi"]["key"]

HEADERS_API = {
    "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
    "x-rapidapi-key": RAPIDAPI_KEY
}

st.title("🔧 Debug API Football")

hoy   = datetime.now(timezone.utc)
desde = (hoy - timedelta(days=3)).strftime("%Y-%m-%d")
hasta = (hoy + timedelta(days=7)).strftime("%Y-%m-%d")

st.write(f"Buscando partidos desde **{desde}** hasta **{hasta}**")

for nombre, liga_id, season in [("LaLiga", 140, 2024), ("Champions", 2, 2024)]:
    st.subheader(nombre)
    try:
        r = requests.get(
            "https://api-football-v1.p.rapidapi.com/v3/fixtures",
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
        st.write(f"Status code: {r.status_code}")
        data = r.json()
        st.write(f"Partidos encontrados: {len(data.get('response', []))}")
        if data.get("errors"):
            st.error(f"Errores API: {data['errors']}")
        if data.get("response"):
            st.json(data["response"][0])  # Mostrar primer partido
    except Exception as e:
        st.error(f"Excepción: {e}")
