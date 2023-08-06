class ONC:
	baseUrl        = "https://data.oceannetworks.ca/"
	token          = None
	showInfo       = False
	outPath        = None
	callsPerSecond = 10
	timeout        = 60


	def __init__(self, token, production=True, showInfo=False, outPath='output', timeout=60):
		self.token = token
		if production:
			self.baseUrl = "https://data.oceannetworks.ca/"
		else:
			self.baseUrl = "https://qa.oceannetworks.ca/"
		self.showInfo = showInfo
		self.outPath = outPath
		self.timeout = timeout
