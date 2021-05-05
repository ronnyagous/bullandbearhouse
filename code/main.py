
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

while (True):

    try:
        bitcoin_data = bitcoinApi.currentPrice()
        bitcoinHistory = bitcoinApi.history()

        priceUsd = float(bitcoin_data["priceUsd"])
        vwap24Hr = float(bitcoin_data["vwap24Hr"])

        percentage = ((priceUsd - vwap24Hr)/(vwap24Hr)) * 100

        logging.debug(f'priceUsd={priceUsd:.2f} vwap24Hr={vwap24Hr:.2f}')
        
        display.displayRate(priceUsd, bitcoinHistory, vwap24Hr)
        display.gotoSleep()

        servo.set_position(percentage)

    except:
        print('some error')

    time.sleep(60)
    
