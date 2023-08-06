from influxed.orm.capabilities.executable import executable
from influxed.ifql import create

class creatable(executable):
    """
        Definition of a object that can initiate a show query
    """
    def create(self, keyword):
        """
            Function for initiating a create query
        """
        return create(keyword, hook=self)
