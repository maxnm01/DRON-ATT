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
from datetime import date
import numpy as np
import copy

# Access to the RDS Database 
Host = "Hostname"
User = "Username"
ID = "ID"
Password = "password"
Port = 

#
DB = pymysql.connect(host = Host, password = Password, user = User, port = Port)
cursor = DB.cursor()
cursor.execute('''USE Client_Emission_Call''')

# Query to get geolocatization data 
SQL2 = " SELECT * FROM Client_Emission_Call_Table"
df = pd.read_sql(SQL2,DB)

# Order df by index 
df = df.sort_index(ascending = False)

#Fix 5G Innovation Lab location
cdmx = [19.390519,-99.4238064]

# Create map to show position
m = folium.Map(cdmx, zoom_start=5)

# Add markers
#tooltip = "Haz clic"
#Add another locations
for i in range(0,len(df)):
    folium.Marker([df.iloc[i]['Latitude'],df.iloc[i]['Longitude']], 
                  popup=df.iloc[i]["Phone_Number"]).add_to(m)

#icon=folium.Icon(color='red', icon='info-sign')
# Save map
m.save('Geolocalización.html')

#Set list of numbers
options = []
for value in np.unique(list(df["Phone_Number"])):
    options.append({"label" : value, "value" : value})

# Create the Dash app
#app = dash.Dash(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.CERULEAN])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "1rem 1rem",
    "background-color": "#1e1e1e"
    
}


sidebar = html.Div(
    [   
        html.H1("DRON - 911",
                className="navbar-dark bg-dark text-white p-3 mb-2 text-center",
                style={'textAlign': 'center', 'top':'-5'}),     
        html.H4("Seleccionar fecha", style={'textAlign': 'center'}),
        dcc.DatePickerRange(initial_visible_month=datetime.now(),
                            start_date = date(2022,7,1),
                            end_date = date(2022,7,6),
                             style={'margin':'0 auto', 'display':'inline-block'}),
        
        html.Hr(),
        html.H4("Seleccionar Estado", style={'textAlign': 'center'}),
        dcc.Dropdown(id='state_dd',
        options=[
            {'label':'Aguascalientes', 'value':'AGS'},
            {'label':'Baja California', 'value':'BC'},
            {'label':'Baja California Sur', 'value':'BCS'},
            {'label':'Campeche', 'value':'CAMP'},
            {'label':'Coahuila', 'value':'COAH'},
            {'label':'Colima', 'value':'COL'},
            {'label':'Chiapas', 'value':'CHIS'},
            {'label':'Chihuahua', 'value':'CHIH'},
            {'label':'Ciudad de México', 'value':'CDMX'},
            {'label':'Durango', 'value':'DGO'},
            {'label':'Guanajuato', 'value':'GTO'},
            {'label':'Guerrero', 'value':'GRO'},
            {'label':'Hidalgo', 'value':'HGO'},
            {'label':'Jalisco', 'value':'JAL'},
            {'label':'Estado de México', 'value':'MEX'},
            {'label':'Michoacán', 'value':'MICH'},
            {'label':'Morelos', 'value':'MOR'},
            {'label':'Nayarit', 'value':'NAY'},
            {'label':'Nuevo León', 'value':'NL'},
            {'label':'Oaxaca', 'value':'OAX'},
            {'label':'Puebla', 'value':'PUE'},
            {'label':'Querétaro', 'value':'QRO'},
            {'label':'Quintana Roo', 'value':'QROO'},
            {'label':'San Luis Potosí', 'value':'SLP'},
            {'label':'Sinaloa', 'value':'SIN'},
            {'label':'Sonora', 'value':'SON'},
            {'label':'Tabasco', 'value':'TAB'},
            {'label':'Tamaulipas', 'value':'TAMPS'},
            {'label':'Tlaxcala', 'value':'TLAX'},
            {'label':'Veracruz', 'value':'VER'},
            {'label':'Yucatán', 'value':'YUC'},
            {'label':'Zacatecas', 'value':'ZAC'}],
            style={'width':'200px', 'margin':'0 auto'}),
        
        html.Hr(),
        html.H4("Seleccionar número", style={'textAlign': 'center'}),
        dcc.Dropdown(id='cell_dd',
        options = options,
            style={'width':'200px', 'margin':'0 auto'})
        
        
    ],
    style=SIDEBAR_STYLE,
)

#app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

# Set up the layout using an overall div
app.layout = html.Div(children=[
    sidebar,
    html.H1(children='Emergency Location Tracking',
            className="navbar-dark bg-dark text-white p-4 mb-2 text-center",
            style={"margin-left": "330px",'textAlign': 'center'}),
    html.Iframe(id = 'map', srcDoc = open('Geolocalización.html', 'r').read(), 
                width = '100%', height = '400', 
                style={
                        "display": "inline-block",
                        "width": "75%",
                        "margin-left": "330px",
                        "verticalAlign": "top"
                    })
])


if __name__ == '__main__':
    app.run_server(debug=True)
