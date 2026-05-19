# Urban Access Brief — Bengaluru

Field intelligence system for city planning: network-based healthcare access, demand–supply gaps, underserved areas, and constrained facility placement (max 3 sites).

**City:** Bengaluru (BBMP extent)  
**Objective:** Maximize population within **15-minute** drive-time access to essential healthcare.

## Quick start

```bash
cd urban-access-brief
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 1) Download OSM facilities + WorldPop (network required; WorldPop ~500MB for India tile)
python scripts/01_download_data.py

# 2) Run full analysis (OSM network download + routing; 15–45 min depending on machine)
python scripts/run_pipeline.py

# 3) Launch dashboard
streamlit run app/streamlit_app.py
```

## Deploy dashboard (Streamlit Community Cloud)

1. Push this repo to GitHub (public or private with Streamlit access).
2. On [share.streamlit.io](https://share.streamlit.io): **New app** → repo → `app/streamlit_app.py`.
3. Pre-run pipeline locally and commit `data/processed/*.geojson` **or** add a Cloud secret and run pipeline in `packages.txt` + custom setup (recommended: commit processed outputs for assessment review).
4. Submit the **live URL** in your assessment.

## Project layout

| Path | Purpose |
|------|---------|
| `config.yaml` | City bbox, speeds, weights, optimization |
| `scripts/01_download_data.py` | Raw data acquisition |
| `scripts/run_pipeline.py` | Full analysis pipeline |
| `src/` | Reusable modules |
| `app/streamlit_app.py` | Hosted interactive UI |
| `docs/REPORT.md` | 2–4 page report template + AI Log |
| `data/processed/` | Outputs (GeoJSON, CSV, summary) |

## Data sources

| Source | Use | Limitations |
|--------|-----|-------------|
| [OpenStreetMap](https://www.openstreetmap.org) | Roads (OSMnx), healthcare POIs | Completeness varies; private clinics under-mapped |
| [WorldPop](https://www.worldpop.org) | Population grid | 100m model, not census ward totals |
| [HealthSites.io](https://healthsites.io) | Optional facility validation | Manual export; optional merge |
| BBMP / Census (optional) | Ward boundaries, demographics | Not required for core pipeline |

## Assumptions (defensible defaults)

- **Mode:** Driving (ambulance / private vehicle proxy for urgent primary care).
- **Speeds:** OSM highway-class speeds in `config.yaml` (urban peak ~20–35 km/h).
- **Time of day:** Static “typical congested” speeds — not peak vs off-peak sensitivity.
- **Capacity:** Type-based proxy (hospital/clinic/doctors), not bed counts.

## Evaluation alignment

1. **Understand the city** — Bengaluru rationale in `docs/REPORT.md`
2. **Real access** — Network travel times via OSMnx + Dijkstra
3. **Demand vs supply** — Nearest-facility load ratios
4. **Underserved** — Multi-factor composite score
5. **Decision** — Greedy 3-facility maximal covering with marginal impact table

## License

Assessment submission — open data sources retain their respective licenses.
# urban-access-brief
