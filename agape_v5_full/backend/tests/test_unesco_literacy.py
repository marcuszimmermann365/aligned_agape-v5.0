
import sys; sys.path.insert(0, 'backend')
from adapters.unesco_literacy import UNESCOUiSLiteracyAdapter
def test_unesco_literacy_avg():
    cfg={'csv_path':'backend/mock_data/unesco_literacy.csv'}
    res = UNESCOUiSLiteracyAdapter(cfg).fetch()
    assert abs(res['value'] - 85.0) < 1e-9
    assert res['raw']['year'] == 2023
