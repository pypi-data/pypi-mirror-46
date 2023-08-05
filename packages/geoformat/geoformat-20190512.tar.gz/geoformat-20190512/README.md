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

### Print data geolayer

Sometime it can be uselful to print in terminal geolayer's attributes.

### Change geolayer coordinate reference system [CRS]

It can be usefull to change the projection for a layer.  In this example we will transform a geolayer in projection Lambert93 [EPSG:2154] to coordinates system WGS84 [EPSG:4326]

### Write geolayer in a OGR compatible GIS file

You can obviously convert a geolayer in a compatible OGR file format.

### Write a container in OGR compatible dataSource

Like geolayer you can write a geoformat container in a folder or a GRG compatible datasource.

