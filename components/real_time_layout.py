from dash import html, dcc
import dash_bootstrap_components as dbc
from components.fig_layout import my_figlayout  
from assets.color_palettes import ACTIVE_PALETTE  

def create_plot_grid(sensor_info):
    """Create the grid of plots with cards"""
    return html.Div([
        html.Div([
            # Card container
            html.Div([
                # Header
                html.Div([
                    html.Div([
                        # Title and tag container
                        html.Div([
                            html.H3(
                                list(sensor_info.keys())[i].split(' (')[0],
                                className='plot-title'
                            ),
                            html.Span('Provisional', className='provisional-tag')
                        ], className='title-container'),
                        html.Button(
                            'View Full Screen',
                            id=f'btn-{i}',
                            n_clicks=0,
                            className='btn-view-full'
                        )
                    ], className='header-content')
                ], className='card-header'),
                
                # Plot container
                html.Div([
                    dcc.Loading(
                        dcc.Graph(
                            id=f'plot-{i}',
                            figure={'data': [], 'layout': my_figlayout}
                        ),
                        type="circle",
                        delay_show=500,
                        delay_hide=2000,
                        color=ACTIVE_PALETTE['primary']  # Spinner color
                    ),
                ], className='plot-container'),
                
                # Info table
                html.Table([
                    html.Tr([
                        html.Td('Medium', className='info-label'),
                        html.Td(info['medium'])
                    ]),
                    html.Tr([
                        html.Td('Sensor', className='info-label'),
                        html.Td(info['sensor'])
                    ])
                ], className='info-table')
            ], className='plot-card')
        ], className='plot-card-container')
        for i, (metric, info) in enumerate(sensor_info.items())
    ], className='plot-grid')

def create_modal():
    """Create the full-screen modal"""
    return html.Div(
        id='full-screen-container',
        style={'display': 'none'},
        children=[
            html.Div([
                html.Div([
                    html.H3("Detailed View", className='modal-title'),
                    html.Button(
                        '×',
                        id='close-full-screen',
                        className='modal-close'
                    )
                ], className='modal-header'),
                html.Div([
                    dcc.Graph(
                        id='full-screen-plot',
                        className='modal-plot'
                    )
                ], className='modal-body')
            ], className='modal-content')
        ]
    )

def create_real_time_layout(sensor_info):
    """Create the complete real-time monitoring layout"""
    return html.Div([
        html.H1(
            "Wildcat Creek Flow sensor (WC001)",
            style={'textAlign': 'center', 'padding': '20px'}
        ),
        create_plot_grid(sensor_info),
        create_modal(),
        # Store components
        dcc.Store(id='stored-data'),
        dcc.Store(id='current-plot-index', data=0)
    ])