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


import datetime

import openfisca_france


from openfisca_core.simulations import ScenarioSimulation, SurveySimulation


def test_case_study(year = 2006):
    openfisca_france.init_country()
    simulation = ScenarioSimulation()
    simulation.set_config(year = year, reforme = False, nmen = 3, maxrev = 100000, x_axis = 'sali')
    # Add husband/wife on the same tax sheet (foyer).
    simulation.scenario.addIndiv(1, datetime.date(1975, 1, 1), 'conj', 'part')
    simulation.set_param()

    # The aefa prestation can be disabled by uncommenting the following line:
    # simulation.disable_prestations( ['aefa'])
    df = simulation.get_results_dataframe()
    print df.to_string()
#    print df.to_json(orient = 'index')


def test_survey(year = 2006):
#    openfisca_france.init_country()
    simulation = SurveySimulation()
    simulation.set_config(year = year)
    simulation.set_param()
    simulation.compute()

if __name__ == '__main__':
    test_case_study()
