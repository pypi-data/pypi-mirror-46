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


from tendril.conventions.motifs.base import MotifBase

from tendril.utils.types.electromagnetic import Resistance
from tendril.utils.types.electromagnetic import VoltageGain

from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)


class MotifInampGainBase(MotifBase):
    def __init__(self, identifier):
        super(MotifInampGainBase, self).__init__(identifier)
        self.rseries = None
        self.target_gain = None

    # Calculators
    @property
    def gain(self):
        return self.res_to_gain(self.R1)

    def res_to_gain(self, res):
        raise NotImplementedError

    def gain_to_res(self, gain):
        raise NotImplementedError

    @gain.setter
    def gain(self, value):
        required_res_val = self.gain_to_res(value)

        if required_res_val and not isinstance(required_res_val, Resistance):
            required_res_val = Resistance(required_res_val)
        elif not required_res_val:
            self.get_elem_by_idx('R1').data['fillstatus'] = 'DNP'
            return

        allowed_res_vals = self.rseries.gen_vals('resistor')

        lastval = None
        # TODO Replace with kind of generalized search?
        for rval in allowed_res_vals:
            if not lastval:
                lastval = rval
            if rval > required_res_val:
                try:
                    value = self.rseries.get_symbol(lastval).value
                except AttributeError:
                    value = self.rseries.get_symbol(lastval)
                self.get_elem_by_idx('R1').data['value'] = value  # noqa
                break
            lastval = rval

    # Elements
    @property
    def R1(self):
        elem = self.get_elem_by_idx('R1')
        assert elem.data['device'] in ['RES SMD', 'RES THRU']
        if elem.data['fillstatus'] == 'DNP':
            return None
        return self.rseries.get_type_value(elem.data['value'])

    # Comfiguration
    @property
    def configdict_base(self):
        inputs = [
            ('desc', 'Instrumentation Amplifier Gain', 'description', str),
            ('Rseries', 'E24', 'Resistance Series', str),
            ('Rmin', '10E', 'Minimum Resistance', str),
            ('Rmax', '10M', 'Maximum Resistance', str),
            ('gain', "1", 'Amplifier DC gain', str),
        ]
        return inputs

    def configure(self, configdict):
        super(MotifInampGainBase, self).configure(configdict)
        self.target_gain = VoltageGain(configdict['gain'])
        self.gain = configdict['gain']
        self.rseries = self._get_component_series('R1', 'resistor')
        self.validate()

    # Intermediate Results
    @property
    def parameters_base(self):
        p_gain = [
            ('R1', "Gain Setting Resistance", ''),
            ('gain', "Amplifier DC Gain", self.target_gain),
        ]
        parameters = [
            (p_gain, "Gain Setting"),
        ]
        return parameters

    # Target Parameter Listing
    @property
    def listing(self):
        return [('Gain', self.gain.quantized_repr)]

    def validate(self):
        pass


def load(manager):
    pass
