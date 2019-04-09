# -*- coding: utf-8 -*-


import numpy as np

from openfisca_core.periods import MONTH
from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_core.variables import Variable
from openfisca_core.formula_helpers import switch
from openfisca_country_template import CountryTaxBenefitSystem
from openfisca_country_template.entities import Person

from pytest import fixture


class choice(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH


class uses_multiplication(Variable):
    value_type = int
    entity = Person
    label = 'Variable with formula that uses multiplication'
    definition_period = MONTH

    def formula(person, period):
        choice = person('choice', period)
        result = (choice == 1) * 80 + (choice == 2) * 90
        return result


class uses_switch(Variable):
    value_type = int
    entity = Person
    label = 'Variable with formula that uses switch'
    definition_period = MONTH

    def formula(person, period):
        choice = person('choice', period)
        result = switch(
            choice,
            {
                1: 80,
                2: 90,
                },
            )
        return result


# TaxBenefitSystem instance declared after formulas
ourtbs = CountryTaxBenefitSystem()
ourtbs.add_variables(choice, uses_multiplication, uses_switch)


@fixture
def month():
    return '2013-01'


@fixture
def simulation(month):
    builder = SimulationBuilder()
    builder.default_period = month
    simulation = builder.build_from_variables(ourtbs, {'choice': np.random.randint(2, size = 1000) + 1})
    simulation.debug = True
    return simulation


def test_switch(simulation, month):
    uses_switch = simulation.calculate('uses_switch', period = month)
    assert isinstance(uses_switch, np.ndarray)


def test_multiplication(simulation, month):
    uses_multiplication = simulation.calculate('uses_multiplication', period = month)
    assert isinstance(uses_multiplication, np.ndarray)


def test_compare_multiplication_and_switch(simulation, month):
    uses_multiplication = simulation.calculate('uses_multiplication', period = month)
    uses_switch = simulation.calculate('uses_switch', period = month)
    assert np.all(uses_switch == uses_multiplication)
