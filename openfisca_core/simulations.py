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

from . import periods
from .tools import empty_clone


class Simulation(object):
    compact_legislation_by_instant_cache = None
    debug = False
    debug_all = False  # When False, log only formula calls with non-default parameters.
    entity_by_column_name = None
    entity_by_key_plural = None
    entity_by_key_singular = None
    period = None
    persons = None
    reference_compact_legislation_by_instant_cache = None
    steps_count = 1
    tax_benefit_system = None
    trace = False
    traceback = None

    def __init__(self, debug = False, debug_all = False, period = None, tax_benefit_system = None, trace = False):
        assert isinstance(period, periods.Period)
        self.period = period
        if debug:
            self.debug = True
        if debug_all:
            assert debug
            self.debug_all = True
        assert tax_benefit_system is not None
        self.tax_benefit_system = tax_benefit_system
        if trace:
            self.trace = True
            self.traceback = collections.OrderedDict()

        # Note: Since simulations are short-lived and must be fast, don't use weakrefs for cache.
        self.compact_legislation_by_instant_cache = {}
        self.reference_compact_legislation_by_instant_cache = {}

        entity_class_by_key_plural = tax_benefit_system.entity_class_by_key_plural
        self.entity_by_key_plural = entity_by_key_plural = dict(
            (key_plural, entity_class(simulation = self))
            for key_plural, entity_class in entity_class_by_key_plural.iteritems()
            )
        self.entity_by_column_name = dict(
            (column_name, entity)
            for entity in entity_by_key_plural.itervalues()
            for column_name in entity.column_by_name.iterkeys()
            )
        self.entity_by_key_singular = dict(
            (entity.key_singular, entity)
            for entity in entity_by_key_plural.itervalues()
            )
        for entity in entity_by_key_plural.itervalues():
            if entity.is_persons_entity:
                self.persons = entity
                break

    def calculate(self, column_name, period = None, lazy = False, requested_formulas_by_period = None):
        if period is None:
            period = self.period
        return self.compute(column_name, period = period, lazy = lazy,
            requested_formulas_by_period = requested_formulas_by_period).array

    def clone(self, debug = False, debug_all = False, trace = False):
        """Copy the simulation just enough to be able to run the copy without modifying the original simulation."""
        new = empty_clone(self)
        new_dict = new.__dict__

        for key, value in self.__dict__.iteritems():
            if key not in ('debug', 'debug_all', 'entity_by_key_plural', 'persons', 'trace'):
                new_dict[key] = value

        if debug:
            new_dict['debug'] = True
        if debug_all:
            new_dict['debug_all'] = True
        if trace:
            new_dict['trace'] = True
            new_dict['traceback'] = collections.OrderedDict()

        new_dict['entity_by_key_plural'] = entity_by_key_plural = dict(
            (key_plural, entity.clone(simulation = new))
            for key_plural, entity in self.entity_by_key_plural.iteritems()
            )
        new_dict['entity_by_column_name'] = dict(
            (column_name, entity)
            for entity in entity_by_key_plural.itervalues()
            for column_name in entity.column_by_name.iterkeys()
            )
        new_dict['entity_by_key_singular'] = dict(
            (entity.key_singular, entity)
            for entity in entity_by_key_plural.itervalues()
            )
        for entity in entity_by_key_plural.itervalues():
            if entity.is_persons_entity:
                new_dict['persons'] = entity
                break

        return new

    def compute(self, column_name, period = None, lazy = False, requested_formulas_by_period = None):
        if period is None:
            period = self.period
        return self.entity_by_column_name[column_name].compute(column_name, period = period, lazy = lazy,
            requested_formulas_by_period = requested_formulas_by_period)

    def get_compact_legislation(self, instant):
        compact_legislation = self.compact_legislation_by_instant_cache.get(instant)
        if compact_legislation is None:
            compact_legislation = self.tax_benefit_system.get_compact_legislation(instant)
            self.compact_legislation_by_instant_cache[instant] = compact_legislation
        return compact_legislation

    def get_holder(self, column_name, default = UnboundLocalError):
        entity = self.entity_by_column_name[column_name]
        if default is UnboundLocalError:
            return entity.holder_by_name[column_name]
        return entity.holder_by_name.get(column_name, default)

    def get_or_new_holder(self, column_name):
        entity = self.entity_by_column_name[column_name]
        return entity.get_or_new_holder(column_name)

    def get_reference_compact_legislation(self, instant):
        reference_compact_legislation = self.reference_compact_legislation_by_instant_cache.get(instant)
        if reference_compact_legislation is None:
            reference_compact_legislation = self.tax_benefit_system.get_reference_compact_legislation(instant)
            self.reference_compact_legislation_by_instant_cache[instant] = reference_compact_legislation
        return reference_compact_legislation

    def graph(self, column_name, edges, nodes, visited):
        self.entity_by_column_name[column_name].graph(column_name, edges, nodes, visited)
