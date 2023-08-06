import requests
import json
from datetime import timedelta
import errno
import puremagic
import humanize
from urllib import parse
from modules._util import printErrorMessage
from modules._OncDiscovery import _OncDiscovery
from modules._OncDelivery import _OncDelivery
from modules._OncRealTime import _OncRealTime
from modules._OncArchive import _OncArchive


class ONC(_OncDiscovery, _OncDelivery, _OncRealTime, _OncArchive):
    
    def __init__(self, token, production: bool=True, showInfo: bool=False, outPath: str='output', timeout: int=60):
        self.token      = token
        self.showInfo   = showInfo
        self.timeout    = timeout

        # sanitize outPath
        outPath = outPath.replace('\\', '/')
        if outPath[-1] == '/':
            outPath = outPath[:-1]
        self.outPath = outPath
        
        if production:
            self.baseUrl = "https://data.oceannetworks.ca/"
        else:
            self.baseUrl = "https://qa.oceannetworks.ca/"


    def print(self, obj, filename: str=""):
        text = json.dumps(obj, indent=4)
        if filename == "":
            print(text)
        else:
            with open(filename, "w+") as file:
                file.write(text)


    def decodeJsonFromUrl(self, url: str):
        '''
        Return a dictionary from the json response of a json data product download url.
        '''
        try:
            return self._doRequest(url, filters)
        except Exception: raise


    def _doRequest(self, url: str, filters: dict=None):
        """
        Generic request wrapper for making simple web service requests
        @param url:    String full url to request
        @param params: Dictionary of parameters to append to the request
        @return:       JSON object obtained on a successful request
        @throws:       Exception if the HTTP request fails with status 400, as a tuple with
                       the error description and the error JSON structure returned
                       by the API, or a generic exception otherwise
        """
        if filters is None: filters = {}
        try:
            self._log('Requesting URL: {:s}{:s}'.format(url, parse.urlencode(filters)))
            response = requests.get(url, filters, timeout=self.timeout)
            
            if response.ok:
                jsonResult = response.json()
            else:
                status = response.status_code
                if status == 400:
                    if self.showInfo:
                        printErrorMessage(response, filters)
                    raise Exception('The request failed with HTTP status 400.', response.json())
                else:
                    raise Exception('The request failed with HTTP status {:d}.'.format(status), response.text)

            elapsed = response.elapsed.total_seconds()
            self._log('Web Service response time: {:s}'.format(self._formatDuration(elapsed)))
        
        except Exception: raise

        self._sanitizeBooleans(jsonResult)
        return jsonResult


    def _sanitizeBooleans(self, data: list):
        """
        For all rows in data, enforce that fields expected to have bool values have the right type
            Will modify the data array
        @param data:   Usually an array of dictionaries
        """
        if not(isinstance(data, list)): return
        if len(data) == 0: return

        fixHasDeviceData = False
        fixHasPropertyData = False

        # check hasDeviceData only if present and of the wrong type
        # for now we only check the first row
        if "hasDeviceData" in data[0]:
            if (type(data[0]["hasDeviceData"]) != bool):   fixHasDeviceData = True
        
        if "hasPropertyData" in data[0]:
            if (type(data[0]["hasPropertyData"]) != bool): fixHasPropertyData = True

        # same for hasPropertyData
        if fixHasDeviceData or fixHasPropertyData:
            for row in data:
                if fixHasDeviceData:
                    row["hasDeviceData"]   = (row["hasDeviceData"] == "true")
                if fixHasPropertyData:
                    row["hasPropertyData"] = (row["hasPropertyData"] == "true")


    
    def _log(self, message: str):
        """
        Prints message to console only when self.showInfo is true
        @param message: String
        """
        if self.showInfo:
            print(message)


    def _formatSize(self, size: float):
        """
        Returns a formatted file size string representation
        @param size: {float} Size in bytes
        """
        return humanize.naturalsize(size)


    def _formatDuration(self, secs: float):
        """
        Returns a formatted time duration string representation of a duration in seconds
        @param seconds: float
        """
        if secs < 1.0:
            txtDownTime = '{:.3f} seconds'.format(secs)
        else:
            d = timedelta(seconds=secs)
            txtDownTime = humanize.naturaldelta(d)

        return txtDownTime


