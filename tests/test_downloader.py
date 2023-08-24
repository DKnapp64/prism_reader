"""test of downloader"""

import datetime as dt
import os
from pathlib import Path

from unittest import mock
from prism_reader.downloader import Downloader


def mock_requests_get() -> bytes:
    """mock of the response for requests.get to test downloader"""
    dir_for_test_data = os.path.dirname(os.path.abspath(__file__)).join("data")
    test_file = dir_for_test_data.join("test_file.zip")
    return open(test_file, "rb").read()

@mock.patch("requests.get", return_value=mock_requests_get())
def test_downloader():
    """test downloader"""
    downloader = Downloader()
    local_file = downloader.download_date(dt.date(2023, 8, 1))
    assert local_file == Path("test_file.zip")
