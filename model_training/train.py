import shutil

import pandas as pd
from fbprophet import Prophet
import pickle
import numpy as np
import os
import plotly.graph_objects as go
from util.get_past_current_date import Date
from util.app_logger import AppLogger
from util.root import ProjectRoot


class ModelTraining:
    """
             Name : ModelTraining Class
             Module : model_training
             Description : This class does following task
                - create model
                - save model
                - forecast future data
                - save future plots
                - save models
             Written By : Ninad,Jai Singh
             Version : 1.0.0
             Revision : None

    """

    def __init__(self, data, model_name):

        """
                                       Name : RunTraining Class Constructor
                                       Module : model_training
                                       Description : Initiates the instance variable which will
                                                     be used by the class
                                       Parameters:
                                           - date : Create date class object to fetch present and past date
                                           - project_root : Project Root Directory Object to get parent directory
                                           - logger : Logger Object to log the details
                                           - path : Path for preprocessed data
                                           - data : data passed for creation of model
                                           - model : used to create model instance
                                           - model_name : same as sensor name to create various sensor model


                                       Returns : None
                                       Written By : Ninad , Jai Singh
                                       Version : 1.0.0
                                       Revision : None

        """
        self.date = Date()
        self.project_root = ProjectRoot().get_project_root()
        app_log = AppLogger("Model Train", os.path.join(self.project_root, 'Logs/Train.log'))
        self.logger = app_log.set_handlers()
        self.path = "Data/ProcessedDataset"
        self.df = data
        self.model = ""
        self.model_name = model_name

    def reformat(self):

        """
                                Name : reformat function
                                Module : model_training
                                Description : This function changes the columns names as
                                 per model requirement for a given dataframe.

                                Parameters: None
                                Returns :
                                    -  df : type(pandas dataframe)
                                    - on failure : Raise Exceptions
                                Written By : Ninad,Jai Singh
                                Version : 1.0.0
                                Revision : None

        """

        try:
            self.df.columns = ["ds", "y"]
            return self.df
        except Exception as e:
            self.logger.error("Error in reformat function!")
            self.logger.exception(e)

    def create_save_model(self):

        """
                                        Name : create_save_model function
                                        Module : model_training
                                        Description : This function creates required model for a given
                                                      data save it to the assigned location
                                        Parameters: None
                                        Returns : Save Models and return None
                                            -  model : type(pickel file)
                                            - on failure : Raise Exceptions
                                        Written By : Ninad,Jai Singh
                                        Version : 1.0.0
                                        Revision : None

        """

        try:
            self.model = Prophet(interval_width=0.95, daily_seasonality=True)
            series = self.reformat()
            model_fit = self.model.fit(series)

            if os.path.exists("Models/ProductionModel/{}".format(self.date.past_date())):
                shutil.move("Models/ProductionModel/{}".format(self.date.past_date()), "Models/ArchivedModel",
                            copy_function=shutil.copytree)

            if not os.path.exists("Models/ProductionModel/{}".format(self.date.today_date())):
                os.mkdir("Models/ProductionModel/{}".format(self.date.today_date()))
            filepath = 'Models/ProductionModel/{}/{}.pkl'.format(self.date.today_date(), self.model_name)

            pickle.dump(self.model, open(filepath, 'wb'))

        except Exception as e:
            self.logger.error("Error in Creating or Loading model as ")
            self.logger.exception(e)

    def load_model(self):
        """
                                                Name : create_save_model function
                                                Module : model_training
                                                Description : This function load the model from the production folder
                                                              for current date.
                                                Parameters: None
                                                Returns :
                                                    -  model : type(pickel file)
                                                    - on failure : Raise Exceptions
                                                Written By : Jai Singh
                                                Version : 1.0.0
                                                Revision : None

            """
        try:
            filepath = 'Models/ProductionModel/{}/{}.pkl'.format(self.date.today_date(), self.model_name)
            loaded_model = pickle.load(open(filepath, 'rb'))
            return loaded_model
        except Exception as e:
            self.logger.error("Error in loading model!")
            self.logger.exception(e)

    def futureForecasting(self, periods, freq):
        """
                                                        Name : futureForecasting function
                                                        Module : model_training
                                                        Description : This function does the forecasting of given model
                                                                      for a required period of time.
                                                        Parameters: None
                                                        Returns :
                                                            - future_df  : type(dataframe)
                                                            - on failure : Raise Exceptions
                                                        Written By : Ninad,Jai Singh
                                                        Version : 1.0.0
                                                        Revision : None

        """

        model = self.load_model()

        try:
            forecast = self.model.make_future_dataframe(periods, freq)
            prediction = model.predict(forecast)
            future_df = prediction[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
            return future_df
        except Exception as e:
            self.logger.error("Error in FutureForecasting of {}".format(self.model_name))
            self.logger.exception(e)

    def accuracy_metrics(self, freq, actual_df):
        """
                                                Name : accuracy_metrics function
                                                Module : model_training
                                                Description : This function gives accuracy metrics which involves MAPE,
                                                              ME, MAE, MPE, RMSE, Corr, Min, Max, Minmax
                                                Parameters: None
                                                Returns : Dict of accuracy metrics
                                                - on failure : Raise Exceptions
                                                Written By : Ninad,Jai Singh
                                                Version : 1.0.0
                                                Revision : None

        """

        actual_df = actual_df
        freq = freq
        try:
            future_forecast = self.futureForecasting(periods=0, freq=freq)
            forecast_df = future_forecast["yhat"]
            mape = np.mean(np.abs(forecast_df - actual_df) / np.abs(actual_df))  # MAPE
            me = np.mean(forecast_df - actual_df)  # ME
            mae = np.mean(np.abs(forecast_df - actual_df))  # MAE
            mpe = np.mean((forecast_df - actual_df) / actual_df)  # MPE
            rmse = np.mean((forecast_df - actual_df) ** 2) ** .5  # RMSE
            corr = np.corrcoef(forecast_df, actual_df)[0, 1]  # corr
            mins = np.amin(np.hstack([forecast_df[:, None],
                                      actual_df[:, None]]), axis=1)
            maxs = np.amax(np.hstack([forecast_df[:, None],
                                      actual_df[:, None]]), axis=1)
            minmax = 1 - np.mean(mins / maxs)  # minmax

            return ({'mape': mape, 'me': me, 'mae': mae,
                     'mpe': mpe, 'rmse': rmse,
                     'corr': corr, 'minmax': minmax})
        except Exception as e:
            self.logger.error("Error in accuracy metrics of {}".format(self.model_name))
            self.logger.exception(e)

    def plot_predictions(self, df, forecast, var):
        """
                        Name : plot_predictions function
                        Module : model_training
                        Description : This function plots the forecasted data Vs raw data graph
                        Parameters: None
                        Returns : Plots of Forecast Data VS Raw Data
                        - sensor_name_fig.jpeg : type(graphJSON)
                        - on failure : Raise Exceptions
                        Written By : Ninad,Jai Singh
                        Version : 1.0.0
                        Revision : None

        """


        fig = go.Figure()

        # Add traces
        fig.add_trace(go.Scatter(x=df['ds'], y=df["y"],
                                 mode='lines+markers',
                                 name='actual test ' + var))
        fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast["yhat"],
                                 mode='lines+markers',
                                 name='Forecasted test' + var))

        fig.update_layout(
            title="Actual Vs Forecasted test " + var,
            xaxis_title="Days ",
            yaxis_title="forecasted " + var,
            font=dict(
                family="Courier New, monospace",
                size=16,
                color="RebeccaPurple"
            )
        )
        try:

            if not os.path.exists("Forecast/Production/{}/Plots".format(self.date.today_date())):
                os.mkdir("Forecast/Production/{}/Plots".format(self.date.today_date()))
            fig.write_image("Forecast/Production/{}/Plots/{}_fig.jpeg".format(self.date.today_date(), format(var)))
        except Exception as e:
            self.logger.info("Error in creating plots for {}".format(self.model_name))
            self.logger.exception(e)
