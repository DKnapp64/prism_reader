"""module for the connection to the PRISM Oregon State FTP server"""
import os
from pathlib import Path

import datetime as dt
import logging
import requests

from attrs import define

URL_DAILY = "https://ftp.prism.oregonstate.edu/daily" 


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_downloadable(url: str):
    """Simple function to test is URL is downloadable"""
    r = requests.get(url, allow_redirects=True, timeout=10)
    content_type = r.headers.get("Content-Type")
    if "zip" in content_type.lower():
        return True
    return False


def make_file_name_from_date(param: str, date: dt.date):
    return f"PRISM_{param}_stable_4kmD2_{date.isoformat().replace('-', '')}_bil.zip"


@define
class Downloader:
    """A simple downloader"""
    url: str = URL_DAILY

    def download_date(self, date: dt.date) -> Path:
        """Function to download all data for a given date"""
        parameters = ["ppt", "tdmean", "tmax", "tmean", "tmin", "vpdmax", "vpdmin"]
        for param in parameters:
            file_name = make_file_name_from_date("ppt", dt.date(2022, 8, 1))
            file_url = f"{URL_DAILY}/{param}/{date.year}/{file_name}"
            if not is_downloadable(file_url):
                logger.info("%s is not downloadable", file_url)
                continue
            r = requests.get(file_url, allow_redirects=True, timeout=10)
            with open(file_name, 'wb') as fp:
                fp.write(r.content)
            os.remove(file_name) 
            return(Path(file_name))
