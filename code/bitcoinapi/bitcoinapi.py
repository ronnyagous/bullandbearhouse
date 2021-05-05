import urllib.request, json
from datetime import datetime, timedelta

import logging

class bbh_bitcoinapi:


    apiUrl = "https://api.coincap.io/v2/assets/bitcoin"

    def __init__(self):
        logging.debug(f'API URl: {self.apiUrl}')

    def currentPrice(self):
        result = None
        request = urllib.request.Request(self.apiUrl, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(request) as response:
            codedData = json.loads(response.read())
            result = codedData['data']

        return result

    def history(self):
        result = None

        interval = 'm1'
        starttime = int(datetime.timestamp(datetime.now() - timedelta(hours=24))) * 1000
        endtime = int(datetime.timestamp(datetime.now())) * 1000

        reqUrl = f'{self.apiUrl}/history?interval={interval}&start={starttime}&end={endtime}'

        logging.debug(reqUrl)

        req = urllib.request.Request(reqUrl, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as url:
            codedData = json.loads(url.read())
            result = codedData['data']

        return result








