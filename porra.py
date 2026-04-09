import streamlit as st
import requests

FD_KEY = st.secrets["footballdata"]["key"]
HEADERS = {"X-Auth-Token": FD_KEY}
BASE = "https://api.football-data.org/v4"

st.title("🔧 Debug football-data.org")

# LaLiga = PD, Champions = CL
for nombre, code in [("LaLiga", "PD"), ("Champions", "CL")]:
    st.subheader(nombre)
    r = requests.get(f"{BASE}/competitions/{code}/matches",
                     headers=HEADERS,
                     params={"status": "SCHEDULED,LIVE,IN_PLAY,PAUSED,FINISHED"},
                     timeout=15)
    st.write(f"Status: {r.status_code}")
    if r.ok:
        data = r.json()
        matches = data.get("matches", [])
        st.write(f"Partidos: {len(matches)}")
        for m in matches[:3]:
            home = m["homeTeam"]["name"]
            away = m["awayTeam"]["name"]
            date = m["utcDate"][:10]
            status = m["status"]
            st.write(f"⚽ {home} vs {away} · {date} · {status}")
    else:
        st.error(r.text)
