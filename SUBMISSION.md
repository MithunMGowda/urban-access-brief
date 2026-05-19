# Quick submission guide

## Your two recommended sites (Site 1 removed)

| Rank | Area | Latitude | Longitude | Maps |
|------|------|----------|-----------|------|
| **2** | North Vijayanagara (Mysore Rd) | 12.97322 | 77.54944 | [Open](https://www.google.com/maps?q=12.97322,77.54944) |
| **3** | South Bapuji Nagar | 12.95520 | 77.54465 | [Open](https://www.google.com/maps?q=12.9552,77.54465) |

**Excluded:** Site 1 @ 12.95972, 77.54470 (not proposed).

---

## Documents

| Document | Path |
|----------|------|
| **Submission report (PDF this)** | `docs/SUBMISSION_REPORT.md` |
| **SOP (how to run & host)** | `docs/SOP.md` |

---

## Run dashboard locally

```bash
cd /Users/mithun.m/urban-access-brief
streamlit run app/streamlit_app.py
```

---

## Host on Streamlit Cloud (~20 min)

```bash
cd /Users/mithun.m/urban-access-brief
git config user.email "YOUR@EMAIL.com"
git config user.name "Your Name"
git add -A && git commit -m "Dashboard: recommended sites 2 and 3"
# Create repo on github.com, then:
git remote add origin https://github.com/YOUR_USER/urban-access-brief.git
git push -u origin main
```

1. https://share.streamlit.io → New app  
2. Repo: `YOUR_USER/urban-access-brief`  
3. Main file: **`app/streamlit_app.py`**  
4. Copy URL → paste in `docs/SUBMISSION_REPORT.md` and assessment form  

**Important:** `data/processed/` must be committed (geojson + json) so the cloud app has data.

---

## Form copy-paste

- **City:** Bengaluru — Vijayanagara & Bapuji Nagar (BBMP)  
- **Objective:** 15-minute drive-time access; propose **2** facilities (Sites 2 & 3); Site 1 excluded  
- **Finding:** Existing coverage 100% on network but hospital #13 overloaded (~8.4×); Sites 2–3 balance load along Mysore Road corridor  

---

## Dashboard URL

_Paste after deploy:_ _______________________________
