import matplotlib.pylab as plt
import numpy as np
import pandas as pd


filepath = "D:\\Download\\VisualTribs\\Output_PEACH\\serial\\Fall1996\\voronoi\\peach_f96_tt_dist3218.pixel"







###############################################################################

def PixelPlot(filepath, Variable):
    PixelCols = ["ID", "Time", "Nwt", "Nf", "Nt", "Mu", "Mi", "Qpout",
                 "Qpin", "Trnsm", "GWflx", "Srf", "Rain", "SoilMoist", 
                 "RootMoist", "AirT", "DewT", "SurfT", "SoilT", 
                 "Press", "RelHum", "SkyCov", "Wind", "NetRad", 
                 "ShrtRadIn", "ShrtRadIn_dir", "ShrtRadIn_dif", 
                 "ShortAbsbVeg", "ShortAbsbSoi", "LngRadIn", 
                 "LngRadOut", "PotEvp", "ActEvp", "EvpTtrs", 
                 "EvpWetCan", "EvpDryCan", "EvpSoil", "Gflux", "Hflux", 
                 "Lflux", "NetPrecip", "LiqWE", "IceWE", "SnWE", "U",
                 "RouteWE", "SnTemp", "SurfAge", "DU", "snLHF", "snSHF", 
                 "snGHF", "snPHF", "snRLout", "snRLin", "snRSin", 
                 "Uerror", "intSWEq", "intSub", "intSnUnload", 
                 "CanStorage", "CumIntercept", "Interception", 
                 "Recharge", "RunOn", "srf_Hour", "Qstrm", "Hlevel", 
                 "CanStorParam", "IntercepCoeff", "ThroughFall", 
                 "CanFieldCap", "DrainCoeff", "DrainExpPar", 
                 "LandUseAlb", "VegHeight", "OptTransmCoeff", "StomRes", 
                 "VegFraction", "LeafAI"]

    with open(filepath) as f:
        Voronoi = f.readlines()
        Voronoi = [x.strip().split() for x in Voronoi]
        Voronoi.insert(0, PixelCols)
        df = pd.DataFrame(Voronoi[1:], columns = Voronoi[0]).set_index('Time')
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
    ax.set_title("Hydrologic Time Series at TIN Node " + df['ID'][0], fontsize = 'large', 
                 fontdict = dict(weight = 'bold'))

    ax.legend()
    plt.show()
    
PixelPlot(filepath, "Interception")


    




































