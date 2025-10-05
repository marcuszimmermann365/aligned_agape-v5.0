
import sys; sys.path.insert(0, 'backend')
from adapters.gpi_visionofhumanity import GPIGlobalAdapter
def test_gpi_avg():
    cfg={'csv_path':'backend/mock_data/gpi_mock.csv'}
    res = GPIGlobalAdapter(cfg).fetch()
    assert abs(res['value'] - 20.0) < 1e-9
