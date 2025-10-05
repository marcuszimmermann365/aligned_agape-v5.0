
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

class PovertyWBAdapter(Adapter):
    name, source = "poverty_rate_extreme", "World Bank"
    def fetch(self) -> DataPoint:
        if self.cfg.get("csv_path"):
            df = pd.read_csv(self.cfg["csv_path"])
        elif self.cfg.get("csv_url"):
            content = _http_get(self.cfg["csv_url"])
            df = pd.read_csv(io.BytesIO(content))
        else:
            raise ValueError("Provide csv_url or csv_path.")
        cols = {c.lower(): c for c in df.columns}
        year_col = None
        for k,v in cols.items():
            if "year" in k:
                year_col = v; break
        pov_col = None
        for k,v in cols.items():
            if "pover" in k:
                pov_col = v; break
        if year_col is None or pov_col is None:
            raise ValueError("Missing Year/Poverty columns for World Bank poverty.")
        df[pov_col] = pd.to_numeric(df[pov_col], errors="coerce")
        y = int(pd.to_numeric(df[year_col], errors="coerce").max())
        latest = df[df[year_col].astype(str)==str(y)]
        if "population" in cols:
            latest = latest.dropna(subset=[pov_col, cols["population"]])
            w = latest[cols["population"]]
            val = float((latest[pov_col]*w).sum()/w.sum())
        else:
            val = float(latest[pov_col].mean())
        return DataPoint(value=val, asof=dt.date.today().isoformat(), source=self.source, raw={"year": y})
