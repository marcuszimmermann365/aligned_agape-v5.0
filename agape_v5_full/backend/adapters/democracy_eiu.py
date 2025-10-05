
from .base import Adapter, DataPoint
import datetime as dt, io, pandas as pd

import requests, time
def _http_get(url: str, timeout: int = 45) -> bytes:
    s = requests.Session()
    for attempt in range(3):
        try:
            r = s.get(url, timeout=timeout)
            r.raise_for_status()
            return r.content
        except Exception:
            if attempt == 2: raise
            time.sleep(1.5*(attempt+1))

class DemocracyEIUAdapter(Adapter):
    name, source = "democracy_idx_avg", "Economist Intelligence Unit"
    def fetch(self) -> DataPoint:
        if self.cfg.get("csv_path"):
            df = pd.read_csv(self.cfg["csv_path"])
        elif self.cfg.get("csv_url"):
            content = _http_get(self.cfg["csv_url"])
            df = pd.read_csv(io.BytesIO(content))
        else:
            raise ValueError("Provide csv_url or csv_path.")
        cols = {c.lower(): c for c in df.columns}
        year = cols.get("year")
        score = None
        for k,v in cols.items():
            if "score" in k or "index" in k:
                score = v; break
        if year is None or score is None:
            raise ValueError("Missing Year/Score columns for Democracy Index.")
        df[score] = pd.to_numeric(df[score], errors="coerce")
        y = int(pd.to_numeric(df[year], errors="coerce").max())
        val = float(df[df[year].astype(str)==str(y)][score].mean())
        return DataPoint(value=val, asof=dt.date.today().isoformat(), source=self.source, raw={"year": y})
