from setuptools import setup, find_packages

setup(
    name='girder-geospatial',
    author='Kitware, Inc.',
    description='Generate metadata for various geospatial datasets',
    version='0.1.0a5',
    packages=find_packages(),
    entry_points={
        'geometa.types': [],
        'girder.plugin': [
            'geometa = geometa:GeometaPlugin'
        ]
    },
    install_requires=[
        'pyproj',
        'shapely',
        # Will fix it once marshmallow publishes new version
        'marshmallow==3.0.0b10',
        'geojson',
        'rasterio',
        'gdal==2.2.3'
    ],
)
