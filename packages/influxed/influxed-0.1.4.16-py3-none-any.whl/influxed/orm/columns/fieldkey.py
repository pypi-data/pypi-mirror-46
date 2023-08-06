import pandas as pd
import datetime as dt
from influxed.ifql.functions import Count, Min, Max, Mean, Distinct, Percentile, Derivative, Sum, Stddev, First, Last
from influxed.ifql.column import Key
from influxed.orm.capabilities.queryable import queryable
from influxed.orm.capabilities.insertable import insertable

class FieldKey(Key, queryable, insertable):

    @property
    def database(self):
        return self.__measurement__.database

    @property
    def measurement(self):
        return self.__measurement__
    
    def set_measurement(self, val):
        self.__measurement__ = val
        return self

    def min(self):
        return Min(self)
 
    def max(self):
        return Max(self)
            
    def mean(self):
        return Mean(self)
          
    def percentile(self):
        return Percentile(self)
           
    def derivative(self):
        return Derivative(self)
            
    def sum(self):
        return Sum(self)
            
    def std(self):
        return Stddev(self)
    


    def __select_prefix__(self, select_statement):
        return select_statement.from_(self.measurement.name).select(self)
