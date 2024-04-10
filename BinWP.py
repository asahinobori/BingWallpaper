#-*- coding: utf-8 -*-
#!/usr/bin/python

#
# BinWP.py
# brief     Get Bing Wallpaper (today to 8 day before)
# author    Yousein Chan
# version   2.0
# date      2024.04.09
#
# history   1.0, 2016.01.16, Yousein Chan, Create the file.
#           1.1, 2018.08.14, Yousein Chan, Fixed for Win7, must use BMP file.
#           2.0, 2024.04.09, Yousein Chan, robust code, log, retry for net request failure

import os
import sys
import json
import glob
import logging
import requests
from requests.adapters import HTTPAdapter
from PIL import Image

import win32gui, win32con, win32api

class BingWallpaper(object):
    # Link below will GET BingWallpaper info data (json)
    # "&n=num" define the total num wallpaper info that will return
    URL_FETCH_BING_IMG = "https://global.bing.com/HPImageArchive.aspx?format=js&idx=0&n=8&pid=hp&FORM=BEHPTB&uhd=1&uhdwidth=2560&uhdheight=1440&setmkt=zh-CN&setlang=en"
    URL_DOWNLOAD_BING_IMG = "https://cn.bing.com"
    LOCAL_STORE_FILE = "./wallpaper.jpg"

    def __init__(self, args):
        self._s = requests.Session()
        self._s.mount('http://', HTTPAdapter(max_retries=3))
        self._s.mount('https://', HTTPAdapter(max_retries=3))

        if(len(args) == 0):
            self._n = 0
        else:
            i = int(args[0])
            if(i < 0):
                self._n = 0
            elif(i > 7):
                self._n = 7
            else:
                self._n = i

    def parseImageURL(self, jsondata):
        title = jsondata["images"][self._n]["title"]
        copyright = jsondata["images"][self._n]["copyright"]
        copyrightlink = self.URL_DOWNLOAD_BING_IMG + jsondata["images"][self._n]["copyrightlink"]
        url = self.URL_DOWNLOAD_BING_IMG + jsondata["images"][self._n]["url"]

        logging.info(f"title: {title}")
        logging.info(f"copyright: {copyright}")
        logging.info(f"copyright link: {copyrightlink}")
        logging.info(f"url: {url}")
        return url

    def fetchJSON(self):
        logging.info("Fetch json start")
        url = self.URL_FETCH_BING_IMG
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"}
        try:
            res = self._s.get(url, timeout=5, headers=headers)
            logging.info("Fetch json successfully")
            return res.text
        except requests.exceptions.RequestException as e:
            print(e)
            logging.info("Fetch json failed")
            sys.exit(1)

    def downloadImage(self, url):
        logging.info("Download image start")
        try:
            request = self._s.get(url, timeout=10, stream=True)
            with open(BingWallpaper.LOCAL_STORE_FILE, 'wb') as fh:
                for chunk in request.iter_content(1024 * 1024):
                    fh.write(chunk)
            logging.info("Download image successfully")
        except requests.exceptions.RequestException as e:
            print(e)
            logging.info("Download image failed")
            sys.exit(1)

    def setWallpaper(self):
        # k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
        # win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "10")
        # win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
        logging.info("Set wallpaper start")
        path = os.getcwd()
        bmpImage = Image.open(path+"\\wallpaper.jpg")
        bmpImage.save(path+"\\wallpaper.bmp", "BMP")
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, path+"\\wallpaper.bmp", 1+2)
        logging.info("Set wallpaper successfully")

    def run(self):
        jsondata = json.loads(self.fetchJSON())
        url = self.parseImageURL(jsondata)
        self.downloadImage(url)

# Bing Wallpaper Auto Change Tool start here
if __name__ == '__main__':
    # setup logging
    logging.basicConfig(level=logging.INFO, filename="log.txt", encoding="utf-8", filemode="a",
                        format="%(asctime)s %(levelname)s [%(process)d] %(message)s")
    logging.info("Start")

    # count image existed
    jpgfile_cnt = 0
    for name in glob.glob("*[0-9]*.jpg"):
        jpgfile_cnt += 1

    # backup last wallpaper
    backupname = jpgfile_cnt + 1
    logging.info(f"backup name: {backupname}.jpg")
    if os.path.exists("wallpaper.jpg"):
        os.rename("wallpaper.jpg", str(backupname)+".jpg")
    
    # fetch latest bing wallpaper
    bingWallpaper = BingWallpaper(sys.argv[1:])
    bingWallpaper.run()

    # set wallpaper
    bingWallpaper.setWallpaper()

    logging.info("Done")
    sys.exit(0)

# Note:
# WallpaperStyle
# 0:  The image is centered if TileWallpaper=0 or tiled if TileWallpaper=1
# 2:  The image is stretched to fill the screen
# 6:  The image is resized to fit the screen while maintaining the aspect ratio. (Windows 7 and later)
# 10: The image is resized and cropped to fill the screen while maintaining the aspect ratio. (Windows 7 and later)

# TileWallpaper
# 0: The wallpaper picture should not be tiled
# 1: The wallpaper picture should be tiled
