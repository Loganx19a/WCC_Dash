from dash import html, dcc
import dash


# Register page
dash.register_page(__name__, path="/historical", name="Historical-data", title="WCC | Historical Data")

layout = html.Div([
    html.H1("Historical page"),
    html.Div("Historical data for your selected dataset will be presented here")
])