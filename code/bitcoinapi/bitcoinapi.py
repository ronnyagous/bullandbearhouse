import urllib.request, json 
from datetime import datetime, timedelta
import time

import logging

class bbh_bitcoinapi:

    apiBaseUrl = 'https://api.coincap.io/v2'

    def __init__(self):
        logging.debug(f'{self.apiBaseUrl}')

    def currentPrice(self, coin):
        reqUrl = f'{self.apiBaseUrl}/assets/{coin}'
        return self.loadData(reqUrl)


    def rate(self, currency):
        reqUrl = f'{self.apiBaseUrl}/rates/{currency}'
        return self.loadData(reqUrl)


    def history(self, coin):

        interval = 'm5'
        starttime = int(datetime.timestamp(datetime.now() - timedelta(hours=24))) * 1000
        endtime = int(datetime.timestamp(datetime.now())) * 1000

        reqUrl = f'{self.apiBaseUrl}/assets/{coin}/history?interval={interval}&start={starttime}&end={endtime}'
        return self.loadData(reqUrl)


    def loadData(self, reqUrl):
        result = None
        logging.debug(reqUrl)

        maxRetry = 10
        retryInterval = 125

        
        for retry in range(1, maxRetry):

            try:
                req = urllib.request.Request(reqUrl, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as url:
                    codedData = json.loads(url.read())
                    result = codedData['data']
            except urllib.error.HTTPError as e:
                if (e.getcode() == 429):
                    logging.debug(f'Too many request. Pausing {retryInterval} ms.')
                    time.sleep(retryInterval / 1000)
                    retryInterval = retryInterval * 2
                else:
                    logging.error(e)

            if (result != None): break



        return result
