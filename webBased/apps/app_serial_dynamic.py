#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 13:33:55 2020

@author: tpham
"""

from shapely.geometry import Polygon
import geopandas as gpd
import base64
import io
import json
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from app import app
###############################################################################
# Setting the dashboard                                                       #
###############################################################################
mapbox_access_token = "pk.eyJ1IjoicGhhbTk1IiwiYSI6ImNrNnB5aDMwZTFwYmwzbG83NmFvYXdncTgifQ.SGeZeoKIsPalUdyPzARNEg"


###############################################################################
# HTML layout functions
###############################################################################
# Top Panel
def build_banner():
    return html.Div(
        id="banner",
        className="twelve columns",   
        style = {'margin-bottom': '0px',
                 'textAlign': 'center',
        },
        children=[
            html.H2("SERIAL DYNAMIC FILE VISUALIZATION"),
        ],
    )
                
###############################################################################
# Main graph
###############################################################################
def main_graph():   
    return html.Div(
        id='main_graph',
        className="row flex-display",
        children=[
            html.Div(
                id='main-table',
                className='three columns',
                children=[
                    # Left top bar with table title
                    html.Div(
                        className='row chart-top-bar',
                        id='table-title-row',
                        children=[
                            html.Span(
                                id='table-title',
                                children=[
                                    html.H5('File Upload'),   
                                ],
                                style={'margin-bottom': '30px',
                                       'textAlign': 'center',
                                },
                            ),
                        ],
                        style={'marginLeft': '10px',
                               'height':'40px',
                       },
                    ),
                    # Container to upload file
                    html.Div(
                        className='row chart-top-bar',
                        id='upload',
                        children=[
                            html.Span(
                                id='files-upload-1',
                                children=[
                                    html.H6('Voronoi File (_voi)'),   
                                ],
                                style={'margin-bottom': '30px',
                                       'textAlign': 'center',
                                },
                            ),
                            # Upload voronoi polygon file
                            html.Div(
                                dcc.Upload(
                                    id='upload-voronoi',
                                    children=[
                                        html.Div(
                                            ['Drag and Drop or ',
                                             html.A('Select File')
                                            ],
                                        ),
                                    ],
                                    style={
                                        'height': '60px',
                                        'lineHeight': '60px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'dashed',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                        'marginLeft': '10px'
                                    },
                                    multiple=False,
                                ),
                            ),
                            html.Span(
                                id='files-upload-2',
                                children=[
                                    html.H6('Dynamic Spatial File (_00d)'),   
                                ],
                                style={'margin-bottom': '30px',
                                       'textAlign': 'center',
                                },
                            ),
                            # Upload integrated file
                            html.Div(
                                dcc.Upload(
                                    id='upload-integrated',
                                    children=[
                                        html.Div(
                                            ['Drag and Drop or ',
                                             html.A('Select File')
                                            ],
                                        ),
                                    ],
                                    style={
                                        'height': '60px',
                                        'lineHeight': '60px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'dashed',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                        'marginLeft': '10px',
                                    },
                                    multiple=False,
                                ),
                            ),
                            # Choosing variables
                            html.Span(
                                id='variable',
                                children=[
                                    html.H6('Variable'),   
                                ],
                                style={'margin-bottom': '30px',
                                       'textAlign': 'center',
                                },
                            ),
                            # Variable Options
                            html.Div(
                                dcc.Dropdown(
                                    className='inline-display',
                                    id='variable-options',
                                    children='color-bar',
                                    options=[
                                        # Color bar
                                        {"label": "1. Elevation [m]", "value": "Z"},
                                        {"label": "2. Slope [radian]", "value": "S"},
                                        {"label": "3. Area [m2]", "value": "CAr"},
                                        {"label": "4. Groundwater Depth [mm]", "value": "Nwt"},
                                        {"label": "5. Moisture Above Water Table [mm]", "value": "Mu"},
                                        {"label": "6. Initialization Moisture [mm]", "value": "Mi"},
                                        {"label": "7. Wetting Front Depth [mm]", "value": "Nf"},
                                        {"label": "8. Top Front Depth [mm]", "value": "Nt"},
                                        {"label": "9. Unsaturated Lateral Flow Out [mm.hr-1]", "value": "Qpout"},
                                        {"label": "10. Unsaturated Lateral Flow In [mm.hr-1]", "value": "Qpin"},
                                        {"label": "11. Surface Runoff [mm]", "value": "Srf"},
                                        {"label": "12. Precipitation [mm.hr-1]", "value": "Rain"},
                                        {"label": "13. Snow Water Equivalent [cm]", "value": "SWE"},
                                        {"label": "14. Snow Temperature [C]", "value": "ST"},
                                        {"label": "15. Ice Part of Water Equivalent [cm]", "value": "IWE"},
                                        {"label": "16. Liquid part of Water Equivalent [cm]", "value": "LWE"},
                                        {"label": "17. Change in Energy of Snow [kW.m-2]", "value": "DU"},
                                        {"label": "18. Internal Energy of Snow [kJ.m-2]", "value": "Upack"},
                                        {"label": "19. Latent Heat Flux from Snow [kJ.m-2]", "value": "sLHF"},
                                        {"label": "20. Sensible Heat Flux Snow [kJ.m-2]", "value": "sSHF"},
                                        {"label": "21. Ground Heat Flux Snow [kJ.m-2]", "value": "sGHF"},
                                        {"label": "22. Precip Heat Flux Snow [kJ.m-2]", "value": "sPHF"},
                                        {"label": "23. Longwave Rad Snow Out [kJ.m-2]", "value": "sRLo"},
                                        {"label": "24. Longwave Rad Snow In [kJ.m-2]", "value": "sRLi"},
                                        {"label": "25. Shortwave Rad Snow In [kJ.m-2]", "value": "sRSi"},
                                        {"label": "26. Error in Energy Balance [J.m-2]", "value": "Uerr"},
                                        {"label": "27. Intercepted SWE [cm]", "value": "IntSWE"},
                                        {"label": "28. Sublimated Snow from Canopy [cm]", "value": "IntSub"},
                                        {"label": "29. Unloaded Snow from Canopy [cm]", "value": "IntUnl"},
                                        {"label": "30. 10-cm Soil Moisture []", "value": "SoilMoist"},
                                        {"label": "31. 100-cm Soil Moisture []", "value": "RootMoist"},
                                        {"label": "32. Canopy Storage [mm]", "value": "CanStorage"},
                                        {"label": "33. Actual Evaporation [mm.hr-1]", "value": "ActEvp"},
                                        {"label": "34. Bare Soil Evaporation [mm.hr-1]", "value": "EvpSoil"},
                                        {"label": "35. Total Evapotranspiration [mm.hr-1]", "value": "ET"},
                                        {"label": "36. Ground Heat Flux [W.m-2]", "value": "Gflux"},
                                        {"label": "37. Sensible Heat Flux [W.m-2]", "value": "Hflux"},
                                        {"label": "38. Latent Heat Flux [W.m-2]", "value": "Lflux"},
                                        {"label": "39. Discharge [m3.s-1]", "value": "Qstrm"},
                                        {"label": "40. Channel Stage [m]", "value": "Hlev"},
                                        {"label": "41. Flow Velocity [m.s-1]", "value": "FlwVlc"},
                                        {"label": "42. Canopy Storage Param [mm]", "value": "CanStorParam"},
                                        {"label": "43. Interception Coeffcient []", "value": "IntercepCoeff"},
                                        {"label": "44. Throughfall Coeffcient []", "value": "Rutter, ThroughFall"},
                                        {"label": "45. Canopy Capacity [mm]", "value": "Rutter, CanFieldCap"},
                                        {"label": "46. Drainage Coefficient [mm.hr-1]", "value": "Rutter, DrainCoeff"},
                                        {"label": "47. Drainage Exp Parameter [mm-1]", "value": "Rutter, DrainExpPar"},
                                        {"label": "48. Albedo []", "value": "LandUseAlb"},
                                        {"label": "49. Vegetation Height [m]", "value": "VegHeight"},
                                        {"label": "50. Optical Transmission []", "value": "OptTransmCoeff"},
                                        {"label": "51. Stomatal Resistance [s.m-1]", "value": "StomRes"},
                                        {"label": "52. Vegetation Fraction []", "value": "VegFraction"},
                                        {"label": "53. Leaf Area Index []", "value": "LeafAI"},                                            
                                        ],
                                        value='Z',
                                        clearable=False,
                                        style={'width': '295px',
                                               'height':'40px',
                                               'verticalAlign': 'middle',
                                               'marginLeft': '10px',
                                               'display': 'inline-display',
                                               
                                        },
                                ),                                        
                            ),
                                                        # Choosing variables
                            html.Span(
                                id='UTM-Zone',
                                children=[
                                    html.H6('UTM Zone'),   
                                ],
                                style={'margin-bottom': '30px',
                                       'textAlign': 'center',
                                },
                            ),
                            # Variable Options
                            html.Div(
                                dcc.Dropdown(
                                    className='inline-display',
                                    id='UTM-options',
                                    children='color-bar',
                                    options=[
                                        # Color bar
                                        {"label": "1. UTM Zone 10N", "value": "EPSG:26910"},
                                        {"label": "2. UTM Zone 11N", "value": "EPSG:26911"},
                                        {"label": "3. UTM Zone 12N", "value": "EPSG:26912"},
                                        {"label": "4. UTM Zone 13N", "value": "EPSG:26913"},
                                        {"label": "5. UTM Zone 14N", "value": "EPSG:26914"},
                                        {"label": "6. UTM Zone 15N", "value": "EPSG:26915"},
                                        {"label": "7. UTM Zone 16N", "value": "EPSG:26916"},
                                        {"label": "8. UTM Zone 17N", "value": "EPSG:26917"},
                                        {"label": "9. UTM Zone 18N", "value": "EPSG:26918"},
                                        {"label": "10. UTM Zone 19N", "value": "EPSG:26919"},

                                          
                                        ],
                                        value='EPSG:26915',
                                        clearable=False,
                                        style={'width': '295px',
                                               'height':'40px',
                                               'verticalAlign': 'middle',
                                               'marginLeft': '10px',
                                               'display': 'inline-display',
                                               
                                        },
                                ),                                        
                            ),            
                                        
                            
                            # External Link
                            html.Span(
                                id='External-link-title',
                                children=[
                                    html.H6('Reset'),   
                                ],
                                style={'margin-bottom': '30px',
                                       'textAlign': 'center',
                                },
                            ),
                            # Reset Button
                            html.Div(
                                [html.Button(
                                    children='Reset',
                                    id='reset_button', 
                                    n_clicks=0),
                                ],                                
                                id = "button1",
                                style={'margin-bottom': '30px',
                                       'width': '300px',
                                       'verticalAlign': 'middle',
                                       'textAlign': 'center',
                                       'marginLeft': '10px',
                                },
                            ),
                        ],
                        style={'marginLeft': '10px',
                               'height': '695px',
                               'backgroundColor': '#21252C',
                        },
                    
                    ),
                ],
            ),
            html.Div(
                id='main-map',
                className='nine columns',
                children=[
                    html.Div(
                        className='row chart-top-bar',
                        id='options',
                        children=[
                            html.Span(
                                id="Input",
                                className="graph-top-left inline-block",
                                children=[
                                    # Top left
                                    html.Div(
                                        dcc.Dropdown(
                                            className='dropdown-period',
                                            id='color-scale',
                                            children='color-bar',
                                            options=[
                                                # Color bar
                                                {"label": "Red-Blue", "value": "rdbu"},
                                                {"label": "HSV", "value": "hsv"},
                                                {"label": "Thermal", "value": "thermal"},
                                                {"label": "Earth", "value": "earth"},
                                                {"label": "Viridis", "value": "viridis"},
                                                {"label": "Solar", "value": "solar"},
                                                {"label": "Tempo", "value": "tempo"},
                                                {"label": "Sunset", "value": "sunset"},
                                                {"label": "Hot", "value": "hot"},
                                                {"label": "YlGnBl", "value": "ylgnbu"},
                                                {"label": "Balance", "value": "balance"},   
                                            ],
                                            value='rdbu',
                                            clearable=False,
                                            style={'width': '150px',
                                                   'height':'40px',},
                                        ),                                        
                                    ),
                                ], 
                                #n_clicks=0,
                                style={'display': 'inline-block',
                                },
                            ),
                            # Top right
                            html.Div(
                                className='graph-top-right inline-block',
                                children=[
                                    html.Div(
                                        className='inline-block',
                                        children=[
                                            dcc.Dropdown(
                                                className='inline-display',
                                                id='mapbox-view-selector',
                                                children='Map Type',
                                                options=[
                                                    {"label": "Outdoor", "value": "outdoors"},
                                                    {"label": "Satellite", "value": "satellite"},
                                                    {"label": "Open-Street", "value": "open-street-map"},
                                                    {"label": "Street",
                                                     "value": "mapbox://styles/mapbox/satellite-streets-v9",
                                                    },
                                                ],
                                                value='outdoors',
                                                clearable=False,
                                                style={'width': '150px',
                                                       'height':'40px',},
                                            ),
                                        ],
                                    ),
                                    
                                ],
                                style={'display': 'inline-block',
                                       'marginLeft': '0px'
                                },
                            ),
                            # Basin Plot
                            html.Div(
                                #className="eight columns",
                                children=[
                                    # Time series graph
                                    dcc.Graph(
                                        id='integrated-basin3',
                                        #className="eight columns",
                                        figure={
                                            'layout': {'plot_bgcolor': '#21252C',
                                            'paper_bgcolor': '#21252C',
                                            },                          
                                        },
                                        config={"scrollZoom": True, 
                                                "displayModeBar": True
                                        },
                                        style={'height':'710px',
                                        },
                                    ),
                                ],  
                                style={'marginLeft': '0px', 
                                       'marginRight': '0px',
                                       'margin-top': '10px',
                                       'margin-bottom': '0px'}
                                ),
                        ],  
                    ),                    
                ],
                style={'display': 'inline-block',
                       'marginLeft': '10px',
                },
            ), 
        ],      
    )             


###############################################################################
# App Layout
###############################################################################                
layout = html.Div(    
    id="Main Container",
    children=[
        build_banner(),
        main_graph(),
    ]        
)


###############################################################################
# Variable header
###############################################################################
Headers = ['id', 'Z', 'S', 'CAr', 'Nwt', 'Mu', 'Mi', 'Nf', 'Nt', 'Qpout', 
           'Qpin', 'Srf', 'Rain', 'SWE', 'ST', 'IWE', 'LWE', 'DU', 'Upack', 
           'sLHF', 'sSHF', 'sGHF', 'sPHF', 'sRLo', 'sRLi', 'sRSi', 'Uerr', 
           'IntSWE', 'IntSub', 'IntUnl', 'SoilMoist', 'RootMoist', 
           'CanStorage', 'ActEvp', 'EvpSoil', 'ET', 'Gflux', 'Hflux', 'Lflux',
           'Qstrm', 'Hlev', 'FlwVlc', 'CanStorParam', 'IntercepCoeff',
           'Rutter, ThroughFall', 'Rutter, CanFieldCap', 'Rutter, DrainCoeff',
           'Rutter, DrainExpPar', 'LandUseAlb', 'VegHeight',
           'OptTransmCoeff', 'StomRes', 'VegFraction', 'LeafAI']



###############################################################################
# Functions
###############################################################################
# Parse voronoi file
def parse_voronoi_file(contents, filename):
    content_type, content_string = contents.split(',')
    #content_type, content_string = contents[0].split(',')
    decoded = base64.b64decode(content_string)
    
    voronoi_file = io.StringIO(decoded.decode('utf-8'))
    
    if '_voi' in filename:
        voronoivertices = voronoi_file.readlines()
        voronoivertices = [x.strip().split(",") for x in voronoivertices]
        
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
    
        return polygon_list
    else:
        raise PreventUpdate
        
                

# Parse integrated file
def parse_integrated_file(contents, filename):
    content_type, content_string = contents.split(',')
    #content_type, content_string = contents[0].split(',')
    decoded = base64.b64decode(content_string)
    integrated_file = io.StringIO(decoded.decode('utf-8'))

    if '_00d' in filename:
        data = integrated_file.readlines()
        data = [x.strip().split(",") for x in data]
        data.insert(0, Headers)
        integrated_data = pd.DataFrame(data[1:], 
                                       columns = data[0]).set_index('id')
        integrated_data.index = pd.to_numeric(integrated_data.index, 
                                              errors = 'coerce')
        
        return integrated_data
          
    else:
        raise PreventUpdate
        

# Merging voronoi and integrated
def merging_voronoi_integrated(voronoi, integrated, UTM_Zone):
    gdf = gpd.GeoDataFrame(integrated, geometry = voronoi)
    # Setting projections
    gdf.crs =  UTM_Zone
    # Reprojecting geodataframe
    gdf = gdf.to_crs("EPSG:4326")

    gdf_json = gdf.to_json()

    gdf_final = json.loads(gdf_json)

    i=1
    for feature in gdf_final["features"]:
        feature ['id'] = str(i).zfill(2)
        i += 1  
        
    return gdf_final
    

    

###############################################################################
# App callback
###############################################################################
# Original Map
@app.callback(
        Output(component_id='integrated-basin3', component_property='figure'),
        [Input(component_id='mapbox-view-selector',component_property='value'),
         # Voronoi file component
         Input(component_id='upload-voronoi',component_property='filename'),
         Input(component_id='upload-voronoi',component_property='contents'),
         # Integrated file component
         Input(component_id='upload-integrated',component_property='filename'),
         Input(component_id='upload-integrated',component_property='contents'),
         # Variable to plot component
         Input(component_id='variable-options',component_property='value'),
         # Color scale component
         Input(component_id='color-scale',component_property='value'),
         # UTM Zone
         Input(component_id='UTM-options',component_property='value'),
         Input(component_id='reset_button',component_property='n_clicks'),],
        #[State(component_id='upload-voronoi', component_property='filename'),
         #State(component_id='upload-voronoi',component_property='contents'),
         #State(component_id='upload-integrated', component_property='filename'),
         #State(component_id='upload-integrated',component_property='contents'),],       
)
def Update_Main_Map(style, filename_voronoi, contents_voronoi,  
                    filename_integrated, contents_integrated,
                    variable, color_scale, UTM_Option, n_clicks):
    # Setting up the layout
    layout = dict(
            clickmode="event+select",
            autosize = True,
            automargin = True,
            margin = dict(l = 0, r = 0, b = 0, t = 0),
            hovermode = "closest",
            plot_bgcolor = "#21252C",
            paper_bgcolor = "#21252C",
            #legend = dict(font = dict(size = 10), orientation = "h"),
            showlegend = False,
            #title = "MAP",
            mapbox = dict(
                    accesstoken = mapbox_access_token,
                    style = style,
                    center = dict(lat=35.2226, lon=-97.4395),
                    zoom = 4,
                    pitch=0,
                    ),
            )
    # Add Placeholder Data
    data =[]
    placeholder_data = go.Scattermapbox(
            lat=['36.084621'],
            lon=['-96.921387'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                    size=0,
                    color='blue',
                    opacity=0.7),
                    #name = 'Bacteria Sampling',
                    hoverinfo='text')
    data.append(placeholder_data)
    
    
    
    if contents_voronoi and contents_integrated:

        # Processing voronoi data
        voronoi_file = parse_voronoi_file(contents_voronoi, 
                                          filename_voronoi)
        #polygon_list = process_voronoi(voronoi_file)
        # Processing integrated file
        integrated_file = parse_integrated_file(contents_integrated,
                                                filename_integrated)
        #spatial_data = process_integrated_file(integrated_file)
        # Merging voronoi and spatial data
        gdf = merging_voronoi_integrated(voronoi_file, integrated_file, UTM_Option)
        
        # Create locatons
        locations = [i['id'] for i in gdf['features']]
        
        # Get variables
        z = [i['properties'][variable] for i in gdf['features']]
        
        spatialplotdata = go.Choroplethmapbox(geojson=gdf, 
                                    locations=locations, 
                                    z=z,
                                    colorscale=color_scale, 
                                    marker_opacity=0.70, 
                                    marker_line_width=0,
                                    name = variable,
                                    text = locations,
                                    hovertemplate='Node ID: %{text} <br>Value: %{z}')
        
        data.append(spatialplotdata)
        
        if n_clicks > 0:
            del contents_voronoi
            del contents_integrated

            n_clicks = None
    
    
    # Return Dict for Figure
    figure = {'data': data,'layout': layout}    
    return figure




