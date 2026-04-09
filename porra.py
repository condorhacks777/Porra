import streamlit as st
import requests

RAPIDAPI_KEY = st.secrets["rapidapi"]["key"]
HEADERS_API = {"x-apisports-key": RAPIDAPI_KEY}
BASE_URL = "https://v3.football.api-sports.io"

st.title("🔧 Debug last/next")

for nombre, liga_id, season in [("LaLiga", 140, 2025), ("Champions", 2, 2025)]:
    st.subheader(nombre)
    for param, n in [("last", 3), ("next", 5)]:
        r = requests.get(
            f"{BASE_URL}/fixtures",
            headers=HEADERS_API,
            params={"league": liga_id, "season": season, param: n},
            timeout=15
        )
        data = r.json()
        partidos = data.get("response", [])
        errores  = data.get("errors", [])
        st.write(f"**{param}={n}** → Status {r.status_code} · {len(partidos)} partidos · Errores: {errores}")
        for p in partidos[:2]:
            st.write(f"  ⚽ {p['teams']['home']['name']} vs {p['teams']['away']['name']} · {p['fixture']['date'][:10]}")
