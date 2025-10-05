
import sys; sys.path.insert(0, 'backend')
from adapters.gfsi_eiu import GFSIAdapter
def test_gfsi_avg():
    cfg={'csv_path':'backend/mock_data/gfsi_mock.csv'}
    res = GFSIAdapter(cfg).fetch()
    assert abs(res['value'] - 20.0) < 1e-9
