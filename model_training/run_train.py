import shutil
import glob
import pandas as pd
from util.get_past_current_date import Date
from model_training.train import ModelTraining
from util.app_logger import AppLogger
import os


class RunTraining:
    """
             Name : RunTraining Class
             Module : model_training
             Description : This class is to run the training process
                            and its  utilise train class.

             Written By : Ninad,Jai Singh
             Version : 1.0.0
             Revision : None

    """

    def __init__(self):
        """
                                Name : RunTraining Class Constructor
                                Module : model_training
                                Description : Initiates the instance variable which will
                                              be used by the class
                                Parameters:
                                    - date : Create date class object to fetch present and past date
                                    - training_data : Preprocessed data directory path
                                    - logger : Logger Object to log the details

                                Returns : None
                                Written By : Ninad , Jai Singh
                                Version : 1.0.0
                                Revision : None

        """
        self.date = Date()
        self.training_data = "Data/ProcessedDataset"
        log_file = os.path.join("Logs", "Train.Log")
        app_log = AppLogger("Run Training", log_file)
        self.logger = app_log.set_handlers()

    def combine_csv(self):
        """
                                Name : combine_csv function
                                Module : model_training
                                Description : Combines all the raw csv in a single csv to
                                              for preprocessing and send the previous day
                                              combined csv for
                                Parameters: None
                                Returns : None
                                Written By : Akshada , Jai Singh
                                Version : 1.0.0
                                Revision : None

        """
        raw_path = 'Data/RawDataset/{}'.format(self.date.today_date())
        files = glob.glob(raw_path + "/*.csv")

        # archiving the previous day combined csv
        if os.path.exists("Data/RawDataset/{}.csv".format(self.date.past_date())):
            shutil.move("Data/RawDataset/{}.csv".format(self.date.past_date()), "Data/ArchivedDataset")

        # creating combined csv file for all sensor data
        if not os.path.exists("Data/RawDataset/{}.csv".format(self.date.today_date())):
            combined_csv = pd.concat([pd.read_csv(f) for f in files])
            combined_csv.to_csv("Data/RawDataset/{}.csv".format(self.date.today_date()))
            shutil.rmtree(raw_path)

    def run_training(self):
        """
                                        Name : run_training function
                                        Module : model_training
                                        Description : This function does the following task
                                            - Create Forecast Data Folder
                                            - Train and Save Model
                                            - Save Forecast Data, Accuracy Metrics, Plots
                                            - Archive the previous models
                                        Parameters: None
                                        Returns : None
                                            - On Failure : Raise Exception
                                        Written By : Ninad , Jai Singh
                                        Version : 1.0.0
                                        Revision : None

        """

        if os.path.exists("Forecast/Production/{}".format(self.date.past_date())):

            shutil.move("Forecast/Production/{}".format(self.date.past_date()), "Forecast/Archive",
                        copy_function=shutil.copytree)
            os.makedirs("Forecast/Production/{}".format(self.date.today_date()))
        elif os.path.exists("Forecast/Production/{}".format(self.date.today_date())):
            shutil.rmtree("Forecast/Production/{}".format(self.date.today_date()))
            os.makedirs("Forecast/Production/{}".format(self.date.today_date()))
        else:
            os.makedirs("Forecast/Production/{}".format(self.date.today_date()))

        all_files = glob.glob(self.training_data + "/*.csv")
        acc_df = pd.DataFrame(index=['mape', 'me', 'mpe',
                                     'mae', 'rmse',
                                     'corr', 'minmax'])

        self.logger.info("Forecast Dir created for storing today's forecast data.")

        for _, sensor_data in enumerate(all_files):
            # load data
            data = pd.read_csv(sensor_data)
            model_name = sensor_data[22:-4]

            self.logger.info("{} Model Training Started".format(model_name))
            # Model Training
            training = ModelTraining(data, model_name)
            model = training.create_save_model()

            self.logger.info("{} Model Created".format(model_name))

            # Model Forecasting
            fs = training.futureForecasting(periods=4320, freq="Min")

            # save the forecasted data to Prediction service/Forecast/ folder
            if not os.path.exists("Forecast/Production/{}/Data".format(self.date.today_date())):
                os.mkdir("Forecast/Production/{}/Data".format(self.date.today_date()))

            fs.to_csv("Forecast/Production/{}/Data/{}_forecast.csv".format(self.date.today_date(), model_name))
            self.logger.info("{} Forecast Data is Saved".format(model_name))

            # accuracy metrics

            accuracy = training.accuracy_metrics(freq="Min", actual_df=data["y"])

            acc_df[model_name] = accuracy.values()

            # Creating plots and saving it to Plots Folder
            plots = training.plot_predictions(data, fs, model_name)
            self.logger.info("Actual vs Forecast for {} saved.".format(model_name))

            # Save the accuracy_metrics
            try:
                if not os.path.exists("Forecast/Production/{}/Metrics".format(self.date.today_date())):
                    os.mkdir("Forecast/Production/{}/Metrics".format(self.date.today_date()))
                acc_df.to_csv("Forecast/Production/{}/Metrics/accuracy.csv".format(self.date.today_date()))
                self.logger.info("Accuracy Metrics for {} saved.".format(model_name))
            except Exception as e:
                self.logger.error("Accuracy Metrics not saved")
                self.logger.exception(e)
