# -*- coding: utf-8 -*-

"""
Created on Thu Jun 30 16:22:10 2022

@author: THINKPAD
"""
import folium
#import geopandas as gpd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import plotly.express as px
import pandas as pd
import pymysql
from datetime import datetime
import numpy as np
import copy

# Access to the RDS Database 
Host = "dron911db.cdu0yrrytj1w.us-east-1.rds.amazonaws.com"
User = "Dron911DB"
ID = "Dron911DB"
Password = "FOuND1y+Me7iK8"
Port = 3306

#
DB = pymysql.connect(host = Host, password = Password, user = User, port = Port)
cursor = DB.cursor()
cursor.execute('''USE Client_Emission_Call''')

# Query to get geolocatization data 
SQL2 = " SELECT * FROM Client_Emission_Call_Table"
df = pd.read_sql(SQL2,DB)

# Order df by index 
df = df.sort_index(ascending = False)

# Create map to show position
m = folium.Map(location=[df.iloc[0]['Latitude'],df.iloc[0]['Longitude']], zoom_start=18)

# Add markers
tooltip = "Haz clic"
folium.Marker([df.iloc[0]['Latitude'],df.iloc[0]['Longitude']], popup="<i>Estoy aqui</>",  
              icon=folium.Icon(color='red', icon='info-sign')).add_to(m)

# Save map
m.save('Geolocalización.html')

# Create the Dash app
#app = dash.Dash(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
#CONTENT_STYLE = {
#    "margin-left": "18rem",
#    "margin-right": "2rem",
#    "padding": "2rem 1rem",
#}

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "Filters", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

#content = html.Div(id="page-content", style=CONTENT_STYLE)

#app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

# Set up the layout using an overall div
app.layout = html.Div(children=[
    sidebar,
    html.H1(children='Localization Tracking'),
    html.Iframe(id = 'map', srcDoc = open('Geolocalización.html', 'r').read(), 
                width = '100%', height = '600')
])


if __name__ == '__main__':
    app.run_server(debug=True)
