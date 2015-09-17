# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
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


from __future__ import division

import collections
import datetime
import inspect
import itertools
import logging
import textwrap

import numpy as np

from . import columns, holders, periods
from .tools import empty_clone, stringify_array


log = logging.getLogger(__name__)


# Exceptions


class NaNCreationError(Exception):
    pass


# Formula categories and period units

ARITHMETIC = 'ARITHMETIC'
STATE = 'STATE'
MONTH = 'MONTH'
YEAR = 'YEAR'


# Formulas


class AbstractFormula(object):
    category = None
    comments = None
    holder = None
    line_number = None
    period_unit = None
    source_code = None
    source_file_path = None

    def __init__(self, holder = None):
        assert holder is not None
        self.holder = holder

    # TODO remove
    # def calculate_output(self, period):
    #     return self.holder.compute(period).array

    def clone(self, holder, keys_to_skip = None):
        """Copy the formula just enough to be able to run a new simulation without modifying the original simulation."""
        new = empty_clone(self)
        new_dict = new.__dict__

        if keys_to_skip is None:
            keys_to_skip = set()
        keys_to_skip.add('holder')
        for key, value in self.__dict__.iteritems():
            if key not in keys_to_skip:
                new_dict[key] = value

        new_dict['holder'] = holder

        return new

    def compute_base_function(self, simulation, period, is_external_output):
        category = self.category
        period_unit = self.period_unit
        holder = self.holder
        entity = holder.entity
        column = holder.column
        column_start_instant = periods.instant(column.start)
        column_stop_instant = periods.instant(column.end)
        if (column_start_instant is None or column_start_instant <= period.start) \
                and (column_stop_instant is None or period.start <= column_stop_instant):
            if category == ARITHMETIC and period_unit == MONTH:
                array = monthly_arithmetic_function(self, simulation, period)
                dated_holder = holder.at_period(period)
                assert (array == dated_holder.array).all(), (array, dated_holder.array)
            elif category == ARITHMETIC and period_unit == YEAR:
                array = yearly_arithmetic_function(self, simulation, period)
                dated_holder = holder.at_period(period)
                assert (array == dated_holder.array).all(), (array, dated_holder.array)
            elif category == STATE and period_unit == MONTH:
                array = monthly_state_function(self, simulation, period)
                dated_holder = holder.at_period(period)
            else:
                # assert False, u'Unexpected value for category attribute: {}'.format(category).encode('utf-8')
                returned_period, array = self.base_function(simulation, period)
                # Store array in cache because legacy base functions don't do it (it was Formula.compute)
                dated_holder = holder.at_period(period)
                dated_holder.array = array
        else:
            # TODO Cache this array?
            array = np.empty(entity.count, dtype = column.dtype)
            array.fill(column.default)
            # Store array in cache because Formula.compute retrieves it later
            dated_holder = holder.at_period(period)
            dated_holder.array = array
        return array

    @property
    def real_formula(self):
        return self

    def set_input(self, period, array):
        self.holder.set_array(period, array)


class AbstractEntityToEntity(AbstractFormula):
    _variable_holder = None
    roles = None  # class attribute. When None the entity value is duplicated to each person belonging to entity.
    variable_name = None  # class attribute

    def clone(self, holder, keys_to_skip = None):
        """Copy the formula just enough to be able to run a new simulation without modifying the original simulation."""
        if keys_to_skip is None:
            keys_to_skip = set()
        keys_to_skip.add('_variable_holder')
        return super(AbstractEntityToEntity, self).clone(holder, keys_to_skip = keys_to_skip)

    def compute(self, period = None, requested_formulas_by_period = None):
        """Call the formula function (if needed) and return a dated holder containing its result."""
        assert period is not None
        holder = self.holder
        column = holder.column
        entity = holder.entity
        simulation = entity.simulation
        debug = simulation.debug
        debug_all = simulation.debug_all
        trace = simulation.trace

        if debug or trace:
            simulation.stack_trace.append(dict(
                parameters_infos = [],
                input_variables_infos = [],
            ))

        # TODO Update method
        variable_holder = self.variable_holder
        variable_dated_holder = variable_holder.compute(period = period, accept_other_period = True,
            requested_formulas_by_period = requested_formulas_by_period)
        output_period = variable_dated_holder.period

        array = self.transform(variable_dated_holder, roles = self.roles)
        if array.dtype != column.dtype:
            array = array.astype(column.dtype)

        if debug or trace:
            variable_infos = (column.name, output_period)
            step = simulation.traceback.get(variable_infos)
            if step is None:
                simulation.traceback[variable_infos] = step = dict(
                    holder = holder,
                )
            step.update(simulation.stack_trace.pop())
            input_variables_infos = step['input_variables_infos']
            if not debug_all or trace:
                step['default_input_variables'] = has_only_default_input_variables = all(
                    np.all(input_holder.get_array(input_variable_period) == input_holder.column.default)
                    for input_holder, input_variable_period in (
                        (simulation.get_holder(input_variable_name), input_variable_period1)
                        for input_variable_name, input_variable_period1 in input_variables_infos
                    )
                )
            step['is_computed'] = True
            if debug and (debug_all or not has_only_default_input_variables):
                log.info(u'<=> {}@{}<{}>({}) --> <{}>{}'.format(column.name, entity.key_plural, str(period),
                    simulation.stringify_input_variables_infos(input_variables_infos), stringify_array(array),
                    str(output_period)))

        dated_holder = holder.at_period(output_period)
        dated_holder.array = array
        return dated_holder

    def graph_parameters(self, edges, get_input_variables_and_parameters, nodes, visited):
        """Recursively build a graph of formulas."""
        holder = self.holder
        column = holder.column
        variable_holder = self.variable_holder
        variable_holder.graph(edges, get_input_variables_and_parameters, nodes, visited)
        edges.append({
            'from': variable_holder.column.name,
            'to': column.name,
            })

    def to_json(self, get_input_variables_and_parameters = None, with_input_variables_details = False):
        cls = self.__class__
        comments = inspect.getcomments(cls)
        doc = inspect.getdoc(cls)
        source_lines, line_number = inspect.getsourcelines(cls)
        variable_holder = self.variable_holder
        variable_column = variable_holder.column
        self_json = collections.OrderedDict((
            ('@type', cls.__bases__[0].__name__),
            ('comments', comments.decode('utf-8') if comments is not None else None),
            ('doc', doc.decode('utf-8') if doc is not None else None),
            ('line_number', line_number),
            ('module', inspect.getmodule(cls).__name__),
            ('source', ''.join(source_lines).decode('utf-8')),
            ))
        if get_input_variables_and_parameters is not None:
            input_variable_json = collections.OrderedDict((
                ('entity', variable_holder.entity.key_plural),
                ('label', variable_column.label),
                ('name', variable_column.name),
                )) if with_input_variables_details else variable_column.name
            self_json['input_variables'] = [input_variable_json]
        return self_json

    @property
    def variable_holder(self):
        # Note: This property is not precomputed at __init__ time, to ease the cloning of the formula.
        variable_holder = self._variable_holder
        if variable_holder is None:
            self._variable_holder = variable_holder = self.holder.entity.simulation.get_or_new_holder(
                self.variable_name)
        return variable_holder


class AbstractGroupedFormula(AbstractFormula):
    used_formula = None

    @property
    def real_formula(self):
        used_formula = self.used_formula
        if used_formula is None:
            return None
        return used_formula.real_formula


class DatedFormula(AbstractGroupedFormula):
    base_function = None  # Class attribute. Overridden by subclasses
    dated_formulas = None  # A list of dictionaries containing a formula jointly with start and stop instants
    dated_formulas_class = None  # Class attribute

    def __init__(self, holder = None):
        super(DatedFormula, self).__init__(holder = holder)

        self.dated_formulas = [
            dict(
                formula = dated_formula_class['formula_class'](holder = holder),
                start_instant = dated_formula_class['start_instant'],
                stop_instant = dated_formula_class['stop_instant'],
                )
            for dated_formula_class in self.dated_formulas_class
            ]
        assert self.dated_formulas

    @classmethod
    def at_instant(cls, instant, default = UnboundLocalError):
        assert isinstance(instant, periods.Instant)
        for dated_formula_class in cls.dated_formulas_class:
            start_instant = dated_formula_class['start_instant']
            stop_instant = dated_formula_class['stop_instant']
            if (start_instant is None or start_instant <= instant) and (
                    stop_instant is None or instant <= stop_instant):
                return dated_formula_class['formula_class']
        if default is UnboundLocalError:
            raise KeyError(instant)
        return default

    def clone(self, holder, keys_to_skip = None):
        """Copy the formula just enough to be able to run a new simulation without modifying the original simulation."""
        if keys_to_skip is None:
            keys_to_skip = set()
        keys_to_skip.add('dated_formulas')
        new = super(DatedFormula, self).clone(holder, keys_to_skip = keys_to_skip)

        new.dated_formulas = [
            {
                key: value.clone(holder) if key == 'formula' else value
                for key, value in dated_formula.iteritems()
                }
            for dated_formula in self.dated_formulas
            ]

        return new

    def compute(self, period = None, requested_formulas_by_period = None):
        # TODO Update method
        dated_holder = None
        stop_instant = period.stop
        for dated_formula in self.dated_formulas:
            if dated_formula['start_instant'] > stop_instant:
                break
            output_period = period.intersection(dated_formula['start_instant'], dated_formula['stop_instant'])
            if output_period is None:
                continue
            dated_holder = dated_formula['formula'].compute(period = output_period,
                requested_formulas_by_period = requested_formulas_by_period)
            if dated_holder.array is None:
                break
            self.used_formula = dated_formula['formula']
            return dated_holder

        holder = self.holder
        column = holder.column
        array = np.empty(holder.entity.count, dtype = column.dtype)
        array.fill(column.default)
        if dated_holder is None:
            dated_holder = holder.at_period(period)
        dated_holder.array = array
        return dated_holder

    def graph_parameters(self, edges, get_input_variables_and_parameters, nodes, visited):
        """Recursively build a graph of formulas."""
        for dated_formula in self.dated_formulas:
            dated_formula['formula'].graph_parameters(edges, get_input_variables_and_parameters, nodes, visited)

    def to_json(self, get_input_variables_and_parameters = None, with_input_variables_details = False):
        return collections.OrderedDict((
            ('@type', u'DatedFormula'),
            ('dated_formulas', [
                dict(
                    formula = dated_formula['formula'].to_json(
                        get_input_variables_and_parameters = get_input_variables_and_parameters,
                        with_input_variables_details = with_input_variables_details,
                        ),
                    start_instant = (None if dated_formula['start_instant'] is None
                        else str(dated_formula['start_instant'])),
                    stop_instant = (None if dated_formula['stop_instant'] is None
                        else str(dated_formula['stop_instant'])),
                    )
                for dated_formula in self.dated_formulas
                ]),
            ))


class EntityToPerson(AbstractEntityToEntity):
    def transform(self, dated_holder, roles = None):
        """Cast an entity array to a persons array, setting only cells of persons having one of the given roles.

        When no roles are given, it means "all the roles" => every cell is set.
        """
        holder = self.holder
        persons = holder.entity
        assert persons.is_persons_entity

        entity = dated_holder.entity
        assert not entity.is_persons_entity
        array = dated_holder.array
        target_array = np.empty(persons.count, dtype = array.dtype)
        target_array.fill(dated_holder.column.default)
        entity_index_array = persons.holder_by_name[entity.index_for_person_variable_name].array
        if roles is None:
            roles = range(entity.roles_count)
        for role in roles:
            boolean_filter = persons.holder_by_name[entity.role_for_person_variable_name].array == role
            try:
                target_array[boolean_filter] = array[entity_index_array[boolean_filter]]
            except:
                log.error(u'An error occurred while transforming array for role {}[{}] in function {}'.format(
                    entity.key_singular, role, holder.column.name))
                raise
        return target_array


class PersonToEntity(AbstractEntityToEntity):
    operation = None

    def transform(self, dated_holder, roles = None):
        """Convert an array of persons to an array of non-person entities.

        When no roles are given, it means "all the roles".
        """
        holder = self.holder
        entity = holder.entity
        assert not entity.is_persons_entity

        persons = dated_holder.entity
        assert persons.is_persons_entity
        array = dated_holder.array

        target_array = np.empty(entity.count, dtype = array.dtype)
        target_array.fill(dated_holder.column.default)
        entity_index_array = persons.holder_by_name[entity.index_for_person_variable_name].array
        if roles is not None and len(roles) == 1:
            assert self.operation is None, 'Unexpected operation {} in formula {}'.format(self.operation,
                holder.column.name)
            role = roles[0]
            # TODO: Cache filter.
            boolean_filter = persons.holder_by_name[entity.role_for_person_variable_name].array == role
            try:
                target_array[entity_index_array[boolean_filter]] = array[boolean_filter]
            except:
                log.error(u'An error occurred while filtering array for role {}[{}] in function {}'.format(
                    entity.key_singular, role, holder.column.name))
                raise
        else:
            operation = self.operation
            assert operation in ('add', 'or'), 'Invalid operation {} in formula {}'.format(operation,
                holder.column.name)
            if roles is None:
                roles = range(entity.roles_count)
            target_array = np.zeros(entity.count,
                dtype = np.bool if operation == 'or' else array.dtype if array.dtype != np.bool else np.int16)
            for role in roles:
                # TODO: Cache filters.
                boolean_filter = persons.holder_by_name[entity.role_for_person_variable_name].array == role
                target_array[entity_index_array[boolean_filter]] += array[boolean_filter]

        return target_array


class SimpleFormula(AbstractFormula):
    base_function = None  # Class attribute. Overridden by subclasses
    function = None  # Class attribute. Overridden by subclasses

    def any_by_roles(self, array_or_dated_holder, entity = None, roles = None):
        holder = self.holder
        target_entity = holder.entity
        simulation = target_entity.simulation
        persons = simulation.persons
        if entity is None:
            entity = holder.entity
        else:
            assert entity in simulation.entity_by_key_singular, u"Unknown entity: {}".format(entity).encode('utf-8')
            entity = simulation.entity_by_key_singular[entity]
        assert not entity.is_persons_entity
        if isinstance(array_or_dated_holder, (holders.DatedHolder, holders.Holder)):
            assert array_or_dated_holder.entity.is_persons_entity
            array = array_or_dated_holder.array
        else:
            array = array_or_dated_holder
            assert isinstance(array, np.ndarray), u"Expected a holder or a Numpy array. Got: {}".format(array).encode(
                'utf-8')
            assert array.size == persons.count, u"Expected an array of size {}. Got: {}".format(persons.count,
                array.size)
        entity_index_array = persons.holder_by_name[entity.index_for_person_variable_name].array
        if roles is None:
            roles = range(entity.roles_count)
        target_array = np.zeros(entity.count, dtype = np.bool)
        for role in roles:
            # TODO Mettre les filtres en cache dans la simulation
            boolean_filter = persons.holder_by_name[entity.role_for_person_variable_name].array == role
            target_array[entity_index_array[boolean_filter]] += array[boolean_filter]
        return target_array

    def cast_from_entity_to_role(self, array_or_dated_holder, default = None, entity = None, role = None):
        """Cast an entity array to a persons array, setting only cells of persons having the given role."""
        assert isinstance(role, int)
        return self.cast_from_entity_to_roles(array_or_dated_holder, default = default, entity = entity, roles = [role])

    def cast_from_entity_to_roles(self, array_or_dated_holder, default = None, entity = None, roles = None):
        """Cast an entity array to a persons array, setting only cells of persons having one of the given roles.

        When no roles are given, it means "all the roles" => every cell is set.
        """
        holder = self.holder
        target_entity = holder.entity
        simulation = target_entity.simulation
        persons = simulation.persons
        if isinstance(array_or_dated_holder, (holders.DatedHolder, holders.Holder)):
            if entity is None:
                entity = array_or_dated_holder.entity
            else:
                assert entity in simulation.entity_by_key_singular, u"Unknown entity: {}".format(entity).encode('utf-8')
                entity = simulation.entity_by_key_singular[entity]
                assert entity == array_or_dated_holder.entity, \
                    u"""Holder entity "{}" and given entity "{}" don't match""".format(entity.key_plural,
                        array_or_dated_holder.entity.key_plural).encode('utf-8')
            array = array_or_dated_holder.array
            if default is None:
                default = array_or_dated_holder.column.default
        else:
            assert entity in simulation.entity_by_key_singular, u"Unknown entity: {}".format(entity).encode('utf-8')
            entity = simulation.entity_by_key_singular[entity]
            array = array_or_dated_holder
            assert isinstance(array, np.ndarray), u"Expected a holder or a Numpy array. Got: {}".format(array).encode(
                'utf-8')
            assert array.size == entity.count, u"Expected an array of size {}. Got: {}".format(entity.count,
                array.size)
            if default is None:
                default = 0
        assert not entity.is_persons_entity
        target_array = np.empty(persons.count, dtype = array.dtype)
        target_array.fill(default)
        entity_index_array = persons.holder_by_name[entity.index_for_person_variable_name].array
        if roles is None:
            roles = range(entity.roles_count)
        for role in roles:
            boolean_filter = persons.holder_by_name[entity.role_for_person_variable_name].array == role
            try:
                target_array[boolean_filter] = array[entity_index_array[boolean_filter]]
            except:
                log.error(u'An error occurred while transforming array for role {}[{}] in function {}'.format(
                    entity.key_singular, role, holder.column.name))
                raise
        return target_array

    def compute(self, period = None, requested_formulas_by_period = None):
        """Call the formula function (if needed) and return a dated holder containing its result."""
        assert period is not None
        holder = self.holder
        column = holder.column
        entity = holder.entity
        simulation = entity.simulation
        debug = simulation.debug
        debug_all = simulation.debug_all
        trace = simulation.trace

        # Ensure that method is not called several times for the same period (infinite loop).
        if requested_formulas_by_period is None:
            requested_formulas_by_period = {}
        period_or_none = None if column.is_permanent else period
        period_requested_formulas = requested_formulas_by_period.get(period_or_none)
        if period_requested_formulas is None:
            requested_formulas_by_period[period_or_none] = period_requested_formulas = set()
        else:
            assert self not in period_requested_formulas, \
                'Infinite loop in formula {}<{}>. Missing values for columns: {}'.format(
                    column.name,
                    period,
                    u', '.join(sorted(set(
                        u'{}<{}>'.format(requested_formula.holder.column.name, period1)
                        for period1, period_requested_formulas1 in requested_formulas_by_period.iteritems()
                        for requested_formula in period_requested_formulas1
                        ))).encode('utf-8'),
                    )
        period_requested_formulas.add(self)

        if debug or trace:
            simulation.stack_trace.append(dict(
                parameters_infos = [],
                input_variables_infos = [],
                ))

        is_external_output = False  # TODO
        array = self.compute_base_function(simulation, period, is_external_output)

        if debug or trace:
            variable_infos = (column.name, period)
            step = simulation.traceback.get(variable_infos)
            if step is None:
                simulation.traceback[variable_infos] = step = dict(
                    holder = holder,
                    )
            step.update(simulation.stack_trace.pop())
            input_variables_infos = step['input_variables_infos']
            if not debug_all or trace:
                step['default_input_variables'] = has_only_default_input_variables = all(
                    np.all(input_holder.get_array(input_variable_period) == input_holder.column.default)
                    for input_holder, input_variable_period in (
                        (simulation.get_holder(input_variable_name), input_variable_period1)
                        for input_variable_name, input_variable_period1 in input_variables_infos
                        )
                    )
            step['is_computed'] = True
            if debug and (debug_all or not has_only_default_input_variables):
                log.info(u'<=> {}@{}<{}>({}) --> {}'.format(column.name, entity.key_plural, str(period),
                    simulation.stringify_input_variables_infos(input_variables_infos), stringify_array(array)))

        dated_holder = holder.at_period(period)
        assert dated_holder.array is not None, \
            'array from cache is None, it should have been stored in cache previously'
        assert (array == dated_holder.array).all(), (
            'array from cache is different than base function output', array, dated_holder.array,
            )
        period_requested_formulas.remove(self)
        return dated_holder

    def filter_role(self, array_or_dated_holder, default = None, entity = None, role = None):
        """Convert a persons array to an entity array, copying only cells of persons having the given role."""
        holder = self.holder
        simulation = holder.entity.simulation
        persons = simulation.persons
        if entity is None:
            entity = holder.entity
        else:
            assert entity in simulation.entity_by_key_singular, u"Unknown entity: {}".format(entity).encode('utf-8')
            entity = simulation.entity_by_key_singular[entity]
        assert not entity.is_persons_entity
        if isinstance(array_or_dated_holder, (holders.DatedHolder, holders.Holder)):
            assert array_or_dated_holder.entity.is_persons_entity
            array = array_or_dated_holder.array
            if default is None:
                default = array_or_dated_holder.column.default
        else:
            array = array_or_dated_holder
            assert isinstance(array, np.ndarray), u"Expected a holder or a Numpy array. Got: {}".format(array).encode(
                'utf-8')
            assert array.size == persons.count, u"Expected an array of size {}. Got: {}".format(persons.count,
                array.size)
            if default is None:
                default = 0
        entity_index_array = persons.holder_by_name[entity.index_for_person_variable_name].array
        assert isinstance(role, int)
        target_array = np.empty(entity.count, dtype = array.dtype)
        target_array.fill(default)
        boolean_filter = persons.holder_by_name[entity.role_for_person_variable_name].array == role
        try:
            target_array[entity_index_array[boolean_filter]] = array[boolean_filter]
        except:
            log.error(u'An error occurred while filtering array for role {}[{}] in function {}'.format(
                entity.key_singular, role, holder.column.name))
            raise
        return target_array

    def graph_parameters(self, edges, get_input_variables_and_parameters, nodes, visited):
        """Recursively build a graph of formulas."""
        holder = self.holder
        column = holder.column
        entity = holder.entity
        simulation = entity.simulation
        variables_name, parameters_name = get_input_variables_and_parameters(column)
        if variables_name is not None:
            for variable_name in sorted(variables_name):
                variable_holder = simulation.get_or_new_holder(variable_name)
                variable_holder.graph(edges, get_input_variables_and_parameters, nodes, visited)
                edges.append({
                    'from': variable_holder.column.name,
                    'to': column.name,
                    })

    def split_by_roles(self, array_or_dated_holder, default = None, entity = None, roles = None):
        """dispatch a persons array to several entity arrays (one for each role)."""
        holder = self.holder
        simulation = holder.entity.simulation
        persons = simulation.persons
        if entity is None:
            entity = holder.entity
        else:
            assert entity in simulation.entity_by_key_singular, u"Unknown entity: {}".format(entity).encode('utf-8')
            entity = simulation.entity_by_key_singular[entity]
        assert not entity.is_persons_entity
        if isinstance(array_or_dated_holder, (holders.DatedHolder, holders.Holder)):
            assert array_or_dated_holder.entity.is_persons_entity
            array = array_or_dated_holder.array
            if default is None:
                default = array_or_dated_holder.column.default
        else:
            array = array_or_dated_holder
            assert isinstance(array, np.ndarray), u"Expected a holder or a Numpy array. Got: {}".format(array).encode(
                'utf-8')
            assert array.size == persons.count, u"Expected an array of size {}. Got: {}".format(persons.count,
                array.size)
            if default is None:
                default = 0
        entity_index_array = persons.holder_by_name[entity.index_for_person_variable_name].array
        if roles is None:
            # To ensure that existing formulas don't fail, ensure there is always at least 11 roles.
            # roles = range(entity.roles_count)
            roles = range(max(entity.roles_count, 11))
        target_array_by_role = {}
        for role in roles:
            target_array_by_role[role] = target_array = np.empty(entity.count, dtype = array.dtype)
            target_array.fill(default)
            boolean_filter = persons.holder_by_name[entity.role_for_person_variable_name].array == role
            try:
                target_array[entity_index_array[boolean_filter]] = array[boolean_filter]
            except:
                log.error(u'An error occurred while filtering array for role {}[{}] in function {}'.format(
                    entity.key_singular, role, holder.column.name))
                raise
        return target_array_by_role

    def sum_by_entity(self, array_or_dated_holder, entity = None, roles = None):
        holder = self.holder
        target_entity = holder.entity
        simulation = target_entity.simulation
        persons = simulation.persons
        if entity is None:
            entity = holder.entity
        else:
            assert entity in simulation.entity_by_key_singular, u"Unknown entity: {}".format(entity).encode('utf-8')
            entity = simulation.entity_by_key_singular[entity]
        assert not entity.is_persons_entity
        if isinstance(array_or_dated_holder, (holders.DatedHolder, holders.Holder)):
            assert array_or_dated_holder.entity.is_persons_entity
            array = array_or_dated_holder.array
        else:
            array = array_or_dated_holder
            assert isinstance(array, np.ndarray), u"Expected a holder or a Numpy array. Got: {}".format(array).encode(
                'utf-8')
            assert array.size == persons.count, u"Expected an array of size {}. Got: {}".format(persons.count,
                array.size)
        entity_index_array = persons.holder_by_name[entity.index_for_person_variable_name].array
        if roles is None:
            roles = range(entity.roles_count)
        target_array = np.zeros(entity.count, dtype = array.dtype if array.dtype != np.bool else np.int16)
        for role in roles:
            # TODO: Mettre les filtres en cache dans la simulation
            boolean_filter = persons.holder_by_name[entity.role_for_person_variable_name].array == role
            target_array[entity_index_array[boolean_filter]] += array[boolean_filter]
        return target_array

    def to_json(self, get_input_variables_and_parameters = None, with_input_variables_details = False):
        function = self.function
        if function is None:
            return None
        comments = inspect.getcomments(function)
        doc = inspect.getdoc(function)
        source_lines, line_number = inspect.getsourcelines(function)
        source = textwrap.dedent(''.join(source_lines).decode('utf-8'))
        self_json = collections.OrderedDict((
            ('@type', u'SimpleFormula'),
            ('comments', comments.decode('utf-8') if comments is not None else None),
            ('doc', doc.decode('utf-8') if doc is not None else None),
            ('line_number', line_number),
            ('module', inspect.getmodule(function).__name__),
            ('source', source),
            ))
        if get_input_variables_and_parameters is not None:
            holder = self.holder
            column = holder.column
            entity = holder.entity
            simulation = entity.simulation
            variables_name, parameters_name = get_input_variables_and_parameters(column)
            if variables_name:
                if with_input_variables_details:
                    input_variables_json = []
                    for variable_name in sorted(variables_name):
                        variable_holder = simulation.get_or_new_holder(variable_name)
                        variable_column = variable_holder.column
                        input_variables_json.append(collections.OrderedDict((
                            ('entity', variable_holder.entity.key_plural),
                            ('label', variable_column.label),
                            ('name', variable_column.name),
                            )))
                    self_json['input_variables'] = input_variables_json
                else:
                    self_json['input_variables'] = list(variables_name)
            if parameters_name:
                self_json['parameters'] = list(parameters_name)
        return self_json


# Formulas Generators


class ConversionColumnMetaclass(type):
    """The metaclass of ConversionColumn classes: It generates a column instead of a formula ConversionColumn class."""
    def __new__(cls, name, bases, attributes):
        """Return a column containing a casting formula, built from ConversionColumn class definition."""
        assert len(bases) == 1, bases
        base_class = bases[0]
        if base_class is object:
            # Do nothing when creating classes DatedFormulaColumn, SimpleFormulaColumn, etc.
            return super(ConversionColumnMetaclass, cls).__new__(cls, name, bases, attributes)

        # Extract attributes.

        formula_class = attributes.pop('formula_class', base_class.formula_class)
        assert issubclass(formula_class, AbstractFormula), formula_class

        cerfa_field = attributes.pop('cerfa_field', None)
        if cerfa_field is not None:
            assert isinstance(cerfa_field, basestring), cerfa_field
            cerfa_field = unicode(cerfa_field)

        doc = attributes.pop('__doc__', None)

        entity_class = attributes.pop('entity_class')

        name = unicode(name)
        label = attributes.pop('label', None)
        label = name if label is None else unicode(label)

        law_reference = attributes.pop('law_reference', None)
        if law_reference is not None:
            assert isinstance(law_reference, (basestring, list))

        url = attributes.pop('url', None)
        if url is not None:
            url = unicode(url)

        variable = attributes.pop('variable')
        assert isinstance(variable, columns.Column)

        # Build formula class and column from extracted attributes.

        formula_class_attributes = dict(
            __module__ = attributes.pop('__module__'),
            )
        if doc is not None:
            formula_class_attributes['__doc__'] = doc

        self = super(ConversionColumnMetaclass, cls).__new__(cls, name.encode('utf-8'), bases, attributes)
        comments = inspect.getcomments(self)
        if comments is not None:
            if isinstance(comments, str):
                comments = comments.decode('utf-8')
            formula_class_attributes['comments'] = comments
        source_file_path = inspect.getsourcefile(self).decode('utf-8')
        if source_file_path is not None:
            formula_class_attributes['source_file_path'] = source_file_path
        try:
            source_lines, line_number = inspect.getsourcelines(self)
        except IOError:
            line_number = None
            source_code = None
        else:
            source_code = textwrap.dedent(''.join(source_lines).decode('utf-8'))
        if source_code is not None:
            formula_class_attributes['source_code'] = source_code
        if line_number is not None:
            formula_class_attributes['line_number'] = line_number

        role = attributes.pop('role', None)
        roles = attributes.pop('roles', None)
        if role is None:
            if roles is not None:
                assert isinstance(roles, (list, tuple)) and all(isinstance(role, int) for role in roles)
        else:
            assert isinstance(role, int)
            assert roles is None
            roles = [role]
        if roles is not None:
            formula_class_attributes['roles'] = roles

        formula_class_attributes['variable_name'] = variable.name

        if issubclass(formula_class, EntityToPerson):
            assert entity_class.is_persons_entity
            column = variable.empty_clone()
        else:
            assert issubclass(formula_class, PersonToEntity)

            assert not entity_class.is_persons_entity

            if roles is None or len(roles) > 1:
                operation = attributes.pop('operation')
                assert operation in ('add', 'or'), 'Invalid operation: {}'.format(operation)
                formula_class_attributes['operation'] = operation

                if operation == 'add':
                    if variable.__class__ is columns.BoolCol:
                        column = columns.IntCol()
                    else:
                        column = variable.empty_clone()
                else:
                    assert operation == 'or'
                    column = variable.empty_clone()
            else:
                column = variable.empty_clone()

        # Ensure that all attributes defined in ConversionColumn class are used.
        assert not attributes, 'Unexpected attributes in definition of filled column {}: {}'.format(name,
            ', '.join(attributes.iterkeys()))

        formula_class = type(name.encode('utf-8'), (formula_class,), formula_class_attributes)

        # Fill column attributes.
        if cerfa_field is not None:
            column.cerfa_field = cerfa_field
        if variable.end is not None:
            column.end = variable.end
        column.entity = entity_class.symbol  # Obsolete: To remove once build_..._couple() functions are no more used.
        column.entity_key_plural = entity_class.key_plural
        column.formula_class = formula_class
        if variable.is_permanent:
            column.is_permanent = True
        column.label = label
        column.law_reference = law_reference
        column.name = name
        if variable.start is not None:
            column.start = variable.start
        if url is not None:
            column.url = url

        return column


class FormulaColumnMetaclass(type):
    """The metaclass of FormulaColumn classes: It generates a column instead of a formula FormulaColumn class."""
    def __new__(cls, name, bases, attributes):
        """Return a column containing a formula, built from FormulaColumn class definition."""
        assert len(bases) == 1, bases
        base_class = bases[0]
        if base_class is object:
            # Do nothing when creating classes DatedFormulaColumn, SimpleFormulaColumn, etc.
            return super(FormulaColumnMetaclass, cls).__new__(cls, name, bases, attributes)

        formula_class = attributes.pop('formula_class', UnboundLocalError)
        reference_column = attributes.pop('reference', None)

        if formula_class is UnboundLocalError:
            formula_class = base_class.formula_class \
                if reference_column is None or reference_column.formula_class is None \
                else reference_column.formula_class

        self = super(FormulaColumnMetaclass, cls).__new__(cls, name, bases, attributes)
        comments = inspect.getcomments(self)
        source_file_path = inspect.getsourcefile(self)
        source_lines, line_number = inspect.getsourcelines(self)
        source_code = textwrap.dedent(''.join(source_lines))

        return new_filled_column(
            base_function = attributes.pop('base_function', UnboundLocalError),
            calculate_output = attributes.pop('calculate_output', UnboundLocalError),
            category = attributes.pop('category', UnboundLocalError),
            cerfa_field = attributes.pop('cerfa_field', UnboundLocalError),
            column = attributes.pop('column', UnboundLocalError),
            comments = comments,
            doc = attributes.pop('__doc__', None),
            entity_class = attributes.pop('entity_class', UnboundLocalError),
            formula_class = formula_class,
            is_permanent = attributes.pop('is_permanent', UnboundLocalError),
            label = attributes.pop('label', UnboundLocalError),
            law_reference = attributes.pop('law_reference', UnboundLocalError),
            line_number = line_number,
            module = attributes.pop('__module__'),
            name = unicode(name),
            period_unit = attributes.pop('period_unit', UnboundLocalError),
            reference_column = reference_column,
            set_input = attributes.pop('set_input', UnboundLocalError),
            source_code = source_code,
            source_file_path = source_file_path,
            start_date = attributes.pop('start_date', UnboundLocalError),
            stop_date = attributes.pop('stop_date', UnboundLocalError),
            url = attributes.pop('url', UnboundLocalError),
            **attributes
            )


class DatedFormulaColumn(object):
    """Syntactic sugar to generate a DatedFormula class and fill its column"""
    __metaclass__ = FormulaColumnMetaclass
    formula_class = DatedFormula


class EntityToPersonColumn(object):
    """Syntactic sugar to generate an EntityToPerson class and fill its column"""
    __metaclass__ = ConversionColumnMetaclass
    formula_class = EntityToPerson


class PersonToEntityColumn(object):
    """Syntactic sugar to generate an PersonToEntity class and fill its column"""
    __metaclass__ = ConversionColumnMetaclass
    formula_class = PersonToEntity


class SimpleFormulaColumn(object):
    """Syntactic sugar to generate a SimpleFormula class and fill its column"""
    __metaclass__ = FormulaColumnMetaclass
    formula_class = SimpleFormula


def calculate_output_add(formula, period):
    return formula.holder.compute_add(period).array


def calculate_output_add_divide(formula, period):
    return formula.holder.compute_add_divide(period).array


def calculate_output_divide(formula, period):
    return formula.holder.compute_divide(period).array


def dated_function(start = None, stop = None):
    """Function decorator used to give start & stop instants to a method of a function in class DatedFormulaColumn."""
    def dated_function_decorator(function):
        function.start_instant = periods.instant(start)
        function.stop_instant = periods.instant(stop)
        return function

    return dated_function_decorator


def last_duration_last_value(formula, simulation, period):
    # This formula is used for variables that are constants between events but are period size dependent.
    # It returns the latest known value for the requested start of period but with the last period size.
    holder = formula.holder
    if holder._array_by_period is not None:
        for last_period, last_array in sorted(holder._array_by_period.iteritems(), reverse = True):
            if last_period.start <= period.start and (formula.function is None or last_period.stop >= period.stop):
                return periods.Period((last_period[0], period.start, last_period[2])), last_array
    if formula.function is not None:
        return period, exec_function(formula, simulation, period)
    column = holder.column
    array = np.empty(holder.entity.count, dtype = column.dtype)
    array.fill(column.default)
    return period, array


def make_reference_formula_decorator(entity_class_by_symbol = None, update = False):
    assert isinstance(entity_class_by_symbol, dict)

    def reference_formula_decorator(column):
        """Class decorator used to declare a formula to the relevant entity class."""
        assert isinstance(column, columns.Column)
        assert column.formula_class is not None

        entity_class = entity_class_by_symbol[column.entity]
        entity_column_by_name = entity_class.column_by_name
        name = column.name
        if not update:
            assert name not in entity_column_by_name, name
        entity_column_by_name[name] = column

        return column

    return reference_formula_decorator


def missing_value(formula, simulation, period):
    if formula.function is not None:
        return period, exec_function(formula, simulation, period)
    holder = formula.holder
    column = holder.column
    raise ValueError(u"Missing value for variable {} at {}".format(column.name, period))


def neutralize_column(column):
    """Return a new neutralized column (to be used by reforms)."""
    return new_filled_column(
        base_function = requested_period_default_value_neutralized,
        label = u'[Neutralized]' if column.label is None else u'[Neutralized] {}'.format(column.label),
        reference_column = column,
        set_input = set_input_neutralized,
        )


def new_filled_column(
    base_function = UnboundLocalError,
    calculate_output = UnboundLocalError,
    category = UnboundLocalError,
    cerfa_field = UnboundLocalError,
    column = UnboundLocalError,
    comments = UnboundLocalError,
    doc = None,
    entity_class = UnboundLocalError,
    formula_class = UnboundLocalError,
    is_permanent = UnboundLocalError,
    label = UnboundLocalError,
    law_reference = UnboundLocalError,
    line_number = UnboundLocalError,
    module = None,
    name = None,
    period_unit = UnboundLocalError,
    reference_column = None,
    set_input = UnboundLocalError,
    source_code = UnboundLocalError,
    source_file_path = UnboundLocalError,
    start_date = UnboundLocalError,
    stop_date = UnboundLocalError,
    url = UnboundLocalError,
    **specific_attributes
        ):
    # Validate arguments.

    if reference_column is not None:
        assert isinstance(reference_column, columns.Column)
        if name is None:
            name = reference_column.name

    assert isinstance(name, unicode)

    if calculate_output is UnboundLocalError:
        calculate_output = None #if reference_column is None else reference_column.formula_class.calculate_output

    # assert category is not UnboundLocalError and category is not None, category

    if cerfa_field is UnboundLocalError:
        cerfa_field = None if reference_column is None else reference_column.cerfa_field
    elif cerfa_field is not None:
        assert isinstance(cerfa_field, basestring), cerfa_field
        cerfa_field = unicode(cerfa_field)

    assert column is not None, """Missing attribute "column" in definition of filled column {}""".format(name)
    if column is UnboundLocalError:
        assert reference_column is not None, """Missing attribute "column" in definition of filled column {}""".format(
            name)
        column = reference_column.empty_clone()
    elif not isinstance(column, columns.Column):
        column = column()
        assert isinstance(column, columns.Column)

    if comments is UnboundLocalError:
        comments = None if reference_column is None else reference_column.formula_class.comments
    elif isinstance(comments, str):
        comments = comments.decode('utf-8')

    assert entity_class is not None, """Missing attribute "entity_class" in definition of filled column {}""".format(
        name)
    if entity_class is UnboundLocalError:
        assert reference_column is not None, \
            """Missing attribute "entity_class" in definition of filled column {}""".format(name)
        entity_class_key_plural = reference_column.entity_key_plural
        entity_class_symbol = reference_column.entity
    else:
        entity_class_key_plural = entity_class.key_plural
        entity_class_symbol = entity_class.symbol

    assert formula_class is not None, """Missing attribute "formula_class" in definition of filled column {}""".format(
        name)
    if formula_class is UnboundLocalError:
        assert reference_column is not None, \
            """Missing attribute "formula_class" in definition of filled column {}""".format(name)
        formula_class = reference_column.formula_class.__bases__[0]
    assert issubclass(formula_class, AbstractFormula), formula_class

    if is_permanent is UnboundLocalError:
        is_permanent = False if reference_column is None else reference_column.is_permanent
    else:
        assert is_permanent in (False, True), is_permanent

    if label is UnboundLocalError:
        label = name if reference_column is None else reference_column.label
    else:
        label = name if label is None else unicode(label)

    if law_reference is UnboundLocalError:
        law_reference = None if reference_column is None else reference_column.law_reference
    else:
        assert isinstance(law_reference, (basestring, list))

    if line_number is UnboundLocalError:
        line_number = None if reference_column is None else reference_column.formula_class.line_number
    elif isinstance(line_number, str):
        line_number = line_number.decode('utf-8')

    # assert period_unit is not UnboundLocalError and period_unit is not None, period_unit

    if set_input is UnboundLocalError:
        set_input = None if reference_column is None else reference_column.formula_class.set_input

    if source_code is UnboundLocalError:
        source_code = None if reference_column is None else reference_column.formula_class.source_code
    elif isinstance(source_code, str):
        source_code = source_code.decode('utf-8')

    if source_file_path is UnboundLocalError:
        source_file_path = None if reference_column is None else reference_column.formula_class.source_file_path
    elif isinstance(source_file_path, str):
        source_file_path = source_file_path.decode('utf-8')

    if start_date is UnboundLocalError:
        start_date = None if reference_column is None else reference_column.start
    elif start_date is not None:
        assert isinstance(start_date, datetime.date)

    if stop_date is UnboundLocalError:
        stop_date = None if reference_column is None else reference_column.end
    elif stop_date is not None:
        assert isinstance(stop_date, datetime.date)

    if url is UnboundLocalError:
        url = None if reference_column is None else reference_column.url
    elif url is not None:
        url = unicode(url)

    # Build formula class and column.

    formula_class_attributes = {}
    if doc is not None:
        formula_class_attributes['__doc__'] = doc
    if module is not None:
        assert isinstance(module, basestring)
        formula_class_attributes['__module__'] = module
    if comments is not None:
        formula_class_attributes['comments'] = comments
    if line_number is not None:
        formula_class_attributes['line_number'] = line_number
    if source_code is not None:
        formula_class_attributes['source_code'] = source_code
    if source_file_path is not None:
        formula_class_attributes['source_file_path'] = source_file_path

    if is_permanent:
        assert base_function is UnboundLocalError
        base_function = permanent_default_value
    elif column.is_period_size_independent:
        assert base_function in (missing_value, requested_period_last_value, UnboundLocalError)
        if base_function is UnboundLocalError:
            base_function = requested_period_last_value
    elif base_function is UnboundLocalError:
        base_function = requested_period_default_value
    if base_function is UnboundLocalError:
        assert reference_column is not None \
            and issubclass(reference_column.formula_class, (DatedFormula, SimpleFormula)), \
            """Missing attribute "base_function" in definition of filled column {}""".format(name)
        base_function = reference_column.formula_class.base_function
    else:
        assert base_function is not None, \
            """Missing attribute "base_function" in definition of filled column {}""".format(name)
    formula_class_attributes['base_function'] = base_function

    if calculate_output is not None:
        formula_class_attributes['calculate_output'] = calculate_output

    formula_class_attributes['category'] = category

    if period_unit is UnboundLocalError:
        period_unit = None
    formula_class_attributes['period_unit'] = period_unit

    if set_input is not None:
        formula_class_attributes['set_input'] = set_input

    if issubclass(formula_class, DatedFormula):
        assert not is_permanent
        dated_formulas_class = []
        for function_name, function in specific_attributes.copy().iteritems():
            start_instant = getattr(function, 'start_instant', UnboundLocalError)
            if start_instant is UnboundLocalError:
                # Function is not dated (and may not even be a function). Skip it.
                continue
            stop_instant = function.stop_instant
            if stop_instant is not None:
                assert start_instant <= stop_instant, 'Invalid instant interval for function {}: {} - {}'.format(
                    function_name, start_instant, stop_instant)

            dated_formula_class_attributes = formula_class_attributes.copy()
            dated_formula_class_attributes['function'] = function
            dated_formula_class = type(name.encode('utf-8'), (SimpleFormula,), dated_formula_class_attributes)

            del specific_attributes[function_name]
            dated_formulas_class.append(dict(
                formula_class = dated_formula_class,
                start_instant = start_instant,
                stop_instant = stop_instant,
                ))
        # Sort dated formulas by start instant and add missing stop instants.
        dated_formulas_class.sort(key = lambda dated_formula_class: dated_formula_class['start_instant'])
        for dated_formula_class, next_dated_formula_class in itertools.izip(dated_formulas_class,
                itertools.islice(dated_formulas_class, 1, None)):
            if dated_formula_class['stop_instant'] is None:
                dated_formula_class['stop_instant'] = next_dated_formula_class['start_instant'].offset(-1, 'day')
            else:
                assert dated_formula_class['stop_instant'] < next_dated_formula_class['start_instant'], \
                    "Dated formulas overlap: {} & {}".format(dated_formula_class, next_dated_formula_class)

        # Add dated formulas defined in (optional) reference column when they are not overridden by new dated
        # formulas.
        if reference_column is not None and issubclass(reference_column.formula_class, DatedFormula):
            for reference_dated_formula_class in reference_column.formula_class.dated_formulas_class:
                reference_dated_formula_class = reference_dated_formula_class.copy()
                for dated_formula_class in dated_formulas_class:
                    if reference_dated_formula_class['start_instant'] == dated_formula_class['start_instant'] \
                            and reference_dated_formula_class['stop_instant'] == dated_formula_class[
                                'stop_instant']:
                        break
                    if reference_dated_formula_class['start_instant'] >= dated_formula_class['start_instant'] \
                            and reference_dated_formula_class['start_instant'] < dated_formula_class[
                                'stop_instant']:
                        reference_dated_formula_class['start_instant'] = dated_formula_class['stop_instant'].offset(
                            1, 'day')
                    if reference_dated_formula_class['stop_instant'] > dated_formula_class['start_instant'] \
                            and reference_dated_formula_class['stop_instant'] <= dated_formula_class[
                                'stop_instant']:
                        reference_dated_formula_class['stop_instant'] = dated_formula_class['start_instant'].offset(
                            -1, 'day')
                    if reference_dated_formula_class['start_instant'] > reference_dated_formula_class[
                            'stop_instant']:
                        break
                else:
                    dated_formulas_class.append(reference_dated_formula_class)
            dated_formulas_class.sort(key = lambda dated_formula_class: dated_formula_class['start_instant'])

        formula_class_attributes['dated_formulas_class'] = dated_formulas_class
    else:
        assert issubclass(formula_class, SimpleFormula), formula_class

        function = specific_attributes.pop('function', UnboundLocalError)
        if is_permanent:
            assert function is UnboundLocalError
        if function is UnboundLocalError:
            assert reference_column is not None and issubclass(reference_column.formula_class, SimpleFormula), \
                """Missing attribute "function" in definition of filled column {}""".format(name)
            function = reference_column.formula_class.function
        else:
            assert function is not None, """Missing attribute "function" in definition of filled column {}""".format(
                name)
        formula_class_attributes['function'] = function

    # Ensure that all attributes defined in ConversionColumn class are used.
    assert not specific_attributes, 'Unexpected attributes in definition of variable {}: {}'.format(name,
        ', '.join(sorted(specific_attributes.iterkeys())))

    formula_class = type(name.encode('utf-8'), (formula_class,), formula_class_attributes)

    # Fill column attributes.
    if cerfa_field is not None:
        column.cerfa_field = cerfa_field
    if stop_date is not None:
        column.end = stop_date
    column.entity = entity_class_symbol  # Obsolete: To remove once build_..._couple() functions are no more used.
    column.entity_key_plural = entity_class_key_plural
    column.formula_class = formula_class
    if is_permanent:
        column.is_permanent = True
    column.label = label
    column.law_reference = law_reference
    column.name = name
    if start_date is not None:
        column.start = start_date
    if url is not None:
        column.url = url

    return column


def permanent_default_value(formula, simulation, period):
    if formula.function is not None:
        return period, exec_function(formula, simulation, period)
    holder = formula.holder
    column = holder.column
    array = np.empty(holder.entity.count, dtype = column.dtype)
    array.fill(column.default)
    return period, array


def reference_input_variable(base_function = None, calculate_output = None, column = None, entity_class = None,
        is_permanent = False, label = None, name = None, set_input = None, start_date = None, stop_date = None,
        update = False, url = None, category = None, period_unit = None):
    """Define an input variable and add it to relevant entity class."""
    if not isinstance(column, columns.Column):
        column = column()
        assert isinstance(column, columns.Column)
    if is_permanent:
        assert base_function is None
        base_function = permanent_default_value
    elif column.is_period_size_independent:
        assert base_function is None
        base_function = requested_period_last_value
    elif base_function is None:
        base_function = requested_period_default_value
    assert isinstance(name, basestring), name
    name = unicode(name)
    label = name if label is None else unicode(label)

    caller_frame = inspect.currentframe().f_back
    column.formula_class = formula_class = type(name.encode('utf-8'), (SimpleFormula,), dict(
        __module__ = inspect.getmodule(caller_frame).__name__,
        base_function = base_function,
        line_number = caller_frame.f_lineno,
        period_unit = period_unit,
        category = category,
        ))
    if calculate_output is not None:
        formula_class.calculate_output = calculate_output
    if set_input is not None:
        formula_class.set_input = set_input

    if stop_date is not None:
        assert isinstance(stop_date, datetime.date)
        column.end = stop_date
    column.entity = entity_class.symbol  # Obsolete: To remove once build_..._couple() functions are no more used.
    column.entity_key_plural = entity_class.key_plural
    if is_permanent:
        column.is_permanent = True
    column.label = label
    column.name = name
    if start_date is not None:
        assert isinstance(start_date, datetime.date)
        column.start = start_date
    if url is not None:
        column.url = unicode(url)

    entity_column_by_name = entity_class.column_by_name
    if not update:
        assert name not in entity_column_by_name, name
    entity_column_by_name[name] = column


# Base functions

def exec_function(formula, simulation, period):
    holder = formula.holder
    column = holder.column
    entity = holder.entity
    debug = simulation.debug
    try:
        array = formula.function(simulation, period)
    except:
        log.error(u'An error occurred while calling formula {}@{}<{}> in module {}'.format(
            column.name, entity.key_plural, str(period), formula.function.__module__,
            ))
        raise
    # TODO Remove this backward compatibility check.
    if isinstance(array, tuple):
        log.debug('Tuple detected! {}'.format(array))
        period, array = array
    assert isinstance(array, np.ndarray), u"Function {}@{}<{}>() --> {}, doesn't return a numpy array".format(
        column.name, entity.key_plural, str(period), array).encode('utf-8')
    assert array.size == entity.count, \
        u'Function {}@{}<{}>() --> {} returns an array of size {}, but size {} is expected for {}'.format(
            column.name, entity.key_plural, str(period), stringify_array(array),
            array.size, entity.count, entity.key_singular).encode('utf-8')
    if debug:
        try:
            # cf http://stackoverflow.com/questions/6736590/fast-check-for-nan-in-numpy
            if np.isnan(np.min(array)):
                nan_count = np.count_nonzero(np.isnan(array))
                raise NaNCreationError(u'Function {}@{}<{}>() --> {} returns {} NaN value(s)'.format(
                    column.name, entity.key_plural, str(period), stringify_array(array), nan_count).encode('utf-8'))
        except TypeError:
            pass
    if array.dtype != column.dtype:
        log.debug(u'Cast array dtype: {} to column dtype: {}'.format(array.dtype, column.dtype))
        array = array.astype(column.dtype)
    return array


def exec_function_or_default(formula, simulation, period):
    holder = formula.holder
    column = holder.column
    if formula.function is not None:
        array = exec_function(formula, simulation, period)
    else:
        array = np.empty(holder.entity.count, dtype = column.dtype)
        array.fill(column.default)
    return array


# def monthly_arithmetic_function(formula, simulation, period, is_external_output):
def monthly_arithmetic_function(formula, simulation, period):
    """
    If requested period is greater than a month (a year or many months),
    then calculate all months and sum the results.
    """
    holder = formula.holder
    column = holder.column
    array_by_period = holder._array_by_period
    if array_by_period is None:
        holder._array_by_period = array_by_period = {}
    cached_array = array_by_period.get(period)
    if cached_array is not None:
        return cached_array
    if period.unit == u'month' and period.size == 1:
        array = exec_function_or_default(formula, simulation, period)
        array_by_period[period] = array
        return array
    else:
        after_instant = period.start.offset(period.size, period.unit)
        array = np.zeros(holder.entity.count, dtype = column.dtype)
        month = period.start.period(u'month')
        while month.start < after_instant:
            month_array = array_by_period.get(month)
            if month_array is None:
                month_array = exec_function_or_default(formula, simulation, month)
                array_by_period[month] = month_array
            array += month_array
            month = month.offset(1)
        array_by_period[period] = array
        return array


def monthly_state_function(formula, simulation, period):
    """
    If requested period is greather than a month,
    then return the first known value of this period
    or exec the function for the first month if it exists
    """
    holder = formula.holder
    column = holder.column
    array_by_period = holder._array_by_period
    if array_by_period is None:
        holder._array_by_period = array_by_period = {}
    cached_array = array_by_period.get(period)
    if cached_array is not None:
        return cached_array
    if period.unit == u'month' and period.size == 1:
        array = exec_function_or_default(formula, simulation, period)
        array_by_period[period] = array
        return array
    else:
        first_month = period.start.period(u'month')
        cached_array_first_month = array_by_period.get(first_month)
        if cached_array_first_month is not None:
            return cached_array_first_month
        elif formula.function is not None:
            return exec_function(formula, simulation, first_month)
        else:
            month = first_month.offset(1)
            after_instant = period.start.offset(period.size, period.unit)
            while month.start < after_instant:
                month_array = array_by_period.get(month)
                if month_array is not None:
                    array_by_period[period] = month_array
                    return month_array
                month = month.offset(1)
            # Cas où on n'a pas trouvé de valeur dans le cache
            array = np.empty(holder.entity.count, dtype = column.dtype)
            array.fill(column.default)
            return array

def yearly_arithmetic_function(formula, simulation, period, is_external_output = False):
    holder = formula.holder
    column = holder.column
    array_by_period = holder._array_by_period
    if array_by_period is None:
        holder._array_by_period = array_by_period = {}
    cached_array = array_by_period.get(period)
    if cached_array is not None:
        return cached_array
    if period.unit == u'year' and period.size == 1:
        array = exec_function_or_default(formula, simulation, period)
        array_by_period[period] = array
        return array
    elif period.unit == u"year":
        after_instant = period.start.offset(period.size, period.unit)
        array = np.zeros(holder.entity.count, dtype = column.dtype)
        year = period.start.period(u'year')
        while year.start < after_instant:
            year_array = array_by_period.get(year)
            if year_array is None:
                year_array = exec_function_or_default(formula, simulation, year)
                array_by_period[year] = year_array
            array += year_array
            year = year.offset(1)
        array_by_period[period] = array
        return array
    elif is_external_output:
        print("TODO")
        #TODO: divice
    else:
        log.error(u'Yearly arithmetic formula {0} cannot be calculated for a monthly period {1}. You can use explicitely calculate_divide if you \
wish to get a monthly approximation of {0}'.format(
            column.name, str(period)))
        raise Exception


def requested_period_added_value(formula, simulation, period):
    # This formula is used for variables that can be added to match requested period.
    holder = formula.holder
    column = holder.column
    period_size = period.size
    period_unit = period.unit
    if holder._array_by_period is not None and (period_size > 1 or period_unit == u'year'):
        after_instant = period.start.offset(period_size, period_unit)
        if period_size > 1:
            array = np.zeros(holder.entity.count, dtype = column.dtype)
            sub_period = period.start.period(period_unit)
            while sub_period.start < after_instant:
                sub_array = holder._array_by_period.get(sub_period)
                if sub_array is None:
                    array = None
                    break
                array += sub_array
                sub_period = sub_period.offset(1)
            if array is not None:
                return period, array
        if period_unit == u'year':
            array = np.zeros(holder.entity.count, dtype = column.dtype)
            month = period.start.period(u'month')
            while month.start < after_instant:
                month_array = holder._array_by_period.get(month)
                if month_array is None:
                    array = None
                    break
                array += month_array
                month = month.offset(1)
            if array is not None:
                return period, array
    if formula.function is not None:
        return period, exec_function(formula, simulation, period)
    array = np.empty(holder.entity.count, dtype = column.dtype)
    array.fill(column.default)
    return period, array


def requested_period_default_value(formula, simulation, period):
    if formula.function is not None:
        return period, exec_function(formula, simulation, period)
    holder = formula.holder
    column = holder.column
    array = np.empty(holder.entity.count, dtype = column.dtype)
    array.fill(column.default)
    return period, array


def requested_period_default_value_neutralized(formula, simulation, period):
    holder = formula.holder
    column = holder.column
    array = np.empty(holder.entity.count, dtype = column.dtype)
    array.fill(column.default)
    return period, array


def requested_period_last_value(formula, simulation, period):
    # This formula is used for variables that are constants between events and period size independent.
    # It returns the latest known value for the requested period.
    holder = formula.holder
    if holder._array_by_period is not None:
        for last_period, last_array in sorted(holder._array_by_period.iteritems(), reverse = True):
            if last_period.start <= period.start and (formula.function is None or last_period.stop >= period.stop):
                return period, last_array
    if formula.function is not None:
        return period, exec_function(formula, simulation, period)
    column = holder.column
    array = np.empty(holder.entity.count, dtype = column.dtype)
    array.fill(column.default)
    return period, array


def set_input_dispatch_by_period(formula, period, array):
    holder = formula.holder
    holder.set_array(period, array)
    period_size = period.size
    period_unit = period.unit
    if period_unit == u'year' or period_size > 1:
        after_instant = period.start.offset(period_size, period_unit)
        if period_size > 1:
            sub_period = period.start.period(period_unit)
            while sub_period.start < after_instant:
                existing_array = holder.get_array(sub_period)
                if existing_array is None:
                    holder.set_array(sub_period, array)
                else:
                    # The array of the current sub-period is reused for the next ones.
                    array = existing_array
                sub_period = sub_period.offset(1)
        if period_unit == u'year':
            month = period.start.period(u'month')
            while month.start < after_instant:
                existing_array = holder.get_array(month)
                if existing_array is None:
                    holder.set_array(month, array)
                else:
                    # The array of the current sub-period is reused for the next ones.
                    array = existing_array
                month = month.offset(1)


def set_input_divide_by_period(formula, period, array):
    holder = formula.holder
    holder.set_array(period, array)
    period_size = period.size
    period_unit = period.unit
    if period_unit == u'year' or period_size > 1:
        after_instant = period.start.offset(period_size, period_unit)
        if period_size > 1:
            remaining_array = array.copy()
            sub_period = period.start.period(period_unit)
            sub_periods_count = period_size
            while sub_period.start < after_instant:
                existing_array = holder.get_array(sub_period)
                if existing_array is not None:
                    remaining_array -= existing_array
                    sub_periods_count -= 1
                sub_period = sub_period.offset(1)
            if sub_periods_count > 0:
                divided_array = remaining_array / sub_periods_count
                sub_period = period.start.period(period_unit)
                while sub_period.start < after_instant:
                    if holder.get_array(sub_period) is None:
                        holder.set_array(sub_period, divided_array)
                    sub_period = sub_period.offset(1)
        if period_unit == u'year':
            remaining_array = array.copy()
            month = period.start.period(u'month')
            months_count = 12 * period_size
            while month.start < after_instant:
                existing_array = holder.get_array(month)
                if existing_array is not None:
                    remaining_array -= existing_array
                    months_count -= 1
                month = month.offset(1)
            if months_count > 0:
                divided_array = remaining_array / months_count
                month = period.start.period(u'month')
                while month.start < after_instant:
                    if holder.get_array(month) is None:
                        holder.set_array(month, divided_array)
                    month = month.offset(1)


def set_input_neutralized(formula, period, array):
    pass
