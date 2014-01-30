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


from __future__ import division

############################################################################
# # Impôt Landais, Piketty, Saez
############################################################################

def _base_csg(salbrut, chobrut, rstbrut, rev_cap_bar, rev_cap_lib):
    '''
    Assiette de la csg
    '''
    return salbrut + chobrut + rstbrut + rev_cap_bar + rev_cap_lib


def _ir_lps(base_csg, nbF, nbH, statmarit, _P):
    '''
    Impôt individuel sur l'ensemble de l'assiette de la csg, comme proposé par
    Landais, Piketty, Saez (2011)
    '''
    P = _P.lps
    nbEnf = (nbF + nbH / 2)
    ae = nbEnf * P.abatt_enfant
    re = nbEnf * P.reduc_enfant
    ce = nbEnf * P.credit_enfant

    couple = (statmarit == 1) | (statmarit == 5)
    ac = couple * P.abatt_conj
    rc = couple * P.reduc_conj

    return -max_(0, P.bareme.calc(max_(base_csg - ae - ac, 0)) - re - rc) + ce
