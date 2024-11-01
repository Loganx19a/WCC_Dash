from dash import html, dcc
import dash

# Register page
dash.register_page(__name__, path='/upload', name='Upload-data', title='WCC | Upload Data')

layout = html.Div([
    html.H1("Upload page"),
    html.Div("Upload your Dataset here")
])