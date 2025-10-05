
def lin_norm(value, hist_min, hist_max, invert=False):
    try:
        v = float(value)
    except Exception:
        return 0.0
    if hist_min is None or hist_max is None:
        return 0.0
    a, b = (float(hist_min), float(hist_max))
    if a == b:
        return 0.5
    if invert:
        a, b = b, a
    t = (v - a) / (b - a)
    return max(0.0, min(1.0, t))

def weighted_avg(items):
    num = 0.0
    den = 0.0
    for it in items:
        w = float(it.get("w", 0.0))
        num += float(it.get("norm", 0.0)) * w
        den += w
    return (num / den) if den > 0 else 0.0

def ema(prev, new, alpha):
    try:
        p = float(prev)
    except Exception:
        p = float(new)
    return float(alpha) * float(new) + (1.0 - float(alpha)) * p
