from shapely.geometry import mapping, Polygon
import matplotlib.pylab as plt
import geopandas as gpd
import pandas as pd
import geoplot
import numpy as np

filepath = "/home/tpham/peach_f98_tt_dist_voi"

spatialfile = "/home/tpham/peach_f98_tt_dist.0180_00d"

Headers = ['id', 'Z', 'S', 'CAr', 'Nwt', 'Mu', 'Mi', 'Nf', 'Nt', 'Qpout', 
           'Qpin', 'Srf', 'Rain', 'SWE', 'ST', 'IWE', 'LWE', 'DU', 'Upack', 
           'sLHF', 'sSHF', 'sGHF', 'sPHF', 'sRLo', 'sRLi', 'sRSi', 'Uerr', 
           'IntSWE', 'IntSub', 'IntUnl', 'SoilMoist', 'RootMoist', 
           'CanStorage', 'ActEvp', 'EvpSoil', 'ET', 'Gflux', 'Hflux', 'Lflux',
           'Qstrm', 'Hlev', 'FlwVlc', 'CanStorParam', 'IntercepCoeff',
           'Rutter, ThroughFall', 'Rutter, CanFieldCap', 'Rutter, DrainCoeff',
           'Rutter, DrainExpPar', 'LandUseAlb', 'VegHeight',
           'OptTransmCoeff', 'StomRes', 'VegFraction', 'LeafAI']

with open(filepath) as f:
    voronoivertices = f.readlines()
    voronoivertices = [x.strip().split(",") for x in voronoivertices]

with open(spatialfile) as f2:
    data = f2.readlines()
    data = [x.strip().split(",") for x in data]
    data.insert(0, Headers)
    df = pd.DataFrame(data[1:], columns = data[0]).set_index('id')
    df.index = pd.to_numeric(df.index, errors='coerce')
    #df[data] = df[data].astype(float)

'''
schema = {
    'geometry': 'Polygon',
    'properties': {'id': 'float', 'Z': 'float', 'S': 'float', 'CAr': 'float',
                   'Nwt': 'float', 'Mu': 'float', 'Mi': 'float', 'Nf': 'float',
                   'Nt': 'float', 'Qpout': 'float', 'Qpin': 'float', 
                   'Srf': 'float', 'Rain': 'float', 'SWE': 'float',
                   'ST': 'float', 'IWE': 'float', 'LWE': 'float',
                   'DU': 'float', 'Upack': 'float', 'sLHF': 'float',
                   'sSHF': 'float', 'sGHF': 'float', 'sPHF': 'float',
                   'sRLo': 'float', 'sRLi': 'float', 'sRSi': 'float',
                   'Uerr': 'float', 'IntSWE': 'float', 'IntSub': 'float',
                   'IntUnl': 'float', 'SoilMoist': 'float', 
                   'RootMoist': 'float', 'CanStorage': 'float',
                   'ActEvp': 'float', 'EvpSoil': 'float', 'ET': 'float',
                   'Gflux': 'float', 'Hflux': 'float', 'Lflux': 'float',
                   'Qstrm': 'float', 'Hlev': 'float', 'FlwVlc': 'float',
                   'CanStorParam': 'float', 'IntercepCoeff': 'float',
                   'Rutter, ThroughFall': 'float', 
                   'Rutter, CanFieldCap': 'float',
                   'Rutter, DrainCoeff': 'float',
                   'Rutter, DrainExpPar': 'float',
                   'LandUseAlb': 'float', 'VegHeight': 'float',
                   'OptTransmCoeff': 'float', 'StomRes': 'float',
                   'VegFraction': 'float', 'LeafAI': 'float'},
}
'''
Result = []
for i in range(0,(len(voronoivertices)),1):
    if len(voronoivertices[i]) == 3:
        my_dict = {'Node': voronoivertices[i][0]}
        voronoivertices[i].pop(0)
        Result.append(my_dict)

voronoivertices.pop(len(voronoivertices)-1)
i = 0        
Result2 = []
vertices_list = []
while i < len(voronoivertices):         
    if voronoivertices[i] != ["END"]:
        vertices_list.append(voronoivertices[i])
    elif voronoivertices[i] == ["END"]:        
        Result2.append(vertices_list)
        vertices_list = []
    i = i + 1

for i in range(0,(len(Result2)),1):
    for row in Result2[i]:
        for k in (0,1):
            row[k] = float(row[k])

Result4 = []
for i in range(0,(len(Result2)),1):
    pol = Polygon(Result2[i])
    Result4.append(pol)

polygon_list = gpd.GeoSeries(Result4)

gdf = gpd.GeoDataFrame(df, geometry = polygon_list)

from matplotlib.colors import Normalize
from matplotlib import cm


fig = Figure(figsize=(10, 6), dpi = 100)
ax = fig.add_subplot(1, 1, 1)


variable = 'RootMoist'
#x = gdf.plot(column = variable, legend=False,cmap = 'hot', edgecolor = 'black',
#        linewidth = 0.1)
mn = gdf[variable].min()
mx = gdf[variable].max()
norm = Normalize(vmin=mn, vmax=mx)
n_cmap = cm.ScalarMappable(norm=norm, cmap="hot")
n_cmap.set_array([])
ax.get_figure().colorbar(n_cmap, ax=ax, orientation = 'vertical')


geoplot.choropleth(gdf, hue=gdf[variable],
    cmap='Greens', figsize=(8, 4)
)


    
'''    

        'properties': {'id': 'float', 'Z': 'float', 'S': 'float', 'CAr': 'float',
                   'Nwt': 'float', 'Mu': 'float', 'Mi': 'float', 'Nf': 'float',
                   'Nt': 'float', 'Qpout': 'float', 'Qpin': 'float', 
                   'Srf': 'float', 'Rain': 'float', 'SWE': 'float',
                   'ST': 'float', 'IWE': 'float', 'LWE': 'float',
                   'DU': 'float', 'Upack': 'float', 'sLHF': 'float',
                   'sSHF': 'float', 'sGHF': 'float', 'sPHF': 'float',
                   'sRLo': 'float', 'sRLi': 'float', 'sRSi': 'float',
                   'Uerr': 'float', 'IntSWE': 'float', 'IntSub': 'float',
                   'IntUnl': 'float', 'SoilMoist': 'float', 
                   'RootMoist': 'float', 'CanStorage': 'float',
                   'ActEvp': 'float', 'EvpSoil': 'float', 'ET': 'float',
                   'Gflux': 'float', 'Hflux': 'float', 'Lflux': 'float',
                   'Qstrm': 'float', 'Hlev': 'float', 'FlwVlc': 'float',
                   'CanStorParam': 'float', 'IntercepCoeff': 'float',
                   'Rutter, ThroughFall': 'float', 
                   'Rutter, CanFieldCap': 'float',
                   'Rutter, DrainCoeff': 'float',
                   'Rutter, DrainExpPar': 'float',
                   'LandUseAlb': 'float', 'VegHeight': 'float',
                   'OptTransmCoeff': 'float', 'StomRes': 'float',
                   'VegFraction': 'float', 'LeafAI': 'float'},
    })
'''    
    
