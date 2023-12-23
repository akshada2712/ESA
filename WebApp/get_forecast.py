import pickle
import datetime as dt
from fbprophet import Prophet
from pathlib import Path

import os


class get_data:

    def __init__(self, sensor):

        """
                Name : Get Data Class
                Module : get_forecast
                Description : It loads the required model and does the forecasting on
                            that model .
                Parameters:
                    - sensor : Name of sensor Choosen.
                Returns : None
                Written By : Ninad
                Version : 1.0.0
                Revision : None

        """
        self.sensor = sensor

    def load_model(self):
        """
                                        Name : load_model function
                                        Module : get_forecast
                                        Description : loads the required model.pkl file for forecasting.
                                        Parameters: None
                                        Returns : laoded model
                                        Written By : Ninad
                                        Version : 1.0.0
                                        Revision : None

                """
        #load the model from disk
        root = Path(__file__).parent
        filepath = os.path.join(root,"Models/ProductionModel/{}.pkl".format(self.sensor))
        loaded_model = pickle.load(open(filepath, 'rb'))
        print("{}model created".format(self.sensor))
        return loaded_model

    def get_forecasted_data(self):
        """
                                                Name : get_forecasted_data function
                                                Module : get_forecast
                                                Description : Creates a  forecast dataframe for a given model
                                                                and does the prediction for given periods and
                                                                freq.
                                                Parameters: None
                                                Returns : future_df (dataframe)
                                                Written By : Ninad
                                                Version : 1.0.0
                                                Revision : None

        """
        model = self.load_model()
        forecast = model.make_future_dataframe(periods=5760, freq="Min")
        prediction = model.predict(forecast)
        future_df = prediction[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        print("{} sensor data Forecasted".format(self.sensor))

        return future_df
