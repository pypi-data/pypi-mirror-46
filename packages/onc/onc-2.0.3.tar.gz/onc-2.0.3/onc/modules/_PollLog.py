from typing import List
from requests import Response
from time import time
from decimal import Decimal

class _PollLog:
    """
    A herler for DataProductFile
    Keeps track of the download process information (messages, time, etc.) in a
    single product download process
    """
    def __init__(self, showInfo: bool):
        """
        @param showInfo same as in parent ONC object
        """
        self._messages = []       # unique messages returned during the product order
        self._showInfo = False  
        self._runStart = 0.0      # {float} timestamp (seconds)
        self._runEnd   = 0.0
        self._showInfo = showInfo # flag for writing console messages
        self._doPrintFileCount = True


    def logMessage(self, response: dict):
        """
        Adds a message to the messages list if it's new
        Prints message to console, or "." if it repeats itself
        """
        # Store and print message
        msg = response[0]['status']

        if not self._messages or msg != self._messages[-1]:
            # Detect and print change in the file count
            fileCount = response[0]['fileCount']
            if self._doPrintFileCount and fileCount > 0:
                self.printInfo('\n   {:d} files generated for this data product'.format(fileCount), True)
                self._doPrintFileCount = False

            self._messages.append(msg)
            self.printInfo('\n   ' + msg, True)
        else:
            self.printInfo('.', True)

        
        # Add a last newline for the last message
        if msg == 'complete':
            print('\n')


    def printInfo(self, msg: str, sameLine: bool = False):
        """
        Conditional printing helper
        """
        if self._showInfo:
            if sameLine:
                print(msg, end="", flush=True)
            else:
                print(msg)

    
    def start(self, name: str):
        if name == 'run':
            self._runStart = time()


    def end(self, name: str):
        if name == 'run':
            self._runEnd = time()


    def getRunningTime(self):
        if self._runEnd != 0:
            return round(self._runEnd - self._runStart, 2)
        else:
            return 0