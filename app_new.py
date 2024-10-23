from dash import Dash, dcc, html, Input, Output, State, callback, ctx
import plotly.express as px
import pandas as pd
import requests
import io
from dash.exceptions import PreventUpdate

# Dash app instance
app = Dash(__name__, title='WCC Dash')

# Assign URL
DATA_URL = 'https://monitormywatershed.org/api/csv-values/?result_ids=4966,4967,4968,4969,4970,4971'

# Define sensor information
SENSOR_INFO = {
    'Specific Conductance (μS/cm)': {'medium': 'Liquid aqueous', 'sensor': 'METER_HYDROS 21'},
    'Water Depth (mm)': {'medium': 'Liquid aqueous', 'sensor': 'METER_HYDROS 21'},
    'Water Temperature (°C)': {'medium': 'Liquid aqueous', 'sensor': 'METER_HYDROS 21'},
    'Battery Voltage (V)': {'medium': 'Equipment', 'sensor': 'EnviroDIY_Mayfly Data Logger v0.x'},
    'Logger Temperature (°C)': {'medium': 'Equipment', 'sensor': 'EnviroDIY_Mayfly Data Logger v0.x'},
    'Signal Strength (%)': {'medium': 'Equipment', 'sensor': 'Digi XBee3™ Cellular LTE CAT 1'}
}

def get_date_range(df):
    """Get the min and max dates from the DataFrame"""
    min_date = pd.to_datetime(df['DateTime'].min())
    max_date = pd.to_datetime(df['DateTime'].max())
    return min_date.strftime('%Y-%m-%d'), max_date.strftime('%Y-%m-%d')

def load_and_process_data():
    """Load and process data from the URL"""
    response = requests.get(DATA_URL)
    df = pd.read_csv(
        io.StringIO(response.text),
        comment='#',
        skip_blank_lines=True
    )
    
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df['DateTimeUTC'] = pd.to_datetime(df['DateTimeUTC'])
    df = df.replace(-9999.0, pd.NA)
    
    column_mapping = {
        'Meter_Hydros21_Cond': 'Specific Conductance (μS/cm)',
        'Meter_Hydros21_Depth': 'Water Depth (mm)',
        'Meter_Hydros21_Temp': 'Water Temperature (°C)',
        'EnviroDIY_Mayfly_Batt': 'Battery Voltage (V)',
        'EnviroDIY_Mayfly_Temp': 'Logger Temperature (°C)',
        'Digi_Cellular_SignalPercent': 'Signal Strength (%)'
    }
    
    df = df.rename(columns=column_mapping)
    
    last_72_hours = df['DateTimeUTC'].max() - pd.Timedelta(hours=72)
    df_filtered = df[df['DateTimeUTC'] > last_72_hours].copy()
    
    return {'complete': df, 'filtered': df_filtered}

# Define the layout
app.layout = html.Div([
    html.H1("Wildcat Creek Flow sensor (WC001)", 
            style={'textAlign': 'center', 'padding': '20px'}),
    
    # Grid of plots
    html.Div([
        html.Div([
            # Card container
            html.Div([
                # Turquoise header
                html.Div([
                    # Left side with title and provisional tag
                    html.Div([
                        html.H3(list(SENSOR_INFO.keys())[i].split(' (')[0], style={
                            'margin': '0',
                            'color': 'black',
                            'fontSize': '18px',
                            'fontWeight': 'bold',
                            'display': 'inline-block'
                        }),
                        html.Span('Provisional', style={
                            'backgroundColor': 'rgba(255, 255, 255, 0.2)',
                            'padding': '2px 8px',
                            'borderRadius': '4px',
                            'marginLeft': '10px',
                            'fontSize': '12px',
                            'color': 'black'
                        })
                    ], style={
                        'display': 'flex',
                        'alignItems': 'center'
                    }),
                    
                    # Right side with button
                    html.Button(
                        'View Full Screen', 
                        id=f'btn-{i}',
                        n_clicks=0,
                        style={
                            'padding': '6px 12px',
                            'backgroundColor': 'white',
                            'color': '#2c3e50',
                            'border': 'none',
                            'borderRadius': '4px',
                            'cursor': 'pointer',
                            'fontSize': '13px',
                            'transition': 'background-color 0.2s',
                            'hover': {
                                'backgroundColor': '#f8f9fa'
                            }
                        }
                    )
                ], style={
                    'backgroundColor': '#7dd0d4',
                    'padding': '10px 15px',
                    'borderTopLeftRadius': '10px',
                    'borderTopRightRadius': '10px',
                    'marginBottom': '15px',
                    'display': 'flex',
                    'justifyContent': 'space-between',
                    'alignItems': 'center'
                }),
                
                # Plot container
                html.Div([
                    dcc.Loading(
                        dcc.Graph(id=f'plot-{i}'),
                        type="circle"
                    ),
                ], style={
                    'width': '100%',
                    'height': '100%',
                    'marginBottom': '15px'
                }),
                
                # Info table 
                html.Table([
                    html.Tr([
                        html.Td('Medium', style={
                            'fontWeight': 'bold',
                            'padding': '8px',
                            'borderBottom': '1px solid #eee',
                            'backgroundColor': '#f8f9fa',
                            'width': '30%',
                            'textAlign': 'left'
                        }),
                        html.Td(SENSOR_INFO[list(SENSOR_INFO.keys())[i]]['medium'], style={
                            'padding': '8px',
                            'borderBottom': '1px solid #eee',
                            'backgroundColor': '#ffffff',
                            'textAlign': 'left'
                        })
                    ]),
                    html.Tr([
                        html.Td('Sensor', style={
                            'fontWeight': 'bold',
                            'padding': '8px',
                            'backgroundColor': '#f8f9fa',
                            'width': '30%',
                            'textAlign': 'left'
                        }),
                        html.Td(SENSOR_INFO[list(SENSOR_INFO.keys())[i]]['sensor'], style={
                            'padding': '8px',
                            'backgroundColor': '#ffffff',
                            'textAlign': 'left'
                        })
                    ])
                ], style={
                    'width': '100%',
                    'borderCollapse': 'collapse',
                    'border': '1px solid #eee',
                    'borderRadius': '4px',
                    'overflow': 'hidden',
                    'fontSize': '14px'
                })
            ], style={
                'backgroundColor': 'white',
                'borderRadius': '10px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08)',
                'marginBottom': '20px',
                'transition': 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
                'overflow': 'hidden',  
                'hover': {
                    'transform': 'translateY(-2px)',
                    'boxShadow': '0 6px 8px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.08)'
                }
            })
        ], style={
            'width': '50%',
            'display': 'inline-block', 
            'padding': '15px',
            'boxSizing': 'border-box',
        }) 
        for i in range(6)
    ], style={
        'width': '100%',
        'maxWidth': '1800px',
        'margin': '0 auto',
        'textAlign': 'center',
        'backgroundColor': '#f5f5f5',
        'padding': '20px'
    }),
    
# Modal
    html.Div(
        id='full-screen-container',
        style={'display': 'none'},  # Start hidden
        children=[
            # Modal content
            html.Div([
                # Header
                html.Div([
                    html.H3("Detailed View", style={'margin': '0', 'flex': '1'}),
                    html.Button(
                        '×',
                        id='close-full-screen',
                        n_clicks=0,
                        style={
                            'fontSize': '24px',
                            'border': 'none',
                            'background': 'none',
                            'cursor': 'pointer',
                            'padding': '5px 10px',
                            'color': '#666'
                        }
                    )
                ], style={
                    'display': 'flex',
                    'justifyContent': 'space-between',
                    'alignItems': 'center',
                    'borderBottom': '1px solid #ddd',
                    'padding': '10px',
                    'height': '50px',  # Fixed height for header
                    'boxSizing': 'border-box'
                }),
                
                # Date picker container
                html.Div([
                    html.Label("Select Date Range:", 
                             style={'marginRight': '10px'}),
                    dcc.DatePickerRange(
                        id='date-range',
                        display_format='YYYY-MM-DD',
                        style={'zIndex': '1001'}
                    )
                ], style={
                    'padding': '20px',
                    'borderBottom': '1px solid #ddd',
                    'height': '70px',  # Fixed height for date picker section
                    'boxSizing': 'border-box'
                }),
                
                # Graph container
                html.Div([
                    dcc.Graph(
                        id='full-screen-plot',
                        style={
                            'height': 'calc(100% - 20px)'  
                        }
                    )
                ], style={
                    'padding': '10px',
                    'height': 'calc(100% - 120px)',  # Subtract header and date picker heights
                    'boxSizing': 'border-box'
                })
                
            ], style={
                'position': 'relative',
                'backgroundColor': 'white',
                'margin': '20px auto',
                'width': '90%',
                'maxWidth': '1200px',
                'borderRadius': '8px',
                'boxShadow': '0 2px 10px rgba(0,0,0,0.1)',
                'height': 'calc(100vh - 40px)',  # Subtract margin
                'display': 'flex',
                'flexDirection': 'column',
                'overflow': 'hidden'  # Prevent content from spilling out
            })
        ]
    ),
    
    # Store components
    dcc.Store(id='stored-data'),
    dcc.Store(id='current-plot-index', data=0),
    dcc.Store(id='modal-trigger', data=False),  # Track if modal should be shown
])

@callback(
    Output('stored-data', 'data'),
    Input('stored-data', 'id')
)
def initialize_data(_):
    data_dict = load_and_process_data()
    return {
        'complete': data_dict['complete'].to_dict('records'),
        'filtered': data_dict['filtered'].to_dict('records')
    }

@callback(
    [Output(f'plot-{i}', 'figure') for i in range(6)],
    Input('stored-data', 'data')
)
def update_grid_plots(data):
    if not data:
        raise PreventUpdate
    
    df = pd.DataFrame(data['filtered'])
    
    columns = [
        'Specific Conductance (μS/cm)',
        'Water Depth (mm)',
        'Water Temperature (°C)',
        'Battery Voltage (V)',
        'Logger Temperature (°C)',
        'Signal Strength (%)'
    ]
    
    figures = []
    for col in columns:
        fig = px.line(
            df, 
            x='DateTime', 
            y=col
        )
        fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),  # Reduced top margin since no title
            hovermode='x unified',
            height=400,
            width=None,
            showlegend=False,
            xaxis_title="Date",
            yaxis_title=col,
            plot_bgcolor='white',
            paper_bgcolor='white',
            title=None  # Remove title for grid plots
        )
        figures.append(fig)
    
    return figures

@callback(
    Output('date-range', 'min_date_allowed'),
    Output('date-range', 'max_date_allowed'),
    Output('date-range', 'start_date'),
    Output('date-range', 'end_date'),
    Output('date-range', 'initial_visible_month'),
    Input('stored-data', 'data')
)
def initialize_date_picker(data):
    if not data:
        raise PreventUpdate
    
    df = pd.DataFrame(data['complete'])
    min_date, max_date = get_date_range(df)
    initial_month = pd.to_datetime(min_date)
    
    return min_date, max_date, min_date, max_date, initial_month

@callback(
    Output('full-screen-container', 'style'),
    Output('full-screen-plot', 'figure'),
    Output('current-plot-index', 'data'),
    Output('modal-trigger', 'data'),
    [Input(f'btn-{i}', 'n_clicks') for i in range(6)],
    Input('close-full-screen', 'n_clicks'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    State('stored-data', 'data'),
    State('current-plot-index', 'data'),
    State('modal-trigger', 'data')
)
def handle_full_screen(*args):
    # Immediately prevent any updates if no explicit trigger
    if not ctx.triggered:
        raise PreventUpdate

    button_clicks = args[:-3]
    stored_data = args[-3]
    current_index = args[-2]
    show_modal = args[-1]
    
    trigger_id = ctx.triggered_id

    base_modal_style = {
        'position': 'fixed',
        'top': '0',
        'left': '0',
        'width': '100%',
        'height': '100%',
        'backgroundColor': 'rgba(0,0,0,0.7)',
        'zIndex': '1000',
        'paddingTop': '20px',
        'overflow': 'auto',
        'display': 'none'  # Default to hidden
    }

    # Handle close button
    if trigger_id == 'close-full-screen':
        return base_modal_style, {}, current_index, False
    
    # Only proceed if it's a button click or if the modal is already shown
    if not (isinstance(trigger_id, str) and (trigger_id.startswith('btn-') or 
            (trigger_id.startswith('date-range') and show_modal))):
        raise PreventUpdate

    # Handle new button click
    if trigger_id.startswith('btn-'):
        current_index = int(trigger_id.split('-')[1])
        show_modal = True
    
    columns = [
        'Specific Conductance (μS/cm)',
        'Water Depth (mm)',
        'Water Temperature (°C)',
        'Battery Voltage (V)',
        'Logger Temperature (°C)',
        'Signal Strength (%)'
    ]
    
    # Create figure with title for full-screen view
    df = pd.DataFrame(stored_data['complete'])
    
    # Handle date filtering
    start_date = args[-5]
    end_date = args[-4]
    if start_date and end_date:
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        df = df[(df['DateTime'] >= start_date) & (df['DateTime'] <= end_date)]

    fig = px.line(
    df, 
    x='DateTime', 
    y=columns[current_index],
    title=None  # Remove title from initial plot 
    )
    fig.update_layout(
        hovermode='x unified',
        height=800,
        title={
            'text': columns[current_index],
            'y': 0.98,        
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top', 
            'font': {'size': 20}
        },
        margin=dict(l=20, r=20, t=60, b=20),  
        xaxis_title="Date",
        yaxis_title=columns[current_index]
    )

    # Only add date range if dates are selected
    if start_date and end_date:
        fig.update_xaxes(range=[start_date, end_date])
    
    # Show modal
    visible_style = {**base_modal_style, 'display': 'block'}
    
    return visible_style, fig, current_index, show_modal



if __name__ == '__main__':
    app.run_server(debug=True)