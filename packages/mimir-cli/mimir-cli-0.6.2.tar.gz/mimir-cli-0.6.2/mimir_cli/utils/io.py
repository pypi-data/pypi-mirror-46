"""
where the helpers go
"""
import errno
import os
import requests
from datetime import datetime
from mimir_cli.globals import PACKAGE, __version__
from distutils.version import StrictVersion


def date_fmt(_date):
    """returns a standard formatted date given a datetime"""
    return _date.strftime("%b %d, %Y %H:%M")


def parse_iso_date(date_str):
    """given an iso date, parse into a date"""
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")


def mkdir(path):
    """creates a folder if it doesnt exist"""
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def get_versions():
    """fetch versions of mimir-cli"""
    response = requests.get("https://pypi.python.org/pypi/{}/json".format(PACKAGE))
    versions = list(response.json()["releases"].keys())
    versions.sort(key=StrictVersion, reverse=True)
    return versions


def is_latest():
    """check if we have the latest (or later) version of mimir-cli"""
    latest = StrictVersion(get_versions()[0])
    current = StrictVersion(__version__)
    return current >= latest
