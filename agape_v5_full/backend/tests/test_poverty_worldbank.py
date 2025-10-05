
import sys; sys.path.insert(0, 'backend')
from adapters.poverty_worldbank import PovertyWBAdapter
def test_poverty_weighted():
    cfg={'csv_path':'backend/mock_data/poverty_mock.csv'}
    res = PovertyWBAdapter(cfg).fetch()
    assert abs(res['value'] - 10.0) < 1e-9
