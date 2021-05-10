#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pictures')

libdir = '/home/pi/e-Paper/RaspberryPi_JetsonNano/python/lib'
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd1in54b_V2, epd1in54_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

class bbh_display:

    epd = None
    isThreeColor = False

    def __init__(self, threeColor = False):
        self.isThreeColor = threeColor
        if (self.isThreeColor):
            self.epd = epd1in54b_V2.EPD()
        else:
            self.epd = epd1in54_V2.EPD()

    def clear(self):
        self.epd.init()
        self.epd.Clear()


    def displayRate(self, priceUsd, bitcoinHistory, vwap24Hr, coinName, rateUsd, currencySymbol):

        price = priceUsd / rateUsd

        self.epd.init()

        blackimage = Image.new('1', (self.epd.width, self.epd.height), 255)  # 255: clear the frame
        drawblack = ImageDraw.Draw(blackimage)

        redimage = Image.new('1', (self.epd.width, self.epd.height), 255)  # 255: clear the frame
        drawred = ImageDraw.Draw(redimage)

        # Step 1: Display priceUsd

        testFontSize = 10
        testFont = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), testFontSize)

        if (price < 1):
            priceText = f'{currencySymbol} {price:.4f}'
        elif (price < 100):
            priceText = f'{currencySymbol} {price:.2f}'
        else:
            priceText = f'{currencySymbol} {price:.0f}'

        priceTextTestSize = testFont.getsize(priceText)
        padding = 2
        availableWidth = self.epd.width - (2 * padding)
        fontSize = int((availableWidth / priceTextTestSize[0]) * testFontSize)
        font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), fontSize)
        drawblack.text((padding, padding), f'{priceText}', font = font, fill = 0)

        priceTextSize = font.getsize(priceText)


        smallFont = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)

        # Step 2: Display coin name

        coinNameSize = smallFont.getsize(coinName)
        coinNameLeft = int((self.epd.width - coinNameSize[0])/2)
        coinNameTop = padding + priceTextSize[1] + padding
        drawblack.text((coinNameLeft, coinNameTop), coinName, font = smallFont, fill = 0x00)


        # Step 3: Display graph


        topMargin = coinNameTop + coinNameSize[1] + padding
        leftMargin = padding
        rightMargin = padding
        availableHeight = self.epd.height - padding - topMargin
        availableWidth = self.epd.width - leftMargin - rightMargin

        minPrice = float(min(bitcoinHistory, key=lambda h: h['priceUsd'])['priceUsd']) / rateUsd
        maxPrice = float(max(bitcoinHistory, key=lambda h: h['priceUsd'])['priceUsd']) / rateUsd

        priceCount = len(bitcoinHistory)

        previousPoint = None

        for index, history in enumerate(bitcoinHistory):

            price = float(bitcoinHistory[index]['priceUsd']) / rateUsd

            x = int(leftMargin + ((index / priceCount) * availableWidth))
            y = int(topMargin + (((maxPrice - price ) / (maxPrice - minPrice)) * availableHeight))

            if (previousPoint != None):
                drawblack.line((previousPoint[0], previousPoint[1], x, y), fill = 0, width = 3)

            previousPoint = (x,y)

        averageY = int(topMargin + (((maxPrice - vwap24Hr ) / (maxPrice - minPrice)) * availableHeight))

        drawblack.line((leftMargin, averageY, leftMargin + availableWidth, averageY), fill = 0, width = 1)



        percChange = ((priceUsd - vwap24Hr)/(vwap24Hr)) * 100
        percChangeText = f'{percChange:.2f}%'
        percChangeTextSize = smallFont.getsize(percChangeText)

        if (priceUsd > vwap24Hr):
            drawblack.rectangle((leftMargin + availableWidth - percChangeTextSize[0], topMargin + availableHeight - percChangeTextSize[1],leftMargin + availableWidth , topMargin + availableHeight), fill = 0xFF)
            drawblack.text((leftMargin + availableWidth - percChangeTextSize[0], topMargin + availableHeight - percChangeTextSize[1]), percChangeText, font = smallFont, fill = 0x00)
        else:
            drawblack.rectangle((leftMargin + availableWidth - percChangeTextSize[0], topMargin, leftMargin + availableWidth, topMargin +  percChangeTextSize[1]), fill = 0xFF)
            drawblack.text((leftMargin + availableWidth - percChangeTextSize[0], topMargin), percChangeText, font = smallFont, fill = 0x00)


        if (maxPrice < 1):
            maxText = f'{maxPrice:.4f}'
        elif (maxPrice < 100):
            maxText = f'{maxPrice:.2f}'
        else:
            maxText = f'{maxPrice:.0f}'

        if (minPrice < 1):
            minText = f'{minPrice:.4f}'
        elif (minPrice < 100):
            minText = f'{minPrice:.2f}'
        else:
            minText = f'{minPrice:.0f}'

        maxTextSize = smallFont.getsize(maxText)
        minTextSize = smallFont.getsize(minText)

        drawblack.rectangle((padding, topMargin,padding + maxTextSize[0], topMargin + maxTextSize[1]), fill = 0xFF)
        drawblack.text((padding, topMargin), maxText, font = smallFont, fill = 0)
        drawblack.rectangle((padding, topMargin + availableHeight - minTextSize[1], padding + minTextSize[0], topMargin + availableHeight ), fill = 0xFF)
        drawblack.text((padding, topMargin + availableHeight - minTextSize[1]), minText, font = smallFont, fill = 0)



        if (self.isThreeColor):
            self.epd.display(self.epd.getbuffer(blackimage.rotate(180)),self.epd.getbuffer(redimage.rotate(180)))
        else:
            self.epd.display(self.epd.getbuffer(blackimage.rotate(180)))

    def gotoSleep(self):
        logging.info("Goto Sleep...")
        self.epd.sleep()


