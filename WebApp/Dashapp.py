import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"
import dash
import dash_table
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import glob
import pickle
import datetime as dt
from fbprophet import Prophet
from get_forecast import get_data
from pathlib import Path

import os


class Dashappcomponents:

    def __init__(self, sensor, start_date, end_date):
        """
                                        Name : Dash app components class
                                        Module : Dashapp
                                        Description : This class all the components required for making
                                                    dash app
                                        Parameters:
                                            - sensor : Name of the sensor selected by users.
                                            - start_date :  start Date selected by user in Date slider
                                            - end_data : end Date selected by user in Date slider
                                            - data :  creating a data class object to fetch forecasted data
                                            - forecasted_df : fetching the forecasted data from the class.

                                        Returns : None
                                        Written By : Ninad
                                        Version : 1.0.0
                                        Revision : None

                """



        # sensor="temp", start_date = "2020-07-20", end_date = "2020-07-21"
        self.sensor  = sensor
        self.start_Date = start_date
        self.end_date = end_date
        data = get_data(sensor)
        self.forecasted_df = data.get_forecasted_data()
        self.root = Path(__file__).parent
        #self.data_path = "Data/ProcessedDataset/"
        #self.model_path = "Models/ProductionModel/25-07-2021/"

    colors = {
        'background': '#e7c27d',
        'bodyColor':'#e7c27d',
        'text': '#8c5511'
    }

    def get_page_heading_style(self):
        """
                                                Name : get_page_heading_style function
                                                Module : Dash app
                                                Description : creates a the background color and styling for
                                                            page heading.
                                                Parameters: None
                                                Returns : page heading color (dict)
                                                Written By : Ninad
                                                Version : 1.0.0
                                                Revision : None

        """

        return {'backgroundColor': colors['background']}

    def get_page_heading_title(self):
        """
                                                Name : get_page_heading_title function
                                                Module : Dash app
                                                Description : creates the title  and styling for
                                                            page heading.
                                                Parameters: None
                                                Returns :  html.H1 (heading)
                                                Written By : Ninad
                                                Version : 1.0.0
                                                Revision : None

        """
        return html.H1(children= 'Environmental sensor analysis Dashboard',
                                            style={
                                            'textAlign': 'center',
                                            'color': "#8c5511"
                                        })

    def get_page_heading_subtitle(self):
        """
                                                Name : get_page_heading_subtitle function
                                                Module : Dash app
                                                Description : creates the subtitle of heading and styling for
                                                            page heading.
                                                Parameters: None
                                                Returns :  html.Div
                                                Written By : Ninad
                                                Version : 1.0.0
                                                Revision : None

        """
        return html.Div(children='Visualize the data generated from Iot sensors.',
                                             style={
                                                 'textAlign':'center',
                                                 'color':"#8c5511"
                                             })

    def generate_page_header(self):
        """
                                                Name : generate_page_header function
                                                Module : Dash app
                                                Description : creates the format for page title and subtitle
                                                              for page heading in dash app.
                                                Parameters: None
                                                Returns :  Header ( heading
                                                Written By : Ninad
                                                Version : 1.0.0
                                                Revision : None

        """
        main_header = dbc.Row(
                                [
                                    dbc.Col(self.get_page_heading_title(),md=12)
                                ],
                                align="center"
                            )
        subtitle_header = dbc.Row(
                                [
                                    dbc.Col(self.get_page_heading_subtitle(),md=12)
                                ],
                                align="center"
                            )
        header = (main_header,subtitle_header)
        return header

    def get_mean(self):
        """
                                                Name :  get_mean function
                                                Module : Dash app.
                                                Description : Gets the mean value for card from forecasted data
                                                Parameters: None
                                                Returns :  mean value (- float)
                                                Written By : Ninad
                                                Version : 1.0.0
                                                Revision : None

        """
        #forecast_df = pd.read_csv("Forecast/25-07-2021/Data/" + sensor +"_forecast.csv")
        df = self.forecasted_df
        forecast_df = df.copy()
        sliced_df = forecast_df[(forecast_df["ds"] > pd.to_datetime("2020-07-12" + " " + " 00:01:00")) & (
                    forecast_df["ds"] < pd.to_datetime("2020-07-20" + " " + "23:59:00"))]
        mean = np.round(sliced_df["yhat"].mean(), 3)
        return mean

    def get_max(self):
        """
                                                Name :  get_max function
                                                Module : Dash app.
                                                Description : Gets the maximum value for card from forecasted data.
                                                Parameters: None.
                                                Returns :  maximum value.( -float)
                                                Written By : Ninad
                                                Version : 1.0.0
                                                Revision : None

        """
        # forecast_df = pd.read_csv("Forecast/25-07-2021/Data/" + sensor +"_forecast.csv")
        df = self.forecasted_df
        forecast_df = df.copy()
        sliced_df = forecast_df[(forecast_df["ds"] > pd.to_datetime("2020-07-12" + " " + " 00:01:00")) & (
                    forecast_df["ds"] < pd.to_datetime("2020-07-20" + " " + "23:59:00"))]
        max_value = np.round(sliced_df["yhat_upper"].mean(), 3)
        return max_value

    def get_min(self):
        """
                                                Name :  get_mean function
                                                Module : Dash app.
                                                Description : Gets the mean value for card from forecasted data
                                                Parameters: None
                                                Returns :  mean value (-float)
                                                Written By : Ninad
                                                Version : 1.0.0
                                                Revision : None

        """

        #forecast_df = pd.read_csv("Forecast/25-07-2021/Data/" + sensor +"_forecast.csv")
        df = self.forecasted_df
        forecast_df = df.copy()
        sliced_df = forecast_df[(forecast_df["ds"] > pd.to_datetime("2020-07-12" + " " + " 00:01:00")) & (
                forecast_df["ds"] < pd.to_datetime("2020-07-20" + " " + "23:59:00"))]
        min_value = np.round(sliced_df["yhat_lower"].mean(), 3)
        return min_value

    def get_sensor_list(self):
        """
                                                Name :  get_senor_list function
                                                Module : Dash app.
                                                Description : Gets the list of sensor.
                                                Parameters: None
                                                Returns :  dct (-dict)
                                                Written By : Ninad
                                                Version : 1.0.0
                                                Revision : None

        """
        dct = {"co": "Co","humidity":"Humidity","lpg":"LPG", "smoke":"Smoke", "temp": "Temp"}
        return dct

    def create_dropdown_list(self,senor_list):
        """
                                                Name :  create_dropdown_list function
                                                Module : Dash app.
                                                Description : create and drop down list to pull the sensor value from
                                                             user
                                                Parameters:
                                                         - sensor_list(gives the list of sensors)
                                                Returns :  mean value (-float)
                                                Written By : Ninad
                                                Version : 1.0.0
                                                Revision : None

        """
        dropdown_list = []
        for keys, values  in senor_list.items():
            sensor_dict = {'label': values ,'value': keys}
            dropdown_list.append(sensor_dict)
        return dropdown_list

    def get_sensor_dropdown(self, id):
        """
                                                Name :  get_sensor_dropdown function
                                                Module : Dash app.
                                                Description : Creates the  sensor dropdown option in dash app
                                                Parameters: id (unique id)
                                                Returns :  html.Div
                                                Written By : Ninad
                                                Version : 1.0.0
                                                Revision : None

        """
        return html.Div([
                            html.Label('Select Sensor'),
                            dcc.Dropdown(id='my-id'+str(id),
                                options=self.create_dropdown_list(self.get_sensor_list()),
                                value='temp'
                            ),
                            html.Div(id='my-div'+str(id))
                        ])

    def generate_card_content(self, card_header,card_value):
        """
                                                Name :  generate_card_content function.
                                                Module : Dash app.
                                                Description : Generates the content and styling for card header an
                                                            card value to be showed in card.
                                                Parameters:
                                                          - card_header
                                                          - card_value
                                                Returns :  list
                                                Written By : Ninad
                                                Version : 1.0.0
                                                Revision : None

        """
        card_head_style = {'textAlign':'center','fontSize':'150%'}
        card_body_style = {'textAlign':'center','fontSize':'200%'}
        card_header = dbc.CardHeader(card_header,style=card_head_style)
        card_body = dbc.CardBody(
            [
                html.H5(f"{float(card_value):,}", className="card-title",style=card_body_style),
                html.P(
                    className="card-text",style={'textAlign':'center'}
                ),
            ]
        )
        card = [card_header,card_body]
        return card

    def generate_cards(self):
        """
                                                Name :  generate_cards function
                                                Module : Dash app.
                                                Description : Creates the card format and content to be showed in dash
                                                            app.
                                                Parameters: None
                                                Returns :  html.Div
                                                Written By : Ninad
                                                Version : 1.0.0
                                                Revision : None

        """
        sv = self.get_sensor_list().get(self.sensor)
        avg = self.get_mean()
        lower_interval = self.get_min()
        upper_interval = self.get_max()
        cards = html.Div(
            [
                dbc.Row(

                    [
                        dbc.Col(dbc.Card(self.generate_card_content("Average {}".format(sv),avg), color="success", inverse=True),md=dict(size=2,offset=3)),
                        dbc.Col(dbc.Card(self.generate_card_content("Minimum {}".format(sv),lower_interval), color="warning", inverse=True),md=dict(size=2)),
                        dbc.Col(dbc.Card(self.generate_card_content("Maximum {}".format(sv), upper_interval),color="dark", inverse=True),md=dict(size=2)),
                    ],
                    className="mb-4",
                ),
            ],id='card1'
        )
        return cards

    def get_future_forecast(self):
        """
                                                Name :  get_future_forecast function
                                                Module : Dash app.
                                                Description : Creates the forecasted graph taking the raw data and
                                                          forecasted data in dash app
                                                Parameters: None
                                                Returns :  fig ( plotly graph)
                                                Written By : Ninad
                                                Version : 1.0.0
                                                Revision : None

        """
       
        sv = self.get_sensor_list().get(self.sensor)
        df = pd.read_csv( os.path.join(self.root,"Data/ProcessedDataset/" + self.sensor + ".csv"))
        # forecast_df = pd.read_csv("Forecast/25-07-2021/Data/" + sensor + "_forecast.csv")
        forecast_df = self.forecasted_df

        fig = go.Figure()
        #Add traces
        fig.add_trace(go.Scatter(x=df['Datetime'], y=np.round(df[self.sensor], 5),
                                 mode='lines+markers',
                                 name='Actual  '))
        fig.add_trace(go.Scatter(x=forecast_df['ds'], y=forecast_df["yhat"],
                                 mode='lines+markers',
                                 name='Forecasted ',
                                 line_color="maroon"))

        fig.update_layout(
            title=  sv + " Forecast",
            xaxis_title="Days ",
            yaxis_title= sv ,
            font=dict(
                family="Courier New, monospace",
                size=20,
                color= "Brown"
            )
        )
        fig.update_layout(title_x=0.5, plot_bgcolor='#ffffff', paper_bgcolor='#ffffff')
        fig.update_layout(height=500,
                          margin={'l': 20, 'b': 0, 'r': 5, 't': 50}
                         )
        return fig

    def graph1(self):
        """
                                                Name :  graph1 function
                                                Module : Dash app.
                                                Description : loads the graph an dash component to show it in dash app.
                                                Parameters: None
                                                Returns :  dcc ( dash core components)
                                                Written By : Ninad
                                                Version : 1.0.0
                                                Revision : None

        """
        return dcc.Graph(id='graph1',figure=self.get_future_forecast())


    def generate_layout(self):
        """
                                                Name :  generate_layout function
                                                Module : Dash app.
                                                Description : generates the whole layout and formating of the dash app
                                                             with the help of all created dash components
                                                Parameters: None
                                                Returns :  app layout
                                                Written By : Ninad
                                                Version : 1.0.0
                                                Revision : None

        """
        page_header = self.generate_page_header()
        layout = dbc.Container(
            [
                page_header[0],
                page_header[1],
                html.Hr(),
                dbc.Col(
                    dcc.DatePickerRange(
                        id="date-picker-range",
                        start_date=dt.datetime(2020, 7, 12),
                        end_date=dt.datetime(2020, 7, 23),
                        min_date_allowed=dt.datetime(2020, 7, 12),
                        max_date_allowed=dt.datetime(2020, 7, 23),
                        end_date_placeholder_text="Select a date"
                    )
                ),
                self.generate_cards(),
                html.Hr(),
                dbc.Row(

                    [
                        dbc.Col(self.get_sensor_dropdown(id=1), md=dict(size=4, offset=4))
                    ]

                ),
                html.Hr(),
                dbc.Row(

                    [

                        dbc.Col(self.graph1(), md=dict(size=8, offset=2))

                    ],
                    align="right",


                ),
            ],

            fluid=True
        )
        return layout
