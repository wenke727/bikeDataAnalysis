import pandas as pd
from tilemap import plot_geodata
from shapely.geometry import Point



df = pd.read_csv('../data/csv_04/2021-04-01.csv')

df


#%%
import geopandas as gpd

gdf = gpd.GeoDataFrame(df)
gdf.loc[:, 'geometry'] = gdf.apply(lambda x: Point(x.START_LNG, x.START_LAT))
