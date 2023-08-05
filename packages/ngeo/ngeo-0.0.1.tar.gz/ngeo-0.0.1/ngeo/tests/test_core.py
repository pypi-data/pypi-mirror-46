
from ngeo import Polygon
from ngeo import MultiPolygon
from ngeo import Line
from ngeo import MultiLine
from ngeo import Point
from ngeo import MultiPoint
from ngeo.data import MockObjs

import numpy as np
import dask.array as da

N = 1
MOCK_POINTS = MockObjs.generate_fiona_points(N)
MOCK_MULTIPOINTS = MockObjs.generate_fiona_multi_point(N)
MOCK_LINES = MockObjs.generate_fiona_line(N)
MOCK_MULTILINESS = MockObjs.generate_fiona_multi_line(N)
MOCK_POLYGONS = MockObjs.generate_fiona_polygon(N)
MOCK_MULTIPOLYGONS = MockObjs.generate_fiona_multi_polygon(N)


def standard_geometry_test(geom_cls, mock_data):

    geom = geom_cls.from_iterator(mock_data)
    assert isinstance(geom, geom_cls)

    arr = geom.to_dask_array()
    assert isinstance(arr, da.Array)

    return geom


def test_point_geometry():
    standard_geometry_test(Point, MOCK_POINTS)


def test_multi_point_geometry_from_iterator():
    standard_geometry_test(MultiPoint, MOCK_MULTIPOINTS)


def test_line_geometry_from_iterator():
    standard_geometry_test(Line, MOCK_LINES)


def test_multi_line_geometry_from_iterator():
    standard_geometry_test(MultiLine, MOCK_MULTILINESS)


def test_polygon_geometry_from_iterator():
    standard_geometry_test(Polygon, MOCK_POLYGONS)


def test_multi_polygon_geometry_from_iterator():
    standard_geometry_test(MultiPolygon, MOCK_MULTIPOLYGONS)


def test_multi_polygon_map_func():

    def test_feature_func(data, coords):
        assert len(coords) > 0
        assert len(data) > 0
        assert len(np.unique(coords[0, :])) == 1

    def test_poly_func(data, coords):
        assert len(coords) > 0
        assert len(data) > 0
        assert len(np.unique(coords[1, :])) == 1

    def test_part_func(data, coords):
        assert len(coords) > 0
        assert len(data) > 0
        assert len(np.unique(coords[2, :])) == 1

    def test_row_func(data, coords):
        assert len(coords) > 0
        assert len(data) > 0
        assert len(np.unique(coords[3, :])) == 1

    def test_col_func(data, coords):
        assert len(coords) > 0
        assert len(data) > 0
        assert len(np.unique(coords[4, :])) == 1

    fc = MockObjs.create_mock_feature_collection(n=10)

    list(fc.geometry.map(test_feature_func, axis=0))
    list(fc.geometry.map(test_poly_func, axis=1))
    list(fc.geometry.map(test_part_func, axis=2))
    list(fc.geometry.map(test_row_func, axis=3))
    list(fc.geometry.map(test_col_func, axis=4))


def test_multi_polygon_check_geometry():
    fc = MockObjs.create_mock_feature_collection()
    result = fc.geometry.check_geometry()
    assert result is not N


def test_feature_class_to_geojson():
    fc = MockObjs.create_mock_feature_collection()
    result = fc.to_geojson()

    assert isinstance(result, dict)
    assert 'type' in result.keys()
    assert 'features' in result.keys()

    first_features = result['features'][0]
    assert isinstance(first_features, dict)
    assert 'type' in first_features.keys()
    assert 'geometry' in first_features.keys()
    assert 'properties' in first_features.keys()


def test_rasterize_multipolyon():
    from ngeo.raster import rasterize

    fc = MockObjs.create_mock_feature_collection()
    result = rasterize(fc, 100, 100)

    assert isinstance(result, np.ndarray)
    assert result.shape[0] == 100
    assert result.shape[1] == 100
    assert result.any()
