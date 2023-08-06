import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

external_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('stats.csv')
df = df.drop(['Unnamed: 0'], axis=1)


app = dash.Dash(__name__, external_stylesheets=external_css)

app.layout = dash_table.DataTable(
    id='stats',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
    # style_header={'backgroundColor': 'rgb(30, 30, 30)'},
    # style_cell={
    #     'backgroundColor': 'rgb(50, 50, 50)',
    #     'color': colors['text']
    # },
    style_data_conditional=[{
        "if": {"column_id": "Calls",
                'filter': 'Calls <= num(100)'},
        "backgroundColor": "#3D9970",
        'color': 'white'
    }]
    )



if __name__ == '__main__':
    app.run_server(debug=True)