import os

import numpy as np
import pandas as pd

from util.app_logger import AppLogger
from util.get_past_current_date import Date
from util.root import ProjectRoot


class DataPreprocessing:
    """
        Name : Data Preprocessing Class
        Module : data_preprocessing
        Description : This class is to preprocess the data from
                      the sensors and make it fit for training.

        Written By : Jai Singh
        Version : 1.0.0
        Revision : None

    """

    def __init__(self):

        """
                Name : Data Preprocessing Class Constructor
                Module : data_preprocessing
                Description : Initiates the instance variable which will
                              be used by the class
                Parameters:
                    - project_root : Project Root Directory Object to get parent directory
                    - logger : Logger Object to log the details
                    - null_present : Tell whether null values are present or not.
                    - null_counts : Count null values in dataset
                    - date : Create date class object to fetch present and past date
                    - raw_data_path : Directory for Raw Data
                    - processed_data_path : Directory for processed data
                    - columns : Name of all sensors.
                Returns : None
                Written By : Jai Singh
                Version : 1.0.0
                Revision : None

        """

        self.project_root = ProjectRoot().get_project_root()
        app_log = AppLogger("Data Preprocessing", os.path.join(self.project_root, 'Logs/DataPreprocessing.log'))
        self.logger = app_log.set_handlers()
        self.null_present = False
        self.null_counts = 0
        self.date = Date()
        self.raw_data_path = os.path.join(self.project_root, "Data/RawDataset/{}.csv".format(self.date.today_date()))
        self.processed_data_path = os.path.join(self.project_root, "Data/ProcessedDataset")
        self.columns = ["co", "humidity", "lpg", "smoke", "temp"]

    def get_data(self):
        """
                Name : get_data function
                Module : data_preprocessing
                Description : fetch data from Data/RawDataset folder
                Parameters: None
                Returns : Data of csv
                    - df  : type(pandas dataframe)
                    - on failure : Raise Exceptions
                Written By : Jai Singh
                Version : 1.0.0
                Revision : None

        """

        try:

            df = pd.read_csv(self.raw_data_path, sep=",", encoding="utf-8", low_memory=False)
            self.logger.info("Reading data from CSV for preprocessing")
            return df
        except Exception as e:
            self.logger.exception("Error in reading data {}".format(e))
            raise Exception

    def isnull_present(self, data):
        """
                        Name : isnull_present
                        Module : data_preprocessing
                        Description : This method checks whether there are null values present
                                      in the pandas Dataframe or not.
                        Parameters:
                            - data : type(pandas dataframe)
                        Returns :
                            - null_present : type(Boolean Value)
                            - on failure : Raise Exceptions
                        Written By : Jai Singh
                        Version : 1.0.0
                        Revision : None

        """

        self.null_present = False
        data = data
        try:
            self.null_counts = data.isna().sum()  # check for the count of null values per column
            for i in self.null_counts:
                if i > 0:
                    self.null_present = True
                    break
            if self.null_present:  # write the logs to see which columns have null values
                dataframe_with_null = pd.DataFrame()
                dataframe_with_null['columns'] = data.columns
                dataframe_with_null['missing values count'] = np.asarray(data.isna().sum())
                dataframe_with_null.to_csv(os.path.join(self.project_root, 'Data/NullData/', "NullValues.csv"))
                return self.null_present
        except Exception as e:
            self.logger.exception(
                'Exception occurred in is_null_present method of the Preprocessor class. Exception message:  ' + str(e))
            raise Exception()

    def drop_column(self):
        """
                        Name : drop_column
                        Module : data_preprocessing
                        Description : This method drops unnamed columns from dataset
                                      which is created while merging the dataset for resampling.
                        Parameters: None
                        Returns : Cleaned dataframe
                            - df : type(Boolean Value)
                        Written By :  Jai Singh
                        Version : 1.0.0
                        Revision : None

        """
        data = self.get_data()
        df = pd.DataFrame(data)
        df.drop(['Unnamed: 0'], axis=1, inplace=True)
        return df

    def to_datetime(self, df):
        """
                                Name : to_datetime
                                Module : data_preprocessing
                                Description : This method will convert a timestamp column in data into Date time
                                                and set it as index.
                                Parameters:
                                    - df : type(pandas dataframe)
                                Returns :
                                    - df : type(pandas dataframe)
                                    - on failure : Raise Exceptions
                                Written By :  Jai Singh
                                Version : 1.0.0
                                Revision : None

        """

        df["Datetime"] = pd.to_datetime(df['Datetime'])
        df.set_index("Datetime", inplace=True)
        self.logger.info("Data conversion to datetime complete!")
        return df

    def resample_data(self, df):
        """
                        Name : resample_data
                        Module : data_preprocessing
                        Description : This method resample the data by minutes
                                      for model training.
                        Parameters:
                            - df : type(pandas dataframe)
                        Returns :
                            - resample_df : type(pandas dataframe)
                            - on failure : Raise Exceptions
                        Written By : Jai Singh
                        Version : 1.0.0
                        Revision : None

        """
        try:
            resample_df = df.resample("Min").mean()
            self.logger.info("Data resampling complete!")
        except Exception as e:
            self.logger.exception("Data resampling interrupted!")
            self.logger.exception(e)

        return resample_df

    def run_preprocessing(self):
        """
                               Name : run_preprocessing
                               Module : data_preprocessing
                               Description : This method will run all methods present in this module
                                             create csv files acc to the sensor data.
                               Parameters: none
                               Returns :
                                    - preprocessed csv file for all sensors
                                    - on failure : Raise Exceptions
                               Written By :  Jai Singh
                               Version : 1.0.0
                               Revision : None


        """

        self.logger.info("Dropping Unnecessary  Columns.")
        data = self.drop_column()

        self.logger.info("Converting dates to DateTime.")
        df = self.to_datetime(data)

        self.logger.info("Checking null Values.")
        self.isnull_present(df)

        self.logger.info("Resampling the data for model training !")
        df_resampled = self.resample_data(df)

        self.logger.info("Checking null values for resampled data!")
        self.isnull_present(df_resampled)

        try:

            for _, column in enumerate(self.columns):
                df = pd.DataFrame(df_resampled, columns=[column])
                df.to_csv(os.path.join(self.processed_data_path, "{}.csv".format(column)))

            self.logger.info("Sensor Data file preprocessing complete.")

        except Exception as e:
            self.logger.exception("Sensor Data file preprocessing interrupted!")
            self.logger.exception(e)
