
import sys; sys.path.insert(0, 'backend')
from adapters.worldbank_access import WorldBankAccessAdapter
import pandas as pd
def test_access_avg():
    df = pd.DataFrame({'Country':['A','B'],'Year':[2024,2024],'Electricity':[95,85],'Internet':[75,65]})
    p = 'backend/mock_data/tmp_access.csv'; df.to_csv(p, index=False)
    res = WorldBankAccessAdapter({'csv_path': p}).fetch()
    assert abs(res['value'] - 80.0) < 1e-9
