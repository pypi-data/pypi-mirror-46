# Near real-time services methods

class _OncRealTime:
    def getDirectScalar(self, filters: dict=None):
        '''
        Method to return scalar data from the scalardata service in JSON Object format
        which match filter criteria defined by a dictionary of filters.
        see https://wiki.oceannetworks.ca/display/help/scalardata+service for usage and available filters
        '''

        url = '{:s}api/properties'.format(self.baseUrl)
        filters['method'] = 'getByLocation'
        filters['token'] = self.token

        return self._doRequest(url, filters)

    
    def getDirectRawByLocation(self, filters: dict={}):
        '''
        Method to return raw data from an instrument, in the payload, in JSON format from the rawdata service 
        which match filter criteria defined by a dictionary of filters
        see https://wiki.oceannetworks.ca/display/help/rawdata+service for usage and available filters
        '''
        url = '{:s}api/rawdata'.format(self.baseUrl)
        filters['method'] = 'getByLocation'
        filters['token'] = self.token
        
        return self._doRequest(url, filters)


    def getDirectRawByDevice(self, filters={}):
        '''
        Method to return raw data from an instrument, in the payload, in JSON format from the rawdata service 
        which match filter criteria defined by a dictionary of filters
        see https://wiki.oceannetworks.ca/display/help/rawdata+service for usage and available filters
        '''
        url = '{:s}api/rawdata'.format(self.baseUrl)
        filters['method'] = 'getByDevice'
        filters['token'] = self.token

        return self._doRequest(url, filters)