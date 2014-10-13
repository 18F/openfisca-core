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


from nose.tools import assert_true

import openfisca_france
from openfisca_france import entities


TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()


def check_input_column_consumers(column):
    column_names = ['idfam', 'idfoy', 'idmen', 'noi', 'quifam', 'quifoy', 'quimen']
    column_names.extend([
        entities.Familles.name_key,
        entities.FoyersFiscaux.name_key,
        entities.Individus.name_key,
        entities.Menages.name_key,
        ])
    if column.name not in column_names:
        if not column.survey_only:
            assert_true(column.consumers, u'Input column {} has no consumer'.format(column.name))


def test():
    for column in tax_benefit_system.column_by_name.itervalues():
        if column.formula_constructor is None:
            yield check_input_column_consumers, column
