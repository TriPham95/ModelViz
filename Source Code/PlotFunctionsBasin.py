import matplotlib.pylab as plt
import numpy as np
import pandas as pd


#Basin-averaged Hydrological Time Series

filepath = "D:/Download/VisualTribs/Output_PEACH/serial/Fall1996/hyd/peach_f96_tt_dist0240_00.mrf"






def BasinAvgPlot(filepath, Variable):
    MRFVariable = ["Time", "Srf", "MAP", "Max", "Min", " Fstate", "MSM100", 
                   "MSMRt", " MSMU", "MGW", "MET", "Sat", "Rain", "AvSWE", 
                   "AvMelt", "AvSTC", "AvDUint", "AvSLHF", "AvSSHF", "AvSPHF", 
                   "AvSGHF", "AvSRLI", "AvSRLO", "AvSRSI", "AvInSn", "AvInSu", 
                   "AvInUn", "SCA", "ChanP"]
    
    with open(filepath) as f:
        BasinAvg = f.readlines()
        BasinAvg = [x.strip().split() for x in BasinAvg]
        BasinAvg.insert(0, MRFVariable)
        df = pd.DataFrame(BasinAvg[1:], columns = BasinAvg[0]).set_index('Time')
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
    ax.set_title("Basin-averaged Hydrological Time Series", fontsize = 'large', 
                 fontdict = dict(weight = 'bold'))

    ax.legend()
    plt.show()
    


BasinAvgPlot(filepath, "AvSRLO")



































































