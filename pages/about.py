from dash import html, dcc
import dash


# Register page
dash.register_page(__name__, path="/about", name="About-page", title="WCC | About")

layout = html.Div([
    html.H1("About page"),
    html.Div("Information about the Wikiwatershed initiative will go here")
])