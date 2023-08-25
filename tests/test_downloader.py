"""test of downloader"""

import datetime as dt
import os
from pathlib import Path

from unittest import mock
from prism_reader.downloader import Downloader, make_file_name_from_date


def mock_requests_get(date: dt.date) -> bytes:
    """mock of the response for requests.get to test downloader"""
    dir_for_test_data = Path(f"{os.path.dirname(os.path.abspath(__file__))}/data")
    test_file_name = f"PRISM_ppt_stable_4kmD2_{date.isoformat().replace('-', '')}_bil.zip"
    test_file = dir_for_test_data.joinpath(test_file_name)
    file_content = open(test_file, "rb").read()
    return mock.MagicMock(
        status_code=200,
        headers={"Content-Type":"application/zip"},
        content=file_content,
    )


def test_downloader():
    """test downloader"""
    with mock.patch("requests.get", return_value=mock_requests_get(dt.date(2022, 8, 1))):
        downloader = Downloader()
        local_file = downloader.download_date(dt.date(2022, 8, 1))
        assert local_file == Path(make_file_name_from_date("ppt", dt.date(2022, 8, 1)))
