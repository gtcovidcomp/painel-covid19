
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from waitress import serve
from app import server
from app import app
from layouts import noPage, mainPage, sobrePage
import callbacks

# see https://dash.plot.ly/external-resources to alter header, footer and favicon
app.index_string = ''' 
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Sala de Situação COVID-19</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        {%config%}
        {%scripts%}
        {%renderer%}
    </body>
</html>
'''

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Update page
# # # # # # # # #
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/' or pathname == '/index':
        return mainPage
    elif pathname == '/sobre':
        return sobrePage
    else:
        return noPage


if __name__ == '__main__':
    app.run_server(debug=True)
