from dash import Dash, html
import dash
import dash_bootstrap_components as dbc
from components.nav import _nav

# Create Dash instance (initialize)
app = Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME
    ],
    use_pages=True
)

# Define the layout
app.layout = dbc.Container([
    dbc.Row([
        # Sidebar
        dbc.Col([_nav], width=2),
        
        # Main content
        dbc.Col([
            dash.page_container
        ], width=10),
    ])
], fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True)