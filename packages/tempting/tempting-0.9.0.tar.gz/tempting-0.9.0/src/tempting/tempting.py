# -*- coding: utf-8 -*-

"""Main module."""

import logging
import os

from .defaults import (
    TEMPTING_CONTEXT_SCHEMA,
    TEMPTING_LOAD_CONFIG,
    DEFAULT_TEMPTINGS_FOLDER,
)
from ting.tings import TingTings

log = logging.getLogger("tempting")


class TemptingContext(object):
    def __init__(self, context_name, cnf, repos=None):

        self._context_name = context_name
        self._cnf = cnf
        self._context_config = cnf.add_interpreter("context", TEMPTING_CONTEXT_SCHEMA)

        if repos is None:
            repos = [DEFAULT_TEMPTINGS_FOLDER]

        self.repos = repos

        self._tempting_index = None

    @property
    def tempting_index(self):

        if self._tempting_index is not None:
            return self._tempting_index

        folder_index_conf = []
        used_aliases = []

        for f in self.repos:

            url = f

            alias = os.path.basename(url).split(".")[0]
            i = 1
            while alias in used_aliases:
                i = i + 1
                alias = "{}_{}".format(alias, i)

            used_aliases.append(alias)
            folder_index_conf.append(
                {"repo_name": alias, "folder_url": url, "loader": "tempting_files"}
            )

        self._tempting_index = TingTings.from_config(
            "temptings",
            folder_index_conf,
            TEMPTING_LOAD_CONFIG,
            indexes=["tempting_name"],
        )
        return self._tempting_index

    def get_tempting(self, tempting_name):

        return self.tempting_index.get(tempting_name)

    def get_tempting_names(self):

        return self.tempting_index.keys()
