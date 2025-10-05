
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

class UNESCOUiSLiteracyAdapter(Adapter):
    name, source = "literacy_rate", "UNESCO UIS"
    def fetch(self) -> DataPoint:
        if self.cfg.get("csv_path"):
            df = pd.read_csv(self.cfg["csv_path"])
        elif self.cfg.get("csv_url"):
            content = _http_get(self.cfg["csv_url"])
            df = pd.read_csv(io.BytesIO(content))
        else:
            raise ValueError("Provide csv_url or csv_path for UNESCO literacy.")
        cols = {c.lower(): c for c in df.columns}
        year = next((v for k,v in cols.items() if "year" in k), None)
        rate = next((v for k,v in cols.items() if "literacy" in k), None)
        if year is None or rate is None:
            raise ValueError("UNESCO literacy CSV must have Year and LiteracyRate columns.")
        df[rate] = pd.to_numeric(df[rate], errors="coerce")
        y = int(pd.to_numeric(df[year], errors="coerce").max())
        latest = df[df[year].astype(str) == str(y)]
        val = float(latest[rate].mean())
        return DataPoint(value=val, asof=dt.date.today().isoformat(), source=self.source, raw={"year": y, "rows": len(latest)})
