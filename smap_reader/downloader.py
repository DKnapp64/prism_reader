"""module for the connection to the PRISM Oregon State FTP server"""

import datetime as dt
import requests
from pathlib import Path

import attrs

URL_DAILY = "https://ftp.prism.oregonstate.edu/daily" 


def is_downloadable(url: str):
    """Simple function to test is URL is downloadable"""
    r = requests.get(url, allow_redirects=True, timeout=10)
    content_type = r.headers.get("Content-Type")
    if "zip" in content_type.lower():
        return True
    return False


@attrs.define
class Downloader:
    """A simple downloader"""
    url: str = URL_DAILY

    def download_date(self, date: dt.date) -> Path:
        """Function to download all data for a given date"""
        parameters = ["ppt", "tdmean", "tmax", "tmean", "tmin", "vpdmax", "vpdmin"]
        for param in parameters:
            file_name = f"PRISM_{param}_stable_4kmD2_{date.isoformat().replace('-', '')}_bil.zip"
            file_url = f"{URL_DAILY}/{param}/{date.year}/{file_name}"
            if is_downloadable(file_url):
                r = requests.get(file_url, allow_redirects=True, timeout=10)
                zip_file = r.content()


