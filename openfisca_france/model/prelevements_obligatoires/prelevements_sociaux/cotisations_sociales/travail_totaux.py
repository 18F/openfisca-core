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


from __future__ import division


import logging


from ....base import *  # noqa analysis:ignore


log = logging.getLogger(__name__)


@reference_formula
class cotisations_patronales(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales patronales"

    def function(self, simulation, period):
        period = period
        cotisations_patronales_contributives = simulation.calculate('cotisations_patronales_contributives', period)
        cotisations_patronales_non_contributives = simulation.calculate(
            'cotisations_patronales_non_contributives', period)
        cotisations_patronales_main_d_oeuvre = simulation.calculate('cotisations_patronales_main_d_oeuvre', period)

        return period, (
            cotisations_patronales_contributives +
            cotisations_patronales_non_contributives +
            cotisations_patronales_main_d_oeuvre
            )


@reference_formula
class cotisations_patronales_contributives(SimpleFormulaColumn):
    column = FloatCol
    label = u"Cotisations sociales patronales contributives"
    entity_class = Individus

    def function(self, simulation, period):
        period = period
        ags = simulation.calculate('ags', period)
        agff_tranche_a_employeur = simulation.calculate_add('agff_tranche_a_employeur', period)
        apec_employeur = simulation.calculate('apec_employeur', period)
        arrco_tranche_a_employeur = simulation.calculate('arrco_tranche_a_employeur', period)
        assedic_employeur = simulation.calculate('assedic_employeur', period)
        cotisation_exceptionnelle_temporaire_employeur = simulation.calculate(
            'cotisation_exceptionnelle_temporaire_employeur', period)
        fonds_emploi_hospitalier = simulation.calculate_add('fonds_emploi_hospitalier', period)
        ircantec_employeur = simulation.calculate_add('ircantec_employeur', period)
        pension_civile_employeur = simulation.calculate_add('pension_civile_employeur', period)
        rafp_employeur = simulation.calculate_add('rafp_employeur', period)
        vieillesse_deplafonnee_employeur = simulation.calculate_add('vieillesse_deplafonnee_employeur', period)
        vieillesse_plafonnee_employeur = simulation.calculate_add('vieillesse_plafonnee_employeur', period)

        cotisations_patronales_contributives = (
            # prive
            ags +
            agff_tranche_a_employeur +
            apec_employeur +
            arrco_tranche_a_employeur +
            assedic_employeur +
            cotisation_exceptionnelle_temporaire_employeur +
            vieillesse_deplafonnee_employeur +
            vieillesse_plafonnee_employeur +
            # public
            fonds_emploi_hospitalier +
            ircantec_employeur +
            pension_civile_employeur +
            rafp_employeur
            )
        return period, cotisations_patronales_contributives


@reference_formula
class cotisations_patronales_non_contributives(SimpleFormulaColumn):
    column = FloatCol
    label = u"Cotisations sociales patronales non-contributives"
    entity_class = Individus

    def function(self, simulation, period):
        period = period
        accident_du_travail = simulation.calculate('accident_du_travail', period)
        allocations_temporaires_invalidite = simulation.calculate_add('allocations_temporaires_invalidite', period)
        famille = simulation.calculate('famille', period)
        maladie_employeur = simulation.calculate_add('maladie_employeur', period)
        taxe_salaires = simulation.calculate_add('taxe_salaires', period)

        cotisations_patronales_non_contributives = (
            allocations_temporaires_invalidite +
            accident_du_travail +
            famille +
            maladie_employeur +
            taxe_salaires
            )
        return period, cotisations_patronales_non_contributives


@reference_formula
class cotisations_salariales_contributives(SimpleFormulaColumn):
    column = FloatCol
    label = u"Cotisations sociales salariales contributives"
    entity_class = Individus

    def function(self, simulation, period):
        period = period
        agff_tranche_a_employe = simulation.calculate_add('agff_tranche_a_employe', period)
        agirc_tranche_b_employe = simulation.calculate_add('agirc_tranche_b_employe', period)
        apec_employe = simulation.calculate_add('apec_employe', period)
        arrco_tranche_a_employe = simulation.calculate_add('arrco_tranche_a_employe', period)
        assedic_employe = simulation.calculate_add('assedic_employe', period)
        cotisation_exceptionnelle_temporaire_employe = simulation.calculate_add(
            'cotisation_exceptionnelle_temporaire_employe', period)
        ircantec_employe = simulation.calculate_add('ircantec_employe', period)
        pension_civile_employe = simulation.calculate_add('pension_civile_employe', period)
        rafp_employe = simulation.calculate_add('rafp_employe', period)
        vieillesse_deplafonnee_employe = simulation.calculate_add('vieillesse_deplafonnee_employe', period)
        vieillesse_plafonnee_employe = simulation.calculate_add('vieillesse_plafonnee_employe', period)

        cotisations_salariales_contributives = (
            # prive
            agff_tranche_a_employe +
            agirc_tranche_b_employe +
            apec_employe +
            arrco_tranche_a_employe +
            assedic_employe +
            cotisation_exceptionnelle_temporaire_employe +
            vieillesse_deplafonnee_employe +
            vieillesse_plafonnee_employe +
            # public
            ircantec_employe +
            pension_civile_employe +
            rafp_employe
            )

        return period, cotisations_salariales_contributives


@reference_formula
class cotisations_salariales_non_contributives(SimpleFormulaColumn):
    column = FloatCol
    label = u"Cotisations sociales salariales non-contributives"
    entity_class = Individus

    def function(self, simulation, period):
        period = period
        contribution_exceptionnelle_solidarite_employe = simulation.calculate_add(
            'contribution_exceptionnelle_solidarite_employe', period)
        maladie_employe = simulation.calculate_add('maladie_employe', period)

        cotisations_salariales_non_contributives = (
            # prive
            maladie_employe +
            # public
            contribution_exceptionnelle_solidarite_employe
            )

        return period, cotisations_salariales_non_contributives


@reference_formula
class cotisations_salariales(SimpleFormulaColumn):
    column = FloatCol
    label = u"Cotisations sociales salariales"
    entity_class = Individus

    def function(self, simulation, period):
        period = period
        cotisations_salariales_contributives = simulation.calculate('cotisations_salariales_contributives', period)
        cotisations_salariales_non_contributives = simulation.calculate(
            'cotisations_salariales_non_contributives', period)

        return period, cotisations_salariales_contributives + cotisations_salariales_non_contributives
