
class executable(object):

    @property
    def mediator(self):
        return self.__mediator__

    @property
    def connection_string(self):
        return self.__connection_string__

    @property
    def username(self):
        return self.__username__

    def execute(self, query):
        return self.mediator.execute(query, connection_string=self.connection_string, username=self.username)
