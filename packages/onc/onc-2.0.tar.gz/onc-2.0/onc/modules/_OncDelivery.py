from datetime import datetime, timedelta
import requests
import os
import humanize
from time import sleep, time
from Exceptions import MaxRetriesException
from util.util import printErrorMessage
from modules._DataProductFile import _DataProductFile
from modules._PollLog import _PollLog

class _OncDelivery:
    """
    Holds the methods that wrap the API data product delivery services
    """
    pollPeriod = 2.0 # Default seconds to wait between consecutive download tries of a file (when no estimate processing time is available)

    
    def orderDataProduct(self, filters, maxRetries: int = 0, downloadResultsOnly: bool = False, includeMetadataFile: bool = True, overwrite: bool = False):
        config = {
            'maxRetries': maxRetries,
            'overwrite' : overwrite,
            'outPath'   : self.outPath,
            'token'     : self.token,
            'baseUrl'   : self.baseUrl,
            'timeout'   : self.timeout,
            'download'  : not downloadResultsOnly,
            'metadata'  : includeMetadataFile
        }
        url = '{:s}api/dataProductDelivery'.format(self.baseUrl)

        try:
            # Request the product
            dpRequestId = self.requestProduct(url, filters)
            config['pollPeriod'] = self.pollPeriod
            
            # Run the product and get the dpRunIds
            runInfo = self.runProduct(url, dpRequestId)
            
            # For all runIds, wait for generation and download if required
            fileList = []
            for runId in runInfo['runIds']:
                if config['download']:
                    fileList.extend(self.downloadProductFiles(config, runId))
                else:
                    fileList.extend(self.infoForProductFiles(config, runId, runInfo['fileCount']))

            # Print the final stats
            self.printTotalStats(fileList, runInfo)

        except Exception: raise

        return self.generateStats(fileList, runInfo)

        
    def requestProduct(self, url, filters):
        """
        Data product request
        """
        filters['method'] = 'request'
        filters['token']  = self.token
        try:
            response = self._doRequest(url, filters)
        except Exception: raise
    
        self.estimatePollPeriod(response)
        self.printProductRequest(response)
        return response['dpRequestId']

    
    def runProduct(self, url, dpRequestId):
        """
        Run a product request and wait until the product generation is complete
        Return a dictionary with information of the run process
        """
        status = ''
        log = _PollLog(True)
        runResult = {'runIds': [], 'fileCount': 0, 'runTime': 0, 'requestCount': 0}
        try:
            start = time()
            while status != 'complete':
                response = requests.get(url, {'method': 'run', 'token': self.token, 'dpRequestId': dpRequestId}, timeout=self.timeout)
                runResult['requestCount'] += 1

                if response.ok:
                    data = response.json()
                else:
                    code = response.status_code
                    if self.showInfo: util.printErrorMessage(response, params)
                    raise Exception('The server request failed with HTTP status {:d}.'.format(code), code)
                
                status = data[0]['status']
                log.logMessage(data)
                sleep(self.pollPeriod)
            
            runResult['fileCount'] = data[0]['fileCount']
            runResult['runTime'] = time() - start
        except Exception: raise
        
        # gather a list of runIds
        for run in data:
            runResult['runIds'].append(run['dpRunId'])

        return runResult
            
    
    def downloadProductFiles(self, config: list, runId: int):
        fileList = []
        index = 1
        try:
            # wait until product has been generated
            status = 200
            print('Downloading data product files with runId {:d}...'.format(runId))
            while status == 200:
                pf = _DataProductFile(runId, str(index), config)
                status = pf.download()
                if status != 404:
                    fileList.append(pf.getInfo())
                index += 1

            # get metadata if required
            if config['metadata']:
                pf = _DataProductFile(runId, 'meta', config)
                status = pf.download()
                if status != 404:
                    fileList.append(pf.getInfo(download=True))

        except Exception: raise

        return fileList


    def infoForProductFiles(self, config: list, runId: int, fileCount: int):
        fileList = []
        self.print(fileCount)
        for index in range(1, fileCount + 1):
            pf = _DataProductFile(runId, str(index), config)
            self.print(index)
            fileList.append(pf.getInfo(download=False))

        if config['metadata']:
            pf = _DataProductFile(runId, 'meta', config)
            fileList.append(pf.getInfo(download=False))

        return fileList


    def printProductRequest(self, response):
        """
        Prints the information from a response given after a data product request
        The request response format might differ depending on the product source (archive or generated on the fly)
        """
        isGenerated = ('estimatedFileSize' in response)
        print('Request Id: {:d}'.format(response['dpRequestId']))
        
        if isGenerated:
            print('Estimated File Size: {:s}'.format(response['estimatedFileSize']))
            print('Estimated Processing Time: {:s}'.format(response['estimatedProcessingTime']))
        else:
            print('File Size: {:s}'.format(response['fileSize']))
            print('Data product is ready for download.')


    def estimatePollPeriod(self, response):
        """
        Sets a poll period adequate to the estimated processing time
        Longer processing times require longer poll periods to avoid going over maxRetries
        """
        # Parse estimated processing time
        txtEstimated = response['estimatedProcessingTime']
        parts = txtEstimated.split(' ')
        if len(parts) == 2:
            unit = parts[1]
            factor = 1
            if unit   == 'min':
                factor = 60
            elif unit == 'hour':
                factor = 3600
            total = factor * int(parts[0])
            self.pollPeriod = max(0.02 * total, 1.0) # poll every 2%
        else:
            # No estimated processing time available, so we keep the default
            pass


    def printTotalStats(self, fileList: list, runInfo: dict):
        """
        Prints a formatted representation of the total time and size downloaded
        after the product order finishes
        """
        downloadCount = 0
        downloadTime = 0
        size = 0
        
        for file in fileList:
            size += file["size"]
            if file["downloaded"]:
                downloadCount += 1
                downloadTime  += file['fileDownloadTime']

        # Print run time
        runTime = timedelta(seconds=runInfo['runTime'])
        print('Total run time: {:s}'.format(humanize.naturaldelta(runTime)))

        # Print download time
        if downloadTime < 1.0:
            txtDownTime = '{:.3f} seconds'.format(downloadTime)
        else:
            txtDownTime = humanize.naturaldelta(downloadTime)
        print('Total download Time: {:s}'.format(txtDownTime))

        # Print size and count of files
        print('{:d} files ({:s}) downloaded'.format(downloadCount, humanize.naturalsize(size)))
        

    def generateStats(self, fileList: list, runInfo: dict):
        size = 0
        downloadTime = 0
        for file in fileList:
            downloadTime += file['fileDownloadTime']
            size += file['size']

        result = {
            'downloadResults': fileList,
            'stats': {
                'runTime'     : round(runInfo['runTime'], 3),
                'downloadTime': round(downloadTime, 3),
                'requestCount': runInfo['requestCount'],
                'totalSize'   : size
            }
        }

        return result