#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2019 Chintalagiri Shashank
#
# This file is part of tendril.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import importlib

from tendril.utils.fsutils import get_namespace_package_names
from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)


class MotifsManager(object):
    def __init__(self, prefix):
        self._prefix = prefix
        self._motifs = {}
        self._load_motifs()

    def _load_motifs(self):
        logger.debug("Loading motif modules from {0}".format(self._prefix))
        modules = list(get_namespace_package_names(self._prefix))
        for m_name in modules:
            if m_name == __name__:
                continue
            m = importlib.import_module(m_name)
            m.load(self)

    def install_motif(self, name, motif):
        logger.debug("Installing motif {0} : {1}".format(name, motif))
        self._motifs[name] = motif

    def __getattr__(self, item):
        return self._motifs[item]

    def create(self, motifst):
        name, _ = motifst.split('.')
        try:
            return self._motifs[name](motifst)
        except KeyError:
            raise ValueError("Motif Unrecognized : {0}".format(motifst))

    def installed_motifs(self):
        return self._motifs.keys()
