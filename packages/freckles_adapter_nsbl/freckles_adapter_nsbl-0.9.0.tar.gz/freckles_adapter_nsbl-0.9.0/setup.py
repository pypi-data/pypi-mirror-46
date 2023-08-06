#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for freckles_adapter_nsbl.
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

from pkg_resources import VersionConflict, require
from setuptools import setup, Command

# flake8: noqa

try:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError


class CleanExternalDataCommand(Command):
    user_options = []

    def initialize_options(self):
        """Abstract method that is required to be overwritten"""

    def finalize_options(self):
        """Abstract method that is required to be overwritten"""

    def _delete_folder(self, path):

        print("- deleting content from target folder: {}".format(path))
        for the_file in os.listdir(path):
            if the_file == ".gitkeep":
                continue
            file_path = os.path.join(path, the_file)

            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    def _download_archive(self, url, target_path, desc="archive"):

        print("- downloading {} from '{}' to '{}'".format(desc, url, target_path))

        resp = urlopen(url)
        zipfile = ZipFile(BytesIO(resp.read()))
        zipfile.extractall(target_path)

    def run(self):

        target_root = os.path.join(
            os.path.realpath(os.path.dirname(__file__)),
            "src",
            "freckles_adapter_nsbl",
            "external",
            "nsbl-default",
        )
        target_frecklets = os.path.join(target_root, "frecklets")
        target_resources = os.path.join(target_root, "resources")

        self._delete_folder(target_frecklets)
        self._delete_folder(target_resources)

        target_root = os.path.join(
            os.path.realpath(os.path.dirname(__file__)),
            "src",
            "freckles_adapter_nsbl",
            "external",
            "nsbl-community",
        )
        target_frecklets = os.path.join(target_root, "frecklets")
        target_resources = os.path.join(target_root, "resources")

        self._delete_folder(target_frecklets)
        self._delete_folder(target_resources)


class DownloadExternalDataCommand(Command):
    user_options = []

    def initialize_options(self):
        """Abstract method that is required to be overwritten"""

    def finalize_options(self):
        """Abstract method that is required to be overwritten"""

    def _delete_folder(self, path):

        print("- deleting content from target folder: {}".format(path))
        for the_file in os.listdir(path):
            if the_file == ".gitkeep":
                continue
            file_path = os.path.join(path, the_file)

            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    def _download_archive(self, url, target_path, desc="archive"):

        print("- downloading {} from '{}' to '{}'".format(desc, url, target_path))

        resp = urlopen(url)
        zipfile = ZipFile(BytesIO(resp.read()))
        zipfile.extractall(target_path)

    def run(self):

        target_root = os.path.join(
            os.path.realpath(os.path.dirname(__file__)),
            "src",
            "freckles_adapter_nsbl",
            "external",
            "nsbl-default",
        )
        target_frecklets = os.path.join(target_root, "frecklets")
        target_resources = os.path.join(target_root, "resources")
        url_frecklets = "https://gitlab.com/frecklets/frecklets-nsbl-default/-/archive/develop/frecklets-nsbl-default-develop.zip"
        url_resources = "https://gitlab.com/frecklets/frecklets-nsbl-default-resources/-/archive/develop/frecklets-nsbl-default-resources-develop.zip"

        self._download_archive(url_frecklets, target_frecklets, desc="frecklets")
        self._download_archive(
            url_resources, target_resources, desc="frecklet resources"
        )

        target_root = os.path.join(
            os.path.realpath(os.path.dirname(__file__)),
            "src",
            "freckles_adapter_nsbl",
            "external",
            "nsbl-community",
        )
        target_frecklets = os.path.join(target_root, "frecklets")
        target_resources = os.path.join(target_root, "resources")
        url_frecklets = "https://gitlab.com/frecklets/frecklets-nsbl-community/-/archive/develop/frecklets-nsbl-community-develop.zip"
        url_resources = "https://gitlab.com/frecklets/frecklets-nsbl-community-resources/-/archive/develop/frecklets-nsbl-community-resources-develop.zip"

        self._download_archive(
            url_frecklets, target_frecklets, desc="community frecklets"
        )
        self._download_archive(
            url_resources, target_resources, desc="community frecklet resources"
        )


try:
    require("setuptools>=38.3")
except VersionConflict:
    print("Error: version of setuptools is too old (<38.3)!")
    sys.exit(1)


if __name__ in ["__main__", "builtins", "__builtin__"]:
    setup(
        use_scm_version=True,
        cmdclass={
            "download_frecklets": DownloadExternalDataCommand,
            "clean_frecklets": CleanExternalDataCommand,
        },
    )
