********************
Welcome to Geoformat
********************

Introduction
############


Geoformat is GDAL / OGR  overlayer wiht MIT licence.
The library aim is to simplify loading and OGR 'DataSource' and 'Layer' manipulations.
Until now this library is in Alpha mode. This means that for the moment the structure of this library is not
full oriented object compatible.

Installation
############

>>> pip install geoformat



Basic manipulations
###################



Geoformat structure
-------------------

.. image:: Geoformat/images



Open a container
----------------

A container is an equivalent to folder or a database containing one or several geolayer.

Open a geolayer
---------------

A geolayer is an equivalent to a file or a table in database containing one or several features with attibutes and/or
geometry.


Print data geolayer
-------------------

Sometime it can be uselful to print in terminal geolayer's attributes.


Write geolayer in a OGR compatible GIS file
-------------------------------------------

You can obviously convert a geolayer in a compatible OGR file format.


Write a container in OGR compatible dataSource
----------------------------------------------

Like geolayer you can write a geoformat container in a folder or a GRG compatible datasource.



