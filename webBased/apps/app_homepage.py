#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 13:33:55 2020

@author: tpham
"""

from shapely.geometry import Polygon
import geopandas as gpd
import dash
import base64
import io
import json
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
###############################################################################
# Setting the dashboard                                                       #
###############################################################################
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)


mapbox_access_token = "pk.eyJ1IjoicGhhbTk1IiwiYSI6ImNrNnB5aDMwZTFwYmwzbG83NmFvYXdncTgifQ.SGeZeoKIsPalUdyPzARNEg"

server = app.server

###############################################################################
# HTML layout functions
###############################################################################
# Top Panel
def build_banner():
    return html.Div(
        id="banner",
        className="twelve columns",   
        style = {'margin-bottom': '30px',
                 'margin-top': '20px',
                 'textAlign': 'center',
        },
        children=[
            html.H1("tRIBS OUTPUT VISUALIZATION"),
        ],
    )


def create_button():
    return html.Div(
        id='Button',
        className='row flex-display',
        children=[
            html.Div(
                [html.A(
                    html.Button("Serial Dynamic Spatial (_00d)", id = "b1"),
                        href="/app_serial_dynamic",
                )],
                id = "button1",
                style={'margin-bottom': '30px',
                       'width': '350px',
                       'verticalAlign': 'middle',
                       'textAlign': 'center',
                       'marginLeft': '10px',
                       'display': 'inline-block'
                       },
            ),
            html.Div(
                [html.A(
                    html.Button("Parallel Dynamic Spatial (_00d.#)", id = "b2"),
                        href="/app_parallel_dynamic",
                )],
                id = "button2",
                style={'margin-bottom': '30px',
                       'width': '350px',
                       'verticalAlign': 'middle',
                       'textAlign': 'center',
                       'marginLeft': '10px',
                       'display': 'inline-block'
                       },
            ),
            html.Div(
                [html.A(
                    html.Button("Serial Integrated Spatial (_00i)", id = "b3"),
                        href="/app_serial_integrated",
                )],
                id = "button3",
                style={'margin-bottom': '30px',
                       'width': '350px',
                       'verticalAlign': 'middle',
                       'textAlign': 'center',
                       'marginLeft': '10px',
                       'display': 'inline-block'
                       },
            ),
            html.Div(
                [html.A(
                    html.Button("Parallel Integrated Spatial (_00i.#)", id = "b4"),
                        href="/app_parallel_integrated",
                )],
                id = "button4",
                style={'margin-bottom': '30px',
                       'width': '350px',
                       'verticalAlign': 'middle',
                       'textAlign': 'center',
                       'marginLeft': '10px',
                       'display': 'inline-block'
                       },
            ),
        ],
        style={'margin-bottom': '30px',               
               'verticalAlign': 'middle',
               'textAlign': 'center',
       },
    )


def create_button2():
    return html.Div(
        id='Button1_1',
        className='row flex-display',
        children=[
            html.Div(
                [html.A(
                    html.Button("My GitHub", id = "b1_1"),
                        href="https://github.com/pham2974",
                )],
                id = "button2a",
                style={'margin-bottom': '30px',
                       'width': '350px',
                       'verticalAlign': 'middle',
                       'textAlign': 'center',
                       'marginLeft': '10px',
                       'display': 'inline-block'
                       },
            ),
            html.Div(
                [html.A(
                    html.Button("My Linkedin", id = "b2_2"),
                        href="https://www.linkedin.com/in/tripham95/",
                )],
                id = "button2_2",
                style={'margin-bottom': '30px',
                       'width': '350px',
                       'verticalAlign': 'middle',
                       'textAlign': 'center',
                       'marginLeft': '10px',
                       'display': 'inline-block'
                       },
            ),
            html.Div(
                [html.A(
                    html.Button("Research Group", id = "b3_3"),
                        href="http://moreno.oucreate.com/index.html",
                )],
                id = "button3_3",
                style={'margin-bottom': '30px',
                       'width': '350px',
                       'verticalAlign': 'middle',
                       'textAlign': 'center',
                       'marginLeft': '10px',
                       'display': 'inline-block'
                       },
            ),
            html.Div(
                [html.A(
                    html.Button("Affiliate", id = "b4_4"),
                        href="http://www.ou.edu/okh2o",
                )],
                id = "button4_4",
                style={'margin-bottom': '30px',
                       'width': '350px',
                       'verticalAlign': 'middle',
                       'textAlign': 'center',
                       'marginLeft': '10px',
                       'display': 'inline-block'
                       },
            ),
        ],
        style={'margin-bottom': '30px',               
               'verticalAlign': 'middle',
               'textAlign': 'center',
       },
    )



###############################################################################
# App Layout
###############################################################################                
layout = html.Div(    
    id="Main Container",
    children=[
        build_banner(),
        create_button(),
        create_button2(),
    ]        
)


# Main
if __name__ == "__main__":
    app.run_server(debug=True)

