import streamlit as st
import requests
from datetime import datetime, timezone

RAPIDAPI_KEY = st.secrets["rapidapi"]["key"]
HEADERS_API = {"x-apisports-key": RAPIDAPI_KEY}
BASE_URL = "https://v3.football.api-sports.io"

st.title("🔧 Debug API Football")

hoy = datetime.now(timezone.utc).strftime("%Y-%m-%d")
st.write(f"Hoy: **{hoy}**")

# Test 1: partidos de hoy
st.subheader("Partidos de HOY (sin liga)")
r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS_API,
                 params={"date": hoy, "timezone": "Europe/Madrid"}, timeout=15)
data = r.json()
st.write(f"Status: {r.status_code} · Partidos: {len(data.get('response', []))}")
if data.get("errors"):
    st.error(str(data["errors"]))
for f in data.get("response", [])[:5]:
    st.write(f"⚽ {f['teams']['home']['name']} vs {f['teams']['away']['name']} · Liga {f['league']['id']} {f['league']['name']}")

st.divider()

# Test 2: LaLiga temporada 2025 últimas jornadas
st.subheader("LaLiga 2025 - última jornada")
r2 = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS_API,
                  params={"league": 140, "season": 2025, "last": 10}, timeout=15)
data2 = r2.json()
st.write(f"Status: {r2.status_code} · Partidos: {len(data2.get('response', []))}")
for f in data2.get("response", [])[:3]:
    st.write(f"⚽ {f['teams']['home']['name']} vs {f['teams']['away']['name']} · {f['fixture']['date'][:10]}")

st.divider()

# Test 3: LaLiga 2025 próximos
st.subheader("LaLiga 2025 - próximos")
r3 = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS_API,
                  params={"league": 140, "season": 2025, "next": 10}, timeout=15)
data3 = r3.json()
st.write(f"Status: {r3.status_code} · Partidos: {len(data3.get('response', []))}")
for f in data3.get("response", [])[:3]:
    st.write(f"⚽ {f['teams']['home']['name']} vs {f['teams']['away']['name']} · {f['fixture']['date'][:10]}")
