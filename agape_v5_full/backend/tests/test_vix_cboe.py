
import sys; sys.path.insert(0, 'backend')
from adapters.vix_cboe import VIXAdapter
def test_vix_latest():
    cfg={'csv_path':'backend/mock_data/vix_latest.csv'}
    res = VIXAdapter(cfg).fetch()
    assert abs(res['value'] - 16.8) < 1e-9
