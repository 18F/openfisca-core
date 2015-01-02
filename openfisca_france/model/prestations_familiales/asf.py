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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

from numpy import (floor, maximum as max_, logical_not as not_, logical_and as and_, logical_or as or_)

from ..base import *  # noqa
from ..pfam import nb_enf


@reference_formula
class asf_elig(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Familles
    label = u"asf_elig"

    def function(self, simulation, period):
        '''
        Eligibilité à l'allocation de soutien familial (ASF)
        '''
        period = period.start.offset('first-of', 'month').period('year')
        isol = simulation.calculate('isol', period)
        residence_mayotte = simulation.calculate('residence_mayotte', period)
        caseT_holder = simulation.compute('caseT', period)
        caseL_holder = simulation.compute('caseL', period)
        alr_holder = simulation.compute('alr', period)

        caseT = self.cast_from_entity_to_role(caseT_holder, role = VOUS)
        caseT = self.any_by_roles(caseT)
        caseL = self.cast_from_entity_to_role(caseL_holder, role = VOUS)
        caseL = self.any_by_roles(caseL)
        alr = self.sum_by_entity(alr_holder)

        return period, not_(residence_mayotte) * isol * (caseT | caseL) * not_(alr > 0)


@reference_formula
class asf_nbenf(SimpleFormulaColumn):
    column = PeriodSizeIndependentIntCol(default = 0)
    entity_class = Familles
    label = u"asf_nbenf"

    def function(self, simulation, period):
        '''
        Nombre d'enfants ouvrant l'éligibilité à l'allocation de soutien familial (ASF)
        '''
        period = period.start.offset('first-of', 'month').period('year')
        age_holder = simulation.compute('age', period)
        smic55_holder = simulation.compute('smic55', period)
        P = simulation.legislation_at(period.start).fam

        # TODO: Ajouter orphelin recueilli, soustraction à l'obligation d'entretien (et date de celle-ci),
        # action devant le TGI pour complêter l'éligibilité
        age = self.split_by_roles(age_holder, roles = ENFS)
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

        return period, nb_enf(age, smic55, P.af.age1, P.af.age3)


@reference_formula
class asf(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Allocation de soutien familial"
    url = "http://vosdroits.service-public.fr/particuliers/F815.xhtml"

    def function(self, simulation, period):
        '''
        Allocation de soutien familial

        L’ASF permet d’aider le conjoint survivant ou le parent isolé ayant la garde
        d’un enfant et les familles ayant à la charge effective et permanente un enfant
        orphelin.
        Vous avez au moins un enfant à votre charge. Vous êtes son père ou sa mère et vous vivez seul(e),
        ou vous avez recueilli cet enfant et vous vivez seul ou en couple.

        http://www.caf.fr/aides-et-services/s-informer-sur-les-aides/solidarite-et-insertion/l-allocation-de-soutien-familial-asf
        '''
        period = period.start.offset('first-of', 'month').period('year')
        asf_elig = simulation.calculate('asf_elig', period)
        asf_nbenf = simulation.calculate('asf_nbenf', period)
        P = simulation.legislation_at(period.start).fam

        # TODO: la valeur est annualisé mais l'ASF peut ne pas être versée toute l'année
        return period, asf_elig * max_(0, asf_nbenf * 12 * P.af.bmaf * P.asf.taux1)

