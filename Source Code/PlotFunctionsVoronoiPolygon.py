from shapely.geometry import mapping, Polygon
import matplotlib.pylab as plt
import geopandas as gpd
import pandas as pd
from matplotlib.colors import Normalize
from matplotlib import cm

filepath = "/home/tpham/Desktop/peach_f98_tt_dist_voi"

spatialfile = "/home/tpham/Desktop/peach_f98_tt_dist.0180_00d"







def VoronoiPolygonPlot(filepath, spatialfile, variable):
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
        df.index = pd.to_numeric(df.index, errors = 'coerce')
    
    
    VoronoiFormat = []
    for i in range(0,(len(voronoivertices)),1):
        if len(voronoivertices[i]) == 3:
            my_dict = {'Node': voronoivertices[i][0]}
            voronoivertices[i].pop(0)
            VoronoiFormat.append(my_dict)
            
    voronoivertices.pop(len(voronoivertices)-1)
    i = 0        
    Vertices = []
    vertices_list = []
    while i < len(voronoivertices):         
        if voronoivertices[i] != ["END"]:
            vertices_list.append(voronoivertices[i])
        elif voronoivertices[i] == ["END"]:        
            Vertices.append(vertices_list)
            vertices_list = []
        i = i + 1
    
    for i in range(0,(len(Vertices)),1):
        del Vertices[i][0]
        
    for i in range(0,(len(Vertices)),1):
        for row in Vertices[i]:
            for k in (0,1):
                row[k] = float(row[k])
                
    PolList = []
    for i in range(0,(len(Vertices)),1):
        pol = Polygon(Vertices[i])
        PolList.append(pol)
        
        
    polygon_list = gpd.GeoSeries(PolList)

    gdf = gpd.GeoDataFrame(df, geometry = polygon_list)


    #variable = 'RootMoist'
    ax = gdf.plot(column = variable, legend=False,cmap = 'hot', edgecolor = 'black',
         linewidth = 0.1)
    mn = gdf[variable].min()
    mx = gdf[variable].max()
    norm = Normalize(vmin=mn, vmax=mx)
    n_cmap = cm.ScalarMappable(norm=norm, cmap="hot")
    n_cmap.set_array([])
    ax.get_figure().colorbar(n_cmap, ax=ax, orientation = 'vertical')

    

















VoronoiPolygonPlot(filepath, spatialfile, 'ET')






























