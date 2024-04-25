# -*- coding: utf-8 -*-
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
#           2.1, 2024.04.25, Yousein Chan, support other platform

import os
import sys
import json
import glob
import logging
import requests
import argparse
import platform
from requests.adapters import HTTPAdapter
from PIL import Image

if platform.system().lower().startswith("win"):
    import win32gui, win32con


class BingWallpaper(object):
    # Link below will GET BingWallpaper info data (json)
    # "&n=num" define the total num wallpaper info that will return
    URL_FETCH_BING_IMG = "https://global.bing.com/HPImageArchive.aspx?format=js&idx=0&n=8&pid=hp&FORM=BEHPTB&uhd=1&uhdwidth=2560&uhdheight=1440&setmkt=zh-CN&setlang=en"
    URL_DOWNLOAD_BING_IMG = "https://cn.bing.com"
    LOCAL_STORE_FILE = "./wallpaper.jpg"
    LOCAL_STORE_FILE_BMP = "./wallpaper.bmp"
    HTTP_HEADER_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
    HTTP_REQUEST_RETRY = 3
    FETCH_JSON_TIMEOUT = 5
    DOWNLOAD_IMG_TIMEOUT = 10

    def __init__(self, num):
        self._s = requests.Session()
        self._s.mount("http://", HTTPAdapter(max_retries=self.HTTP_REQUEST_RETRY))
        self._s.mount("https://", HTTPAdapter(max_retries=self.HTTP_REQUEST_RETRY))

        if num < 0:
            self._n = 0
        elif num > 7:
            self._n = 7
        else:
            self._n = num

    def fetchJSON(self):
        logger.info("Fetch json start")
        url = self.URL_FETCH_BING_IMG
        timeout = self.FETCH_JSON_TIMEOUT
        headers = {"User-Agent": self.HTTP_HEADER_USER_AGENT}
        try:
            res = self._s.get(url, timeout=timeout, headers=headers)
            logger.info("Fetch json successfully")
            return res.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Fetch json failed, exception: {e}")
            sys.exit(1)

    def parseImageURL(self, jsondata):
        title = jsondata["images"][self._n]["title"]
        copyright = jsondata["images"][self._n]["copyright"]
        copyrightlink = (
            self.URL_DOWNLOAD_BING_IMG + jsondata["images"][self._n]["copyrightlink"]
        )
        url = self.URL_DOWNLOAD_BING_IMG + jsondata["images"][self._n]["url"]

        logger.info(f"title: {title}")
        logger.info(f"copyright: {copyright}")
        logger.info(f"copyright link: {copyrightlink}")
        logger.info(f"url: {url}")
        return url

    def downloadImage(self, url):
        logger.info("Download image start")
        timeout = self.DOWNLOAD_IMG_TIMEOUT
        try:
            request = self._s.get(url, timeout=timeout, stream=True)
            with open(self.LOCAL_STORE_FILE, "wb") as fh:
                for chunk in request.iter_content(1024 * 1024):
                    fh.write(chunk)
            logger.info("Download image successfully")
        except requests.exceptions.RequestException as e:
            logger.error(f"Download image failed, exception: {e}")
            sys.exit(1)

    # only work on Windows system
    def setWallpaper(self):
        logger.info("Set wallpaper start")
        path = os.getcwd()
        bmpImage = Image.open(path + self.LOCAL_STORE_FILE)
        bmpImage.save(path + self.LOCAL_STORE_FILE_BMP, "BMP")
        win32gui.SystemParametersInfo(
            win32con.SPI_SETDESKWALLPAPER, path + self.LOCAL_STORE_FILE_BMP, 1 + 2
        )
        logger.info("Set wallpaper successfully")

    def run(self):
        jsondata = json.loads(self.fetchJSON())
        url = self.parseImageURL(jsondata)
        self.downloadImage(url)


# Bing Wallpaper Auto Change Tool start here
if __name__ == "__main__":
    # setup argument parser
    parser = argparse.ArgumentParser(
        description="Get Bing Wallpaper (today to the day before the 8th day)."
    )
    parser.add_argument(
        "-n", "--num", default=0, type=int, help="the day before the Nth day"
    )
    parser.add_argument(
        "-p",
        "--pure",
        action="store_true",
        help="only download but not set wallpaper",
        dest="pure",
    )
    args = parser.parse_args()

    # setup logging
    logFormatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(process)d] %(message)s"
    )
    logHandler = logging.FileHandler("log.txt", "a", "utf-8")
    logHandler.setFormatter(logFormatter)
    logger = logging.getLogger()
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)

    logger.info("Start")

    # count image existed
    jpgfile_cnt = 0
    for name in glob.glob("*[0-9]*.jpg"):
        jpgfile_cnt += 1

    # backup last wallpaper
    backupname = jpgfile_cnt + 1
    logger.info(f"backup name: {backupname}.jpg")
    if os.path.exists(BingWallpaper.LOCAL_STORE_FILE):
        os.rename(BingWallpaper.LOCAL_STORE_FILE, str(backupname) + ".jpg")

    # fetch latest bing wallpaper
    bingWallpaper = BingWallpaper(args.num)
    bingWallpaper.run()

    # set wallpaper, work on Windows system
    if (not args.pure) and platform.system().lower().startswith("win"):
        bingWallpaper.setWallpaper()

    logger.info("Done")
    sys.exit(0)
