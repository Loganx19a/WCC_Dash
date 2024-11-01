from dash import html, dcc
import dash


# Register the page
dash.register_page(__name__, path='/', name='Homepage', title='WCC | Homepage')

layout = html.Div([
    html.H1("Homepage"),
    html.P("Welcome to the homepage!")
])