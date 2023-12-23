
import uvicorn
from fastapi import FastAPI
import os
from util.app_logger import AppLogger
from load_data.database_import import MongoDb
from data_preprocessing.data_preprocessing import DataPreprocessing
from model_training.run_train import RunTraining
from util.root import ProjectRoot


"""
This file is the main file which contains all the urls
to run etl, model training and deployment.

The application is available at : http://127.0.0.1:8000/docs
"""


project_root = ProjectRoot().get_project_root()  # setting project root location
app_log = AppLogger("Main", os.path.join(project_root, 'Logs/Main.log'))  # adding logger
logger = app_log.set_handlers()

app = FastAPI(
    title="Environment Sensor Analysis APIs",
    description="This is a Environment Sensor Analysis project, with auto docs for the API and everything",
    version="1.0.0",
)

@app.get("/etl", tags=['ETL'])
def load_data():
    """
        Name : ETL API
        Module : main

        Description :This api fetch the data from mongodb atlas and store it as
                    individual csv file with sensor_name.csv
        Parameters:
            - None

        Returns :
            - On Successful run "Data Prepared for training"
            
        Written By : Jai Singh
        Version : 1.0.0
        Revision : None

    """

    logger.info('ETL API Hit')
    etl = MongoDb()
    logger.info('Starting to Import Data')
    etl.import_to_csv()
    logger.info('All the data are fetched from Database and ready to be combined !')
    return {"Data Prepared for training"}


@app.get('/train', tags=['Train'])
def train():
    """
        Name : Train API

        Module : main

        Description :This api does the following task in order
            - Combine all the data from sensors in single csv
            - Preprocessing and Resampling the data
            - Train the models and save the future forecast data and plots
            
        Parameters:
            - None

        Returns :
            - On Successful run "Data Prepared for training"

        Written By : Jai Singh
        Version : 1.0.0
        Revision : None

    """

    os.chdir(project_root)
    model_trainer = RunTraining()
    data_preprocessor = DataPreprocessing()

    logger.info("Train API HIT")
    logger.info('Loading data from RawData !')
    model_trainer.combine_csv()
    logger.info('ETL completed, all sensor data combine csv created')

    logger.info("Data Preprocessing Started !")
    data_preprocessor.run_preprocessing()
    logger.info("Preprocessing Completed !")

    logger.info("Model Training Started !")
    model_trainer.run_training()
    logger.info("Model Training Completed !")

    return {"Training Completed"}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
