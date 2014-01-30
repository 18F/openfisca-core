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


import nose

import openfisca_france
openfisca_france.init_country()
from openfisca_core.simulations import ScenarioSimulation


def test_cotsoc():
    """
    test pour un célibataire pour un revenu de 20 000, 50 000 € et 150 000 €
    et des revenus de différentes origines
    """
    dico = {
# test pour un célibataire ayant un revenu salarial (1AJ)
#            "sali": [
#            {"year" : 2010, "amount": 20000, "irpp":-1181 },
#            {"year" : 2011, "amount": 20000, "irpp":-1181 },
#            {"year" : 2010, "amount": 50000, "irpp":-7934 },
#            {"year" : 2011, "amount": 50000, "irpp":-7934 },
#            {"year" : 2010, "amount": 150000, "irpp":-42338},
#            {"year" : 2011, "amount": 150000, "irpp":-42338}
#                    ],
# test pour un retraité célibataire ayant une pension (1AS)
#            "rsti": [
#            {"year" : 2010, "amount": 20000, "irpp":-1181 },
#            {"year" : 2011, "amount": 20000, "irpp":-1181 },
#            {"year" : 2010, "amount": 50000, "irpp":-8336 },
#            {"year" : 2011, "amount": 50000, "irpp":-8336 },
#            {"year" : 2010, "amount": 150000, "irpp":-46642 },
#            {"year" : 2011, "amount": 150000, "irpp":-46642 },
#                    ],
# test sur un revenu des actions soumises à un prélèvement libératoire de 21 % (2DA)
            "f2da" : [
            {"year" : 2012, "amount": 20000,
             "vars" :
                {"prelsoc_cap_lib":-(4.5 + 2 + 0.3) * 0.01 * 20000,
                 "csg_cap_lib":-.082 * 20000,
                 "crds_cap_lib":-.005 * 20000 } },
            {"year" : 2011, "amount": 20000,
             "vars" :
                {"prelsoc_cap_lib":-(3.4 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_cap_lib":-.082 * 20000,
                 "crds_cap_lib":-.005 * 20000 } },
            {"year" : 2010, "amount": 20000,
             "vars" : {"prelsoc_cap_lib":-(2.2 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_cap_lib":-.082 * 20000,
                 "crds_cap_lib":-.005 * 20000 } }
                    ],
# # test sur un revenu (2DH) issu des produits d'assurance vie
# # et de capitalisation soumis au prélèvement libératoire de 7.5 %
#            "f2dh" :[
#            {"year" : 2010, "amount": 20000, "irpp":345},
#            {"year" : 2011, "amount": 20000, "irpp":345},
#            {"year" : 2010, "amount": 50000, "irpp":345},
#            {"year" : 2011, "amount": 50000, "irpp":345},
#            {"year" : 2010, "amount": 150000, "irpp":345},
#            {"year" : 2011, "amount": 150000, "irpp":345},
#                    ],
# test sur un revenu des actions et  parts (2DC)
            "f2dc" :[
            {"year" : 2012, "amount": 20000,
             "vars" :
                {"prelsoc_cap_bar":-(4.5 + 2 + 0.3) * 0.01 * 20000,
                 "csg_cap_bar":-.082 * 20000,
                 "crds_cap_bar":-.005 * 20000 } },
            {"year" : 2011, "amount": 20000,
             "vars" :
                {"prelsoc_cap_bar":-(3.4 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_cap_bar":-.082 * 20000,
                 "crds_cap_bar":-.005 * 20000 } },
            {"year" : 2010, "amount": 20000,
             "vars" :
                {"prelsoc_cap_bar":-(2.2 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_cap_bar":-.082 * 20000,
                 "crds_cap_bar":-.005 * 20000 } },
                     ],
# # test sur le revenu de valeurs mobilières (2TS)
            "f2ts" :[
            {"year" : 2012, "amount": 20000,
             "vars" :
                {"prelsoc_cap_bar":-(4.5 + 2 + 0.3) * 0.01 * 20000,
                 "csg_cap_bar":-.082 * 20000,
                 "crds_cap_bar":-.005 * 20000 } },
            {"year" : 2011, "amount": 20000,
             "vars" :
                {"prelsoc_cap_bar":-(3.4 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_cap_bar":-.082 * 20000,
                 "crds_cap_bar":-.005 * 20000 } },
            {"year" : 2010, "amount": 20000,
             "vars" :
                {"prelsoc_cap_bar":-(2.2 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_cap_bar":-.082 * 20000,
                 "crds_cap_bar":-.005 * 20000 } },
                     ],
# # test sur les intérêts (2TR)
            "f2tr" :[
            {"year" : 2012, "amount": 20000,
             "vars" :
                {"prelsoc_cap_bar":-(4.5 + 2 + 0.3) * 0.01 * 20000,
                 "csg_cap_bar":-.082 * 20000,
                 "crds_cap_bar":-.005 * 20000 } },
            {"year" : 2011, "amount": 20000,
             "vars" :
                {"prelsoc_cap_bar":-(3.4 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_cap_bar":-.082 * 20000,
                 "crds_cap_bar":-.005 * 20000 } },
            {"year" : 2010, "amount": 20000,
             "vars" :
                {"prelsoc_cap_bar":-(2.2 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_cap_bar":-.082 * 20000,
                 "crds_cap_bar":-.005 * 20000 } },
                     ],
# # test sur les revenus fonciers (4BA)
            "f4ba":[
            {"year" : 2012, "amount": 20000,
             "vars" :
                {"prelsoc_fon":-(4.5 + 2 + 0.3) * 0.01 * 20000,
                 "csg_fon":-.082 * 20000,
                 "crds_fon":-.005 * 20000 } },
            {"year" : 2011, "amount": 20000,
             "vars" :
                {"prelsoc_fon":-(3.4 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_fon":-.082 * 20000,
                 "crds_fon":-.005 * 20000 } },
            {"year" : 2010, "amount": 20000,
             "vars" :
                {"prelsoc_fon":-(2.2 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_fon":-.082 * 20000,
                 "crds_fon":-.005 * 20000 } },
                     ],
# # test sur les plus-values mobilières (3VG)
            "f3vg" :[
            {"year" : 2012, "amount": 20000,
             "vars" :
                {"prelsoc_pv_mo":-(4.5 + 2 + 0.3) * 0.01 * 20000,
                 "csg_pv_mo":-.082 * 20000,
                 "crds_pv_mo":-.005 * 20000 } },
            {"year" : 2011, "amount": 20000,
             "vars" :
                {"prelsoc_pv_mo":-(3.4 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_pv_mo":-.082 * 20000,
                 "crds_pv_mo":-.005 * 20000 } },
            {"year" : 2010, "amount": 20000,
             "vars" :
                {"prelsoc_pv_mo":-(2.2 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_pv_mo":-.082 * 20000,
                 "crds_pv_mo":-.005 * 20000 } },
                     ],
# # test sur les plus-values immobilières (3VZ)
            "f3vz" :[
            {"year" : 2012, "amount": 20000,
             "vars" :
                {"prelsoc_pv_immo":-(4.5 + 2 + 0.3) * 0.01 * 20000,
                 "csg_pv_immo":-.082 * 20000,
                 "crds_pv_immo":-.005 * 20000 } },
            {"year" : 2011, "amount": 20000,
             "vars" :
                {"prelsoc_pv_immo":-(3.4 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_pv_immo":-.082 * 20000,
                 "crds_pv_immo":-.005 * 20000 } },
            {"year" : 2010, "amount": 20000,
             "vars" :
                {"prelsoc_pv_immo":-(2.2 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_pv_immo":-.082 * 20000,
                 "crds_pv_immo":-.005 * 20000 } },
                     ],
            }


    for revenu, test_list in dico.iteritems():
        for item in test_list:
            year = item["year"]
            amount = item["amount"]

            for var, value in item["vars"].iteritems():
                simulation = ScenarioSimulation()
                simulation.set_config(year = year, nmen = 1)
                simulation.set_param()

                from openfisca_qt.scripts.cecilia import complete_2012_param  # TODO: FIXME when 2012 done
                if year == 2012:
                    complete_2012_param(simulation.P)

                test_case = simulation.scenario
                if revenu in ["rsti", "sali"]:
                    test_case.indiv[0].update({revenu: amount})
                elif revenu in ["f2da", "f2dh", "f2dc", "f2ts", "f2tr", "f4ba", "f3vg", "f3vz"]:
                    test_case.declar[0].update({revenu: amount})
                else:
                    assert False
                df = simulation.get_results_dataframe(index_by_code = True)
                if not abs(df.loc[var][0] - value) < 1:
                    print abs(df.loc[var][0] - value)
                    print year
                    print revenu
                    print amount
                    print var
                    print "OpenFisca :", abs(df.loc[var][0])
                    print "Real value :", value

                assert abs(df.loc[var][0] - value) < 1


if __name__ == '__main__':

#    test_cotsoc()
    nose.core.runmodule(argv = [__file__, '-v', '-i test_*.py'])
#     nose.core.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)
