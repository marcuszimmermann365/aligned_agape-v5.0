
import sys; sys.path.insert(0, 'backend')
from adapters.ghi_globalhunger import GHIAdapter
def test_ghi_avg():
    cfg={'csv_path':'backend/mock_data/ghi_mock.csv'}
    res = GHIAdapter(cfg).fetch()
    assert abs(res['value'] - 20.0) < 1e-9
