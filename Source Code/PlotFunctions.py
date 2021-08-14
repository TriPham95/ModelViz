import matplotlib.pylab as plt
import numpy as np
import pandas as pd

###############################################################################
filepath = "/home/tpham/Documents/VisualTribs/Output_PEACH/serial/Fall1998/hyd/peach_f98_tt_dist_Outlet.qout"


###############################################################################
# Basin Outlet Discharge Time Series
###############################################################################
def QoutletPlot(filepath):
    with open(filepath) as f:
        QoutletContent = f.readlines()
        QoutletContent = [x.strip().split("\t") for x in QoutletContent]
        QoutletContent.insert(0, ['Time', 'Qstrm', 'HLevel'])
        df = pd.DataFrame(QoutletContent[1:], 
                      columns = QoutletContent[0]).set_index('Time')
        df['Qstrm'] = df['Qstrm'].astype(float)
        df['HLevel'] = df['HLevel'].astype(float)
        df.index = pd.to_numeric(df.index, errors='coerce')

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax2 = ax1.twinx()

    for tick in ax1.yaxis.get_ticklabels():
        #tick.set_fontsize('large')
        tick.set_color('blue')
        tick.set_weight('bold')
            
    for tick in ax1.xaxis.get_ticklabels():
        #tick.set_fontsize('large')
        tick.set_color('black')
        tick.set_weight('bold')
        
    for tick in ax2.yaxis.get_ticklabels():
        tick.set_fontsize('large')
        tick.set_color('red')
        tick.set_weight('bold')

    plot1 = ax1.plot(df.index, df['Qstrm'], 'b-')
    plot2 = ax2.plot(df.index, df['HLevel'], 'r-')
    
       
    ax1.set_ylabel('Discharge (m^3/s)', color = 'blue', 
                   fontsize = 12, fontdict = dict(weight = 'bold'))
    ax2.set_ylabel('Channel Stage (m)', color = 'red', 
                   fontsize = 12, fontdict = dict(weight = 'bold'))
    ax1.set_xlabel('Time (Hour)', fontsize = 12, 
                   fontdict = dict(weight = 'bold'))
    xtick = np.arange(df.index.min(), df.index.max(), 5)
    ax1.set_xticks(xtick, minor = True)
    ax1.grid(True, which = 'major', axis='y', linewidth = 0.1)
    ax1.grid(True, which = 'major', axis='x', linewidth = 0.1)
    ax1.set_title("Basin Outlet Discharge Time Series", fontsize = 'large', 
                  fontdict = dict(weight = 'bold'))
    Combined = plot1 + plot2
    Labels = [l.get_label() for l in Combined]
    ax1.legend(Combined, Labels, loc=0)
    plt.show()


QoutletPlot(filepath)

###############################################################################
# Discharge Time Series at Interior Channel Locations
###############################################################################
filepath2 = "/home/tpham/Documents/VisualTribs/Output_PEACH/serial/Fall1996/hyd/peach_f96_tt_dist_5948.qout"


def QinterirorPlot(filepath):
    with open(filepath) as f:
        QoutletContent = f.readlines()
        QoutletContent = [x.strip().split("\t") for x in QoutletContent]
        QoutletContent.insert(0, ['Time', 'Qstrm', 'HLevel'])
        df = pd.DataFrame(QoutletContent[1:], 
                      columns = QoutletContent[0]).set_index('Time')
        df['Qstrm'] = df['Qstrm'].astype(float)
        df['HLevel'] = df['HLevel'].astype(float)
        df.index = pd.to_numeric(df.index, errors='coerce')

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax2 = ax1.twinx()

    for tick in ax1.yaxis.get_ticklabels():
        #tick.set_fontsize('large')
        tick.set_color('blue')
        tick.set_weight('bold')
            
    for tick in ax1.xaxis.get_ticklabels():
        #tick.set_fontsize('large')
        tick.set_color('black')
        tick.set_weight('bold')
        
    for tick in ax2.yaxis.get_ticklabels():
        tick.set_fontsize('large')
        tick.set_color('red')
        tick.set_weight('bold')

    plot1 = ax1.plot(df.index, df['Qstrm'], 'b-')
    plot2 = ax2.plot(df.index, df['HLevel'], 'r-')
    
       
    ax1.set_ylabel('Discharge (m^3/s)', color = 'blue', 
                   fontsize = 12, fontdict = dict(weight = 'bold'))
    ax2.set_ylabel('Channel Stage (m)', color = 'red', 
                   fontsize = 12, fontdict = dict(weight = 'bold'))
    ax1.set_xlabel('Time (Hour)', fontsize = 12, 
                   fontdict = dict(weight = 'bold'))
    xtick = np.arange(df.index.min(), df.index.max(), 5)
    ax1.set_xticks(xtick, minor = True)
    ax1.grid(True, which = 'major', axis='y', linewidth = 0.1)
    ax1.grid(True, which = 'major', axis='x', linewidth = 0.1)
    ax1.set_title("Basin Interior Discharge Time Series", fontsize = 'large', 
                  fontdict = dict(weight = 'bold'))
    Combined = plot1 + plot2
    Labels = [l.get_label() for l in Combined]
    ax1.legend(Combined, Labels, loc=0)
    plt.show()

QinterirorPlot(filepath2)














































































