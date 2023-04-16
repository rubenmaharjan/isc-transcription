from abc import ABC, abstractmethod

class Transcribe(ABC):
    """
           A class to represent the type of forecast chosen for replenishment calculation later.
           e.g. Poor Man's Forecast, Moving Window and so on.

           ...

           Attributes
           ----------
           getDataQuery : string
               The query to get output for current case of executor run.

           insertFrcst : string
               The query to be run into warehouse for calculation and storage of forecast.

           Methods
           -------
           getOutput(result) : formats result of query obtained from Snowflake
               to convert into a ease of use pandas dataframe.

           loadData(start_date, end_date) : Load data of given number of weeks before runtime. Useful
               when running in cron batches

           insertManualForecast(): Inserts manual sku locations along with run_id by passing it
                 directly from the executor itself.

           execute(): Function to be called to run module from DSPExecutor.
    """

    @property
    def insertFrcst(self):
        return self._insertFrcst

    @insertFrcst.setter
    def insertFrcst(self, insertFrcst):
        self._insertFrcst = insertFrcst


    @abstractmethod
    def transcribe(self):
        """
        Creates the class with initial values assigned

        Returns
        -------
        self

        """
