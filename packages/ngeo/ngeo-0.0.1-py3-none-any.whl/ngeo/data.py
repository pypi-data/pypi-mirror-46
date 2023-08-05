import math
import random
import pandas as pd
import numpy as np

from ngeo import FeatureCollection
from ngeo import MultiPolygon



# taken from https://stackoverflow.com/
# questions/8997099/algorithm-to-generate-random-2d-polygon
def generate_polygon(ctrX, ctrY, aveRadius, irregularity,
                     spikeyness, numVerts):
    '''Start with the centre of the polygon at ctrX, ctrY,
    then creates the polygon by sampling points on a circle
    around the centre.
    Randon noise is added by varying the angular spacing between
    sequential points,
    and by varying the radial distance of each point from the centre.

    Params:
    ctrX, ctrY - coordinates of the "centre" of the polygon

    aveRadius - in px, the average radius of this polygon,
        this roughly controls
        how large the polygon is, really only useful for order of magnitude.

    irregularity - [0,1] indicating how much variance there is in the angular
        spacing of vertices. [0,1] will map to [0, 2pi/numberOfVerts]

    spikeyness - [0,1] indicating how much variance there
        is in each vertex from
        the circle of radius aveRadius. [0,1] will map to [0, aveRadius]

    numVerts - self-explanatory

    Returns a list of vertices, in CCW order.
    '''
    irregularity = clip(irregularity, 0, 1) * 2 * math.pi / numVerts
    spikeyness = clip(spikeyness, 0, 1) * aveRadius

    # generate n angle steps
    angleSteps = []
    lower = (2*math.pi / numVerts) - irregularity
    upper = (2*math.pi / numVerts) + irregularity
    _sum = 0
    for i in range(numVerts):
        tmp = random.uniform(lower, upper)
        angleSteps.append(tmp)
        _sum = _sum + tmp

    # normalize the steps so that point 0 and point n+1 are the same
    k = _sum / (2*math.pi)
    for i in range(numVerts):
        angleSteps[i] = angleSteps[i] / k

    # now generate the points
    points = []
    angle = random.uniform(0, 2*math.pi)
    for i in range(numVerts):
        r_i = clip(random.gauss(aveRadius, spikeyness), 0, 2*aveRadius)
        x = ctrX + r_i*math.cos(angle)
        y = ctrY + r_i*math.sin(angle)
        points.append((int(x), int(y)))
        angle = angle + angleSteps[i]

    return points + [points[0]]


def clip(x, _min, _max):
    if(_min > _max):
        return x
    elif(x < _min):
        return _min
    elif(x > _max):
        return _max
    else:
        return x


class MockObjs(object):

    @staticmethod
    def generate_fiona_points(n=1):
        for i in range(n):
            t = "Point"
            coordinates = generate_polygon(0, 0, 10, .5, .5, 5)
            crs = dict(init="EPSG:4326")
            geom = dict(crs=crs, type=t, coordinates=coordinates[0])
            props = pd.DataFrame()
            yield dict(geometry=geom, properties=props, crs=crs)

    @staticmethod
    def generate_fiona_multi_point(n=1):
        for i in range(n):
            t = "MultiPoint"
            coordinates = generate_polygon(0, 0, 10, .5, .5, 5)
            crs = dict(init="EPSG:4326")
            geom = dict(crs=crs, type=t, coordinates=coordinates)
            props = pd.DataFrame()
            yield dict(geometry=geom, properties=props, crs=crs)

    @staticmethod
    def generate_fiona_line(n=1):
        for i in range(n):
            t = "Line"
            crs = dict(init="EPSG:4326")
            poly = generate_polygon(0, 0, 10, .5, .5, 10)
            line = poly[:-2]

            geom = {}
            geom['coordinates'] = line
            geom['type'] = t
            geom['crs'] = crs

            props = pd.DataFrame()
            yield dict(geometry=geom, properties=props, crs=crs)

    @staticmethod
    def generate_fiona_multi_line(n=1):
        for i in range(n):
            t = "MultiLine"
            crs = dict(init="EPSG:4326")
            poly1 = generate_polygon(0, 0, 10, .5, .5, 10)
            poly2 = generate_polygon(0, 0, 10, .5, .5, 10)

            geom = {}
            geom['coordinates'] = [poly1[:-2], poly2[:-2]]
            geom['type'] = t
            geom['crs'] = crs

            props = pd.DataFrame()
            yield dict(geometry=geom, properties=props, crs=crs)

    @staticmethod
    def generate_fiona_polygon(n=1):
        for i in range(n):
            t = "Polygon"
            coordinates = [generate_polygon(0, 0, 10, .15, .15, 50)]
            crs = dict(init="EPSG:4326")

            geom = {}
            geom['coordinates'] = coordinates
            geom['type'] = t
            geom['crs'] = crs

            props = pd.DataFrame()
            yield dict(geometry=geom, properties=props, crs=crs)

    @staticmethod
    def generate_fiona_multi_polygon(n=1):
        for i in range(n):
            coordinates = [[generate_polygon(0, 0, 10, .05, .05, 20),
                            generate_polygon(0, 0, 5, .05, .05, 10)],
                           [generate_polygon(30, 30, 10, .05, .05, 20),
                            generate_polygon(30, 30, 5, .05, .05, 10)]]

            crs = dict(init="EPSG:4326")

            t = "MultiPolygon"
            geom = {}
            geom['coordinates'] = coordinates
            geom['type'] = t
            geom['crs'] = crs

            props = pd.DataFrame()
            yield dict(geometry=geom, properties=props, crs=crs)

    @staticmethod
    def create_mock_feature_collection(n=1):
        geom_source = MockObjs.generate_fiona_multi_polygon(n)
        geom = MultiPolygon.from_iterator(geom_source)
        data = dict(a=np.arange(geom.shape[0]))
        props = pd.DataFrame(data)
        crs = dict(init='EPSG:4326')
        fc = FeatureCollection(geometry=geom, properties=props, crs=crs)
        return fc
