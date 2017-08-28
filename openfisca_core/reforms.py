# -*- coding: utf-8 -*-

import copy

from . import legislations
from .taxbenefitsystems import TaxBenefitSystem


class Reform(TaxBenefitSystem):
    name = None

    def __init__(self, baseline):
        self.baseline = baseline
        self._legislation_json = baseline.get_legislation()
        self.legislation_at_instant_cache = baseline.legislation_at_instant_cache
        self.column_by_name = baseline.column_by_name.copy()
        self.decomposition_file_path = baseline.decomposition_file_path
        self.Scenario = baseline.Scenario
        self.key = unicode(self.__class__.__name__)
        if not hasattr(self, 'apply'):
            raise Exception("Reform {} must define an `apply` function".format(self.key))
        self.apply()

    def __getattr__(self, attribute):
        return getattr(self.baseline, attribute)

    @property
    def full_key(self):
        key = self.key
        assert key is not None, 'key was not set for reform {} (name: {!r})'.format(self, self.name)
        if self.baseline is not None and hasattr(self.baseline, 'key'):
            baseline_full_key = self.baseline.full_key
            key = u'.'.join([baseline_full_key, key])
        return key

    def modify_legislation_json(self, modifier_function):
        """
        Copy the baseline TaxBenefitSystem legislation_json attribute and return it.
        Used by reforms which need to modify the legislation_json, usually in the build_reform() function.
        Validates the new legislation.
        """
        baseline_legislation_json = self.baseline.get_legislation()
        baseline_legislation_json_copy = copy.deepcopy(baseline_legislation_json)
        reform_legislation_json = modifier_function(baseline_legislation_json_copy)
        assert reform_legislation_json is not None, \
            'modifier_function {} in module {} must return the modified legislation_json'.format(
                modifier_function.__name__,
                modifier_function.__module__,
                )
        assert isinstance(reform_legislation_json, legislations.Node)
        self._legislation_json = reform_legislation_json
        self.legislation_at_instant_cache = {}


def update_legislation(legislation_json, path = None, period = None, value = None, start = None, stop = None):
    """
    Update legislation JSON with a value defined for a specific couple of period defined by
    its start and stop instant or a period object.

    Returns the modified `legislation_json`.

    This function modifies `legislation_json`.

    This function is deprecated, use ValuesHistory.update() instead.
    """

    current_node = legislation_json
    for child_name in path:
        current_node = current_node[child_name]

    current_node.update(period=period, start=start, stop=stop, value=value)

    return legislation_json
