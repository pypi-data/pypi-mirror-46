# Welcome to Geoformat

## Introduction

Geoformat is GDAL / OGR  overlayer wiht MIT licence.
The library aim is to simplify loading and OGR 'DataSource' and 'Layer' manipulations.
Until now this library is in Alpha mode. This means that for the moment the structure of this library is not
full oriented object compatible.

## Installation


```sh
$ pip install geoformat
```

## Basic manipulations



### Geoformat structure

![Strucutre of Geoformat](https://framagit.org/Guilhain/Geoformat/raw/master/images/geoformat.png)

### Open a geocontainer

A container is an equivalent to folder or a database containing one or several geolayer.

```py
import geoformat

commune_path = 'data/FRANCE_IGN/COMMUNE_2016_MPO_L93.shp'
gare_path = 'data/FRANCE_IGN/GARES_PT_L93.shp'

layer_list = [commune_path, gare_path]

geocontainer = geoformat.ogr_layers_to_geocontainer(layer_list)

print(geocontainer['layers'].keys())

# >>>dict_keys(['COMMUNE_2016_MPO_L93', 'GARES_PT_L93'])
```

### Open a geolayer

A geolayer is an equivalent to a file or a table in database containing one or several features with attibutes and/or
geometry.

```py
import geoformat

departement_path = 'data/FRANCE_IGN/DEPARTEMENT_2016_L93.shp'

geolayer = geoformat.ogr_layer_to_geolayer(departement_path)

print(len(geolayer['features']))

# >>>96
```


### Print data geolayer

Sometime it can be uselful to print in terminal geolayer's attributes.

```py
import geoformat

region_path = 'data/FRANCE_IGN/REGION_2016_L93.shp'

geolayer = geoformat.ogr_layer_to_geolayer(region_path)

for line in geoformat.print_features_data_table(geolayer):
    print(line)
    
### >>>
+--------+----------+-------------------------------------+------------+------------+
| i_feat | CODE_REG | NOM_REG                             | POPULATION | SUPERFICIE |
+========+==========+=====================================+============+============+
| 0      | 76       | LANGUEDOC-ROUSSILLON-MIDI-PYRENEES  | 5683878    | 7243041    |
| 1      | 75       | AQUITAINE-LIMOUSIN-POITOU-CHARENTES | 5844177    | 8466821    |
| 2      | 84       | AUVERGNE-RHONE-ALPES                | 7757595    | 7014795    |
| 3      | 32       | NORD-PAS-DE-CALAIS-PICARDIE         | 5987883    | 3187435    |
| 4      | 44       | ALSACE-CHAMPAGNE-ARDENNE-LORRAINE   | 5552388    | 5732928    |
| 5      | 93       | PROVENCE-ALPES-COTE D'AZUR          | 4953675    | 3155736    |
| 6      | 27       | BOURGOGNE-FRANCHE-COMTE             | 2819783    | 4746283    |
| 7      | 52       | PAYS DE LA LOIRE                    | 3660852    | 2997777    |
| 8      | 28       | NORMANDIE                           | 3328364    | 2728511    |
| 9      | 11       | ILE-DE-FRANCE                       | 11959807   | 1205191    |
| 10     | 24       | CENTRE-VAL DE LOIRE                 | 2570548    | 3905914    |
| 11     | 53       | BRETAGNE                            | 3258707    | 2702269    |
| 12     | 94       | CORSE                               | 320208     | 875982     |
+--------+----------+-------------------------------------+------------+------------+

```

### Change geolayer coordinate reference system [CRS]

It can be usefull to change the projection for a layer.  In this example we will transform a geolayer in projection Lambert93 [EPSG:2154] to coordinates system WGS84 [EPSG:4326].

```py
import geoformat

region_path = 'data/FRANCE_IGN/REGION_2016_L93.shp'

geolayer = geoformat.ogr_layer_to_geolayer(region_path)

geolayer = geoformat.reproject_geolayer(geolayer, out_crs=4326)

print(geolayer['metadata']['geometry_ref']['crs'])

# >>>4326

```


### Write geolayer in a OGR compatible GIS file

You can obviously convert a geolayer in a compatible OGR file format.
In this case ye put a geolayer in 'ESRi SHAPEFILE' format and we create a new file in 'GEOJSON' (we add a reprojection because geojson should be in WGS84 coordinates system).

```py
import geoformat

gares_shp_path = 'data/FRANCE_IGN/GARES_L93.shp'
gares_geojson_path =  'data/FRANCE_IGN/GARES_L93.geojson'

geolayer = geoformat.ogr_layer_to_geolayer(gares_shp_path)

geolayer = geoformat.reproject_geolayer(geolayer, out_crs=4326)

geoformat.geolayer_to_ogr_layer(geolayer, gares_geojson_path, 'GEOJSON')

```

### Write a container in OGR compatible dataSource

Like geolayer you can write a geoformat container in a folder or a GRG compatible datasource.
Here we have a geocontainer with a lot of layers and we want to save all of this in an other folder (but it can be also a 'POSTGRESQL' database).

```py
import geoformat

# INPUT
commune_path = 'data/FRANCE_IGN/COMMUNE_2016_MPO_L93.shp'
gare_path = 'data/FRANCE_IGN/GARES_PT_L93.shp'

# OUTPUT
output_folder = 'data/'

layer_list = [commune_path, gare_path]

geocontainer = geoformat.ogr_layers_to_geocontainer(layer_list)

geoformat.geocontainer_to_ogr_format(geocontainer, output_folder, 'kml')

```


