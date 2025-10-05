
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

class NetBlocksAdapter(Adapter):
    name, source = "netblocks_outage_days", "NetBlocks"
    def fetch(self) -> DataPoint:
        if self.cfg.get("csv_path"):
            df = pd.read_csv(self.cfg["csv_path"])
        elif self.cfg.get("csv_url"):
            content = _http_get(self.cfg["csv_url"])
            df = pd.read_csv(io.BytesIO(content))
        else:
            raise ValueError("Provide csv_url or csv_path.")
        cols = {c.lower(): c for c in df.columns}
        date_col = None
        for k,v in cols.items():
            if "date" in k:
                date_col = v; break
        if date_col is None:
            raise ValueError("Missing date column for NetBlocks.")
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        cutoff = pd.Timestamp(dt.date.today()) - pd.Timedelta(days=365)
        recent = df[df[date_col] >= cutoff]
        if "incidents" in cols:
            v = recent[recent[cols["incidents"]] > 0][date_col].dt.date.nunique()
        else:
            v = recent[date_col].dt.date.nunique()
        return DataPoint(value=float(v), asof=dt.date.today().isoformat(), source=self.source, raw={"window_days": 365})
