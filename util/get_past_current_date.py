from datetime import datetime


class Date:
    """
                    Name: Date Class
                    Module : util
                    Description: This class is used to get current day date
                    and previous day date.
                    Written By: Jai Singh
                    Version: 1.0
                    Revisions: None
    """

    def __init__(self):
        """
                        Name: Date Class Constructor
                        Module : util
                        Description: Initiates the instance variable which will
                                     be used by the class
                        Parameters :
                            - now : Today's Date and Time
                            - year : Current year
                            - month : Current Month
                            - day : Current Day
                            - current_date : Current date in format ("%d-%m-%Y")
                        Returns : None
                        Written By: Jai Singh
                        Version: 1.0
                        Revisions: None
        """

        self.now = datetime.now()  # current date and time
        self.year = self.now.strftime("%Y")
        self.month = self.now.strftime("%m")
        self.day = self.now.strftime("%d")
        self.current_date = self.now.strftime("%d-%m-%Y")

    def today_date(self):
        """
                    Name: today_date function
                    Module : util
                    Description: This function is used to get current day date.
                    Parameters : None
                    Returns : Todays Date
                        -todays_date : type(date)
                    On Failure: None
                    Written By: Jai Singh
                    Version: 1.0
                    Revisions: None
        """
        todays_date = self.current_date
        return todays_date

    def past_date(self):
        """
                    Name: today_date function
                    Module : util
                    Description: This function is used to get previous day date.
                    Parameters : None
                    Returns : Previous Date
                        -previous_date : type(date)
                    On Failure: None
                    Written By: Jai Singh
                    Version: 1.0
                    Revisions: None
        """
        past_day = str(int(self.day) - 1)
        previous_date = past_day + "-" + self.month + "-" + self.year

        return previous_date
