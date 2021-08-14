# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tkinter as tk
import geopandas as gpd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import Normalize
from matplotlib import cm
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox as msg    
from tkinter import filedialog
from shapely.geometry import Polygon
plt.ioff()
###############################################################################
# Reading pixel data
###############################################################################
def PixelData(filepath, Variable):
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
    return df
###############################################################################
# Reading basin data
###############################################################################
def BasinData(filepath, Variable):
    MRFVariable = ["Time", "Srf", "MAP", "Max", "Min", " Fstate", "MSM100", 
                   "MSMRt", "MSMU", "MGW", "MET", "Sat", "Rain", "AvSWE", 
                   "AvMelt", "AvSTC", "AvDUint", "AvSLHF", "AvSSHF", "AvSPHF", 
                   "AvSGHF", "AvSRLI", "AvSRLO", "AvSRSI", "AvInSn", "AvInSu", 
                   "AvInUn", "SCA"]    
    with open(filepath) as f:
        BasinAvg = f.readlines()
        BasinAvg = [x.strip().split() for x in BasinAvg]
        BasinAvg.insert(0, MRFVariable)
        df = pd.DataFrame(BasinAvg[1:], columns = BasinAvg[0]).set_index('Time')
        df.index = pd.to_numeric(df.index, errors = 'coerce')
        df[Variable] = df[Variable].astype(float)
    return df
###############################################################################
# Reading Qoutlet data
###############################################################################
def QoutletData(filepath):
    with open(filepath) as f:
        QoutletContent = f.readlines()
        QoutletContent = [x.strip().split("\t") for x in QoutletContent]
        QoutletContent.insert(0, ['Time', 'Qstrm', 'HLevel'])
        df = pd.DataFrame(QoutletContent[1:], 
                      columns = QoutletContent[0]).set_index('Time')
        df['Qstrm'] = df['Qstrm'].astype(float)
        df['HLevel'] = df['HLevel'].astype(float)
        df.index = pd.to_numeric(df.index, errors='coerce')
    return df
###############################################################################
# Reading spatial data
###############################################################################
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
        for row in Vertices[i]:
            for k in (0,1):
                row[k] = float(row[k])
                
    PolList = []
    for i in range(0,(len(Vertices)),1):
        pol = Polygon(Vertices[i])
        PolList.append(pol)
        
        
    polygon_list = gpd.GeoSeries(PolList)
    gdf = gpd.GeoDataFrame(df, geometry = polygon_list)    
    return gdf
###############################################################################
# Reading integrated data                                                     #    
###############################################################################
def IntegratedPlot(filepath, spatialfile, variable):
    Headers = ['id', ' BndCd', 'Z', 'VAr', 'CAr', 'Curv', 'EdgL', 'tan(Slp)', 
               'FWidth', 'Aspect', 'SV', 'LV', 'AvSM', 'AvRtM', 'HOccr', 'HRt', 
               'SbOccr', 'SbRt', 'POccr', 'PRt', 'SatOccr', 'SatRt', 
               'SoiSatOccr', 'RchDsch', 'AveET', 'EvpFrct', 'cLHF', 
               'cMelt', 'cSHF', 'cPHF', 'cRLIn', 'cRLo', 
               'cRSIn', 'cGHF', 'cUErr', 'cHrsSun', 'cHrsSnow', 'persTime', 
               'peakWE', 'peakTime', 'initTime', 'cIntSub', 'cintUnl', 
               'AvCanStorParam', 'AvIntercCoeff', 'AvTF', 'AvCanFieldCap',
               'AvDrainCoeff', 'AvDrainExpPar', 'AvLUAlb', 'AvVegHeight', 
               'AvOTCoeff', 'AvStomRes', 'AvVegFract', 'AvLeafAI']   
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
        for row in Vertices[i]:
            for k in (0,1):
                row[k] = float(row[k])
                
    PolList = []
    for i in range(0,(len(Vertices)),1):
        pol = Polygon(Vertices[i])
        PolList.append(pol)
        
        
    polygon_list = gpd.GeoSeries(PolList)
    gdf = gpd.GeoDataFrame(df, geometry = polygon_list)    
    return gdf
###############################################################################
# Creating right click menu                                                   #
############################################################################### 
def rClicker(e):
    ''' right click context menu for all Tk Entry and Text widgets
    '''
    try:
        def rClick_Copy(e, apnd=0):
            e.widget.event_generate('<Control-c>')
        def rClick_Cut(e):
            e.widget.event_generate('<Control-x>')
        def rClick_Paste(e):
            e.widget.event_generate('<Control-v>')
        e.widget.focus()
        nclst=[
               (' Cut', lambda e=e: rClick_Cut(e)),
               (' Copy', lambda e=e: rClick_Copy(e)),
               (' Paste', lambda e=e: rClick_Paste(e)),
               ]
        rmenu = Menu(None, tearoff=0, takefocus=0)
        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)
        rmenu.tk_popup(e.x_root+40, e.y_root+10, entry="0")
    except tk.TclError:
        print (' - rClick menu, something wrong')
        pass    
    return "break"
###############################################################################
# Documentation                                                               #
###############################################################################    
class Documentation():
    def Title(self):
        "Visual tRIBS"     
    def Information(self):
        '''This software is written and designed by Tri G. Pham, Hernan A. Moreno, Jason R. Vogel at the University of Oklahoma.
Copyright 2019
        '''           
    def PixelExplanation(self):        
        '''1.Depth to groundwater table, Nwt [mm]
2.Wetting front depth, Nf [mm]
3.Top front depth, Nt [mm]
4.Total moisture above the water table, Mu [mm]
5.Moisture content in the initialization profile, Mi [mm]
6.Unsaturated lateral flow out from cell, Qpout [mm/hr]
7.Unsaturated lateral flow into cell, Qpin [mm/hr]
8.Transmissivity, Trnsm [m2/hr]
9.Groundwater flux, GWflx [m3/hr]
10. Surface Runoff, Srf [mm]
11.Rainfall, Rain [mm/hr]
12.Soil Moisture, top 10 cm, SoilMoist []
13.Root Zone Moisture, top 1 m, RootMoist []
14.Air Temperature, AirT [C]
15.Dew Point Temperature, DewT [C]
16.Surface Temperature, SurfT [C]
17.Soil Temperature, SoilT [C]
18.Atmospheric Pressure, Press [Pa]
19.Relative Humidity, RelHum []
20.Sky Cover, SkyCov []
21.Wind Speed, Wind [m/s]
22.Net Radiation, NetRad [W/m2]
23.Incoming Shortwave Radiation, ShrtRadIn [W/m2]
24.Incoming Direct Shortwave Radiation, ShrtRadIn_dir [W/m2]
25.Incoming Diffuse Shortwave Radiation, ShrtRadIn_dif [W/m2]
26.Shortwave Absorbed Radiation, Vegetation, ShortAbsbVeg [W/m2]
27.Shortwave Absorbed Radiation, Soil, ShortAbsbSoi [W/m2]
28.Incoming Longwave Radiation, LngRadIn [W/m2]
29.Outgoing Longwave Radiation, LngRadOut [W/m2]
30.Potential Evaporation, PotEvp [mm/hr]
31.Actual Evaporation, ActEvp [mm/hr]
32.Total Evapotranspiration, EvpTtrs [mm/hr]
33.Evaporation from Wet Canopy, EvpWetCan [mm/hr]
34.Evaporation from Dry Canopy(Transpiration), EvpDryCan [mm/hr]
35.Evaporation from Bare Soil, EvpSoil [mm/hr]
36.Ground Heat Flux, Gflux [W/m2]
37.Sensible Heat Flux, Hflux [W/m2]
38.Latent Heat Flux, Lflux [W/m2]
39.Net Precipitation, NetPrecip [mm/hr]
40.Liquid Water Equivalent, LiqWE [cm]
41.Ice Water Equivalent, IceWE [cm]
42.Snow Water Equivalent, SnWE [cm]
43.Internal Energy of Snow Pack, U [kJ/m2]
44.Routed Melt Water Equivalent, RouteWE [cm]
45.Snow Temperature, SnTemp [C]
46.Snow Surface Age, SurfAge [hr]
47.Change in Snow Pack Internal Energy, DU [kJ/m2]
48.Latent Heat Flux from Snow Cover, snLHF [kJ/m2]
49.Sensible Heat Flux from Snow Cover, snSHF [kJ/m2]
50.Ground Heat Flux from Snow Cover, snGHF [kJ/m2]
51.Precip Heat Flux from Snow Cover, snPHF [kJ/m2]
52.Outgoing Longw. Rad. from Snow, snRLout [kJ/m2]
53.Incom. Longw. Radn. from Snow, snRLin [kJ/m2]
54.Incom. Shortw. Radn. from Snow,  snRSin [kJ/m2]
55.Error in Energy Balance, Uerror [kJ/m2]
56.Intercepted Snow Water Equivalent, intSWEq [cm]
57.Sublim. Snow Water Equiv. from Canopy, intSub [cm]
58.Unloaded SWE from Canopy, intSnUnload [cm]
59.Canopy Storage, CanStorage [mm]
60.Cumulative Interception, CumIntercept [mm]
61.Interception, Interception [mm]
62.Runon, RunOn [mm]
63.Surface Runoff in Hour, srf_Hour [mm]
64.Discharge, Qstrm [m3/s]
65.Channel Stage, Hlevel [m]
66.Canopy Storage Parameter, CanStorParam [mm]
67.Interception Coefficient, IntercepCoeff []
68.Free Throughfall Coeff.- Rutter, ThroughFall []
69.Canopy Field Capacity – Rutter, CanFieldCap [mm]
70.Drainage coefficient – Rutter, DrainCoeff [mm/hr]
71.Drainage Expon. Param. – Rutter, DrainExpPar [mm-1]
72.Albedo, LandUseAlb []
73.Vegetation Height , VegHeight [m]
74.Optical Transmission Coeff., OptTransmCoeff []
75.Canopy- Average Stomatal Resistance, StomRes 	[s/m]
76.Vegetation Fraction, VegFraction 	[]
77.Canopy Leaf Area Index, LeafAI []
        '''
    def BasinExplanation(self):        
        '''1.Time [hr]
2.Surface Runoff from Hydrologic Routing, Srf [m3/s]
3.Mean Areal Precipitation, MAP [mm/hr]
4.Maximum Rainfall Rate, Max [mm/hr]
5.Minimum Rainfall Rate, Min [mm/hr]
6.Forecast State, Fstate []
7.Mean Surface Soil Moisture (in top 10 cm), MSM100 []
8.Mean Soil Moisture in Root Zone (in top 1 m), MSMRt []
9.Mean Soil Moisture in Unsaturated Zone (above water table), MSMU []
10.Mean Depth to Groundwater, MGW [mm]
11.Mean Evapotranspiration, MET [mm]
12.Areal Fraction of Surface Saturation, Sat []
13.Areal Fraction of Rainfall, Rain []
14.Average Snow Water Equivalent, AvSWE [cm]
15.Average Amount of Snow Melt, AvMelt[cm]
16.Average Snow Temperature, AvSTC[C]
17.Average Change in Snow Pack Internal Energy, AvDUint [kJ/m2]
18.Average Latent Heat Flux from Snow Covered Areas, AvSLHF [kJ/m2]
19.Average Sensible Heat Flux from Snow Covered Areas, AvSSHF [kJ/m2]
20.Average Precipitation Heat Flux from Snow Covered Areas, AvSPHF [kJ/m2]
21.Average Ground Heat Flux from Snow Covered Areas, AvSGHF [kJ/m2]
22.Average Incoming Longwave Radiation from Snow Covered Areas, AvSRLI [kJ/m2]
23.Average Outgoing Longwave Radiation from Snow Covered Areas, AvSRLO [kJ/m2]
24.Average Incoming Shortwave Radiation from Snow Covered Areas, AvSRSI [kJ/m2]
25.Mean Intercepted Snow Water Equivalent, AvInSn [cm]
26.Mean Sublimation from Intercepted Snow, AvInSu [cm]
27.Mean Unloaded Snow from Canopy, AvInUn [cm]
28.Fraction Snow Covered Area, SCA []
29.Channel percolation, ChanP [m3]
'''
    def SpatialExplanation(self):
        '''1.Node Identification, ID [id]
2.Elevation, Z [m]
3.Slope, S [|radian|]
4.Contributing Area, CAr [m2]
5.Depth to groundwater table, Nwt [mm]
6.Total moisture above the water table, Mu [mm]
7.Moisture content in the initialization profile, Mi [mm]
8.Wetting front depth, Nf [mm]
9.Top front depth, Nt [mm]
10.Unsaturated lateral flow out from cell, Qpout [mm/hr]
11.Unsaturated lateral flow into cell, Qpin [mm/hr]
12.Surface Runoff, Srf [mm]
13.Rainfall, Rain [mm/hr]
14.Snow Water Equivalent, SWE [cm]
15.Snow Temperature, ST [C]
16.Ice Part of Water Equivalent, IWE [cm]
17.Liquid part of Water Equivalent, LWE [cm]
18.Change in Internal Energy of Snow Pack, DU [kW/m2]
19.Internal Energy of Snow Pack, Upack [kJ/m2]
20.Latent Heat Flux from Snow Cover, sLHF [kJ/m2]
21.Sensible Heat Flux from Snow Cover,  sSHF [kJ/m2]
22.Ground Heat Flux from Snow Cover,  sGHF [kJ/m2]
23.Precipitation Heat Flux from Snow Cover,  sPHF [kJ/m2]
24.Outgoing Longwave Radiation from Snow Cover, sRLo [kJ/m2]
25.Incoming Longwave Radation from Snow Cover,  sRLi [kJ/m2]
26.Incoming Shortwave Radiation from Snow Cover, sRSi [kJ/m2]
27.Error in Energy Balance, Uerr [J/m2]
28.Intercepted SWE, IntSWE [cm]
29.Sublimated Snow from Canopy, IntSub [cm]
30.Unloaded Snow from Canopy, IntUnl [cm]
31.Soil Moisture, top 10 cm, SoilMoist []
32.Root  Zone Moisture, top 1 m, RootMoist []
33.Canopy Storage, CanStorage [mm]
34.Actual Evaporation, ActEvp [mm/hr]
35.Evaporation from Bare Soil, EvpSoil [mm/hr]
36.Total Evapotranspiration, ET [mm/hr]
37.Ground Heat Flux, Gflux [W/m2]
38.Sensible Heat Flux, Hflux [W/m2]
39.Latent Heat Flux, Lflux [W/m2]
40.Discharge, Qstrm [m3/s]
41.Channel Stage, Hlev [m]
42.Channel Flow Velocity, FlwVlc [m/s]
43.Canopy Storage Parameter, CanStorParam [mm]
44.Interception Coefficient, IntercepCoeff []
45.Free Throughfall Coeff.- Rutter, ThroughFall []
46.Canopy Field Capacity – Rutter, CanFieldCap [mm]
47.Drainage coefficient – Rutter, DrainCoeff [mm/hr]
48.Drainage Expon. Param. – Rutter, DrainExpPar [mm-1]
49.Albedo, LandUseAlb []
50.Vegetation Height , VegHeight [m]
51.Optical Transmission Coeff., OptTransmCoeff []
52.Canopy- Average Stomatal Resistance, StomRes [s/m]
53.Vegetation Fraction, VegFraction []
54.Canopy Leaf Area Index, LeafAI []
'''
    def IntegratedSpatialExplanation(self):
        '''1.Node Identification, ID [id]
2.Boundary Flag, BndCd []
3.Elevation, Z [m]
4.Voronoi Area, VAr [m2]
5.Contributing Area, CAr [km2]
6.Curvature, Curv []
7.Flow Edge Length, EdgL [m]
8.Tangent of Flow Edge Slope, tan(Slp) []
9.Width of Voronoi Flow Window, FWidth [m]
10.Site Aspect as Angle from North, Aspect [radian]
11.Sky View Factor, SV []
12.Land View Factor, LV []
13.Average Soil Moisture, top 10 cm, AvSM []
14.Average Root Zone Moisture, top 1 m, AvRtM[]
15.Infiltration-excess Runoff Occurences, HOccr [# of TIMESTEP]
16.Infiltration-excess Runoff Average Rate, HRt [mm/hr]
17.Saturation-excess Runoff Occurences, SbOccr [# of TIMESTEP]
18.Saturation-excess Runoff Average Rate, SbRt [mm/hr]
19.Perched Return Runoff Occurences, POccr [# of TIMESTEP]
20.Perched Return Runoff Average Rate, PRt [mm/hr]
21.Groundwater Exfiltration Runoff Occurences, SatOccr [# of GWSTEP]
22.Groundwater Exfiltration Runoff Average Rate, SatRt [mm/hr]
23.Soil Saturation Occurences, SoiSatOccr [# of TIMESTEP]
24.Recharge-Discharge Variable, RchDsch [m]
25.Average Evapotranspiration, AveET [mm/hr]
26.Evaporative Fraction, EvpFrct[]
27.Cumulative Latent Heat Flux from Snow Cover, cLHF [kJ/m2]
28.Cumulative Melt, cMelt [cm]
29.Cumulative Sensible Heat Flux from Snow Cover, cSHF [kJ/m2]
30.Cumulative Precipitation Heat Flux from Snow Cover, cPHF [kJ/m2]
31.Cumulative Incoming Longwave Radiation from Snow Cover, cRLIn [kJ/m2]
32.Cumulative Outgoing Longwave Radiation from Snow Cover, cRLo [kJ/m2]
33.Cumulative Incoming Shortwave Radiation from Snow Cover, cRSIn [kJ/m2]
34.Cumulative Ground Heat Flux from Snow Cover, cGHF [kJ/m2]
35.Cumulative Energy Balance Error, cUErr [kJ/m2]
36.Cumulative Hours Exposed to Sun, cHrsSun [hr]
37.Cumulative Hours Snow Covered, cHrsSnow [hr]
38.Longest Time of Continuous Snow Cover, persTime [hr]
39.Maximum Season SWE, peakWE [cm]
40.Simulation Hour of Maximum SWE, peakTime [hr]
41.Simulation Hr of Initial SWE, initTime [hr]
42.Cumulative Sublimated Snow from Canopy, cIntSub [cm]
43.Cumulative Unloaded Snow from Canopy, cintUnl [cm]
44.Av. Canopy Storage Parameter, AvCanStorParam [mm]
45.Av. Intercep. Coeff., AvIntercCoeff []
46.Av. Free Throughfall Coeff.- Rutter, AvTF []
47.Av. Canopy Field Capac. – Rutter, AvCanFieldCap [mm]
48.Av. Drain. Coeff. – Rutter, AvDrainCoeff [mm/hr]
49.Av. Drain. Expon. Param. – Rutter, AvDrainExpPar [mm-1]
50.Av. Albedo,AvLUAlb []
51.Av. Veg. Height , AvVegHeight [m]
52.Av. Optical Transm. Coeff., AvOTCoeff []
53.Av. Canopy- Average Stom. Resist., AvStomRes [s/m]
54.Av. Veg. Frac., AvVegFract []
55.Av. Canopy Leaf Area Index, AvLeafAI []
'''       
###############################################################################
# Menu Creation and Formatting                                                #
###############################################################################              
class MenuBar:
    def __init__(self, window):
        self.window = window
        # Menu bar
    def create_menubar(self):
        menubar = Menu(self.window)
        self.window.config(menu = menubar)
        # Add File Menu 
        file_menu = Menu(menubar, tearoff = 0)
        # Add Exit Menu
        file_menu.add_command(label = "Exit", command = self._quit)
        # Add File Cascade
        menubar.add_cascade(label = "File", menu = file_menu)
        # Add Help Menu
        help_menu = Menu(menubar, tearoff=0)
        # Add About Menu
        help_menu.add_command(label = "About", 
                              command = lambda: msg.showinfo("Software Information", 
                                                             Documentation.Information.__doc__))
        menubar.add_cascade(label = "Help", menu = help_menu)
        
    # Quit menu
    def _quit(self):
        self.window.quit()
        self.window.destroy()
        exit()


###############################################################################
# Tab Creation                                                                #
############################################################################### 
class TabCreation:
    def __init__(self, window):
        self.window = window
        
    def create_tabs(self):
        # Create Tab Control
        self.tabControl = ttk.Notebook(self.window)
        #######################################################################
        # Create Tab 1
        #######################################################################
        self.tab1 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text = "Pixel Time Series")        
        FrameLayout(self.window, self.tab1).Tab1_InputFrame()
        FrameLayout(self.window, self.tab1).Tab1_TextFrame()
        #######################################################################
        # Create Tab 2
        #######################################################################
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab2, text = "Basin Time Series")
        FrameLayout(self.window, self.tab2).Tab2_InputFrame()
        FrameLayout(self.window, self.tab2).Tab2_TextFrame()
        #######################################################################
        # Create Tab 3
        #######################################################################
        self.tab3 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab3, text = "Dynamic Spatial Output")
        FrameLayout(self.window, self.tab3).Tab3_InputFrame()
        FrameLayout(self.window, self.tab3).Tab3_TextFrame()
        #######################################################################
        # Create Tab 4
        #######################################################################
        self.tab4 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab4, text = "Integrated Spatial Output")
        FrameLayout(self.window, self.tab4).Tab4_InputFrame()
        FrameLayout(self.window, self.tab4).Tab4_TextFrame()
        #self.tabControl.pack(expand = 1, fill = "both")
        #######################################################################
        # Create Tab 5
        #######################################################################
        self.tab5 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab5, text = "Basin Outlet Time Series")
        FrameLayout(self.window, self.tab5).Tab5_InputFrame()
        self.tabControl.pack(expand = 1, fill = "both")
        
###############################################################################
# Tab Layout Formatting                                                       #
############################################################################### 
class FrameLayout:
    def __init__(self, window, tab):
        self.window = window
        self.tab = tab
    ###########################################################################
    # Pixel Inputs
    ###########################################################################
    def Tab1_InputFrame(self):
        self.PixelFile = tk.StringVar()
        self.VariabletoPlot = tk.StringVar()
        
        self.label_1_1 = ttk.Label(text = "Input", 
                                   style = "Bold.TLabel",
                                   font = ("Verdana", "9", "bold"))        
        self.Inputs_Frame = ttk.LabelFrame(self.tab, labelwidget = self.label_1_1)
        self.Inputs_Frame.grid(column = 0, row = 0, rowspan = 3, 
                               columnspan = 20, sticky = "NS")
        self.Inputs_Button = tk.Button(self.Inputs_Frame, 
                                       text = "Browse .pix File",
                                       font = ("Verdana", "9", "bold"),                                       
                                       command = self.loadpixelfile)    
        self.Inputs_Button.grid(column = 0, row = 1)
        self.PixelName = tk.Text(self.Inputs_Frame, 
                                 height = 1, width = 29)
        self.PixelName.grid(column = 1, row = 1)
        self.PixelName.config(state = "normal")      
        ttk.Label(self.Inputs_Frame, 
                  text = "Variable to Plot",
                  justify = "center", font = ("Verdana", "9", "bold")).grid(column = 0, row = 2)      
        Options = ["Nwt", "Nf", "Nt", "Mu", "Mi", "Qpout",
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
        
        self.ValueOption_Entry = ttk.Combobox(self.Inputs_Frame,
                                              state = "readonly",
                                              textvariable = self.VariabletoPlot,
                                              values = Options)
        self.ValueOption_Entry.config(width = 18)
        self.ValueOption_Entry.grid(column = 1, row = 2)
     
        self.PixelPlot_Button = tk.Button(self.Inputs_Frame,
                                          text = "Plot",
                                          font = ("Verdana", "9", "bold"),
                                          command = self.PixelPlot)
        self.PixelPlot_Button.grid(column = 0, row = 3)
        
        self.PixelPlotSave_Button = tk.Button(self.Inputs_Frame,
                                          text = "Export",
                                          font = ("Verdana", "9", "bold"),
                                          command = self.save_file)
        self.PixelPlotSave_Button.grid(column = 1, row = 3)
     
        for child in self.Inputs_Frame.winfo_children(): 
            child.grid_configure(padx = 4, pady = 2) 
            
    ###########################################################################
    # Pixel Text Box for Explaination
    ###########################################################################
    def Tab1_TextFrame(self):
        self.label_1_2 = ttk.Label(text = "Variable Explanation", 
                                   style = "Bold.TLabel", 
                                   font = ("Verdana", "9", "bold"))  
        self.Inputs_Frame1 = ttk.LabelFrame(self.tab, labelwidget = self.label_1_2)
        self.Inputs_Frame1.grid(column = 0, row = 3, rowspan = 27, 
                              columnspan = 20, sticky = "NS")     

        self.TextExplaination = tk.Text(self.Inputs_Frame1, height = 42, 
                                        width = 62,
                                        font = ("Verdana", "7"))
        
        self.TextExplaination.tag_configure("left", justify='left')
        self.TextExplaination.insert(tk.END, Documentation().PixelExplanation.__doc__)
        self.TextExplaination.config(state = 'disabled')
        for child in self.Inputs_Frame1.winfo_children(): 
            child.grid_configure(padx = 4, pady = 2) 
            
    ###########################################################################
    # Pixel Plot
    ###########################################################################     
    def PixelPlot(self):
        self.label_2_2 = ttk.Label(text = "Variable Plot", 
                                   style = "Bold.TLabel",
                                   font = ("Verdana", "9", "bold"))
        self.PixelPlot_Frame = ttk.LabelFrame(self.tab, 
                                             labelwidget = self.label_2_2) 
        self.PixelPlot_Frame.grid(column = 21, 
                                 row = 0, 
                                 rowspan = 30, 
                                 columnspan = 200,
                                 sticky = "NS")
 
        filepath = self.PixelName.get("1.0","end-1c")
        Variable = self.ValueOption_Entry.get()        
        df = PixelData(filepath, Variable)
        self.fig = Figure(figsize=(10, 6), dpi = 100)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.clear()
        for tick in self.ax.yaxis.get_ticklabels():
            tick.set_color('black')
            tick.set_weight('bold')            
        for tick in self.ax.xaxis.get_ticklabels():
            tick.set_color('black')
            tick.set_weight('bold')                
        self.ax.plot(df.index, df[Variable], 'k-')
        self.ax.set_ylabel(Variable, color = 'black', 
                      fontsize = 12, fontdict = dict(weight = 'bold'))
        self.ax.set_xlabel('Time (Hour)', fontsize = 12, 
                      fontdict = dict(weight = 'bold'))
        xtick = np.arange(df.index.min(), df.index.max(), 5)
        self.ax.set_xticks(xtick, minor = True)
        self.ax.grid(True, which = 'major', axis='y', linewidth = 0.1)
        self.ax.grid(True, which = 'major', axis='x', linewidth = 0.1)
        self.ax.set_title("Hydrologic Time Series at TIN Node " + df['ID'][0], fontsize = 'large', 
                     fontdict = dict(weight = 'bold'))
        self.ax.legend(Variable, loc = 'best')
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.PixelPlot_Frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column = 0, row = 0)
        
    
    ###########################################################################
    # Basin Inputs
    ###########################################################################
    def Tab2_InputFrame(self):
        self.BasinFile = tk.StringVar()
        self.VariabletoPlot = tk.StringVar()
        
        self.label_1 = ttk.Label(text = "Input", 
                                   style = "Bold.TLabel",
                                   font = ("Verdana", "9", "bold"))        
        self.Inputs_Frame = ttk.LabelFrame(self.tab, labelwidget = self.label_1)
        self.Inputs_Frame.grid(column = 0, row = 0, rowspan = 3, 
                               columnspan = 20, sticky = "NS")
        self.Inputs_Button = tk.Button(self.Inputs_Frame, 
                                       text = "Browse .mrf File",
                                       font = ("Verdana", "9", "bold"),
                                       command = self.loadbasinfile)    
        self.Inputs_Button.grid(column = 0, row = 1)
        self.BasinName = tk.Text(self.Inputs_Frame, 
                                 height = 1, width = 29)
        self.BasinName.grid(column = 1, row = 1)
        self.BasinName.config(state = "normal")      
        ttk.Label(self.Inputs_Frame, 
                  text = "Variable to Plot",
                  justify = "center",
                  font = ("Verdana", "9", "bold")).grid(column = 0, row = 2)  

        Options = ["Srf", "MAP", "Max", "Min", "Fstate", "MSM100", "MSMRt", 
                   "MSMU", "MGW", "MET", "Sat", "Rain", "AvSWE", "AvMelt", 
                   "AvSTC", "AvDUint", "AvSLHF", "AvSSHF", "AvSPHF", 
                   "AvSGHF", "AvSRLI", "AvSRLO", "AvSRSI", "AvInSn", "AvInSu", 
                   "AvInUn", "SCA"]
    
        self.ValueOption_Entry = ttk.Combobox(self.Inputs_Frame,
                                              state = "readonly",
                                              textvariable = self.VariabletoPlot,
                                              values = Options)
        self.ValueOption_Entry.config(width = 16)
        self.ValueOption_Entry.grid(column = 1, row = 2)
     
        self.BasinPlot_Button = tk.Button(self.Inputs_Frame,
                                          text = "Plot",
                                          font = ("Verdana", "9", "bold"),
                                          command = self.BasinPlot)
        self.BasinPlot_Button.grid(column = 0, row = 3)
        
        self.BasinPlotSave_Button = tk.Button(self.Inputs_Frame,
                                          text = "Export",
                                          font = ("Verdana", "9", "bold"),
                                          command = self.save_file)
        self.BasinPlotSave_Button.grid(column = 1, row = 3)
        
        

        for child in self.Inputs_Frame.winfo_children(): 
            child.grid_configure(padx = 4, pady = 2) 
            
            
    ###########################################################################
    # BasinText Box for Explaination
    ###########################################################################
    def Tab2_TextFrame(self):
        self.label_2_2 = ttk.Label(text = "Variable Explanation", 
                                   style = "Bold.TLabel", 
                                   font = ("Verdana", "9", "bold"))  
        self.Inputs_Frame1 = ttk.LabelFrame(self.tab, labelwidget = self.label_2_2)
        self.Inputs_Frame1.grid(column = 0, row = 3, rowspan = 27, 
                              columnspan = 20, sticky = "NS")     

        self.TextExplaination = tk.Text(self.Inputs_Frame1, height = 42, 
                                        width = 62,
                                        font = ("Verdana", "7"))
        
        self.TextExplaination.tag_configure("left", justify='left')
        self.TextExplaination.insert(tk.END, Documentation().BasinExplanation.__doc__)
        self.TextExplaination.config(state = 'disabled')
        for child in self.Inputs_Frame1.winfo_children(): 
            child.grid_configure(padx = 4, pady = 2)             
            
            
            
            
    ###########################################################################
    # Basin Plot
    ###########################################################################
    def BasinPlot(self):
        self.label_2_2 = ttk.Label(text = "Variable Plot", 
                                   style = "Bold.TLabel",
                                   font = ("Verdana", "9", "bold"))
        self.BasinPlot_Frame = ttk.LabelFrame(self.tab, 
                                             labelwidget = self.label_2_2) 
        self.BasinPlot_Frame.grid(column = 21, 
                                 row = 0, 
                                 rowspan = 30, 
                                 columnspan = 200,
                                 sticky = "NS")
 
        filepath = self.BasinName.get("1.0","end-1c")
        Variable = self.ValueOption_Entry.get()        
        df = BasinData(filepath, Variable)
        self.fig = Figure(figsize=(10, 6), dpi = 100)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.clear()
        for tick in self.ax.yaxis.get_ticklabels():
            tick.set_color('black')
            tick.set_weight('bold')            
        for tick in self.ax.xaxis.get_ticklabels():
            tick.set_color('black')
            tick.set_weight('bold')                
        self.ax.plot(df.index, df[Variable], 'k-')
        self.ax.set_ylabel(Variable, color = 'black', 
                      fontsize = 12, fontdict = dict(weight = 'bold'))
        self.ax.set_xlabel('Time (Hour)', fontsize = 12, 
                      fontdict = dict(weight = 'bold'))
        xtick = np.arange(df.index.min(), df.index.max(), 5)
        self.ax.set_xticks(xtick, minor = True)
        self.ax.grid(True, which = 'major', axis='y', linewidth = 0.1)
        self.ax.grid(True, which = 'major', axis='x', linewidth = 0.1)
        self.ax.set_title("Basin-averaged Hydrological Time Series", 
                          fontsize = 'large', 
                     fontdict = dict(weight = 'bold'))
        self.ax.legend(Variable, loc = 'best')
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.BasinPlot_Frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column = 0, row = 0)        
        
    
        
            
    ###########################################################################
    # Voronoi Spatial Inputs
    ###########################################################################
    def Tab3_InputFrame(self):
        self.SpatialFile = tk.StringVar()
        self.VoronoiFile = tk.StringVar()
        self.VariabletoPlot = tk.StringVar()
        
        
        
        self.label_1 = ttk.Label(text = "Spatial Input", 
                                 style = "Bold.TLabel", 
                                 font = ("Verdana", "9", "bold"))        
        self.Inputs_Frame = ttk.LabelFrame(self.tab, labelwidget = self.label_1)
        self.Inputs_Frame.grid(column = 0, row = 0, rowspan = 3, 
                               columnspan = 20, sticky = "NS")
        
        
        self.VoronoiInputs_Button1 = tk.Button(self.Inputs_Frame, 
                                               text = "Browse voi File",
                                               font = ("Verdana", "9", "bold"),
                                               command = self.loadvoifile)
        self.VoronoiInputs_Button1.grid(column = 0, row = 1)        
        self.VoronoiName = tk.Text(self.Inputs_Frame, 
                                   height = 1, width = 28)
        self.VoronoiName.grid(column = 1, row = 1)
        
   
        self.SpatialInputs_Button2 = tk.Button(self.Inputs_Frame, 
                                               text = "Browse 00d File",
                                               font = ("Verdana", "9", "bold"),
                                               command = self.loadspatialfile)
        self.SpatialInputs_Button2.grid(column = 0, row = 2)        
        self.SpatialName = tk.Text(self.Inputs_Frame, 
                                   height = 1, width = 28)
        self.SpatialName.grid(column = 1, row = 2)
        
        ttk.Label(self.Inputs_Frame, 
                  text = "Variable to Plot",
                  justify = "center", 
                  font = ("Verdana", "9", "bold")).grid(column = 0, row = 3)  

        Options = ['Z', 'S', 'CAr', 'Nwt', 'Mu', 'Mi', 'Nf', 'Nt', 'Qpout', 
                   'Qpin', 'Srf', 'Rain', 'SWE', 'ST', 'IWE', 'LWE', 'DU', 
                   'Upack', 'sLHF', 'sSHF', 'sGHF', 'sPHF', 'sRLo', 'sRLi', 
                   'sRSi', 'Uerr', 'IntSWE', 'IntSub', 'IntUnl', 'SoilMoist', 
                   'RootMoist', 'CanStorage', 'ActEvp', 'EvpSoil', 'ET', 
                   'Gflux', 'Hflux', 'Lflux', 'Qstrm', 'Hlev', 'FlwVlc', 
                   'CanStorParam', 'IntercepCoeff', 'Rutter, ThroughFall', 
                   'Rutter, CanFieldCap', 'Rutter, DrainCoeff',
                   'Rutter, DrainExpPar', 'LandUseAlb', 'VegHeight',
                   'OptTransmCoeff', 'StomRes', 'VegFraction', 'LeafAI']
    
        self.ValueOption_Entry = ttk.Combobox(self.Inputs_Frame,
                                              state = "readonly",
                                              textvariable = self.VariabletoPlot,
                                              values = Options)
        self.ValueOption_Entry.config(width = 16)
        self.ValueOption_Entry.grid(column = 1, row = 3)
        

        
        
        self.SpatialPlot_Button = tk.Button(self.Inputs_Frame,
                                            text = "Plot",
                                            font = ("Verdana", "9", "bold"),
                                            command = self.SpatialPlot)    
        self.SpatialPlot_Button.grid(column = 0, row = 4)
        self.SpatialSave_Button = tk.Button(self.Inputs_Frame,
                                          text = "Export",
                                          font = ("Verdana", "9", "bold"),
                                          command = self.save_file)        
        self.SpatialSave_Button.grid(column = 1, row = 4)
        
        for child in self.Inputs_Frame.winfo_children(): 
            child.grid_configure(padx = 4, pady = 2)             
            
            
    ###########################################################################
    # Spatial Text Box for Explaination
    ###########################################################################
    def Tab3_TextFrame(self):
        self.label_3_2 = ttk.Label(text = "Variable Explanation", 
                                   style = "Bold.TLabel", 
                                   font = ("Verdana", "9", "bold"))  
        self.Inputs_Frame1 = ttk.LabelFrame(self.tab, labelwidget = self.label_3_2)
        self.Inputs_Frame1.grid(column = 0, row = 3, rowspan = 27, 
                              columnspan = 20, sticky = "NS")     

        self.TextExplaination = tk.Text(self.Inputs_Frame1, height = 38, 
                                        width = 62,
                                        font = ("Verdana", "7"))
        
        self.TextExplaination.tag_configure("left", justify='left')
        self.TextExplaination.insert(tk.END, Documentation().SpatialExplanation.__doc__)
        self.TextExplaination.config(state = 'disabled')
        for child in self.Inputs_Frame1.winfo_children(): 
            child.grid_configure(padx = 4, pady = 2)  


    ###########################################################################
    # Spatial Plot
    ###########################################################################
    def SpatialPlot(self):
        self.label_2_2 = ttk.Label(text = "Variable Plot", 
                                   style = "Bold.TLabel", 
                                   font = ("Verdana", "9", "bold"))
        self.SpatialPlot_Frame = ttk.LabelFrame(self.tab, 
                                             labelwidget = self.label_2_2) 
        self.SpatialPlot_Frame.grid(column = 21, 
                                    row = 0, 
                                    rowspan = 30, 
                                    columnspan = 200,
                                    sticky = "NS")
        
        filepath = self.VoronoiName.get("1.0","end-1c")  
        spatialfile = self.SpatialName.get("1.0","end-1c") 
        variable = self.ValueOption_Entry.get()

        
        gdf = VoronoiPolygonPlot(filepath, spatialfile, variable)
        
        self.fig = Figure(figsize=(10, 6), dpi = 100)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.clear()
        
        
        gdf.plot(column = variable, ax = self.ax, legend = False, cmap = 'hot', 
                 edgecolor = 'black', linewidth = 0.1)
        self.ax.set_xlabel('Latitude (UTM)', fontsize = 12, 
                      fontdict = dict(weight = 'bold'))
        self.ax.set_ylabel('Longitude (UTM)', fontsize = 12, 
                      fontdict = dict(weight = 'bold'))
        
        self.ax.set_title("Dynamic Spatial Output Plot", 
                          fontsize = 'large', 
                          fontdict = dict(weight = 'bold'))
        
        mn = gdf[variable].min()
        mx = gdf[variable].max()
        norm = Normalize(vmin = mn, vmax = mx)
        n_cmap = cm.ScalarMappable(norm = norm, cmap = "hot")
        n_cmap.set_array([])
        self.ax.get_figure().colorbar(n_cmap, ax = self.ax, orientation = 'vertical')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.SpatialPlot_Frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column = 0, row = 0)     

           
    ###########################################################################
    # Basin Outlet Inputs
    ###########################################################################
    def Tab5_InputFrame(self):
        self.BasinOutletFile = tk.StringVar()
        self.VariabletoPlot = tk.StringVar()
        
        self.label_1 = ttk.Label(text = "Input", 
                                 style = "Bold.TLabel", 
                                 font = ("Verdana", "9", "bold"))        
        self.Inputs_Frame = ttk.LabelFrame(self.tab, labelwidget = self.label_1)
        self.Inputs_Frame.grid(column = 0, row = 0, rowspan = 30, 
                               columnspan = 20, sticky = "NS")
        self.Inputs_Button = tk.Button(self.Inputs_Frame, 
                                       text = "Browse File",
                                       font = ("Verdana", "9", "bold"),
                                       command = self.loadqoutfile)    
        self.Inputs_Button.grid(column = 0, row = 1)
        self.BasinQoutName = tk.Text(self.Inputs_Frame, 
                                 height = 1, width = 16)
        self.BasinQoutName.grid(column = 1, row = 1)
        self.BasinQoutName.config(state = "normal")      
     
        self.BasinQoutPlot_Button = tk.Button(self.Inputs_Frame,
                                          text = "Plot",
                                          font = ("Verdana", "9", "bold"),
                                          command = self.BasinOutletPlot)
        self.BasinQoutPlot_Button.grid(column = 0, row = 2)
        
        self.BasinQoutPlotSave_Button = tk.Button(self.Inputs_Frame,
                                          text = "Export",
                                          font = ("Verdana", "9", "bold"),
                                          command = self.save_file)
        self.BasinQoutPlotSave_Button.grid(column = 1, row = 2)
        
        

        for child in self.Inputs_Frame.winfo_children(): 
            child.grid_configure(padx = 4, pady = 2) 
            
 
    ###########################################################################
    # Basin Outlet Plot
    ###########################################################################
    def BasinOutletPlot(self):
        self.label_2_2 = ttk.Label(text = "Variable Plot", 
                                   style = "Bold.TLabel", 
                                   font = ("Verdana", "9", "bold"))
        self.BasinPlot_Frame = ttk.LabelFrame(self.tab, 
                                             labelwidget = self.label_2_2) 
        self.BasinPlot_Frame.grid(column = 21, 
                                 row = 0, 
                                 rowspan = 30, 
                                 columnspan = 200,
                                 sticky = "NS")
 
        filepath = self.BasinQoutName.get("1.0","end-1c")       
        df = QoutletData(filepath)
   
        self.fig = Figure(figsize=(10, 6), dpi = 100)
        self.ax = self.fig.add_subplot(1, 1, 1)
        ax2 = self.ax.twinx()
        self.ax.clear()
        ax2.clear()
        for tick in self.ax.yaxis.get_ticklabels():
            tick.set_color('black')
            tick.set_weight('bold')            
        for tick in self.ax.xaxis.get_ticklabels():
            tick.set_color('black')
            tick.set_weight('bold')  
        for tick in ax2.yaxis.get_ticklabels():
            tick.set_fontsize('large')
            tick.set_color('red')
            tick.set_weight('bold')

        plot1 = self.ax.plot(df.index, df['Qstrm'], 'b-')
        plot2 = ax2.plot(df.index, df['HLevel'], 'r-')

     
        self.ax.set_ylabel('Discharge (m^3/s)', color = 'blue', 
                      fontsize = 12, fontdict = dict(weight = 'bold'))
        
        ax2.set_ylabel('Channel Stage (m)', color = 'red', 
                   fontsize = 12, fontdict = dict(weight = 'bold'))
        

        self.ax.set_xlabel('Time (Hour)', fontsize = 12, 
                      fontdict = dict(weight = 'bold'))
 
        xtick = np.arange(df.index.min(), df.index.max(), 5)
        self.ax.set_xticks(xtick, minor = True)
        self.ax.grid(True, which = 'major', axis='y', linewidth = 0.1)
        self.ax.grid(True, which = 'major', axis='x', linewidth = 0.1)
        self.ax.set_title("Basin Outlet Discharge Time Series", 
                          fontsize = 'large', 
                          fontdict = dict(weight = 'bold'))
        Combined = plot1 + plot2
        Labels = [l.get_label() for l in Combined]
        self.ax.legend((plot1[0], plot2[0]),('Discharge (m3s)', 'Channel Stage (m)'), loc='best')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.BasinPlot_Frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column = 0, row = 0)     

        




    ###########################################################################
    # Integrated Spatial Inputs
    ###########################################################################
    def Tab4_InputFrame(self):
        self.SpatialFile = tk.StringVar()
        self.VoronoiFile = tk.StringVar()
        self.VariabletoPlot = tk.StringVar()
        
        
        
        self.label_1 = ttk.Label(text = "Spatial Input", 
                                 style = "Bold.TLabel", 
                                 font = ("Verdana", "9", "bold"))        
        self.Inputs_Frame = ttk.LabelFrame(self.tab, labelwidget = self.label_1)
        self.Inputs_Frame.grid(column = 0, row = 0, rowspan = 3, 
                               columnspan = 20, sticky = "NS")
        
        
        self.VoronoiInputs_Button1 = tk.Button(self.Inputs_Frame, 
                                               text = "Browse voi File",
                                               font = ("Verdana", "9", "bold"),
                                               command = self.loadvoifile)
        self.VoronoiInputs_Button1.grid(column = 0, row = 1)        
        self.VoronoiName = tk.Text(self.Inputs_Frame, 
                                   height = 1, width = 28)
        self.VoronoiName.grid(column = 1, row = 1)
        
   
        self.SpatialInputs_Button2 = tk.Button(self.Inputs_Frame, 
                                               text = "Browse 00i File",
                                               font = ("Verdana", "9", "bold"),
                                               command = self.loadintegratedspatialfile)
        self.SpatialInputs_Button2.grid(column = 0, row = 2)        
        self.SpatialName = tk.Text(self.Inputs_Frame, 
                                   height = 1, width = 28)
        self.SpatialName.grid(column = 1, row = 2)
        
        ttk.Label(self.Inputs_Frame, 
                  text = "Variable to Plot",
                  justify = "center", 
                  font = ("Verdana", "9", "bold")).grid(column = 0, row = 3)  

        Options = [' BndCd', 'Z', 'VAr', 'CAr', 'Curv', 'EdgL', 'tan(Slp)', 
                   'FWidth', 'Aspect', 'SV', 'LV', 'AvSM', 'AvRtM', 'HOccr', 'HRt', 
                   'SbOccr', 'SbRt', 'POccr', 'PRt', 'SatOccr', 'SatRt', 
                   'SoiSatOccr', 'RchDsch', 'AveET', 'EvpFrct', 'cLHF', 
                   'cMelt', 'cSHF', 'cPHF', 'cRLIn', 'cRLo', 
                   'cRSIn', 'cGHF', 'cUErr', 'cHrsSun', 'cHrsSnow', 'persTime', 
                   'peakWE', 'peakTime', 'initTime', 'cIntSub', 'cintUnl', 
                   'AvCanStorParam', 'AvIntercCoeff', 'AvTF', 'AvCanFieldCap',
                   'AvDrainCoeff', 'AvDrainExpPar', 'AvLUAlb', 'AvVegHeight', 
                   'AvOTCoeff', 'AvStomRes', 'AvVegFract', 'AvLeafAI']
    
        self.ValueOption_Entry = ttk.Combobox(self.Inputs_Frame,
                                              state = "readonly",
                                              textvariable = self.VariabletoPlot,
                                              values = Options)
        self.ValueOption_Entry.config(width = 16)
        self.ValueOption_Entry.grid(column = 1, row = 3)
        

        
        
        self.SpatialPlot_Button = tk.Button(self.Inputs_Frame,
                                            text = "Plot",
                                            font = ("Verdana", "9", "bold"),
                                            command = self.IntegratedSpatialPlot)    
        self.SpatialPlot_Button.grid(column = 0, row = 4)
        self.SpatialSave_Button = tk.Button(self.Inputs_Frame,
                                          text = "Export",
                                          font = ("Verdana", "9", "bold"),
                                          command = self.save_file)        
        self.SpatialSave_Button.grid(column = 1, row = 4)
        
        for child in self.Inputs_Frame.winfo_children(): 
            child.grid_configure(padx = 4, pady = 2)             
            
            
    ###########################################################################
    # Spatial Text Box for Explaination
    ###########################################################################
    def Tab4_TextFrame(self):
        self.label_4_2 = ttk.Label(text = "Variable Explanation", 
                                   style = "Bold.TLabel", 
                                   font = ("Verdana", "9", "bold"))  
        self.Inputs_Frame1 = ttk.LabelFrame(self.tab, labelwidget = self.label_4_2)
        self.Inputs_Frame1.grid(column = 0, row = 3, rowspan = 27, 
                              columnspan = 20, sticky = "NS")     

        self.TextExplaination = tk.Text(self.Inputs_Frame1, height = 38, 
                                        width = 62,
                                        font = ("Verdana", "7"))
        
        self.TextExplaination.tag_configure("left", justify='left')
        self.TextExplaination.insert(tk.END, Documentation().IntegratedSpatialExplanation.__doc__)
        self.TextExplaination.config(state = 'disabled')
        for child in self.Inputs_Frame1.winfo_children(): 
            child.grid_configure(padx = 4, pady = 2)  


    ###########################################################################
    # Integrated Spatial Plot
    ###########################################################################
    def IntegratedSpatialPlot(self):
        self.label_2_2 = ttk.Label(text = "Variable Plot", 
                                   style = "Bold.TLabel", 
                                   font = ("Verdana", "9", "bold"))
        self.SpatialPlot_Frame = ttk.LabelFrame(self.tab, 
                                             labelwidget = self.label_2_2) 
        self.SpatialPlot_Frame.grid(column = 21, 
                                    row = 0, 
                                    rowspan = 30, 
                                    columnspan = 200,
                                    sticky = "NS")
        
        filepath = self.VoronoiName.get("1.0","end-1c")  
        spatialfile = self.SpatialName.get("1.0","end-1c") 
        variable = self.ValueOption_Entry.get()

        
        gdf = IntegratedPlot(filepath, spatialfile, variable)
        
        self.fig = Figure(figsize=(10, 6), dpi = 100)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.clear()
        
        
        gdf.plot(column = variable, ax = self.ax, legend = False, cmap = 'hot', 
                 edgecolor = 'black', linewidth = 0.1)
        self.ax.set_xlabel('Latitude (UTM)', fontsize = 12, 
                      fontdict = dict(weight = 'bold'))
        self.ax.set_ylabel('Longitude (UTM)', fontsize = 12, 
                      fontdict = dict(weight = 'bold'))
        
        self.ax.set_title("Integrated Spatial Output Plot", 
                          fontsize = 'large', 
                          fontdict = dict(weight = 'bold'))
        
        mn = gdf[variable].min()
        mx = gdf[variable].max()
        norm = Normalize(vmin = mn, vmax = mx)
        n_cmap = cm.ScalarMappable(norm = norm, cmap = "hot")
        n_cmap.set_array([])
        self.ax.get_figure().colorbar(n_cmap, ax = self.ax, orientation = 'vertical')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.SpatialPlot_Frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column = 0, row = 0)     








    ###########################################################################
    # Get Pixel file from .pixel
    ###########################################################################
    def loadpixelfile(self):
        fname = filedialog.askopenfilename(initialdir = "/",
                                           title = "Select file", 
                                           filetypes = (("Pixel file","*.pixel"), 
                                                        ("All files","*.*")))
        self.PixelName.delete(1.0, "end")
        self.PixelName.insert(1.0, fname) 
    ###########################################################################
    # Get Basin file from .mrf
    ###########################################################################   
    def loadbasinfile(self):
        fname = filedialog.askopenfilename(initialdir = "/",
                                           title = "Select file", 
                                           filetypes = (("Basin Avg file","*.mrf"), 
                                                        ("All files","*.*")))
        self.BasinName.delete(1.0, "end")
        self.BasinName.insert(1.0, fname)           
    ###########################################################################
    # Get qout file from .qout
    ###########################################################################   
    def loadqoutfile(self):
        fname = filedialog.askopenfilename(initialdir = "/",
                                           title = "Select file", 
                                           filetypes = (("Outlet Discharge file","*_Outlet.qout"), 
                                                        ("All files","*.*")))
        self.BasinQoutName.delete(1.0, "end")
        self.BasinQoutName.insert(1.0, fname)        
    ###########################################################################
    # Get voi file from _voi
    ###########################################################################   
    def loadvoifile(self):
        fname = filedialog.askopenfilename(initialdir = "/",
                                           title = "Select file", 
                                           filetypes = (("Voronoi vertices","*_voi"), 
                                                        ("All files","*.*")))
        self.VoronoiName.delete(1.0, "end")
        self.VoronoiName.insert(1.0, fname)           
    ###########################################################################
    # Get spatial file from _00d
    ###########################################################################   
    def loadspatialfile(self):
        fname = filedialog.askopenfilename(initialdir = "/",
                                           title = "Select file", 
                                           filetypes = (("Spatial file","*_00d"), 
                                                        ("All files","*.*")))
        self.SpatialName.delete(1.0, "end")
        self.SpatialName.insert(1.0, fname)     
    ###########################################################################
    # Get spatial file from _00i
    ###########################################################################   
    def loadintegratedspatialfile(self):
        fname = filedialog.askopenfilename(initialdir = "/",
                                           title = "Select file", 
                                           filetypes = (("Spatial file","*_00i"), 
                                                        ("All files","*.*")))
        self.SpatialName.delete(1.0, "end")
        self.SpatialName.insert(1.0, fname)     
    ###########################################################################
    # Save command
    ###########################################################################
    def save_file(self):
        fname = filedialog.asksaveasfilename(title = "Save as",
                                             filetypes = (("PNG files (.png)", "*.png"),
                                                          ("JPEG files (.jpg)", "*.jpg"),
                                                          ("All files", "*.*"),
                                                          ('pdf file', '*.pdf')),
                                                          defaultextension = ".pdf")
        self.fig.savefig(fname, dpi = 300)










































###############################################################################
###############################################################################
class VisualtRIBSGUI():
    # Initializer method
    def __init__(self):         
        # Software Title
        # Create instance
        self.window = tk.Tk()  
        self.window.style = ttk.Style()
        #self.window.style.theme_use("clam") 
        # Define Resolution
        self.window.geometry('1400x680')
        # Allow resizing
        self.window.resizable(True, True)
        # Add software name
        self.window.title(Documentation.Title.__doc__)
        # Add menu bar
        MenuBar(self.window).create_menubar()
        # Add Tab
        TabCreation(self.window).create_tabs()
     
def main(): 
    oop = VisualtRIBSGUI()
    oop.window.mainloop()

if __name__ == '__main__':
    main()       
        
        















































