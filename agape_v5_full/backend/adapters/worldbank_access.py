
from .base import Adapter, DataPoint
import datetime as dt, io, pandas as pd, numpy as np

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

class WorldBankAccessAdapter(Adapter):
    name, source = "access_avg_electricity_internet", "World Bank API"
    def fetch(self) -> DataPoint:
        # This demo expects curated Excel/CSV already flattened to: Country,Year,Electricity,Internet
        if self.cfg.get("csv_path"):
            df = pd.read_csv(self.cfg["csv_path"])
        else:
            raise ValueError("Provide csv_path for WorldBankAccess demo.")
        cols = {c.lower(): c for c in df.columns}
        year = cols.get("year")
        el = None
        it = None
        for k,v in cols.items():
            if "electric" in k:
                el = v
            if "internet" in k:
                it = v
        if year is None or el is None or it is None:
            raise ValueError("Missing Year/Electricity/Internet columns.")
        df[el] = pd.to_numeric(df[el], errors="coerce")
        df[it] = pd.to_numeric(df[it], errors="coerce")
        y = int(pd.to_numeric(df[year], errors="coerce").max())
        latest = df[df[year].astype(str)==str(y)][[el,it]].mean()
        val = float(latest.mean())
        return DataPoint(value=val, asof=dt.date.today().isoformat(), source=self.source, raw={"year": y})
