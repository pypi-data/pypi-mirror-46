from ngeo import Point
from ngeo import MultiPoint
from ngeo import Line
from ngeo import MultiLine
from ngeo import MultiPolygon
from ngeo import FeatureCollection

from numba import njit

import numpy as np
import pandas as pd


def _geometry_class_mapping():
    __GEOMETRY_CLASSES__ = {}
    __GEOMETRY_CLASSES__['MultiPolygon'] = MultiPolygon
    __GEOMETRY_CLASSES__['Polygon'] = MultiPolygon
    __GEOMETRY_CLASSES__['MultiPoint'] = MultiPoint
    __GEOMETRY_CLASSES__['Point'] = Point
    __GEOMETRY_CLASSES__['MultiLine'] = MultiLine
    __GEOMETRY_CLASSES__['LineString'] = Line
    __GEOMETRY_CLASSES__['Line'] = Line
    return __GEOMETRY_CLASSES__


def project(fc, epsg='EPSG:3857', inplace=True):
    """
    TODO: Add docstring
    """

    try:
        from pyproj import Proj, transform

    except ImportError:
        raise ImportError('project requires pyproj (conda install pyproj)')

    if isinstance(epsg, int):
        epsg = 'epsg:{}'.format(epsg)

    if fc.crs['init'].lower() == epsg.lower():
        raise ValueError('FeatureCollection already in crs {}'.format(epsg))

    in_proj = Proj(init=fc.crs['init'])
    out_proj = Proj(init=epsg)

    xs, ys = transform(in_proj, out_proj,
                       fc.geometry.data[0::2],
                       fc.geometry.data[1::2])

    if inplace:
        fc.geometry.data[0::2], fc.geometry.data[1::2] = xs, ys
        fc.crs['init'] = epsg
    else:
        new_coo = fc.geometry.copy()
        new_coo.data[0::2], new_coo.data[1::2] = xs, ys
        new_geom_class = GEOMETRY_CLASSES[fc.geometry.geometry_type]
        new_geom = new_geom_class(coords=new_coo.coords,
                                  data=new_coo.data,
                                  shape=new_coo.shape,
                                  fill_value=new_coo.fill_value)
        new_geom.coords = new_geom.coords.astype(np.uint32)
        return FeatureCollection(new_geom, fc.properties, fc.crs)


@njit
def _calculate_extents(data, coords):

    # Shape (N features, 4)
    nfeatures = coords[0, :].max() + 1
    out = np.zeros((nfeatures, 4), dtype=data.dtype)

    cursor_index = 0
    feature_index = 0

    feature_xmin = np.inf
    feature_ymin = np.inf
    feature_xmax = -np.inf
    feature_ymax = -np.inf

    for i in range(0, data.shape[0], 2):
        f = coords[0, i]

        if f != feature_index:

            out[feature_index, 0] = feature_xmin
            out[feature_index, 1] = feature_ymin
            out[feature_index, 2] = feature_xmax
            out[feature_index, 3] = feature_ymax

            feature_index = f
            feature_xmin = np.inf
            feature_ymin = np.inf
            feature_xmax = -np.inf
            feature_ymax = -np.inf

        x = data[i]
        y = data[i+1]

        if x < feature_xmin:
            feature_xmin = x
        elif x > feature_xmax:
            feature_xmax = x

        if y < feature_ymin:
            feature_ymin = y
        elif y > feature_ymax:
            feature_ymax = y

        cursor_index += 1

    out[feature_index, 0] = feature_xmin
    out[feature_index, 1] = feature_ymin
    out[feature_index, 2] = feature_xmax
    out[feature_index, 3] = feature_ymax

    return out


def calculate_extents(fc, append_to_props=False):
    '''
    TODO: Add docstring
    '''
    bboxes = _calculate_extents(fc.geometry.data, fc.geometry.coords)

    if append_to_props:
        fc.properties['XMIN'] = pd.Series(bboxes[:, 0])
        fc.properties['YMIN'] = pd.Series(bboxes[:, 1])
        fc.properties['XMAX'] = pd.Series(bboxes[:, 2])
        fc.properties['YMAX'] = pd.Series(bboxes[:, 3])
    else:
        return bboxes


@njit
def _calculate_area(data, coords):
    '''
    Calculate area of a simple polygon part
    '''

    if coords.shape[0] == 4:
        fidx = coords[0, 0]
        polyidx = coords[0, 0]
        partidx = coords[1, 0]
    elif coords.shape[0] == 5:
        fidx = coords[0, 0]
        polyidx = coords[1, 0]
        partidx = coords[2, 0]
    else:
        return None

    xs, ys = data[0::2], data[1::2]
    area = 0.0
    n = len(xs)
    j = n - 1
    for i in range(0, n):
        area += (xs[j] + xs[i]) * (ys[j] - ys[i])
        j = i

    # I added abs here to always return positive so I can handle
    # hole explicitly by checking the polygon part
    return (fidx, polyidx, partidx, abs(area / 2.0))


def calculate_area(fc, append_to_props=False):
    '''
    TODO: Add docstring
    '''
    if fc.geometry.geometry_type == 'Polygon':
        areas_gen = fc.geometry.map(_calculate_area, axis=1)
    elif fc.geometry.geometry_type == 'MultiPolygon':
        areas_gen = fc.geometry.map(_calculate_area, axis=2)
    else:
        msg = ('Input feature class must be'
               ' of geometry_type Polygon or'
               ' MultiPolygon')
        raise ValueError(msg)

    areas = np.empty(shape=(fc.geometry.count,))

    for feature_id, polygon_id, part_id, area in areas_gen:
        print(feature_id, polygon_id, part_id, area)
        if part_id > 0:
            areas[feature_id] -= area
        else:
            areas[feature_id] += area

    if append_to_props:
        fc.properties['AREA'] = areas
    else:
        return areas

GEOMETRY_CLASSES = _geometry_class_mapping()
