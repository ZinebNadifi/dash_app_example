import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

table = pd.read_csv("nama_10_gdp_1_Data.csv", engine= "python", na_values = [":", "NaN"])
table

table1 = table[(table["GEO"] !='European Union (current composition)') & 
           (table["GEO"] !='European Union (without United Kingdom)') &
          (table["GEO"] != 'European Union (15 countries)') &
          (table["GEO"] != 'Euro area (EA11-2000, EA12-2006, EA13-2007, EA15-2008, EA16-2010, EA17-2013, EA18-2014, EA19)') &
          (table["GEO"] != 'Euro area (19 countries)') &
          (table["GEO"] != 'Euro area (12 countries)')]
df = table1.drop("Flag and Footnotes", axis=1)

df["unit_item"] = df["NA_ITEM"] + ' ' + df["UNIT"]

available_indicators = df['unit_item'].unique()
countries = df["GEO"].unique()

app.layout = html.Div([
html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value= available_indicators[0]
            ),
            dcc.RadioItems(
                id='xaxis-type1',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value= available_indicators[0]
            ),
            dcc.RadioItems(
                id='yaxis-type1',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic1'),

    dcc.Slider(
        id='year--slider1',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    )
]),
html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in countries],
                value= countries[0]
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value= available_indicators[0]
            ),
            dcc.RadioItems(
                id='yaxis-type2',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'height': '130px'})
    ], style={'margin-top': '30px', 'margin-bottom': '20px'}),

    dcc.Graph(id='indicator-graphic2')
])])

#callback updates the figure, für jede sache die du updaten willst brauchst du eine neue callback function

@app.callback(
    dash.dependencies.Output('indicator-graphic1', 'figure'),
    [dash.dependencies.Input('xaxis-column1', 'value'),
     dash.dependencies.Input('yaxis-column1', 'value'),
     dash.dependencies.Input('xaxis-type1', 'value'),
     dash.dependencies.Input('yaxis-type1', 'value'),
     dash.dependencies.Input('year--slider1', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['unit_item'] == xaxis_column_name]['Value'],
            y=dff[dff['unit_item'] == yaxis_column_name]['Value'],
            text=dff[dff['unit_item'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('indicator-graphic2', 'figure'),
    [dash.dependencies.Input('xaxis-column2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value'),
     dash.dependencies.Input('yaxis-type2', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name, yaxis_type):
    dff = df[df['GEO'] == xaxis_column_name]
    
    return {
        'data': [go.Scatter(
            x = pd.Series(dff['TIME'].unique()),
            y = dff[dff['unit_item'] == yaxis_column_name]['Value'],
            mode = 'lines'
        )],
        'layout': go.Layout(
            xaxis={
                'title': "Year"
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server()

