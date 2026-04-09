import streamlit as st
import requests
from datetime import datetime, timedelta, timezone

RAPIDAPI_KEY = st.secrets["rapidapi"]["key"]

HEADERS_API = {"x-apisports-key": RAPIDAPI_KEY}
BASE_URL = "https://v3.football.api-sports.io"

st.title("🔧 Debug API Football")

hoy   = datetime.now(timezone.utc)
desde = (hoy - timedelta(days=3)).strftime("%Y-%m-%d")
hasta = (hoy + timedelta(days=7)).strftime("%Y-%m-%d")

st.write(f"Desde **{desde}** hasta **{hasta}**")

for nombre, liga_id in [("LaLiga", 140), ("Champions", 2)]:
    st.subheader(nombre)
    for season in [2025, 2026]:
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
        data = r.json()
        n = len(data.get("response", []))
        st.write(f"Temporada {season} → {n} partidos")
        if n > 0:
            p = data["response"][0]
            st.write(f"✅ {p['teams']['home']['name']} vs {p['teams']['away']['name']} · {p['fixture']['date'][:10]}")
