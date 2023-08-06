#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for tempting.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 3.1.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
import os
import shutil
import sys
from io import BytesIO
from zipfile import ZipFile

# flake8: noqa

try:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError


from pkg_resources import VersionConflict, require
from setuptools import setup, Command


class CleanExternalData(Command):
    user_options = []

    def initialize_options(self):
        """Abstract method that is required to be overwritten"""

    def finalize_options(self):
        """Abstract method that is required to be overwritten"""

    def run(self):
        target = os.path.join(
            os.path.realpath(os.path.dirname(__file__)),
            "src",
            "tempting",
            "external",
            "temptings",
        )
        url = "https://gitlab.com/frecklets/temptings-default/-/archive/develop/temptings-default-develop.zip"

        print("- deleting content from target folder: {}".format(target))
        for the_file in os.listdir(target):
            if the_file == ".gitkeep":
                continue
            file_path = os.path.join(target, the_file)

            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)


class DownloadExternalDataCommand(Command):
    user_options = []

    def initialize_options(self):
        """Abstract method that is required to be overwritten"""

    def finalize_options(self):
        """Abstract method that is required to be overwritten"""

    def run(self):
        target = os.path.join(
            os.path.realpath(os.path.dirname(__file__)),
            "src",
            "tempting",
            "external",
            "temptings",
        )
        url = "https://gitlab.com/frecklets/temptings-default/-/archive/develop/temptings-default-develop.zip"

        print("- downloading temptings from '{}' to '{}'".format(url, target))

        resp = urlopen(url)
        zipfile = ZipFile(BytesIO(resp.read()))
        zipfile.extractall(target)


try:
    require("setuptools>=38.3")
except VersionConflict:
    print("Error: version of setuptools is too old (<38.3)!")
    sys.exit(1)


if __name__ in ["__main__", "builtins", "__builtin__"]:
    setup(
        use_scm_version=True,
        cmdclass={
            "download_temptings": DownloadExternalDataCommand,
            "clean_temptings": CleanExternalData,
        },
    )
