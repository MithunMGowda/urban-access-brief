"""
Urban Access Brief — Vijayanagara & Bapuji Nagar
Recommended facilities: Site 2 and Site 3 only (Site 1 excluded).
"""

from __future__ import annotations

import json
from pathlib import Path

import folium
import geopandas as gpd
import pandas as pd
import streamlit as st
from folium.plugins import HeatMap
from streamlit_folium import st_folium

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"

st.set_page_config(
    page_title="BBMP Healthcare Access | Vijayanagara & Bapuji Nagar",
    page_icon="🏥",
    layout="wide",
)

st.title("Healthcare Access — Vijayanagara & Bapuji Nagar")
st.caption("Bengaluru · BBMP wards · Your road network · Recommended sites **2 & 3** (priority 1 removed)")


@st.cache_data
def load_geo(name: str):
    p = PROCESSED / name
    return gpd.read_file(p) if p.exists() else None


@st.cache_data
def load_json(name: str):
    p = PROCESSED / name
    return json.loads(p.read_text()) if p.exists() else {}


demand = load_geo("demand_access.geojson")
facilities = load_geo("facilities_load.geojson")
proposed = load_geo("proposed_facilities.geojson")
wards = load_geo("wards.geojson")
study = load_geo("study_area.geojson")
sites = load_json("recommended_sites.json")
summary = load_json("summary.json")

if demand is None:
    st.error("Run `python3 scripts/run_user_data.py` first to build data/processed/.")
    st.stop()

# --- Recommended sites panel (hero) ---
st.header("Recommended new facilities")
st.info(
    "**Priority 1 (12.9597°N, 77.5447°N — south Bapujinagar)** was **removed** from this recommendation "
    "after review. The two sites below are proposed for implementation."
)

rec = sites.get("recommended", [])
if rec:
    c1, c2 = st.columns(2)
    for col, site in zip([c1, c2], rec):
        with col:
            st.subheader(f"Site {site['rank']}: {site['name']}")
            st.metric("Coordinates", f"{site['lat']:.5f}, {site['lon']:.5f}")
            st.link_button("Open in Google Maps", site["google_maps"], use_container_width=True)

with st.expander("Why was Site 1 excluded?"):
    ex = sites.get("excluded", {})
    st.markdown(
        f"- **Location:** {ex.get('lat')}, {ex.get('lon')}\n"
        f"- **Reason:** {ex.get('reason', 'Planning review')}"
    )

st.divider()

# --- Metrics ---
total_pop = float(demand["population"].sum())
within = float(demand.loc[demand["min_travel_min"] <= 15, "population"].sum())
m1, m2, m3, m4 = st.columns(4)
m1.metric("Population (study area)", f"{total_pop:,.0f}")
m2.metric("Within 15 min (existing)", f"{100 * within / total_pop:.1f}%")
m3.metric("Existing hospitals", len(facilities) if facilities is not None else 0)
m4.metric("Recommended new sites", 2)

# --- Map ---
threshold = st.sidebar.slider("Access threshold (min)", 5, 30, 15)
show_heat = st.sidebar.checkbox("Population heatmap", True)
show_existing = st.sidebar.checkbox("Existing hospitals", True)
layer = st.sidebar.radio("Map focus", ["Recommended sites 2 & 3", "Demand–supply load", "Access & travel time"])

center = [12.965, 77.546]
m = folium.Map(location=center, zoom_start=14, tiles="CartoDB positron")

if study is not None and not study.empty:
    folium.GeoJson(
        study.to_json(),
        style_function=lambda _: {"color": "#f9a825", "weight": 2, "fillOpacity": 0.1, "fillColor": "#fff9c4"},
    ).add_to(m)
if wards is not None and not wards.empty:
    folium.GeoJson(
        wards.to_json(),
        style_function=lambda _: {"color": "#6a1b9a", "weight": 2, "fillOpacity": 0},
    ).add_to(m)

if show_heat:
    pts = [[r.geometry.y, r.geometry.x, float(r["population"])] for _, r in demand.iterrows()]
    if pts:
        HeatMap(pts, radius=14, blur=12).add_to(m)

for _, row in demand.iterrows():
    color = "#1a9850" if row["min_travel_min"] <= threshold else "#d73027"
    folium.CircleMarker(
        [row.geometry.y, row.geometry.x],
        radius=4,
        color=color,
        fill=True,
        fill_opacity=0.5,
        popup=f"Pop {row['population']:.0f} · {row['min_travel_min']:.1f} min",
    ).add_to(m)

if show_existing and facilities is not None:
    for _, row in facilities.iterrows():
        lr = row.get("load_ratio", 0)
        folium.CircleMarker(
            [row.geometry.y, row.geometry.x],
            radius=7,
            color="#d73027" if lr > 1 else "#2166ac",
            fill=True,
            popup=f"{row.get('name', 'Hospital')}<br>Load ratio: {lr:.2f}",
        ).add_to(m)

if proposed is not None and not proposed.empty:
    colors = {2: "green", 3: "darkgreen"}
    for _, row in proposed.iterrows():
        rank = int(row.get("priority_rank", 0))
        folium.Marker(
            [row.geometry.y, row.geometry.x],
            popup=f"<b>{row['name']}</b><br>{row.get('rationale', '')}",
            icon=folium.Icon(color=colors.get(rank, "red"), icon="plus-sign"),
        ).add_to(m)

st.subheader(layer)
st_folium(m, width=1200, height=550)

if layer == "Demand–supply load" and facilities is not None:
    st.subheader("Existing facility load (BBMP + buffer)")
    st.dataframe(
        facilities[["name", "load_ratio", "assigned_demand", "capacity"]].sort_values(
            "load_ratio", ascending=False
        ),
        hide_index=True,
    )
    st.caption("Red markers = overloaded (load ratio > 1). Site 2 targets relief near hospital #13.")

st.divider()
with st.expander("Data & method (for assessors)"):
    st.markdown(
        """
        | Layer | Source |
        |-------|--------|
        | Wards | `2003_BBMP.shp` (Vijayanagara, Bapuji Nagar) |
        | Roads | `roads.geojson` + `junctions.geojson` |
        | Hospitals | Desktop `bbmp hospital.geojson` (+ 2.5 km buffer) |
        | Population | WorldPop raster or ward-density fallback |
        | Access | Minimum **drive** time on clipped road graph (15 min threshold) |

        **Recommendation logic:** Ranked underserved grid cells along Mysore/Chord Road; **Site 1 dropped**; **Sites 2–3** retained for north Vijayanagara and south Bapuji Nagar equity.
        """
    )
