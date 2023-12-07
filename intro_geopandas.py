#for installation of geopandas see https://geopandas.readthedocs.io/en/latest/getting_started/install.html
#install dependencies correctliy: fiona, pyproj, rtree, shapely, pygeos (experimental). Optional psycopg2 (for PostGIS connection), GeoAlchemy2 (for writing to PostGIS), geopy (for geocoding)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import fiona
import pyproj
import rtree
import shapely
import geopandas as gpd

#read geodata
myworkspace="C:/DATA"
#read Swiss cantons
cantons_gdf=gpd.read_file(myworkspace+"/"+"ch_kantone.shp")
#show attribute table
cantons_gdf.head()
#check columns
cantons_gdf.columns
#show the geoopandas dataframe
cantons_gdf
#plot cantons
cantons_gdf.plot('EINWOHNERZ', legend=True)

#check projection
cantons_gdf.crs

#re-project to WGS84
cantons_gdf_WGS84=cantons_gdf.to_crs("EPSG:4326")
cantons_gdf_WGS84.crs
cantons_gdf_WGS84.plot()

#calculate area in km2
cantons_gdf["area_km2"]=cantons_gdf.area/1000000

#add a column
cantons_gdf["popdensity"]=cantons_gdf["EINWOHNERZ"]/cantons_gdf["area_km2"]
cantons_gdf.plot('popdensity', legend=True)

#read hydropower stations
hydropowerstations_gdf=gpd.read_file(myworkspace+"/"+"ch_hydropowerplants.shp")
hydropowerstations_gdf.crs
hydropowerstations_gdf.plot()
#re-project from LV03 to LV95 (EPSG = 2056)
hydropowerstations_gdf_LV95=hydropowerstations_gdf.to_crs("EPSG:2056")
hydropowerstations_gdf_LV95.plot()


hydropowerstations_gdf.columns
#plot hydropower stations
hydropowerstations_gdf.plot('Type', legend=True)

#buffer hydro power stations
hydropowerstations_gdf_buffer=hydropowerstations_gdf.buffer(10000)
hydropowerstations_gdf_buffer.plot()

#plot hydropower stations and cantons together
ax=cantons_gdf.plot()
ax.set_title("hydropower stations in Swiss Cantons")
hydropowerstations_gdf_LV95.plot(ax=ax, marker='o', color='red', markersize=5)

#overlay between hydropower stations and cantons
hydropower_cantons=gpd.overlay(hydropowerstations_gdf_LV95, cantons_gdf, how="intersection")
hydropower_cantons.plot()

#calculate how many hydropower stations are located in each Canton
hydropowerplantspercanton=hydropower_cantons[["geometry","NAME"]].groupby(by="NAME").count()
hydropowerplantspercanton.rename(columns={"geometry":"numpowplants"}, inplace=True)
hydropowerplantspercanton

#join this back to the cantons geodataframe
cantons_gdf=cantons_gdf.merge(hydropowerplantspercanton, on="NAME")
cantons_gdf[["NAME", "numpowplants"]]


#plot number of powerplants per canton
ax=cantons_gdf.plot("numpowplants", legend=True)
ax.set_title("hydropower plants per Swiss Canton")
hydropowerstations_gdf_LV95.plot(ax=ax, marker='o', color='black', markersize=1)

#write the output file
hydropowerstations_gdf_LV95.to_file(myworkspace+"/"+"ch_hydropowerplantsLV95.shp")
cantons_gdf.to_file(myworkspace+"/"+"ch_hydropowerplantspercanton.shp")

#re-project hydropower stations to WGS84
hydropowerstations_gdf_WGS84=hydropowerstations_gdf_LV95.to_crs("EPSG:4326")
hydropowerstations_gdf_WGS84.crs
hydropowerstations_gdf_WGS84.plot()
hydropowerstations_gdf_Mercator=hydropowerstations_gdf_WGS84.to_crs("EPSG:3857")


#plotting with background maps
#background maps  need Mercator projection
import contextily as ctx
ax = hydropowerstations_gdf_Mercator.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
ctx.add_basemap(ax)
plt.title('hydropower stations')

#other example: read a file from internet
url = "http://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_land.geojson"
df = gpd.read_file(url)
df.plot()

