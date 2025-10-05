
import sys; sys.path.insert(0, 'backend')
from adapters.news_entropy_gdelt import NewsEntropyAdapter
def test_entropy_json():
    cfg={'json_path': 'backend/mock_data/news_topics.json'}
    res = NewsEntropyAdapter(cfg).fetch()
    assert 0.80 < res['value'] < 0.82
