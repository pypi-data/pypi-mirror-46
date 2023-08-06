class _OncDiscovery:
	"""
	Holds the methods that wrap the API discovery services
	"""
	def getLocations(self, filters=None):
		"""
		return a list of locations which match filter criteria defined by a dictionary of filters
		@param filters: Dictionary (optional)
		@return: JSON response object or None if an error happened
		"""
		if filters is None: filters = {}
		url = '{:s}api/locations'.format(self.baseUrl)
		filters['method'] = 'get'
		filters['token'] = self.token

		return self._doRequest(url, filters)


	def getLocationHierarchy(self, filters=None):
		"""
		return a list of locations which match filter criteria defined by a dictionary of filters,
		organized by hierarchy per getTree method
		@param filters: Dictionary (optional)
		@return: JSON response object or None if an error happened
		"""
		if filters is None: filters = {}
		url = '{:s}api/locations'.format(self.baseUrl)
		filters['method'] = 'getTree'
		filters['token'] = self.token

		return self._doRequest(url, filters)


	def getDeployments(self, filters=None):
		"""
		return a list of deployments which match filter criteria defined by a dictionary of filters
		@param filters: Dictionary (optional)
		@return: JSON response object or None if an error happened
		"""
		if filters is None: filters = {}
		url = '{:s}api/deployments'.format(self.baseUrl)
		filters['method'] = 'get'
		filters['token'] = self.token

		return self._doRequest(url, filters)


	def getDevices(self, filters=None):
		"""
		return a list of devices which match filter criteria defined by a dictionary of filters
		@param filters: Dictionary (optional)
		@return: JSON response object or None if an error happened
		"""
		if filters is None: filters = {}
		url = '{:s}api/devices'.format(self.baseUrl)
		filters['method'] = 'get'
		filters['token'] = self.token
		return self._doRequest(url, filters)
		

	def getDeviceCategories(self, filters=None):
		"""
		return a list of device categories which match filter criteria defined by a dictionary of filters
		@param filters: Dictionary (optional)
		@return: JSON response object or None if an error happened
		"""
		if filters is None: filters = {}
		url = '{:s}api/deviceCategories'.format(self.baseUrl)
		filters['method'] = 'get'
		filters['token'] = self.token

		return self._doRequest(url, filters)


	def getProperties(self, filters=None):
		"""
		return a list of properties which match filter criteria defined by a dictionary of filters
		@param filters: Dictionary (optional)
		@return: JSON response object or None if an error happened
		"""
		if filters is None: filters = {}
		url = '{:s}api/properties'.format(self.baseUrl)
		filters['method'] = 'get'
		filters['token'] = self.token

		return self._doRequest(url, filters)


	def getDataProducts(self, filters=None):
		"""
		return a list of data products which match filter criteria defined by a dictionary of filters
		@param filters: Dictionary (optional)
		@return: JSON response object or None if an error happened
		"""
		if filters is None: filters = {}
		url = '{:s}api/dataProducts'.format(self.baseUrl)
		filters['method'] = 'get'
		filters['token'] = self.token

		return self._doRequest(url, filters)
		