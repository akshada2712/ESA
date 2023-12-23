import dash
import dash_table
import plotly.io as pio
pio.renderers.default = "browser"
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from Dashapp import Dashappcomponents

# Boostrap theme for app
BS = "https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/litera/bootstrap.min.css"

# creating dash app and assigning title
app = dash.Dash(__name__, external_stylesheets = [BS])
app.title = 'ESA Dashboard'

# server callbacks
# to upadtes the output as per user inputs

@app.callback(
    [Output(component_id='graph1',component_property='figure'),
     Output(component_id='card1',component_property='children')
     ],
    [Input(component_id='my-id1',component_property='value'),
     Input("date-picker-range", "start_date"),
     Input("date-picker-range", "end_date")
     ]
)

# Taking the user inputs and giving it to
# the output functions
def update_output_div(input_value1, start_date , end_date ):
    ui = Dashappcomponents(input_value1, start_date, end_date)
    return ui.get_future_forecast() , ui.generate_cards()


app.layout = Dashappcomponents(sensor="temp", start_date = "2020-07-20", end_date = "2020-07-24").generate_layout()

if __name__ == "__main__":
    app.run_server(host="127.0.0.1", debug=True)