import dash 
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from dash import callback
import plotly.express as px
import pandas as pd
import requests
import io

from components.real_time_layout import create_real_time_layout
from components.fig_layout import my_figlayout, my_linelayout

# Register page
dash.register_page(__name__, path='/real-time', name='Real-time', title='WCC | Real-time')

# Define sensor information
SENSOR_INFO = {
    'Specific Conductance (μS/cm)': {
        'medium': 'Liquid aqueous',
        'sensor': 'METER_HYDROS 21'
    },
    'Water Depth (mm)': {
        'medium': 'Liquid aqueous',
        'sensor': 'METER_HYDROS 21'
    },
    'Water Temperature (°C)': {
        'medium': 'Liquid aqueous',
        'sensor': 'METER_HYDROS 21'
    },
    'Battery Voltage (V)': {
        'medium': 'Equipment',
        'sensor': 'EnviroDIY_Mayfly Data Logger v0.x'
    },
    'Logger Temperature (°C)': {
        'medium': 'Equipment',
        'sensor': 'EnviroDIY_Mayfly Data Logger v0.x'
    },
    'Signal Strength (%)': {
        'medium': 'Equipment',
        'sensor': 'Digi XBee3™ Cellular LTE CAT 1'
    }
}

# Data URL
DATA_URL = 'https://monitormywatershed.org/api/csv-values/?result_ids=4966,4967,4968,4969,4970,4971'

# Define the page layout
layout = create_real_time_layout(SENSOR_INFO)

# Callback to load data
@callback(
    Output('stored-data', 'data'),
    Input('stored-data', 'id')
)
def initialize_data(_):
    response = requests.get(DATA_URL)
    df = pd.read_csv(io.StringIO(response.text), comment='#', skip_blank_lines=True)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df['DateTimeUTC'] = pd.to_datetime(df['DateTimeUTC'])
    df = df.replace(-9999.0, pd.NA)
    
    # Rename columns to match display names
    column_mapping = {
        'Meter_Hydros21_Cond': 'Specific Conductance (μS/cm)',
        'Meter_Hydros21_Depth': 'Water Depth (mm)',
        'Meter_Hydros21_Temp': 'Water Temperature (°C)',
        'EnviroDIY_Mayfly_Batt': 'Battery Voltage (V)',
        'EnviroDIY_Mayfly_Temp': 'Logger Temperature (°C)',
        'Digi_Cellular_SignalPercent': 'Signal Strength (%)'
    }
    df = df.rename(columns=column_mapping)
    # Filter for last 72 hours
    last_72_hours = df['DateTimeUTC'].max() - pd.Timedelta(hours=72)
    df_filtered = df[df['DateTimeUTC'] > last_72_hours].copy()

    return df_filtered.to_dict('records')

# Callback to update plots
@callback(
    [Output(f'plot-{i}', 'figure') for i in range(6)],
    Input('stored-data', 'data')
)
def update_grid_plots(data):
    if not data:
        raise PreventUpdate
    
    df = pd.DataFrame(data)
    figures = []
    
    for metric in SENSOR_INFO.keys():
        fig = px.line(df, x='DateTime', y=metric)
        fig.update_layout(
            height=400,
            showlegend=False,
            **my_figlayout
        )
        fig.update_traces(line=my_linelayout)
        figures.append(fig)
    
    return figures