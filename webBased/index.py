#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 12:42:44 2020

@author: tpham
"""
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from app import server
from apps import app_homepage, app_serial_dynamic, app_serial_integrated, app_parallel_dynamic, app_parallel_integrated





###############################################################################
# App Layout
###############################################################################                
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):            
    if pathname == '/':
        return app_homepage.layout
    elif pathname == '/app_serial_dynamic':
        return app_serial_dynamic.layout
    elif pathname == '/app_serial_integrated':
        return app_serial_integrated.layout
    elif pathname == '/app_parallel_dynamic':
        return app_parallel_dynamic.layout
    elif pathname == '/app_parallel_integrated':
        return app_parallel_integrated.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
