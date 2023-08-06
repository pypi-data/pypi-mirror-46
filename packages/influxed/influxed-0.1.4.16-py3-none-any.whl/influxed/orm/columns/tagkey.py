from enum import Enum
import pandas as pd
from influxed.ifql.column import Key
from influxed.orm.capabilities.queryable import queryable

class TagKey(Key, queryable):
    

    @property
    def database(self):
        return self.__measurement__.database

    @property
    def measurement(self):
        return self.__measurement__
    
    def set_measurement(self, val):
        self.__measurement__ = val
        return self

    def insert(self, val):
        """
            Insert a str, enum, or tuple of val and time or a pandas series of tags
        """
        if(isinstance(val, (str, bytes))):
            pass
        elif(issubclass(val, Enum)):
            pass
        elif(isinstance(val, (tuple, list))):
            val, time = val
            pass
        elif(isinstance(val, pd.Series)):
            pass

    def __select_prefix__(self, select_statement):
        return select_statement.from_(self.measurement.name).select(self)
