from dash import html, dcc
import dash

# Register page
dash.register_page(__name__, path="/predictive-analytics", name="Predictive-analytics", title="WCC | Predictive Analytics")

layout = html.Div([
    html.H1("Predictive Analytics page"),
    html.Div("This page will feature predictive analytics to attempt to predict the water-quality data (specific conductance)")
])