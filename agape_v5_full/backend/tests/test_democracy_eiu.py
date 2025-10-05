
import sys; sys.path.insert(0, 'backend')
from adapters.democracy_eiu import DemocracyEIUAdapter
def test_democracy_avg():
    cfg={'csv_path':'backend/mock_data/democracy_mock.csv'}
    res = DemocracyEIUAdapter(cfg).fetch()
    assert abs(res['value'] - 20.0) < 1e-9
