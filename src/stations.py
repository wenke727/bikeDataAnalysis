import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

df = pd.read_csv('../input/subway_all_lines.csv', sep='\t')

gdf = gpd.GeoDataFrame(df)
gdf.loc[:, 'geometry'] = gdf.apply(lambda x: Point(x.long, x.lat))
