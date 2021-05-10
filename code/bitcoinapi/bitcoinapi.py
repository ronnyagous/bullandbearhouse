  GNU nano 3.2                                                                                                   bitcoinapi/bitcoinapi.py                                                                                                             
import urllib.request, json
from datetime import datetime, timedelta

import logging

class bbh_bitcoinapi:

    apiBaseUrl = 'https://api.coincap.io/v2'

    def __init__(self):
        logging.debug(f'{self.apiBaseUrl}')

    def currentPrice(self, coin):
        result = None
        reqUrl = f'{self.apiBaseUrl}/assets/{coin}'

        logging.debug(reqUrl)

        request = urllib.request.Request(reqUrl, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(request) as response:
            codedData = json.loads(response.read())
            result = codedData['data']

        return result

    def rate(self, currency):
        result = None
        reqUrl = f'{self.apiBaseUrl}/rates/{currency}'

        logging.debug(reqUrl)

        request = urllib.request.Request(reqUrl, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(request) as response:
            codedData = json.loads(response.read())
            result = codedData['data']

        return result


    def history(self, coin):
        result = None

        interval = 'm1'
        starttime = int(datetime.timestamp(datetime.now() - timedelta(hours=24))) * 1000
        endtime = int(datetime.timestamp(datetime.now())) * 1000

        reqUrl = f'{self.apiBaseUrl}/assets/{coin}/history?interval={interval}&start={starttime}&end={endtime}'

        logging.debug(reqUrl)

        req = urllib.request.Request(reqUrl, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as url:
            codedData = json.loads(url.read())
            result = codedData['data']

        return result
