from datetime import datetime, timedelta
from arrow import get
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from temperature import get_temperatures, calculate_moving_average
from cities import get_cities


app = dash.Dash(__name__)

geo = get_cities()
city = geo[0].tolist()

avg = get_temperatures(city, ['2001-01-01', '2021-01-01'])
# for each city in avg get the mean temperature
cityAvg = avg.mean(axis=0)
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
            ],
            value=[]
        )
    ]),

    html.Div([
        dcc.DatePickerRange(
            id='date-picker-range',
            min_date_allowed=datetime(2000, 1, 1),
            max_date_allowed=datetime(2020, 12, 31),
            initial_visible_month=datetime(2020, 1, 1),
            start_date=datetime(2019, 1, 1),
            end_date=datetime(2020, 12, 31),
        )
    ]),

    html.Div(
        style={
            'display': 'grid',
            'grid-template-rows': '50% 50%'
        },
        children=[
            html.Div(
                style={'grid-column': '1'},
                children=[
                    dcc.Graph(
                        id='temperature-graph',
                        figure={}
                    )
                ]
            ),
            html.Div(
                style={'grid-column': '2'},
                children=[
                    dcc.Graph(
                        id='temperature-table',
                        figure={}
                    )
                ]
            )
        ]
    ),
])

@app.callback(
    dash.dependencies.Output('temperature-table', 'figure'),
    [dash.dependencies.Input('city-dropdown', 'value'),])

def update_table(value):
    # filter avg with the selected cities in values and store in avg_t
    avg_t = avg[value]
    
    # create a table with the mean, max and min temperatures for each city
    fig = go.Figure(data=[go.Table(
        header=dict(values=['City', 'Mean Temperature', 'Max Temperature', 'Min Temperature']),
        cells=dict(values=[avg_t.columns, avg_t.mean().round(2), avg_t.max().round(2), avg_t.min().round(2)]))
    ])

    return fig


# create a callback function to update the graph with the selected city and date range
@app.callback(
    dash.dependencies.Output('temperature-graph', 'figure'),
    [dash.dependencies.Input('city-dropdown', 'value'),
     dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date'),
     dash.dependencies.Input('mean-checkbox', 'value'),])

def update_graph(value, start_date, end_date, mean):

    start_date = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end_date = datetime.strptime(end_date[:10], '%Y-%m-%d')

    start_date = start_date - timedelta(days=365)

    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')

    df = calculate_moving_average(get_temperatures(value, [start_date, end_date]))

    fig = go.Figure()

    for c in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[c], mode='lines', name=c))
    
    # add a line with the average for each city and name it 'x historical average'

    x = 0
    for c in df.columns:
        x += cityAvg[c]
        
    fig.add_trace(go.Scatter(x=df.index, y=[x] * len(df), mode='lines', name='Historical Average'))

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
