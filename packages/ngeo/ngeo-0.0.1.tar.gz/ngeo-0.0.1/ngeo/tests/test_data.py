from ngeo import FeatureCollection
from ngeo.data import MockObjs


def test_create_mock_feature_collection():
    fc = MockObjs.create_mock_feature_collection()
    import pdb;pdb.set_trace()
    assert isinstance(fc, FeatureCollection)

