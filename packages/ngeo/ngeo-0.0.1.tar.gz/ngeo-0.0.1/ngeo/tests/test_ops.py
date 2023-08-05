
from ngeo.data import MockObjs

import numpy as np

from ngeo.ops import project
from ngeo.ops import calculate_area
from ngeo.ops import calculate_extents

N = 1
MOCK_POINTS = MockObjs.generate_fiona_points(N)
MOCK_MULTIPOINTS = MockObjs.generate_fiona_multi_point(N)
MOCK_LINES = MockObjs.generate_fiona_line(N)
MOCK_MULTILINESS = MockObjs.generate_fiona_multi_line(N)
MOCK_POLYGONS = MockObjs.generate_fiona_polygon(N)
MOCK_MULTIPOLYGONS = MockObjs.generate_fiona_multi_polygon(N)


def test_project():

    fc = MockObjs.create_mock_feature_collection()
    assert fc.crs['init'].lower() == 'EPSG:4326'.lower()

    fc2 = project(fc, epsg=3857, inplace=False)
    assert fc.crs['init'].lower() == 'EPSG:4326'.lower()
    assert fc2.crs['init'].lower() == 'EPSG:3857'.lower()

    project(fc, epsg=3857, inplace=True)
    assert fc.crs['init'].lower() == 'EPSG:3857'.lower()


def test_calculate_area():
    fc = MockObjs.create_mock_feature_collection()
    result = calculate_area(fc, append_to_props=False)
    assert isinstance(result, np.ndarray)
    assert len(result.shape) == 1
    assert result.shape[0] == fc.geometry.count

    calculate_area(fc, append_to_props=True)
    assert 'AREA' in fc.properties.columns


def test_calculate_extents():
    fc = MockObjs.create_mock_feature_collection()
    result = calculate_extents(fc, append_to_props=False)
    assert isinstance(result, np.ndarray)
    assert len(result.shape) == 2
    assert result.shape[0] == fc.geometry.count
    assert result.shape[1] == 4

    calculate_extents(fc, append_to_props=True)
    assert isinstance(result, np.ndarray)
    assert 'XMIN' in fc.properties.columns
    assert 'YMIN' in fc.properties.columns
    assert 'XMAX' in fc.properties.columns
    assert 'XMAX' in fc.properties.columns
