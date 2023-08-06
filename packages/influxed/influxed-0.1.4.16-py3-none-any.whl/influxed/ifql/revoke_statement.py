from influxed.ifql.statement import common_statement_formatter


class revoke_statement_builder(common_statement_formatter):
    """
        REVOKE [READ,WRITE,ALL] ON <database_name> FROM <username>
    """

    def __init__(self, previleges, hook=None):
        super(grant_statement_builder, self).__init__(self, hook=hook)
        self.__previleges__ = previleges

    def from_(self, username):
        self.username = username
        return self 

    def on(self, database):
        self.__database__ = database
        return self

    def format_from(self):
        return f'FROM {self.username}'

    def format_on(self):
        return f'ON {self.__database__}'

    def format_previleges(self):
        if(isinstance(self.__previleges__, PRIVILEGES)):
            return self.__previleges__.value.split(' ')[0]
        return self.__previleges__.split(' ')[0]

    def format(self):
        return f'REVOKE {self.format_previleges()} {self.format_on()} {self.format_to()}'