#!/usr/bin/env python3

from display import display
from bitcoinapi import bitcoinapi
from servo import servo

import time
import logging

bitcoinApi = bitcoinapi.bbh_bitcoinapi()
display = display.bbh_display(True)

servo = servo.bbh_servo()
servo.set_position(0)

display.clear()
time.sleep(1)

if (True):
    currency = "united-states-dollar"
else:
    currency = "euro"

coin = "bitcoin"


while (True):

    try:
        bitcoin_data = bitcoinApi.currentPrice(coin)
        bitcoinHistory = bitcoinApi.history(coin)
        rate = bitcoinApi.rate(currency)
        
        priceUsd = float(bitcoin_data["priceUsd"])
        vwap24Hr = float(bitcoin_data["vwap24Hr"])
        coinName = bitcoin_data["name"]
        rateUsd = float(rate["rateUsd"])
        currencySymbol = rate["currencySymbol"]

        percentage = ((priceUsd - vwap24Hr)/(vwap24Hr)) * 100

        display.displayRate(priceUsd, bitcoinHistory, vwap24Hr, coinName, rateUsd, currencySymbol)
        display.gotoSleep()

        servo.set_position(percentage)

    except Exception as e:
        print(f'Exception: {e}')

    time.sleep(60)
    
