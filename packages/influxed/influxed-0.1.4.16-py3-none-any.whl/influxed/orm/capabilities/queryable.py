from influxed.orm.capabilities.executable import executable
from influxed.ifql import select

class queryable(executable):

    @property
    def connection_string(self):
        return self.database.connection_string

    @property
    def username(self):
        return self.database.username

    @property
    def mediator(self):
        return self.database.mediator

    @property
    def database(self):
        raise NotImplementedError()
        
    @property
    def __query__(self):
        return select(hook=self).on(self.database.name)
    
    def __select_prefix__(self, show_statement):
        return show_statement

    @property
    def query(self):
        return self.__select_prefix__(self.__query__)
    