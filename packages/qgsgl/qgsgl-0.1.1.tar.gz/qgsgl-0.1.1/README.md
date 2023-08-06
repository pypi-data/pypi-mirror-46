# Conversion tool for QGIS map project into webmapgl style

## Usage

### Sources

#### GeoJSON

```py
from qgsgl import GeoJSONSource

url = 'https://example.com/data/stations.geojson'
source = GeoJSONSource('stations', url)
source.add_layer(station_layer)
source.write('/www/data/stations.geojson')
style.add_source(source)
```

#### Vector

```py
from qgsgl import VectorSource

url = 'https://example.com/tiles/project.json'
source = VectorSource('project', url)
source.add_layer(station_layer, min_zoom=12, max_zoom=14)
source.add_layer(street_layer, min_zoom=10, max_zoom=14)
source.write('/www/tiles/project.mbtiles')
style.add_source(source)
```

## Running Tests
```
python -m unittest discover
```
