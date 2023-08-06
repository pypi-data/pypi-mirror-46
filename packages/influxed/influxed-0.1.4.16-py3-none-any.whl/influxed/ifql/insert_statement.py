from influxed.ifql.exceptions import MissingArgument
from influxed.ifql.line_protocol import to_lines


class insert_statement_builder(object):
    database = None
    hook = None
    __data__ = None
    __measurement__ = None

    def __init__(self, data=None, hook=None, **kwarg):
        self.__data__ = data if data is not None else {}
        if(isinstance(self.__data__, dict)):
            self.__data__.update(kwarg)
        self.hook = hook

    def on(self, database):
        self.database = database
        return self

    def measurement(self, measurement):
        self.__measurement__ = measurement
        return self

    def data(self, data):
        self.__data__ = data
        return self

    def format_lines(self):
        if(self.__data__ is None or self.database is None or self.__measurement__ is None):
            raise MissingArgument(f'Missing argument database={self.database}, measurement={self.measurement} or data')
        return to_lines(self.__data__, self.__measurement__)

    def format(self):
        return '\n'.join(self.format_lines())

    def exec(self):
        if(self.hook):
            return self.hook.sync_execute(self)
        return self.format()