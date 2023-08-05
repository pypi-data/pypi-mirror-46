import numpy as np
import json

from numba import njit

import pandas as pd

from sparse import load_npz
from sparse import save_npz

from ngeo.core import Point
from ngeo.core import MultiPoint
from ngeo.core import Line
from ngeo.core import MultiLine
from ngeo.core import Polygon
from ngeo.core import MultiPolygon


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


def from_shapefile(shapefile_path):
    '''
    TODO: Add docstring
    '''

    try:
        import fiona
    except ImportError:
        raise ImportError('Fiona library is required to read shapefiles')

    with fiona.open(shapefile_path) as source:
        geometry_type = source.meta['schema']['geometry']
        geom_class = GEOMETRY_CLASSES[geometry_type]
        geom = geom_class.from_iterator(source)
        props = [feat['properties'] for feat in source]
        return FeatureCollection(geometry=geom,
                                 properties=pd.DataFrame(props),
                                 crs=source.crs)


def to_shapefile(feature_collection):

    try:
        import fiona
        from fiona.crs import from_epsg
    except ImportError:
        raise ImportError('Fiona library is required to read shapefiles')


def import_shapefile(shapefile_path, output_name):
    '''
    TODO: Add docstring
    '''

    fc = from_shapefile(shapefile_path)

    print('saving geometry...')
    fc.save(output_name)


def add_feature_collection_to_bokeh_figure(feature_collection, bokeh_figure,
                                           head=None, glyph_args=None):

    xs, ys = feature_collection.geometry.nested(head=head)
    geom_type = feature_collection.geometry.geometry_type.lower()

    NEON_COLORS = dict(blue="#01FFF4",
                       green="#7CFF01",
                       yellow="#FFF205",
                       red="#FE0000",
                       pink="#FF1178")

    if not glyph_args:

        if geom_type == 'multipolygon':
            glyph_args = dict(fill_color=NEON_COLORS['blue'],
                              fill_alpha=.9,
                              line_color='white',
                              line_alpha=.7)

        elif geom_type == 'polygon':
            glyph_args = dict(fill_color=NEON_COLORS['blue'],
                              fill_alpha=.9,
                              line_color='white',
                              line_alpha=.7)

        elif geom_type == 'multiline':
            glyph_args = dict(line_color=NEON_COLORS['yellow'],
                              line_alpha=.9)

        elif geom_type == 'line':
            glyph_args = dict(line_color=NEON_COLORS['yellow'],
                              line_alpha=.9)

        # i don't think there is a multi_point glyph...
        # but that could be a good PR...
        # could also just duplicate attributes to convert to point
        elif geom_type == 'multipoint':
            glyph_args = dict(color=NEON_COLORS['green'],
                              fill_alpha=.9,
                              line_color='white',
                              line_alpha=.7)

        elif geom_type == 'point':
            glyph_args = dict(fill_color=NEON_COLORS['green'],
                              fill_alpha=.9,
                              line_color='white',
                              line_alpha=.7)

    if geom_type == 'multipolygon':
        bokeh_figure.multi_polygons(xs=xs, ys=ys, **glyph_args)

    elif geom_type == 'polygon':
        # normalize to multi_polygon
        bokeh_figure.multi_polygons(xs=[xs], ys=[ys], **glyph_args)

    elif geom_type == 'multiline':
        bokeh_figure.multi_line(xs=xs, ys=ys, **glyph_args)

    elif geom_type == 'line':
        bokeh_figure.multi_line(xs=xs, ys=ys, **glyph_args)

    # i don't think there is a multi_point glyph...
    # but that could be a good PR...
    # could also just duplicate attributes to convert to point
    elif geom_type == 'multipoint':
        bokeh_figure.circle(x=xs, y=ys, **glyph_args)

    elif geom_type == 'point':
        bokeh_figure.circle(x=xs, y=ys, **glyph_args)

    return bokeh_figure


class FeatureCollection(object):
    '''
    TODO: Add docstring
    '''

    def __init__(self, geometry, properties, crs):

        self.geometry = geometry
        self.properties = properties
        self.crs = crs

    def __getitem__(self, key):

        new_props = self.properties[key]

        if isinstance(key, str):
            return new_props
        else:
            new_coo = self.geometry[new_props.index.tolist(), ...]
            new_geom_class = GEOMETRY_CLASSES[self.geometry.geometry_type]
            new_geom = new_geom_class(coords=new_coo.coords,
                                      data=new_coo.data,
                                      shape=new_coo.shape,
                                      fill_value=new_coo.fill_value)
            new_geom.coords = new_geom.coords.astype(np.uint32)
            return FeatureCollection(new_geom, new_props, self.crs)

    def __repr__(self):

        msg = '{} FeatureCollection ({}MB)\n'
        msg += self.geometry.__repr__() + '\n'
        msg += self.properties.__repr__()

        return msg.format(self.geometry.geometry_type,
                          self.geometry.nbytes // (1024.0 * 1024.0))

    def to_geojson(self):
        props = self.properties.to_dict(orient='records')
        features = [{'properties': p, 'type': 'Feature'} for p in props]

        for f in features:
            for prop in f['properties'].keys():
                if f['properties'][prop] is np.nan:
                    f['properties'][prop] = None

        geom_gen = self.geometry.to_geojson()
        for i, nested_coords in enumerate(geom_gen):
            geom = {'type': self.geometry.geometry_type}
            geom['coordinates'] = nested_coords
            features[i]['geometry'] = geom

        return {'type': 'FeatureCollection', 'features': features}

    @classmethod
    def load(cls, name):
        '''
        TODO: Add docstring
        '''

        meta_output_name = '{}.metadata.json'.format(name)

        with open(meta_output_name, 'r') as metadata_file:
            metadata_obj = json.loads(metadata_file.read())

        geom_output_name = '{}.npz'.format(name)
        arr = load_npz(geom_output_name)

        geom_class = GEOMETRY_CLASSES[metadata_obj['geometry_type']]
        geom = geom_class(coords=arr.coords,
                          data=arr.data,
                          shape=arr.shape,
                          fill_value=arr.fill_value)

        data_output_name = '{}.parq'.format(name)
        props = pd.read_parquet(data_output_name)

        return FeatureCollection(geometry=geom,
                                 properties=props,
                                 crs=metadata_obj.get('crs'))

    def metadata(self):
        '''
        TODO: Add docstring
        '''
        meta = {}
        meta['crs'] = self.crs
        meta['geometry_type'] = self.geometry.geometry_type
        meta['nbytes_in_memory'] = int(self.geometry.nbytes + (self.properties
                                                               .memory_usage()
                                                               .sum()))
        return meta

    def save(self, name):
        '''
        TODO: Add docstring
        '''
        geom_output_name = '{}.npz'.format(name)
        save_npz(geom_output_name, self.geometry, True)

        data_output_name = '{}.parq'.format(name)
        if isinstance(self.properties, pd.DataFrame):
            self.properties.to_parquet(data_output_name)

        meta_output_name = '{}.metadata.json'.format(name)
        with open(meta_output_name, 'w') as metadata_file:
            metadata_file.write(json.dumps(self.metadata()))

    def plot(self, size="md", head=None,
             portrait=False, square=False, use_notebook=True,
             output_file_path='fig.html', glyph_args=None,
             grid_visible=False, axis_visible=False,
             fig_args=dict(background_fill_color='black')):

        try:

            from bokeh.plotting import figure
            from bokeh.io import output_notebook
            from bokeh.io import output_file
            from bokeh.io import show

            if use_notebook:
                output_notebook()

        except ImportError:
            raise ImportError('Bokeh library is required for plotting')

        SIZES = dict(sm=(100 * 2, 100 * 3),
                     md=(300 * 2, 300 * 3),
                     lg=(600 * 2, 600 * 3))

        if portrait:
            plot_width, plot_height = SIZES[size]
        else:
            plot_height, plot_width = SIZES[size]

        if square:
            plot_width = plot_height

        xmin, ymin, xmax, ymax, = self.geometry.full_extent

        fig = figure(plot_height=plot_height,
                     plot_width=plot_width,
                     output_backend="webgl",
                     x_range=(xmin, xmax), y_range=(ymin, ymax),
                     **fig_args)
        fig.xgrid.visible = grid_visible
        fig.ygrid.visible = grid_visible
        fig.axis.visible = axis_visible

        fig = add_feature_collection_to_bokeh_figure(self, fig, head=head,
                                                     glyph_args=glyph_args)

        if not use_notebook:
            output_file(output_file_path)

        show(fig)

        return fig


GEOMETRY_CLASSES = _geometry_class_mapping()

if __name__ == '__main__':

    import sys
    import_shapefile(*sys.argv[1:])
