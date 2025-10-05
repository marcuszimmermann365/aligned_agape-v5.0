
import sys; sys.path.insert(0, 'backend')
from adapters.ucdp_battledeaths import UCDPDeathsAdapter
def test_ucdp_sum():
    cfg={'csv_path':'backend/mock_data/ucdp_mock.csv'}
    res = UCDPDeathsAdapter(cfg).fetch()
    assert abs(res['value'] - 3500.0) < 1e-9
