
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

class HDIAdapter(Adapter):
    name, source = "hdi_global_avg", "UNDP / OWID"
    def fetch(self) -> DataPoint:
        if self.cfg.get("csv_path"):
            df = pd.read_csv(self.cfg["csv_path"])
        elif self.cfg.get("csv_url"):
            content = _http_get(self.cfg["csv_url"])
            df = pd.read_csv(io.BytesIO(content))
        else:
            raise ValueError("Provide csv_url or csv_path.")
        cols = {c.lower(): c for c in df.columns}
        year = None
        for k,v in cols.items():
            if "year" in k:
                year = v; break
        hdi_col = None
        for k,v in cols.items():
            if "hdi" in k:
                hdi_col = v; break
        if year is None or hdi_col is None:
            raise ValueError("Missing Year/HDI columns.")
        df[hdi_col] = pd.to_numeric(df[hdi_col], errors="coerce")
        y = int(pd.to_numeric(df[year], errors="coerce").max())
        val = float(df[df[year].astype(str)==str(y)][hdi_col].mean())
        return DataPoint(value=val, asof=dt.date.today().isoformat(), source=self.source, raw={"year": y})
