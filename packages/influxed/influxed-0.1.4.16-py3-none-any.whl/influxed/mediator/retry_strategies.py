import logging


class a_retry_strategy(object):
    """
        Definition of a retry strategy
    """
    def __init__(self, influx_client):
        self.influx_client = influx_client
        self.logger = logging.getLogger('InfluxedRetryStrat')

    def retry(self, query):
        """
            Called when a request failed
        """
        raise NotImplementedError('This method has not yet been implemented')

    async def async_retry(self, query):
        """
            Retry async
        """
        raise NotImplementedError('This method has not yet been implemented')

class no_retry_strategy(a_retry_strategy):
    """
        Implementation of a retry strategy with no retry.
    """

    def retry(self, query):
        self.logger.warning(f'No response returned')
        return None
    
    async def async_retry(self, query):
        return None

class retry_n_times(a_retry_strategy):
    """
        Implementation of a retry strategy that retries n times
    """
    max_tries = 5

    def __init__(self, influx_client):
        self.number_of_tries = 0
        super(retry_n_times, self).__init__(influx_client)
    
    def retry(self, query):
        self.number_of_tries += 1
        if(self.number_of_tries < self.max_tries):
            return self.influx_client.__send__(query)
        self.logger.info(f'No response returned')
        return None

    async def async_retry(self, query):
        self.number_of_tries += 1
        if(self.number_of_tries < self.max_tries):
            return await self.influx_client.__send__(query)
        self.logger.info(f'No response returned')
        return None
        