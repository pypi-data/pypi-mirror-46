NGEO
---------
:round_pushpin: Fast, Accurate Python library for Vector & Raster Operations

:zap: Easily extensible with [Numba](http://numba.pydata.org/)

:fast_forward: Easily scalable with [Dask](http://dask.pydata.org)

:earth_africa: Geared towards GIS Professionals

:clipboard: Notebook-friendly

:confetti_ball: No GDAL / GEOS Dependency

Build
-----
[![CircleCI](https://circleci.com/gh/parietal-io/geom-array.svg?style=svg&circle-token=f3ef8270774838472b3d0d9000f467faed3a99c3)](https://circleci.com/gh/parietal-io/geom-array)


Notes
-----

- PRE-ALPHA: `THIS IS JUST A PROTOTYPE AND SHOULDN'T BE USED FOR ANYTHING REAL!`
- Vector geometries are built using [sparse](http://sparse.pydata.org) arrays.
- Feature properties are backed by [Pandas](http://pandas.org) dataframes.
- The `FeatureCollection` object wraps geometry and properties and provides Pandas-based selection / filtering
- Feature Collections can be saved as a set of files:
  - Geometry: `feature_collection.npz`
  - Properties: `feature_collection.parq`
  - Metadata: `feature_collection.metadata.json`
- Bokeh is an optional dependency for plotting
- Pyproj is an optional dependency for coordinate projection
