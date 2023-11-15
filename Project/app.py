from datetime import datetime
import plotly.express as px
import dash
from dash import dcc
from dash import html
from temperature import get_temperatures
from cities import get_cities


app = dash.Dash(__name__)

geo = get_cities()[0].tolist()

data = get_temperatures(["Aberdeen", "Ankara"], ['2013-10-23', '2023-10-25'])

app.layout = html.Div([
    html.H1('Historical Temperatures by City'),

    html.Div([
        dcc.Dropdown(
            id='city-dropdown',
            options=[i for i in geo],
            value=[geo[0]],
            multi=True
        )
    ]),

    html.Div([
        dcc.DatePickerRange(
            id='date-picker-range',
            min_date_allowed=datetime(1950, 1, 1),
            max_date_allowed=datetime(2020, 12, 31),
            initial_visible_month=datetime(2020, 1, 1),
            start_date=datetime(2020, 1, 1),
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
     dash.dependencies.Input('date-picker-range', 'end_date')])

def update_graph(value, start_date, end_date):
    # create a line chart with the temperature from data with plotly express
    print(start_date[:10], end_date[:10])
    data = get_temperatures(value, [start_date[:10], end_date[:10]])
    fig = px.line(data, x = 'Date', y = 'Temperature', color = 'City')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
