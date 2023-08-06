import datetime as dt
from influxed.orm.capabilities.executable import executable
from influxed.ifql.insert_statement import insert_statement_builder


class insertable(executable):

    def __build_inserts__(self, val):
        if(hasattr(self, 'name')):
            if(isinstance(val, (int, float))):
                val = (val, dt.datetime.now())
            if(isinstance(val, (tuple))):
                val, time = val
                if(isinstance(val, dt.datetime)):
                    tmp = val
                    val = time
                    time = tmp
                val = {
                    'time': time,
                    getattr(self, 'name'): val
                }
        
        statement = insert_statement_builder(data=val, hook=self)
        return self.__insert_prefix__(statement)

    def __insert_prefix__(self, insert_statement):
        return insert_statement

    def insert(self, val, measurement=None):
        """
            Insert int, float, double, etc. or tuple of time and value or pandas series
        """
        self.execute(self.__build_inserts__(val))

