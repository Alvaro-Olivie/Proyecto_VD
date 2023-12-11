from datetime import datetime, timedelta
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from predictions import predict_next_year, create_regression
from temperature import get_temperatures, calculate_moving_average
from cities import get_cities
import pandas as pd
import plotly.express as px


app = dash.Dash(__name__)
server = app.server

geo = get_cities()
city = geo[0].tolist()

avg = get_temperatures(city, ['2001-01-01', '2023-12-01'])
# for each city in avg get the mean temperature
cityAvg = avg.mean(axis=0)
# data = get_temperatures(["Aberdeen", "Ankara"], ['2013-10-23', '2023-10-25'])

app.layout = html.Div([
    html.H1('Historical Temperatures by City', style={'textAlign': 'center', 'marginBottom': 30}),

    dcc.Tabs([
        dcc.Tab(label='City Data', children=[
            html.Div([
                dcc.Dropdown(
                    id='city-dropdown',
                    options=[{'label': i, 'value': i} for i in city],
                    value=[city[0]],
                    multi=True,
                    style={'width': '80%', 'margin': 'auto'}
                )
            ], style={'textAlign': 'center', 'marginBottom': 20}),

            html.Div([
                dcc.Checklist(
                    id='mean-checkbox',
                    options=[
                        {'label': 'Show Mean Temperature', 'value': 'mean'},
                    ],
                    value=[],
                    style={'margin': 'auto'}
                )
            ], style={'textAlign': 'center'}),

            html.Div([
                dcc.DatePickerRange(
                    id='date-picker-range',
                    min_date_allowed=datetime(2000, 1, 1),
                    max_date_allowed=datetime(2023, 12, 1),
                    initial_visible_month=datetime(2003, 1, 1),
                    start_date=datetime(2003, 12, 1),
                    end_date=datetime(2023, 12, 1),
                )
            ], style={'textAlign': 'center'}),

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

            html.Div(
                children=[
                    dcc.Graph(
                        id='city-map',
                        figure={}
                    )
                ],
                style={
                    'margin-bottom': '20px',  # Add some spacing between the Divs
                    'border': '1px solid #ddd',  # Add a border around the Div
                    'border-radius': '5px',  # Add rounded corners
                    'padding': '10px'  # Add some padding inside the Div
                }
            ),
        ]),

        dcc.Tab(label='Predictions Model', children=[
            html.Div([
                dcc.Dropdown(
                    id='city-dropdown-predictions',
                    options=[{'label': i, 'value': i} for i in city],
                    value=[city[0]],
                    multi=True,
                    style={'width': '80%', 'margin': 'auto'}
                )
            ], style={'textAlign': 'center', 'marginBottom': 20}),
            html.Div([
                dcc.Checklist(
                    id='mean-checkbox-predictions',
                    options=[
                        {'label': 'Show Mean Prediction', 'value': 'mean'},
                    ],
                    value=[],
                    style={'margin': 'auto'}
                )
            ], style={'textAlign': 'center'}),

            html.Div(
                children=[
                    dcc.Graph(
                        id='prediction-graph',
                        figure={}
                    )
                ],
                style={
                    'border': '1px solid #ddd',  # Add a border around the Div
                    'border-radius': '5px',  # Add rounded corners
                    'padding': '10px'  # Add some padding inside the Div
                }
            )
        ]),
    ])
])

@app.callback(
    dash.dependencies.Output('temperature-table', 'figure'),
    [dash.dependencies.Input('city-dropdown', 'value'),])

def update_table(value):
    # round not working!!!!!!!!!!!
    # filter avg with the selected cities in values and store in avg_t
    avg_t = avg[value]

    m = [str(element) for element in avg_t.mean().round(2).values]
    ma = [str(element) for element in avg_t.max().round(2).values]
    mi = [str(element) for element in avg_t.min().round(2).values]
    
    # create a table with the mean, max and min temperatures for each city
    fig = go.Figure(data=[go.Table(
        header=dict(values=['City', 'Mean Temperature', 'Max Temperature', 'Min Temperature']),
        cells=dict(values=[avg_t.columns, m, ma, mi]))
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

    x = x / len(df.columns)
        
    fig.add_trace(go.Scatter(x=df.index, y=[x] * len(df), mode='lines', name='Historical Average'))

    if 'mean' in mean:
        fig.add_trace(go.Scatter(x=df.index, y=df.mean(axis=1), mode='lines', name='Mean'))

    fig.update_layout(
        xaxis=dict(title='Date'),
        yaxis=dict(title='Temperature (°C)'),
        showlegend=True
    )

    return fig

@app.callback(
    dash.dependencies.Output('city-map', 'figure'),
    [dash.dependencies.Input('city-dropdown', 'value'),])

def update_map(value):
    avg_t = avg[value]

    # Create a DataFrame with two columns, city and average temperature
    avg_t = avg_t.mean().reset_index()
    avg_t.columns = ['City', 'Average Temperature']

    # Filter geo with the selected cities in values and store in geo_t
    geo_t = geo[geo[0].isin(value)]

    # Add column names to geo_t
    geo_t.columns = ['City', 'Country', 'Latitude', 'Longitude']

    # Merge avg_t and geo_t on city
    geo_t = pd.merge(geo_t, avg_t, on='City')

    # Create the map using Plotly Express
    fig = px.scatter_geo(
        geo_t,
        lon='Longitude',
        lat='Latitude',
        text='City',
        size='Average Temperature',
        title='Average Temperature for Each City',
        template='plotly',
        color='Average Temperature',
        color_continuous_scale='Viridis',  # You can choose a different color scale
        size_max=25,  # Adjust the maximum marker size
        labels={'Average Temperature': 'Avg. Temp'},
        hover_data={'Average Temperature': ':.2f'},
    )

    # Add legend
    fig.update_layout(legend_title_text='Average Temperature (°C)')

    return fig

@app.callback(
    dash.dependencies.Output('prediction-graph', 'figure'),
    [dash.dependencies.Input('city-dropdown-predictions', 'value'),
     dash.dependencies.Input('mean-checkbox-predictions', 'value'),])

def update_prediction(value, mean):
    # Get historical temperatures and calculate the moving average
    historical_data = calculate_moving_average(get_temperatures(value))

    # Make predictions for the next year
    predicted_data = predict_next_year(historical_data)

    # Combine historical and predicted data for plotting
    combined_data = pd.concat([historical_data, predicted_data])

    lr = create_regression(combined_data)

    fig = go.Figure()

    # Plotting using Plotly Express for a cleaner and more interactive visualization
    for city in value:
        # Add trace for historical data
        fig.add_trace(go.Scatter(x=historical_data.index, y=historical_data[city],
                      mode='lines',
                      name=f'Historical Data - {city}',
                      ))
        # Add trace for predicted data
        fig.add_trace(go.Scatter(x=predicted_data.index, y=predicted_data[city],
                          mode='lines',
                          name=f'Predicted Data - {city}',
                          ))
        
        fig.add_trace(go.Scatter(x=lr.index, y=lr[city],
                          mode='lines',
                          name=f'Trend - {city}',
                          ))


    if 'mean' in mean:   
        # Add another 2 traces for the historical and predicted average temperatures
        fig.add_trace(go.Scatter(x=historical_data.index, y=historical_data.mean(axis=1),
                        mode='lines',
                        name='Historical Average',
                        ))
        fig.add_trace(go.Scatter(x=predicted_data.index, y=predicted_data.mean(axis=1),
                            mode='lines',
                            name='Predicted Average',
                            ))
        fig.add_trace(go.Scatter(x=lr.index, y=lr.mean(axis=1),
                          mode='lines',
                          name=f'Trend',
                          ))

    # update the layout
    fig.update_layout(
        xaxis=dict(title='Date'),
        yaxis=dict(title='Temperature (°C)'),
        showlegend=True
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
