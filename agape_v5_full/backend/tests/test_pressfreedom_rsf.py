
import sys; sys.path.insert(0, 'backend')
from adapters.pressfreedom_rsf import PressFreedomRSFAdapter
def test_rsf_avg():
    cfg={'csv_path':'backend/mock_data/rsf_mock.csv'}
    res = PressFreedomRSFAdapter(cfg).fetch()
    assert abs(res['value'] - 20.0) < 1e-9
