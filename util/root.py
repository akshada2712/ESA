from pathlib import Path


class ProjectRoot:
    """
              Name : ProjectRoot Class
              Module : util
              Description : This class is to run give the current project root
                            directory.

              Written By : Jai Singh
              Version : 1.0.0
              Revision : None


    """
    def __init__(self):
        """
                      Name : ProjectRoot Class Constructor
                      Module : util
                      Description : Initiates the instance variable which will
                                    be used by the class
                      Parameters:  root folder of project
                          - root : type(string)
                      Returns : None
                      Written By : Jai Singh
                      Version : 1.0.0
                      Revision : None


            """
        self.root = Path(__file__).parent.parent

    def get_project_root(self) -> Path:
        """
                              Name : get_project_root Class
                              Module : util
                              Description : Return the path of the project
                              Parameters: None
                              Returns :
                                - root : Return the path of the project
                              Written By : Jai Singh
                              Version : 1.0.0
                              Revision : None


        """
        return self.root
