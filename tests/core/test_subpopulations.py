import numpy as np
from numpy.testing import assert_array_equal
from pytest import fixture, approx

from openfisca_core.periods import period as make_period

from .test_entities import TEST_CASE, new_simulation, FIRST_PARENT, SECOND_PARENT, PARENT, CHILD

period = make_period('2019-01')


@fixture
def simulation():
    return new_simulation(TEST_CASE)


@fixture
def p_subpop(simulation):
    condition = np.asarray([True, True, False, True, True, False])
    return simulation.persons.get_subpopulation(condition)


@fixture
def p_subpop_2(simulation):
    condition_2 = np.asarray([True, True, True, False, False, False])
    return simulation.persons.get_subpopulation(condition_2)

def test_ids(p_subpop):
    assert_array_equal(p_subpop.ids, ['ind0', 'ind1', 'ind3', 'ind4'])


def test_has_role(p_subpop):
    assert_array_equal(p_subpop.has_role(PARENT), [True, True, False, True])


def test_default_array(p_subpop):
    assert_array_equal(p_subpop.default_array('salary'), [0, 0, 0, 0])


def test_cache_global_write_subpop_read(simulation, p_subpop):
    simulation.set_input('salary', period, [1000, 2000, 0, 1200, 2400, 800])

    cached_array_subpop = p_subpop.get_cached_array('salary', period)
    assert_array_equal(cached_array_subpop.value, [1000, 2000, 1200, 2400])
    assert cached_array_subpop.mask is None


def test_cache_subpop_write_global_read(simulation, p_subpop):
    p_subpop.put_in_cache('salary', period, [1000, 2000, 1200, 2400])
    cached_array = simulation.persons.get_cached_array('salary', period)

    assert_array_equal(cached_array.value, [1000, 2000, 1200, 2400])
    assert_array_equal(cached_array.mask, p_subpop.condition)


def test_cache_subpop_write_subpop_read(p_subpop, p_subpop_2):
    p_subpop.put_in_cache('salary', period, [1000, 2000, 1200, 2400])

    cached_array = p_subpop_2.get_cached_array('salary', period)
    assert_array_equal(cached_array.value,[1000, 2000])
    assert_array_equal(cached_array.mask, [True, True, False])


def test_cache_2_subpop_write_global_read(simulation, p_subpop, p_subpop_2):
    p_subpop.put_in_cache('salary', period, np.asarray([1000, 2000, 1200, 2400]))
    p_subpop_2.put_in_cache('salary', period, np.asarray([1000, 2000, 500]))

    cached_array = simulation.persons.get_cached_array('salary', period)

    assert_array_equal(cached_array.value, [1000, 2000, 500, 1200, 2400])
    assert_array_equal(cached_array.mask, [True, True, True, True, True, False])


# def test_household_sub_pop():
#     test_case = {
#         'persons': {'ind0': {}, 'ind1': {}, 'ind2': {}, 'ind3': {}, 'ind4': {}, 'ind5': {}, 'ind6': {}},
#         'households': {
#             'h1': {'children': ['ind2', 'ind3'], 'parents': ['ind0', 'ind1']},
#             'h3': {'parents': ['ind4']},
#             'h2': {'children': ['ind6'], 'parents': ['ind5']},
#             },
#         }

#     simulation = new_simulation(test_case)
#     simulation.set_input('age', period, np.asarray([40, 37, 7, 19, 30, 54, 16]))

#     condition = simulation.household.nb_persons() > 1
#     households = simulation.household.get_subpopulation(condition)

#     age = households.members('age', period)
#     assert_array_equal(age, [40, 37, 7, 19, 54, 16])

#     assert_array_equal(households.members_entity_id, [0, 0, 0, 0, 1, 1])
#     assert_array_equal(households.members_role, [FIRST_PARENT, SECOND_PARENT, CHILD, CHILD, FIRST_PARENT, CHILD])
#     assert_array_equal(households.members_position, [0, 1, 2, 3, 0, 1])

#     assert_array_equal(households.sum(age), [40 + 37 + 19 + 7, 54 + 16])
#     assert_array_equal(households.any(age > 50), [False, True])
