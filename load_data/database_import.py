import codecs
import csv
import os
import shutil
import pymongo
from util.get_past_current_date import Date
from util.app_logger import AppLogger
from util.root import ProjectRoot


class MongoDb:
    """
          Name : MongoDb Class
          Module : database_import
          Description : This class is to fetch the data from
                        the mongodb database where all the data
                        from the sensors are stored.

          Written By : Jai Singh
          Version : 1.0.0
          Revision : None

      """

    def __init__(self):
        """
                        Name : MongoDb Class Constructor
                        Module : database_import
                        Description : Initiates the instance variable which will
                                      be used by the class
                        Parameters:
                            - date : Create date class object to fetch present and past date
                            - project_root : Project Root Directory Object to get parent directory
                            - logger : Logger Object to log the details
                            - server_url : MongoDb Database URL
                            - db : MongoDB Database Name
                            - collections : Create the collection name
                            - csv_path : Raw Dataset path
                        Returns : None
                        Written By : Jai Singh
                        Version : 1.0.0
                        Revision : None

        """
        self.date = Date()
        self.project_root = ProjectRoot().get_project_root()
        app_log = AppLogger("Database Import", os.path.join(self.project_root, 'Logs/ETL.log'))
        self.logger = app_log.set_handlers()
        self.server_url = "mongodb+srv://m001-student:m001-mongodb-basics@esa.gnknw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        self.db = 'ESA'
        self.collections = ["co", "humidity", "lpg", "smoke", "temp"]
        self.csv_path = "Data/RawDataset"

    def connect_to_server(self) -> object:
        """
                        Name : connect_to_server function
                        Module : database_import
                        Description : Create connection to database
                        Parameters: None
                        Returns : Database connection object
                            - db  : type(Mongodb Object)
                            - on failure : Raise Exceptions
                        Written By : Jai Singh
                        Version : 1.0.0
                        Revision : None

        """

        try:
            client = pymongo.MongoClient(self.server_url)
            self.logger.info("Sever Connected !")
            try:
                db = client[self.db]
                return db
            except ConnectionError:
                self.logger.exception("Cant not connect to db !")
        except ConnectionError:
            self.logger.exception("Can not connect to server!")
        except Exception as e:
            self.logger.exception(e)

    def import_to_csv(self):
        """
                                Name : import_to_csv function
                                Module : database_import
                                Description : Fetch all the data from database and store
                                              collection wise csv
                                Parameters: None
                                Returns : Collection Wise Csv
                                    - sensor.csv : type(Mongodb Object)
                                    - on failure : Raise Exceptions
                                Written By : Jai Singh
                                Version : 1.0.0
                                Revision : None

        """

        # checking whether the folder for current data is present or not
        try:
            # if project root is present the change the directory to Data/RawDataset
            if os.path.isdir(os.path.join(self.project_root, self.csv_path)):
                os.chdir(os.path.join(self.project_root, self.csv_path))

                # if above statement is ture then check whether the directory
                # still exist if yes then delete existing directory and create
                # directory for today date and change the current working to today's date folder
                if os.path.isdir(os.path.join(self.project_root, self.csv_path, self.date.today_date())):
                    shutil.rmtree(os.path.join(self.project_root, self.csv_path, self.date.today_date()))
                    os.mkdir(os.path.join(self.project_root, self.csv_path, self.date.today_date()))
                    os.chdir(os.path.join(self.project_root, self.csv_path, self.date.today_date()))

                else:
                    os.mkdir(os.path.join(self.project_root, self.csv_path, self.date.today_date()))
                    os.chdir(os.path.join(self.project_root, self.csv_path, self.date.today_date()))
        except FileNotFoundError:
            self.logger.exception("Raw Dataset Folder not present")
        except Exception as e:
            self.logger.exception(e)

        # connecting to the server and then saving all the sensors data in the individual csv

        db = self.connect_to_server()

        try:
            for _, sensor in enumerate(self.collections):
                collection = db[sensor]
                self.logger.info("Writing data on {}.csv".format(sensor))
                cursor = collection.find()
                # csv file
                file = sensor + ".csv"
                try:
                    with codecs.open(file, 'w', 'utf-8') as csvfile:
                        writer = csv.writer(csvfile)
                        # Write column_name first
                        writer.writerow(["Datetime", sensor])
                        # Write multiple lines with writerows
                        for data in cursor:
                            writer.writerows([[data["Datetime"], data[sensor]]])

                    self.logger.info("{}.csv file created".format(sensor))
                except OSError:
                    self.logger.exception("{}.csv file created".format(sensor))
                except Exception as e:
                    self.logger.exception(e)
        except ConnectionError:
            self.logger.exception("Not able to find {} data in database".format(sensor))
        except Exception as e:
            self.logger.exception(e)
