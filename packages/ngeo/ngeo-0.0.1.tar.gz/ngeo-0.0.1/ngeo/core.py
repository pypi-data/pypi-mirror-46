from collections import defaultdict

from functools import reduce
from operator import add

import numpy as np

from numba import njit
from numba import jit

from sparse import COO


class GeometryABC(COO):
    '''
    TODO: Add docstring
    '''

    def nested(self, head=None):

        if head and head < 1:
            raise ValueError('Invalid head arg.')

        return self._flat_to_nested(self.data, self.coords, head)

    def to_dask_array(self, feature_count=10):
        try:
            import dask.array as da
        except ImportError:
            msg = ('dask library required to_dask_array\n'
                   '(conda install -c conda-forge dask)\n')
            raise ImportError(msg)

        shp = self.shape

        nfeats = min(feature_count, shp[0])

        chunk_shp = [nfeats]
        for p in shp[1:]:
            chunk_shp.append(p)

        return da.from_array(self, chunks=tuple(chunk_shp), asarray=False)

    def check_geometry(self):
        raise NotImplementedError()

    @property
    def geometry_type(self):
        return self.__class__.__name__

    def get_feature(self, i):
        return self[i, ...]

    def get_feature_edges(self, i, axis=0):
        breaks = self._breaks(axis=axis)

        if i == 0:
            return (0, breaks[i])
        else:
            return (breaks[i]+1, breaks[i+1])

    def map(self, func, axis=0, *args, **kwargs):
        '''
        Map a function across some axis of the geometry...
        I was having trouble using {np, da}.apply_along_axis so wrote this...

        Example
        -------
        f = lambda data, coords: return len(data) + len(coords)
        fc = MultiPolygon()
        fc.map(f, axis=0)

        >>> [10, 20, 30]
        '''

        breaks = self._breaks(axis=axis)

        if len(breaks) == 0:
            yield [func(self.data, self.coords, *args, **kwargs)]

        else:

            for i, b in enumerate([0] + breaks):

                if i == 0:
                    yield func(self.data[0: breaks[i]+1],
                               self.coords[:, 0:breaks[i]+1],
                               *args, **kwargs)

                elif i == len(breaks):
                    yield func(self.data[breaks[i-1]+1:],
                               self.coords[:, breaks[i-1]+1:],
                               *args, **kwargs)

                else:
                    yield func(self.data[breaks[i-1]+1:breaks[i]+1],
                               self.coords[:, breaks[i-1]+1:breaks[i]+1],
                               *args, **kwargs)

    def _breaks(self, axis=0):
        '''
        Finds the edges between features for a given axis

        Example
        -------
        edges = geom.feature_breaks

        >>> array([399, 425, 700])
        '''
        # TODO: numba-ize
        len_coords = self.coords.shape[-1]
        all_breaks = [np.where(self.coords[a][:-1] != self.coords[a][1:])[0].tolist()
                      for a in range(axis + 1)]  # NOQA
        flat_breaks = np.array(reduce(add, all_breaks))
        flat_breaks = np.append(flat_breaks, len_coords)
        unique_breaks = np.unique(flat_breaks).astype(int)
        return unique_breaks

    @property
    def feature_breaks(self):
        return self._breaks(axis=0)

    @property
    def part_breaks(self):
        raise NotImplementedError("Only implemented for MultiPolygon Polygon")

    @property
    def polygon_breaks(self):
        raise NotImplementedError("Only implemented for MultiPolygon")

    @property
    def line_breaks(self):
        raise NotImplementedError("Only implemented for MultiLine")

    @property
    def full_extent(self):
        xs = self.data[0::2]
        ys = self.data[1::2]
        return xs.min(), ys.min(), xs.max(), ys.max()

    @property
    def count(self):
        return int(self.coords[0, :].max() + 1)

    @classmethod
    def from_iterator(cls, geometry_generator, ignore_errors=True):
        raise NotImplementedError()

    @classmethod
    def from_sparse(cls, coo_sparse, geometry_type):
        raise NotImplementedError()

    @classmethod
    def from_shapefile(cls, shapefile_path):

        try:
            import fiona
        except ImportError:
            raise ImportError('Fiona library is required to read shapefiles')

        with fiona.open(shapefile_path) as geom_generator:
            return cls.from_iterator(geom_generator)


class Point(GeometryABC):

    @staticmethod
    @jit
    def _flat_to_nested(data, coords, head):

        # Shape (N features, 4)
        if head:
            nth_index = head - 1
        else:
            nth_index = coords[0, :].max()

        xs, ys = data[0::2], data[1::2]
        return xs[:nth_index], ys[:nth_index]

    @classmethod
    def from_iterator(cls, geometry_generator):
        '''
        TODO: Add docstring
        '''
        # hack to avoid resetting generator...remove later
        geometry_generator = list(geometry_generator)

        num_features = 0
        coordinate_ndim = 2

        for f, feat in enumerate(geometry_generator):
            num_features += 1

        data = np.empty((num_features * coordinate_ndim,), dtype=np.float64)
        coords = np.empty((2, num_features * coordinate_ndim), dtype=np.uint32)
        insert_idx = 0
        for f, feat in enumerate(geometry_generator):
            geom = feat['geometry']['coordinates']
            for d in range(coordinate_ndim):
                data[insert_idx] = geom[d]
                coords[0, insert_idx] = f
                coords[1, insert_idx] = d
                insert_idx += 1

        out_geom = Point(coords=coords,
                         data=data,
                         shape=(num_features,
                                coordinate_ndim),
                         fill_value=0)

        # sparse library auto-promotes to int64...convert back.
        out_geom.coords = out_geom.coords.astype(np.uint32)

        return out_geom


class MultiPoint(GeometryABC):
    '''
    TODO: Add docstring
    '''

    @staticmethod
    @jit
    def _flat_to_nested(data, coords, head):

        # Shape (N features, 4)
        if head:
            nfeatures = head
        else:
            nfeatures = coords[0, :].max() + 1

        xs = []
        ys = []

        feature_index = None
        for i in range(0, data.shape[0], 2):
            cfeat = coords[0, i]
            x = data[i]
            y = data[i + 1]
            if cfeat != feature_index:
                # return early for head arg.
                if cfeat > nfeatures - 1:
                    return xs, ys

                xs.append([])
                ys.append([])
                feature_index = cfeat

            xs[feature_index].append(x)
            ys[feature_index].append(y)

        return xs, ys

    @classmethod
    def from_iterator(cls, geometry_generator):
        '''
        TODO: Add docstring
        '''

        # hack to avoid resetting generator...remove later
        geometry_generator = list(geometry_generator)

        num_features = 0
        max_point_count = 0
        coordinate_ndim = 2
        num_vertices = 0

        for f, feat in enumerate(geometry_generator):
            num_features += 1

            # change points into multipoints
            if feat['geometry']['type'] == 'Point':
                geom = [feat['geometry']['coordinates']]
            else:
                geom = feat['geometry']['coordinates']

            point_count = len(geom)
            num_vertices += len(geom)

            if point_count > max_point_count:
                max_point_count = point_count

        data = np.empty((num_vertices * 2,), dtype=np.float64)
        coords = np.empty((3, num_vertices * 2), dtype=np.uint32)
        insert_idx = 0
        for f, feat in enumerate(geometry_generator):
            if feat['geometry']['type'] == 'Point':
                geom = [feat['geometry']['coordinates']]
            else:
                geom = feat['geometry']['coordinates']

            for ipoint, point in enumerate(geom):
                for d in range(coordinate_ndim):
                    data[insert_idx] = point[d]
                    coords[0, insert_idx] = f
                    coords[1, insert_idx] = ipoint
                    coords[2, insert_idx] = d
                    insert_idx += 1

        out_geom = MultiPoint(coords=coords,
                              data=data,
                              shape=(num_features,
                                     max_point_count,
                                     coordinate_ndim),
                              fill_value=0)

        # sparse library auto-promotes to int64...convert back.
        out_geom.coords = out_geom.coords.astype(np.uint32)

        return out_geom


class Line(GeometryABC):
    '''
    TODO: Add docstring
    '''

    @staticmethod
    @jit
    def _flat_to_nested(data, coords, head):

        # Shape (N features, 4)
        if head:
            nfeatures = head
        else:
            nfeatures = coords[0, :].max() + 1

        xs = []
        ys = []

        feature_index = None
        for i in range(0, data.shape[0], 2):
            cfeat = coords[0, i]
            x = data[i]
            y = data[i + 1]
            if cfeat != feature_index:
                # return early for head arg.
                if cfeat > nfeatures - 1:
                    return xs, ys

                xs.append([])
                ys.append([])
                feature_index = cfeat

            xs[feature_index].append(x)
            ys[feature_index].append(y)

        return xs, ys

    @classmethod
    def from_iterator(cls, geometry_generator):
        '''
        TODO: Add docstring
        '''

        # hack to avoid resetting generator...remove later
        geometry_generator = list(geometry_generator)

        num_features = 0
        max_point_count = 0
        coordinate_ndim = 2
        num_vertices = 0

        for f, feat in enumerate(geometry_generator):
            num_features += 1
            geom = feat['geometry']['coordinates']
            point_count = len(geom)
            num_vertices += len(geom)

            if point_count > max_point_count:
                max_point_count = point_count

        data = np.empty((num_vertices * 2,), dtype=np.float64)
        coords = np.empty((3, num_vertices * 2), dtype=np.uint32)
        insert_idx = 0
        for f, feat in enumerate(geometry_generator):
            geom = feat['geometry']['coordinates']
            for iline, line in enumerate(geom):
                for d in range(coordinate_ndim):
                    data[insert_idx] = line[d]
                    coords[0, insert_idx] = f
                    coords[1, insert_idx] = iline
                    coords[2, insert_idx] = d
                    insert_idx += 1

        out_geom = Line(coords=coords,
                        data=data,
                        shape=(num_features,
                               max_point_count,
                               coordinate_ndim),
                        fill_value=0)

        # sparse library auto-promotes to int64...convert back.
        out_geom.coords = out_geom.coords.astype(np.uint32)

        return out_geom


class MultiLine(GeometryABC):

    @staticmethod
    @jit
    def _flat_to_nested(data, coords, head):

        # Shape (N features, 4)
        if head:
            nfeatures = head
        else:
            nfeatures = coords[0, :].max() + 1

        xs = []
        ys = []

        feature_index = None
        line_index = None

        for i in range(0, data.shape[0], 2):

            cfeat = coords[0, i]
            cline = coords[1, i]

            x = data[i]
            y = data[i + 1]

            if cfeat != feature_index:

                # return early for head arg.

                if cfeat > nfeatures - 1:
                    return xs, ys

                xs.append([])
                ys.append([])
                line_index = None
                feature_index = cfeat

            if cline != line_index:
                line_index = None
                xs[feature_index].append([])
                ys[feature_index].append([])
                line_index = cline

            xs[feature_index][line_index].append(x)
            ys[feature_index][line_index].append(y)

        return xs, ys

    @classmethod
    def from_iterator(cls, geometry_generator):
        '''
        TODO: Add docstring
        '''

        # hack to avoid resetting generator...remove later
        geometry_generator = list(geometry_generator)

        num_features = 0  # length of the series (5D)
        max_line_count = 0  # depth of cube (3D)
        max_line_coordinate_length = 0  # height of cube (2D)
        coordinate_ndim = 2   # 1D
        num_vertices = 0
        num_lines = 0

        for f, feat in enumerate(geometry_generator):
            num_features += 1

            # change lines into multilines
            line_types = ['line', 'linestring']
            if feat['geometry']['type'].lower() in line_types:
                geom = [feat['geometry']['coordinates']]
            else:
                geom = feat['geometry']['coordinates']

            line_count = len(geom)
            if line_count > max_line_count:
                max_line_count = line_count

            for p, line in enumerate(geom):
                num_lines += 1
                line_coordinate_length = len(line)
                if line_coordinate_length > max_line_coordinate_length:
                    max_line_coordinate_length = line_coordinate_length
                num_vertices += len(line)

        data = np.empty((num_vertices * 2,), dtype=np.float64)
        coords = np.empty((4, num_vertices * 2), dtype=np.uint32)
        insert_idx = 0
        for f, feat in enumerate(geometry_generator):
            # change lines into multilines
            line_types = ['line', 'linestring']
            if feat['geometry']['type'].lower() in line_types:
                geom = [feat['geometry']['coordinates']]
            else:
                geom = feat['geometry']['coordinates']

            for p, line in enumerate(geom):
                for i, coord in enumerate(line):
                    for d in range(coordinate_ndim):
                        data[insert_idx] = coord[d]
                        coords[0, insert_idx] = f
                        coords[1, insert_idx] = p
                        coords[2, insert_idx] = i
                        coords[3, insert_idx] = d
                        insert_idx += 1

        out_geom = MultiLine(coords=coords,
                             data=data,
                             shape=(num_features,
                                    max_line_count,
                                    max_line_coordinate_length,
                                    coordinate_ndim),
                             fill_value=0)

        # sparse library auto-promotes to int64...convert back.
        out_geom.coords = out_geom.coords.astype(np.uint32)

        return out_geom


class Polygon(GeometryABC):
    '''
    TODO: Add docstring
    '''

    @staticmethod
    @njit
    def _check_ring_is_closed(part_data, part_coords):
        return part_data[0] == part_data[-2] and part_data[1] == part_data[-1]

    def check_geometry(self):

        report = defaultdict(list)

        # check if all parts are closed
        for i, c in enumerate(self.map(self._check_ring_is_closed, axis=1)):
            if not c:
                report['unclosed_parts'].append(i)

        return report

    @staticmethod
    @jit
    def _flat_to_nested(data, coords, head):

        # Shape (N features, 4)
        if head:
            nfeatures = head
        else:
            nfeatures = coords[0, :].max() + 1

        xs = []
        ys = []

        feature_index = None
        part_index = None

        for i in range(0, data.shape[0], 2):

            cfeat = coords[0, i]
            cpart = coords[1, i]

            x = data[i]
            y = data[i + 1]

            if cfeat != feature_index:

                # return early for head arg.

                if cfeat > nfeatures - 1:
                    return xs, ys

                xs.append([])
                ys.append([])
                part_index = None
                feature_index = cfeat

            if cpart != part_index:
                part_index = None
                xs[feature_index].append([])
                ys[feature_index].append([])
                part_index = cpart

            xs[feature_index][part_index].append(x)
            ys[feature_index][part_index].append(y)

        return xs, ys

    @classmethod
    def from_iterator(cls, geometry_generator):
        '''
        TODO: Add docstring
        '''
        # hack to avoid resetting generator...remove later
        geometry_generator = list(geometry_generator)

        num_features = 0  # length of the series (5D)
        max_part_count = 0  # depth of cube (3D)
        max_part_coordinate_length = 0  # height of cube (2D)
        coordinate_ndim = 2   # 1D
        num_vertices = 0
        num_parts = 0

        for f, feat in enumerate(geometry_generator):
            num_features += 1

            geom = feat['geometry']['coordinates']

            part_count = len(geom)
            if part_count > max_part_count:
                max_part_count = part_count

            for p, part in enumerate(geom):
                num_parts += 1
                part_coordinate_length = len(part)
                if part_coordinate_length > max_part_coordinate_length:
                    max_part_coordinate_length = part_coordinate_length
                num_vertices += len(part)

        data = np.empty((num_vertices * 2,), dtype=np.float64)
        coords = np.empty((4, num_vertices * 2), dtype=np.uint32)
        insert_idx = 0
        for f, feat in enumerate(geometry_generator):
            geom = feat['geometry']['coordinates']

            for p, part in enumerate(geom):
                for i, coord in enumerate(part):
                    for d in range(coordinate_ndim):
                        data[insert_idx] = coord[d]
                        coords[0, insert_idx] = f
                        coords[1, insert_idx] = p
                        coords[2, insert_idx] = i
                        coords[3, insert_idx] = d
                        insert_idx += 1

        out_geom = Polygon(coords=coords,
                           data=data,
                           shape=(num_features,
                                  max_part_count,
                                  max_part_coordinate_length,
                                  coordinate_ndim),
                           fill_value=0)

        # sparse library auto-promotes to int64...convert back.
        out_geom.coords = out_geom.coords.astype(np.uint32)

        return out_geom


class MultiPolygon(GeometryABC):
    '''
    TODO: Add docstring
    '''

    FEATURE_DIM = 0
    POLYGON_DIM = 1
    PART_DIM = 2
    ROW_DIM = 3
    COL_DIM = 4

    @staticmethod
    @njit
    def _get_nbytes(part_data, part_coords):
        return part_data.nbytes + part_coords.nbytes

    @staticmethod
    @njit
    def _check_ring_is_closed(part_data, part_coords):
        return part_data[0] == part_data[-2] and part_data[1] == part_data[-1]

    def check_geometry(self):

        report = defaultdict(list)

        # check if all parts are closed
        for i, c in enumerate(self.map(self._check_ring_is_closed, axis=2)):
            if not c:
                report['unclosed_parts'].append(i)

        return report

    @property
    def parts(self, feature_index):
        return self.data[:, :, :]

    @staticmethod
    @jit
    def _flat_to_nested(data, coords, head):

        # shape (n features, 4)
        if head:
            nfeatures = head
        else:
            nfeatures = coords[0, :].max() + 1

        xs = []
        ys = []

        feature_index = None
        poly_index = None
        part_index = None

        for i in range(0, data.shape[0], 2):

            cfeat = coords[0, i]
            cpoly = coords[1, i]
            cpart = coords[2, i]

            x = data[i]
            y = data[i + 1]

            if cfeat != feature_index:

                if cfeat > nfeatures - 1:
                    return xs, ys

                xs.append([])
                ys.append([])
                poly_index = None
                part_index = None
                feature_index = cfeat

            if cpoly != poly_index:
                part_index = None
                xs[feature_index].append([])
                ys[feature_index].append([])
                poly_index = cpoly

            if cpart != part_index:
                xs[feature_index][poly_index].append([])
                ys[feature_index][poly_index].append([])
                part_index = cpart

            xs[feature_index][poly_index][part_index].append(x)
            ys[feature_index][poly_index][part_index].append(y)

        return xs, ys

    def to_geojson(self):
        '''
        TODO: refactor to use geometry.map(lambda...)
        '''

        feature_index = None
        poly_index = None
        part_index = None
        coords = None

        for i in range(0, self.data.shape[0], 2):

            cfeat = self.coords[0, i]
            cpoly = self.coords[1, i]
            cpart = self.coords[2, i]

            x = self.data[i]
            y = self.data[i + 1]

            if cfeat != feature_index:

                if coords:
                    yield coords

                coords = []
                poly_index = None
                part_index = None
                feature_index = cfeat

            if cpoly != poly_index:
                part_index = None
                coords.append([])
                poly_index = cpoly

            if cpart != part_index:
                coords[poly_index].append([])
                part_index = cpart

            coords[poly_index][part_index].append((x, y))

        yield coords

    @classmethod
    def from_iterator(cls, geometry_generator):
        '''
        TODO: Add docstring
        '''

        # hack to avoid resetting generator...remove later
        geometry_generator = list(geometry_generator)

        num_features = 0  # length of the series (5D)
        max_poly_count = 0  # depth of cube (4D)
        max_part_count = 0  # depth of cube (3D)
        max_part_coordinate_length = 0  # height of cube (2D)
        coordinate_ndim = 2   # 1D
        num_vertices = 0
        num_parts = 0

        for f, feat in enumerate(geometry_generator):
            num_features += 1

            # change polygons into multipolygon
            if feat['geometry']['type'] == 'Polygon':
                geom = [feat['geometry']['coordinates']]
            else:
                geom = feat['geometry']['coordinates']

            poly_count = len(geom)
            if poly_count > max_poly_count:
                max_poly_count = poly_count

            for ipoly, poly in enumerate(geom):
                part_count = len(poly)
                if part_count > max_part_count:
                    max_part_count = part_count
                for p, part in enumerate(poly):
                    num_parts += 1
                    part_coordinate_length = len(part)
                    if part_coordinate_length > max_part_coordinate_length:
                        max_part_coordinate_length = part_coordinate_length
                    num_vertices += len(part)

        data = np.empty((num_vertices * 2,), dtype=np.float64)
        coords = np.empty((5, num_vertices * 2), dtype=np.uint32)
        insert_idx = 0
        for f, feat in enumerate(geometry_generator):
            if feat['geometry']['type'] == 'Polygon':
                geom = [feat['geometry']['coordinates']]
            else:
                geom = feat['geometry']['coordinates']

            for ipoly, poly in enumerate(geom):
                for p, part in enumerate(poly):
                    for i, coord in enumerate(part):
                        for d in range(coordinate_ndim):

                            data[insert_idx] = coord[d]
                            coords[0, insert_idx] = f
                            coords[1, insert_idx] = ipoly
                            coords[2, insert_idx] = p
                            coords[3, insert_idx] = i
                            coords[4, insert_idx] = d
                            insert_idx += 1

        out_geom = MultiPolygon(coords=coords,
                                data=data,
                                shape=(num_features,
                                       max_poly_count,
                                       max_part_count,
                                       max_part_coordinate_length,
                                       coordinate_ndim),
                                fill_value=0)

        # sparse library auto-promotes to int64...convert back.
        out_geom.coords = out_geom.coords.astype(np.uint32)

        return out_geom
