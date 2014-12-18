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


# TODO switch to to average tax rates

from __future__ import division

import copy

import logging

from openfisca_core import periods, reforms
from openfisca_core.accessors import law
from openfisca_france import entities


log = logging.getLogger(__name__)

from openfisca_france.model.base import QUIFAM, QUIFOY


VOUS = QUIFOY['vous']
CHEF = QUIFAM['chef']


def _decote(ir_plaf_qf, nb_adult, plf2015 = law.plf2015):
    '''
    Décote
    '''
    decote_celib = (ir_plaf_qf < plf2015.decote_seuil_celib) * (plf2015.decote_seuil_celib - ir_plaf_qf)
    decote_couple = (ir_plaf_qf < plf2015.decote_seuil_couple) * (plf2015.decote_seuil_couple - ir_plaf_qf)
    return (nb_adult == 1) * decote_celib + (nb_adult == 2) * decote_couple


def build_reform_entity_class_by_symbol():

    reform_entity_class_by_symbol = entities.entity_class_by_symbol.copy()
    foyers_fiscaux_class = reform_entity_class_by_symbol['foy']

    # update column_by_name
    reform_column_by_name = foyers_fiscaux_class.column_by_name.copy()
    function_by_column_name = dict(
        decote = _decote,
        )

    for name, function in function_by_column_name.iteritems():
        column = foyers_fiscaux_class.column_by_name[name]
        reform_column = reforms.replace_simple_formula_column_function(column, function)
        reform_column_by_name[name] = reform_column

    class ReformFoyersFiscaux(foyers_fiscaux_class):
        column_by_name = reform_column_by_name

    reform_entity_class_by_symbol['foy'] = ReformFoyersFiscaux

    return reform_entity_class_by_symbol


def build_new_legislation_nodes():
    return {
        "plf2015": {
            "@type": "Node",
            "description": "PLF 2015",
            "children": {
                "decote_seuil_celib": {
                    "@type": "Parameter",
                    "description": "Seuil de la décôte pour un célibataire",
                    "format": "integer",
                    "unit": "currency",
                    "values": [{'start': u'2013-01-01', 'stop': u'2014-12-31', 'value': 1135}],
                    },
                "decote_seuil_couple": {
                    "@type": "Parameter",
                    "description": "Seuil de la décôte pour un couple",
                    "format": "integer",
                    "unit": "currency",
                    "values": [{'start': u'2013-01-01', 'stop': u'2014-12-31', 'value': 1870}],
                    },
                },
            },
        }


def build_reform(tax_benefit_system):

    reference_legislation_json = tax_benefit_system.legislation_json
    reform_legislation_json = copy.deepcopy(reference_legislation_json)
    reform_year = 2014
    reform_period = periods.period('year', reform_year)

    reform_legislation_json = reforms.update_legislation(
        legislation_json = reform_legislation_json,
        path = ('children', 'ir', 'children', 'bareme', 'brackets', 1, 'rate'),
        period = reform_period,
        value = 0,
        )
    reform_legislation_json = reforms.update_legislation(
        legislation_json = reform_legislation_json,
        path = ('children', 'ir', 'children', 'bareme', 'brackets', 2, 'threshold'),
        period = reform_period,
        value = 9690,
        )

    reform_legislation_json['children'].update(build_new_legislation_nodes())

    to_entity_class_by_key_plural = lambda entity_class_by_symbol: {
        entity_class.key_plural: entity_class
        for symbol, entity_class in entity_class_by_symbol.iteritems()
        }

    reform = reforms.Reform(
        entity_class_by_key_plural = to_entity_class_by_key_plural(build_reform_entity_class_by_symbol()),
        legislation_json = reform_legislation_json,
        name = u'PLF2015',
        reference = tax_benefit_system,
        )

    return reform
