# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import collections

import numpy as np

from . import periods


class DatedHolder(object):
    """A view of an holder, for a given period"""
    holder = None
    period = None

    def __init__(self, holder, period):
        self.holder = holder
        self.period = period

    @property
    def array(self):
        return self.holder.get_array(self.period)

    @array.deleter
    def array(self):
        self.holder.delete_array(self.period)

    @array.setter
    def array(self, array):
        self.holder.set_array(self.period, array)

    @property
    def column(self):
        return self.holder.column

    @property
    def entity(self):
        return self.holder.entity


class Holder(object):
    _array = None  # Only used when column.is_period_invariant
    _array_by_period = None  # Only used when not column.is_period_invariant
    column = None
    entity = None
    formula = None

    def __init__(self, column = None, entity = None):
        assert column is not None
        assert self.column is None
        self.column = column
        assert entity is not None
        self.entity = entity

    @property
    def array(self):
        if not self.column.is_period_invariant:
            return self.get_array(self.entity.simulation.period)
        return self._array

    @array.deleter
    def array(self):
        simulation = self.entity.simulation
        if not self.column.is_period_invariant:
            return self.delete_array(simulation.period)
        if simulation.trace:
            simulation.traceback.pop(self.column.name, None)
        del self._array

    @array.setter
    def array(self, array):
        simulation = self.entity.simulation
        if not self.column.is_period_invariant:
            return self.set_array(simulation.period, array)
        if simulation.trace:
            name = self.column.name
            step = simulation.traceback.get(name)
            if step is None:
                simulation.traceback[name] = dict(
                    holder = self,
                    )
        self._array = array

    def at_period(self, period):
        return self if self.column.is_period_invariant else DatedHolder(self, period)

    def calculate(self, lazy = False, period = None, requested_formulas_by_period = None):
        dated_holder = self.compute(lazy = lazy, period = period,
            requested_formulas_by_period = requested_formulas_by_period)
        return dated_holder.array

    def compute(self, lazy = False, period = None, requested_formulas_by_period = None):
        """Compute array if needed and/or convert it to requested period and return a dated holder containig it.

        The returned dated holder is always of the requested period.
        """
        if period is None:
            period = self.entity.simulation.period
        column = self.column
        formula = self.formula
        dated_holder = None
        # if formula is None or column.start is not None and column.start > periods.stop_date(period) \
        #         or column.end is not None and column.end < periods.start_date(period):
        if formula is not None:
            assert formula.period_unit in ('year', 'month')  # TODO: start_day may not be sufficient.
            period_start_date = periods.start_date(period)
            # Check that the start day of the column belongs to period.
            if (column.start is None or column.start <= period_start_date) \
                    and (column.end is None or column.end >= period_start_date):
                dated_holder = formula.compute(lazy = lazy, requested_formulas_by_period = requested_formulas_by_period)
                if dated_holder is not None and dated_holder.period != period:
                    dated_holder = None
        if dated_holder is None:
            dated_holder = self.at_period(period)
        array = dated_holder.array
        if array is not None:
            return dated_holder
        if not lazy and array is None:
            array = np.empty(self.entity.count, dtype = column.dtype)
            array.fill(column.default)
            dated_holder.array = array
        return dated_holder

    def delete_array(self, period):
        if self.column.is_period_invariant:
            del self.array
            return
        assert period is not None
        simulation = self.entity.simulation
        if simulation.trace:
            simulation.traceback.pop(self.column.name, None)
        array_by_period = self._array_by_period
        if array_by_period is not None:
            array_by_period.pop(period, None)
            if not array_by_period:
                del self._array_by_period

    def get_array(self, period):
        if self.column.is_period_invariant:
            return self.array
        assert period is not None
        array_by_period = self._array_by_period
        if array_by_period is None:
            return None
        return array_by_period.get(period)

    def graph(self, edges, nodes, visited):
        column = self.column
        if self in visited:
            return
        visited.add(self)
        nodes.append(dict(
            id = column.name,
            group = self.entity.key_plural,
            label = column.name,
            title = column.label,
            ))
        period_date = self.entity.simulation.period_date
        formula = self.formula
        if formula is None or column.start is not None and column.start > period_date or column.end is not None \
                and column.end < period_date:
            return
        formula.graph_parameters(edges, nodes, visited)

    def new_test_case_array(self, period):
        array = self.get_array(period)
        if array is None:
            return None
        entity = self.entity
        return array.reshape([entity.simulation.steps_count, entity.step_size]).sum(1)

    @property
    def real_formula(self):
        formula = self.formula
        if formula is None:
            return None
        return formula.real_formula

    def set_array(self, period, array):
        if self.column.is_period_invariant:
            self.array = array
            return
        assert period is not None
        simulation = self.entity.simulation
        if simulation.trace:
            name = self.column.name
            step = simulation.traceback.get(name)
            if step is None:
                simulation.traceback[name] = dict(
                    holder = self,
                    )
        array_by_period = self._array_by_period
        if array_by_period is None:
            self._array_by_period = array_by_period = {}
        array_by_period[period] = array

    def to__field_json(self):
        self_json = self.column.to_json()
        self_json['entity'] = self.entity.key_plural  # Override entity symbol given by column. TODO: Remove.
        formula = self.formula
        if formula is not None:
            self_json['formula'] = formula.to_json()
        entity = self.entity
        simulation = entity.simulation
        self_json['consumers'] = consumers_json = []
        for consumer in sorted(self.column.consumers or []):
            consumer_holder = simulation.get_or_new_holder(consumer)
            consumer_column = consumer_holder.column
            consumers_json.append(collections.OrderedDict((
                ('entity', consumer_holder.entity.key_plural),
                ('label', consumer_column.label),
                ('name', consumer_column.name),
                )))
        return self_json
