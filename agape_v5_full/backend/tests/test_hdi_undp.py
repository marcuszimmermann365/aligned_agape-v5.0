
import sys; sys.path.insert(0, 'backend')
from adapters.hdi_undp import HDIAdapter
import pandas as pd
def test_hdi_mean():
    df = pd.DataFrame({'Country':['A','B'],'Year':[2020,2020],'HDI':[0.7,0.9]})
    p = 'backend/mock_data/tmp_hdi.csv'; df.to_csv(p, index=False)
    res = HDIAdapter({'csv_path': p}).fetch()
    assert abs(res['value'] - 0.8) < 1e-9
