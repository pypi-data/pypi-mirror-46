# Copyright (C) 2015 Chintalagiri Shashank
#
# This file is part of Tendril.
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
"""
This file is part of tendril
See the COPYING, README, and INSTALL files for more information
"""

from tendril.conventions.series import get_series


class MotifBase(object):
    columns = ['refdes', 'device', 'value', 'footprint',
               'fillstatus', 'group', 'package', 'status']

    def __init__(self, identifier):
        self._type = None
        self._ident = None
        self._elements = []
        self.refdes = identifier
        self._configdict = None

    @property
    def refdes(self):
        return self._type + '.' + self._ident

    @refdes.setter
    def refdes(self, value):
        value = value.split(':')[0]
        self._type, self._ident = value.split('.')

    @property
    def desc(self):
        return self._configdict.get('desc', '')

    # Elements
    def add_element(self, bomline):
        self._elements.append(bomline)

    @property
    def elements(self):
        return sorted(self._elements, key=lambda x: x.motif)

    def get_elem_by_idx(self, idx):
        for elem in self._elements:
            if elem.data['motif'].split(':')[1] == idx:
                return elem
        raise KeyError(self.refdes, idx)

    def _line_generator(self):
        for elem in self._elements:
            yield elem

    def get_line_gen(self):
        return self._line_generator()

    # Configuration
    @property
    def configdict_base(self):
        raise NotImplementedError

    def get_configdict_stub(self):
        stub = {}
        for parameter in self.configdict_base:
            stub[parameter[0]] = parameter[1]
        return stub

    def configure(self, configdict):
        self._configdict = configdict

    # Input Parameters
    @property
    def inputs(self):
        inputs = []
        for parameter in self.configdict_base:
            if parameter[0] is not 'desc':
                inputs.append((
                    parameter[0],
                    parameter[3](self._configdict[parameter[0]]),
                    parameter[2]
                ))
        return inputs

    # Show your work Parameters
    @property
    def parameters_base(self):
        raise NotImplementedError

    @property
    def parameters(self):
        parameters = []
        for group in self.parameters_base:
            parameters.append(([
                (e[1], e[0], e[2], self.__getattribute__(e[0]))
                for e in group[0]
            ], group[1]))
        return parameters

    # Target Parameter Listing
    @property
    def listing(self):
        raise NotImplementedError

    # Component Series Control
    def _get_component_series(self, idx, stype):
        if stype == 'capacitor':
            sstr = 'Cseries'
            smin = 'Cmin'
            smax = 'Cmax'
        elif stype == 'resistor':
            sstr = 'Rseries'
            smin = 'Rmin'
            smax = 'Rmax'
        else:
            raise NotImplementedError

        dev = self.get_elem_by_idx(idx).data['device']
        fp = self.get_elem_by_idx(idx).data['footprint']
        if fp[0:3] == "MY-":
            fp = fp[3:]
        return get_series(self._configdict[sstr], stype,
                          start=self._configdict[smin],
                          end=self._configdict[smax],
                          device=dev,
                          footprint=fp)

    def _set_component(self, idx, target, series):
        value = series.get_closest_value(target)
        if not value:
            raise ValueError
        try:
            svalue = series.get_symbol(value).value
        except AttributeError:
            svalue = series.get_symbol(value)
        self.get_elem_by_idx(idx).data['value'] = svalue  # noqa
        return series.get_type_value(svalue)

    def validate(self):
        raise NotImplementedError

    def __repr__(self):
        return "<{0} {1}>".format(self.__class__.__name__, self._ident)


def load(module):
    pass
