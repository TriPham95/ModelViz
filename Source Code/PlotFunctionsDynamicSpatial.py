import matplotlib.pylab as plt
import numpy as np
import pandas as pd


#Basin-averaged Hydrological Time Series

filepath = "D:/Download/VisualTribs/Output_PEACH/serial/Fall1996/voronoi/peach_f96_tt_dist.0180_00d"






def DynamicSpatialPlot(filepath, Variable):
    timestamp_00d = ["ID", "Z", "S", "CAr", "Nwt", "Mu", "Mi", "Nf", "Nt",
                     "Qpout", "Qpin", "Srf", "Rain", "SWE", "ST", "IWE", "LWE",
                     "DU", "Upack", "sLHF", " sSHF", "sGHF", "sPHF", "sRLo", 
                     "sRLi", "sRSi", "Uerr", "IntSWE", "IntSub", "IntUnl", 
                     "SoilMoist", "RootMoist", "CanStorage", "ActEvp", 
                     "EvpSoil", "ET", "Gflux", "Hflux", "Lflux", "Qstrm", 
                     "Hlev", "FlwVlc", "CanStorParam", "IntercepCoeff", 
                     "ThroughFall", "CanFieldCap", "DrainCoeff", "DrainExpPar", 
                     "LandUseAlb", "VegHeight", "OptTransmCoeff", "StomRes", 
                     "VegFraction", "LeafAI"]
    
    with open(filepath) as f:
        DynamicSpatial = f.readlines()
        DynamicSpatial = [x.strip().split(",") for x in DynamicSpatial]
        DynamicSpatial.insert(0, timestamp_00d)
        df = pd.DataFrame(DynamicSpatial[1:], columns = DynamicSpatial[0])
        df.index = pd.to_numeric(df.index, errors='coerce')
        df[Variable] = df[Variable].astype(float)
    
    
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for tick in ax.yaxis.get_ticklabels():
        tick.set_color('black')
        tick.set_weight('bold')            
    for tick in ax.xaxis.get_ticklabels():
        tick.set_color('black')
        tick.set_weight('bold')

    ax.plot(df.index, df[Variable], 'k-')
    ax.set_ylabel(Variable, color = 'black', 
                  fontsize = 12, fontdict = dict(weight = 'bold'))
    ax.set_xlabel('Time (Hour)', fontsize = 12, 
                  fontdict = dict(weight = 'bold'))
    xtick = np.arange(df.index.min(), df.index.max(), 5)
    ax.set_xticks(xtick, minor = True)
    ax.grid(True, which = 'major', axis='y', linewidth = 0.1)
    ax.grid(True, which = 'major', axis='x', linewidth = 0.1)
    ax.set_title("Dynamic Spatial Output at " + df["ID"][0], fontsize = 'large', 
                 fontdict = dict(weight = 'bold'))

    ax.legend()
    plt.show()


DynamicSpatialPlot(filepath, "Hflux")














  