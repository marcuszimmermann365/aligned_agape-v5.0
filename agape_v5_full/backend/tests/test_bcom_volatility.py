
import sys; sys.path.insert(0, 'backend')
from adapters.bcom_volatility import BCOMVolAdapter
def test_bcom_vol_latest():
    cfg={'csv_path':'backend/mock_data/bcom_volatility_daily.csv'}
    res = BCOMVolAdapter(cfg).fetch()
    assert abs(res['value'] - 15.2) < 1e-9
