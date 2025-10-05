
import sys; sys.path.insert(0, 'backend')
from adapters.fsi_fundforpeace import FSIGlobalAdapter
def test_fsi_avg():
    cfg={'csv_path':'backend/mock_data/fsi_mock.csv'}
    res = FSIGlobalAdapter(cfg).fetch()
    assert abs(res['value'] - 20.0) < 1e-9
