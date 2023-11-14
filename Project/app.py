import dash
from dash import dcc
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('My Dash App'),
    
    html.Div([
        html.H2('Section 1'),
        dcc.Graph(
            id='graph1',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'title': 'Graph 1'
                }
            }
        )
    ]),
    
    html.Div([
        html.H2('Section 2'),
        dcc.Graph(
            id='graph2',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'title': 'Graph 2'
                }
            }
        )
    ]),
    
    html.Div([
        html.H2('Section 3'),
        dcc.Graph(
            id='graph3',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'title': 'Graph 3'
                }
            }
        )
    ]),
    
    html.Div([
        html.H2('Section 4'),
        dcc.Graph(
            id='graph4',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'title': 'Graph 4'
                }
            }
        )
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
