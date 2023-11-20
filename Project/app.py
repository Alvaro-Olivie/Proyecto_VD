from datetime import datetime
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from temperature import get_temperatures
from cities import get_cities


app = dash.Dash(__name__)

geo = get_cities()
city = geo[0].tolist()

# data = get_temperatures(["Aberdeen", "Ankara"], ['2013-10-23', '2023-10-25'])

app.layout = html.Div([
    html.H1('Historical Temperatures by City'),

    html.Div([
        dcc.Dropdown(
            id='city-dropdown',
            options=[i for i in city],
            value=[city[0]],
            multi=True
        )
    ]),

    html.Div([
        dcc.Checklist(
            id='mean-checkbox',
            options=[
                {'label': 'Show Mean Temperature', 'value': 'mean'},
                {'label': 'Dont Show Individuals', 'value': 'individuals'},
            ],
            value=[]
        )
    ]),

    html.Div([
        dcc.DatePickerRange(
            id='date-picker-range',
            min_date_allowed=datetime(1950, 1, 1),
            max_date_allowed=datetime(2020, 12, 31),
            initial_visible_month=datetime(2020, 1, 1),
            start_date=datetime(2000, 1, 1),
            end_date=datetime(2020, 12, 31),
        )
    ]),

    html.Div([
       # create a line chart with the temperature from data
         dcc.Graph(
            id='temperature-graph',
            figure= {}
         )
    ])
])

# create a callback function to update the graph with the selected city and date range
@app.callback(
    dash.dependencies.Output('temperature-graph', 'figure'),
    [dash.dependencies.Input('city-dropdown', 'value'),
     dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date'),
     dash.dependencies.Input('mean-checkbox', 'value'),])

def update_graph(value, start_date, end_date, mean):
    # create a line chart with the temperature from data with plotly express
    df = get_temperatures(value, [start_date[:10], end_date[:10]])

    fig = go.Figure()

    if 'individuals' not in mean:
        for c in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df[c], mode='lines', name=c))
    
    if 'mean' in mean:
        fig.add_trace(go.Scatter(x=df.index, y=df.mean(axis=1), mode='lines', name='Mean'))

    fig.update_layout(
        title='Daily Temperatures Over 10 Years',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Temperature (°C)'),
        showlegend=True
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
