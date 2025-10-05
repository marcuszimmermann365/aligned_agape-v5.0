
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

class VIXAdapter(Adapter):
    name, source = "vix", "CBOE"
    def fetch(self) -> DataPoint:
        if self.cfg.get("csv_path"):
            df = pd.read_csv(self.cfg["csv_path"])
        elif self.cfg.get("csv_url"):
            content = _http_get(self.cfg["csv_url"])
            df = pd.read_csv(io.BytesIO(content))
        else:
            raise ValueError("Provide csv_url or csv_path for VIX.")
        cols = {c.lower(): c for c in df.columns}
        date_col = next((v for k,v in cols.items() if "date" in k), None)
        close_col = next((v for k,v in cols.items() if "close" in k or "last" in k or "price" in k), None)
        if date_col is None or close_col is None:
            raise ValueError("VIX CSV must have Date and Close.")
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df[close_col] = pd.to_numeric(df[close_col], errors="coerce")
        df = df.dropna(subset=[date_col, close_col]).sort_values(date_col)
        latest = df.iloc[-1]
        return DataPoint(value=float(latest[close_col]), asof=str(latest[date_col].date()), source=self.source, raw={"rows": len(df)})
