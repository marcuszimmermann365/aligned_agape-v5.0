
# Agape V5 – Empirically Grounded Explorer (Runnable Skeleton)

## 1) Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## 2) Run collector once
```bash
python backend/collector/background_collector.py
# world_state.json -> backend/world_data/world_state.json
```

## 3) Start API & open dashboard
```bash
uvicorn backend.live_server:app --reload --port 8000
# Open: http://localhost:8000/static/dashboard.html
```

## 4) Tests
```bash
PYTHONPATH=backend:. pytest -q
```

Hinweis: `backend/world_data/catalog.yaml` enthält Platzhalter-Feeds; bitte an eure Endpoints anpassen.
