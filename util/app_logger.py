import logging


class AppLogger:
    """
                 Name: AppLogger Class
                 Module : util
                 Description: This class is used for logging functionality
                 Written By: Jai Singh
                 Version: 1.0
                 Revisions: None
    """

    def __init__(self, moduleName, path):
        """
                         Name: AppLogger Class Constructor
                         Module : util
                         Description:Initiates the instance variable which will
                                     be used by the class
                         Parameters:
                             - logger :  Logger Object to log the details and it take
                             moduleName as input
                             - path : log file path
                             - logfile : path where logfile is to be created

                         Returns : None
                         Written By: Jai Singh
                         Version: 1.0
                         Revisions: None
        """

        self.logger = logging.getLogger(moduleName)
        self.logFile = path

    def set_handlers(self):
        """
                    Name: set_handlers functions
                    Description: This function is used for setting the
                    configuration of logs, set format of logging message.
                    Parameters : None
                    Returns :
                        - logger : type(Logger Object)

                    Written By: Jai Singh
                    Version: 1.0
                    Revisions: None
        """

        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)

        # setting console and file handler
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(self.logFile)
        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.DEBUG)

        # setting format of log message
        console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_format)
        file_handler.setFormatter(file_format)

        # adding handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        return self.logger
