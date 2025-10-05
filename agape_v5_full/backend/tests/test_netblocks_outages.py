
import sys; sys.path_insert = ['backend'] + sys.path
from adapters.netblocks_outages import NetBlocksAdapter
def test_netblocks_days():
    cfg={'csv_path':'backend/mock_data/netblocks_mock.csv'}
    res = NetBlocksAdapter(cfg).fetch()
    assert res['value'] >= 1.0
