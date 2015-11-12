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


import datetime

import numpy as np
from numpy.core.defchararray import startswith

from openfisca_core import periods
from openfisca_core.columns import BoolCol, DateCol, FixedStrCol, FloatCol, IntCol
from openfisca_core.formulas import (dated_function, DatedFormulaColumn, EntityToPersonColumn,
    PersonToEntityColumn, reference_input_variable, set_input_divide_by_period, SimpleFormulaColumn)
from openfisca_core.tests import dummy_country
from openfisca_core.tests.dummy_country import Familles, Individus, reference_formula
from openfisca_core.tools import assert_near


# Input variables


reference_input_variable(
    column = IntCol,
    entity_class = Individus,
    label = u"Âge (en nombre de mois)",
    name = 'age_en_mois',
    )


reference_input_variable(
    column = DateCol,
    entity_class = Individus,
    label = u"Date de naissance",
    name = 'birth',
    )


reference_input_variable(
    column = FixedStrCol(max_length = 5),
    entity_class = Familles,
    is_permanent = True,
    label = u"""Code INSEE "depcom" de la commune de résidence de la famille""",
    name = 'depcom',
    )


reference_input_variable(
    column = FloatCol,
    entity_class = Individus,
    label = "Salaire brut",
    name = 'salaire_brut',
    set_input = set_input_divide_by_period,
    )


# Calculated variables


@reference_formula
class age(SimpleFormulaColumn):
    column = IntCol
    entity_class = Individus
    label = u"Âge (en nombre d'années)"

    def function(self, simulation, period):
        birth = simulation.get_array('birth', period)
        if birth is None:
            age_en_mois = simulation.get_array('age_en_mois', period)
            if age_en_mois is not None:
                return period, age_en_mois // 12
            birth = simulation.calculate('birth', period)
        return period, (np.datetime64(period.date) - birth).astype('timedelta64[Y]')


@reference_formula
class dom_tom(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Familles
    label = u"La famille habite-t-elle les DOM-TOM ?"

    def function(self, simulation, period):
        period = period.start.period(u'year').offset('first-of')
        depcom = simulation.calculate('depcom', period)

        return period, np.logical_or(startswith(depcom, '97'), startswith(depcom, '98'))


@reference_formula
class dom_tom_individu(EntityToPersonColumn):
    entity_class = Individus
    label = u"La personne habite-t-elle les DOM-TOM ?"
    variable = dom_tom


@reference_formula
class revenu_disponible(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Revenu disponible de l'individu"

    def function(self, simulation, period):
        period = period.start.period(u'year').offset('first-of')
        rsa = simulation.calculate_add('rsa', period)
        salaire_imposable = simulation.calculate('salaire_imposable', period)

        return period, rsa + salaire_imposable * 0.7


@reference_formula
class revenu_disponible_famille(PersonToEntityColumn):
    entity_class = Familles
    label = u"Revenu disponible de la famille"
    operation = 'add'
    variable = revenu_disponible


@reference_formula
class rsa(DatedFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"RSA"

    @dated_function(datetime.date(2010, 1, 1))
    def function_2010(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salaire_imposable = simulation.calculate_divide('salaire_imposable', period)

        return period, (salaire_imposable < 500) * 100.0

    @dated_function(datetime.date(2011, 1, 1), datetime.date(2012, 12, 31))
    def function_2011_2012(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salaire_imposable = simulation.calculate_divide('salaire_imposable', period)

        return period, (salaire_imposable < 500) * 200.0

    @dated_function(datetime.date(2013, 1, 1))
    def function_2013(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salaire_imposable = simulation.calculate_divide('salaire_imposable', period)

        return period, (salaire_imposable < 500) * 300


@reference_formula
class salaire_imposable(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Salaire imposable"

    def function(self, simulation, period):
        period = period.start.period(u'year').offset('first-of')
        dom_tom_individu = simulation.calculate('dom_tom_individu', period)
        salaire_net = simulation.calculate('salaire_net', period)

        return period, salaire_net * 0.9 - 100 * dom_tom_individu


@reference_formula
class salaire_net(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Salaire net"

    def function(self, simulation, period):
        period = period.start.period(u'year').offset('first-of')
        salaire_brut = simulation.calculate('salaire_brut', period)

        return period, salaire_brut * 0.8


# TaxBenefitSystem instance declared after formulas
tax_benefit_system = dummy_country.init_tax_benefit_system()


def test_1_axis():
    year = 2013
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 3,
                name = 'salaire_brut',
                max = 100000,
                min = 0,
                ),
            ],
        period = year,
        parent1 = {},
        parent2 = {},
        ).new_simulation(debug = True)
    assert_near(simulation.calculate('revenu_disponible_famille'), [7200, 28800, 54000], absolute_error_margin = 0.005)


def test_2_parallel_axes_1_constant():
    year = 2013
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            [
                dict(
                    count = 3,
                    name = 'salaire_brut',
                    max = 100000,
                    min = 0,
                    ),
                dict(
                    count = 3,
                    index = 1,
                    name = 'salaire_brut',
                    max = 0.0001,
                    min = 0,
                    ),
                ],
            ],
        period = year,
        parent1 = {},
        parent2 = {},
        ).new_simulation(debug = True)
    assert_near(simulation.calculate('revenu_disponible_famille'), [7200, 28800, 54000], absolute_error_margin = 0.005)


def test_2_parallel_axes_different_periods():
    year = 2013
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            [
                dict(
                    count = 3,
                    name = 'salaire_brut',
                    max = 120000,
                    min = 0,
                    period = year - 1,
                    ),
                dict(
                    count = 3,
                    index = 1,
                    name = 'salaire_brut',
                    max = 120000,
                    min = 0,
                    period = year,
                    ),
                ],
            ],
        period = year,
        parent1 = {},
        parent2 = {},
        ).new_simulation(debug = True)
    assert_near(simulation.calculate('salaire_brut', year - 1), [0, 0, 60000, 0, 120000, 0], absolute_error_margin = 0)
    assert_near(simulation.calculate('salaire_brut', '{}-01'.format(year - 1)), [0, 0, 5000, 0, 10000, 0],
        absolute_error_margin = 0)
    assert_near(simulation.calculate('salaire_brut', year), [0, 0, 0, 60000, 0, 120000], absolute_error_margin = 0)
    assert_near(simulation.calculate('salaire_brut', '{}-01'.format(year)), [0, 0, 0, 5000, 0, 10000],
        absolute_error_margin = 0)


def test_2_parallel_axes_same_values():
    year = 2013
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            [
                dict(
                    count = 3,
                    name = 'salaire_brut',
                    max = 100000,
                    min = 0,
                    ),
                dict(
                    count = 3,
                    index = 1,
                    name = 'salaire_brut',
                    max = 100000,
                    min = 0,
                    ),
                ],
            ],
        period = year,
        parent1 = {},
        parent2 = {},
        ).new_simulation(debug = True)
    assert_near(simulation.calculate('revenu_disponible_famille'), [7200, 50400, 100800], absolute_error_margin = 0.005)


def test_age():
    year = 2013
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        parent1 = dict(
            birth = datetime.date(year - 40, 1, 1),
            ),
        ).new_simulation(debug = True)
    assert_near(simulation.calculate('age'), [40], absolute_error_margin = 0.005)

    simulation = tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        parent1 = dict(
            age_en_mois = 40 * 12 + 11,
            ),
        ).new_simulation(debug = True)
    assert_near(simulation.calculate('age'), [40], absolute_error_margin = 0.005)


def check_revenu_disponible(year, depcom, expected_revenu_disponible):
    global tax_benefit_system
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 3,
                name = 'salaire_brut',
                max = 100000,
                min = 0,
                ),
            ],
        famille = dict(depcom = depcom),
        period = periods.period(year),
        parent1 = dict(),
        parent2 = dict(),
        ).new_simulation(debug = True)
    revenu_disponible = simulation.calculate('revenu_disponible')
    assert_near(revenu_disponible, expected_revenu_disponible, absolute_error_margin = 0.005)
    revenu_disponible_famille = simulation.calculate('revenu_disponible_famille')
    expected_revenu_disponible_famille = np.array([
        expected_revenu_disponible[i] + expected_revenu_disponible[i + 1]
        for i in range(0, len(expected_revenu_disponible), 2)
        ])
    assert_near(revenu_disponible_famille, expected_revenu_disponible_famille, absolute_error_margin = 0.005)


def test_revenu_disponible():
    yield check_revenu_disponible, 2009, '75101', np.array([0, 0, 25200, 0, 50400, 0])
    yield check_revenu_disponible, 2010, '75101', np.array([1200, 1200, 25200, 1200, 50400, 1200])
    yield check_revenu_disponible, 2011, '75101', np.array([2400, 2400, 25200, 2400, 50400, 2400])
    yield check_revenu_disponible, 2012, '75101', np.array([2400, 2400, 25200, 2400, 50400, 2400])
    yield check_revenu_disponible, 2013, '75101', np.array([3600, 3600, 25200, 3600, 50400, 3600])

    yield check_revenu_disponible, 2009, '97123', np.array([-70.0, -70.0, 25130.0, -70.0, 50330.0, -70.0])
    yield check_revenu_disponible, 2010, '97123', np.array([1130.0, 1130.0, 25130.0, 1130.0, 50330.0, 1130.0])
    yield check_revenu_disponible, 2011, '98456', np.array([2330.0, 2330.0, 25130.0, 2330.0, 50330.0, 2330.0])
    yield check_revenu_disponible, 2012, '98456', np.array([2330.0, 2330.0, 25130.0, 2330.0, 50330.0, 2330.0])
    yield check_revenu_disponible, 2013, '98456', np.array([3530.0, 3530.0, 25130.0, 3530.0, 50330.0, 3530.0])
