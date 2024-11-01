from dash import html
import dash_bootstrap_components as dbc

_nav = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.I(className="fa-solid fa-water fa-3x")
            ], className='nav-logo')
        ], width=4),
        dbc.Col([
            html.H1(['WCC Dashboard'], className='nav-text')
        ], width=8)
    ]),
    dbc.Row([
        dbc.Nav([
            dbc.NavLink("About", href="/about", active="exact"),
            dbc.NavLink("Home", href="/", active="exact"),
            dbc.NavLink("Upload Dataset", href="/upload", active="exact"),
            dbc.NavLink("Real-time", href="/real-time", active="exact"),
            dbc.NavLink("Historical", href="/historical", active="exact"),
            dbc.NavLink("Predictive Analytics", href="/predictive-analytics", active="exact")
        ], vertical=True, pills=True, class_name='nav-menu')
    ])
])