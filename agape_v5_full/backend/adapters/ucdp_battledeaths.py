
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

class UCDPDeathsAdapter(Adapter):
    name, source = "ucdp_conflict_fatalities", "UCDP"
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
        deaths = None
        for k,v in cols.items():
            if "fatal" in k or "deaths" in k:
                deaths = v; break
        if year is None or deaths is None:
            raise ValueError("Missing Year/Fatalities columns for UCDP.")
        df[deaths] = pd.to_numeric(df[deaths], errors="coerce")
        y = int(pd.to_numeric(df[year], errors="coerce").max())
        val = float(df[df[year].astype(str)==str(y)][deaths].sum())
        return DataPoint(value=val, asof=dt.date.today().isoformat(), source=self.source, raw={"year": y})
