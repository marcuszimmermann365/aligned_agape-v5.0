
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

import json, math
class NewsEntropyAdapter(Adapter):
    name, source = "news_topic_entropy_bits", "GDELT or similar"
    def fetch(self) -> DataPoint:
        if self.cfg.get("json_path"):
            data = json.load(open(self.cfg["json_path"], "r", encoding="utf-8"))
            date_str = data.get("date") or dt.date.today().isoformat()
            counts = [t.get("count") for t in data.get("topics", []) if t.get("count") is not None]
        elif self.cfg.get("json_url"):
            content = _http_get(self.cfg["json_url"])
            data = json.loads(content.decode("utf-8"))
            date_str = data.get("date") or dt.date.today().isoformat()
            counts = [t.get("count") for t in data.get("topics", []) if t.get("count") is not None]
        else:
            if self.cfg.get("csv_path"):
                df = pd.read_csv(self.cfg["csv_path"])
            elif self.cfg.get("csv_url"):
                content = _http_get(self.cfg["csv_url"])
                df = pd.read_csv(io.BytesIO(content))
            else:
                raise ValueError("Provide json_url/json_path or csv_url/csv_path.")
            cols = {c.lower(): c for c in df.columns}
            count_col = None
            for k,v in cols.items():
                if "count" in k or "freq" in k:
                    count_col = v; break
            date_col = None
            for k,v in cols.items():
                if "date" in k:
                    date_col = v; break
            if count_col is None:
                raise ValueError("Missing Count/Freq column for news entropy.")
            if date_col is None:
                date_str = dt.date.today().isoformat()
            else:
                latest = str(pd.to_datetime(df[date_col], errors="coerce").max().date())
                date_str = latest
                df = df[df[date_col]==latest]
            counts = [float(x) for x in df[count_col].dropna().values.tolist() if x>0]
        if not counts:
            raise ValueError("No topic counts available.")
        s = float(sum(counts))
        probs = [c/s for c in counts if c>0]
        H = -sum(p*math.log2(p) for p in probs)
        return DataPoint(value=float(H), asof=date_str, source=self.source, raw={"topics": len(counts)})
