import requests
import os
from time import sleep
from Exceptions import MaxRetriesException
from ._util import printErrorMessage


class _DataProductFile:
    """
    Donwloads a single data product file
    Is able to poll and wait if required
    """

    def __init__(self, runId: int, index: str, config: list):
        self._runId       = runId
        self._index       = index
        self._config      = config
        self._retries     = 0
        self._status      = 202
        self._downloaded  = False
        self._baseUrl     = '{:s}api/dataProductDelivery'.format(config['baseUrl'])
        self._downloadUrl = ''
        self._filePath    = ''
        self._fileSize    = 0
        self._runningTime = 0
        self._downloadingTime = 0

    
    def download(self):
        """
        Download a file for the data product at runId
        Can poll, wait and retry if the file is not ready to download
        Return the file information
        """
        
        # Do not try to download the file if unnecesary
        if not self._config['download']:
            return 200


        filters = {
            'method': 'download',
            'token': self._config['token'],
            'dpRunId': self._runId,
            'index': self._index
        }

        try:
            #self._log.start('run')
            self._status = 202
            maxRetries = self._config['maxRetries']
            
            
            while self._status == 202:
                response = requests.get(self._baseUrl, filters, timeout=self._config['timeout'])
                self._downloadUrl = response.url
                self._status = response.status_code
                self._retries += 1
                
                if maxRetries > 0 and self._retries > maxRetries:
                    raise MaxRetriesException('   Maximum number of retries ({:d}) exceeded'.format(maxRetries))
                
                # Status 200: file downloaded, 202: processing, 204: no data, 400: error, 404: index out of bounds, 410: gone (file deleted from FTP) 
                if self._status == 200:
                    # File downloaded, get filename from header and save
                    self._downloaded = True
                    self._downloadingTime = round(response.elapsed.total_seconds(), 3)
                    filename = self.extractNameFromHeader(response)
                    self.saveAsFile(response, filename, self._config['overwrite'])
                
                elif self._status == 202:
                    # Still processing, wait and retry
                    sleep(self._config['pollPeriod'])
                
                elif self._status == 204:
                    # No data found
                    print('   No data found.')
                
                elif self._status == 400:
                    # API Error
                    printErrorMessage(response, filters)
                
                elif self._status == 404:
                    # Index too high, no more files to download
                    pass

                else:
                    # Gone
                    print('   FTP Error: File not found. If this product order is recent, retry downloading this product using the method downloadProduct with the runId: ' + runId)
                    printErrorMessage(response, filters)
        
        except Exception:
            raise

        return self._status


    def extractNameFromHeader(self, response):
        """
        In a download request response 200, extracts and returns the file name from the response
        """
        txt = response.headers['Content-Disposition']
        filename = txt.split('filename=')[1]
        return filename


    def saveAsFile(self, response, filename: str, overwrite: bool):
        """
        Saves the file downloaded in the response object, in the outPath, with filename
        If overwrite, will overwrite files with the same name
        """
        # Create outPath directory if not exists
        outPath = self._config['outPath']
        if not os.path.exists(outPath):
            os.makedirs(outPath)
        
        # Save file in outPath if it doesn't exist yet
        filePath = outPath + '/' + filename
        if overwrite or (not os.path.exists(filePath)):
            try:
                open(filePath, 'wb+').write(response.content)
                print('   Saved file: "{:s}"'.format(filePath))
                self._filePath = filePath
                self._fileSize = len(response.content)
            except Exception:
                raise
        else:
            print('   Skipping "{:s}": File already exists.'.format(filePath))



    def getInfo(self, download=False):
        
        if download:
            txtStatus = 'error'
            if self._status == 200:
                txtStatus = 'complete'
            elif self._status == 202:
                txtStatus = 'running'
            elif self._status == 404:
                txtStatus = 'not found'
        else:
            # When the files are not downloaded, prepare placeholder results
            txtStatus = 'complete'
            self._downloadUrl = '{:s}?method=download&token={:s}&dpRunId={:d}&index={:s}'.format(self._baseUrl, self._config['token'], self._runId, str(self._index))
        
        return {
            'url'             : self._downloadUrl,
            'status'          : txtStatus,
            'size'            : self._fileSize,
            'file'            : self._filePath,
            'index'           : self._index,
            'downloaded'      : self._downloaded,
            'fileDownloadTime': float(self._downloadingTime)
        }