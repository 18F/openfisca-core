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

from numpy import int32, logical_not as not_, maximum as max_, minimum as min_, zeros

from ..base import *  # noqa


@reference_formula
class acs_montant(DatedFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Montant de l'ACS en cas d'éligibilité"

    @dated_function(date(2000, 1, 1), date(2009, 7, 31))
    def function_2000(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        age_holder = simulation.compute('age', period)

        ages = self.filter_role(age_holder, role = CHEF)
        return period, 0 * ages

    @dated_function(date(2009, 8, 1))
    def function_2009(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        age_holder = simulation.compute('age', period)
        P = simulation.legislation_at(period.start).cmu

        ages_couple = self.split_by_roles(age_holder, roles = [CHEF, PART])
        ages_pac = self.split_by_roles(age_holder, roles = ENFS)

        return period, ((nb_par_age(ages_couple, 0, 15) + nb_par_age(ages_pac, 0, 15)) * P.acs_moins_16_ans +
            (nb_par_age(ages_couple, 16, 49) + nb_par_age(ages_pac, 16, 25)) * P.acs_16_49_ans +
            nb_par_age(ages_couple, 50, 59) * P.acs_50_59_ans +
            nb_par_age(ages_couple, 60, 200) * P.acs_plus_60_ans)


@reference_formula
class cmu_forfait_logement_base(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Forfait logement applicable en cas de propriété ou d'occupation à titre gratuit"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        cmu_nbp_foyer = simulation.calculate('cmu_nbp_foyer', period)
        P = simulation.legislation_at(period.start).cmu.forfait_logement
        law_rsa = simulation.legislation_at(period.start).minim.rmi

        return period, forfait_logement(cmu_nbp_foyer, P, law_rsa)


@reference_formula
class cmu_forfait_logement_al(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Forfait logement applicable en cas d'aide au logement"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        cmu_nbp_foyer = simulation.calculate('cmu_nbp_foyer', period)
        P = simulation.legislation_at(period.start).cmu.forfait_logement_al
        law_rsa = simulation.legislation_at(period.start).minim.rmi

        return period, forfait_logement(cmu_nbp_foyer, P, law_rsa)


@reference_formula
class cmu_nbp_foyer(SimpleFormulaColumn):
    column = PeriodSizeIndependentIntCol
    entity_class = Familles
    label = u"Nombre de personnes dans le foyer CMU"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        nb_par = simulation.calculate('nb_par', period)
        cmu_nb_pac = simulation.calculate('cmu_nb_pac', period)

        return period, nb_par + cmu_nb_pac


@reference_formula
class cmu_eligible_majoration_dom(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        residence_guadeloupe = simulation.calculate('residence_guadeloupe', period)
        residence_martinique = simulation.calculate('residence_martinique', period)
        residence_guyane = simulation.calculate('residence_guyane', period)
        residence_reunion = simulation.calculate('residence_reunion', period)

        return period, residence_guadeloupe | residence_martinique | residence_guyane | residence_reunion


@reference_formula
class cmu_c_plafond(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Plafond annuel de ressources pour l'éligibilité à la CMU-C"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        cmu_eligible_majoration_dom = simulation.calculate('cmu_eligible_majoration_dom', period)
        cmu_nbp_foyer = simulation.calculate('cmu_nbp_foyer', period)
        P = simulation.legislation_at(period.start).cmu

        return period, (P.plafond_base *
            (1 + cmu_eligible_majoration_dom * P.majoration_dom) *
            (1 + (cmu_nbp_foyer >= 2) * P.coeff_p2 +
                max_(0, min_(2, cmu_nbp_foyer - 2)) * P.coeff_p3_p4 +
                max_(0, cmu_nbp_foyer - 4) * P.coeff_p5_plus))


@reference_formula
class acs_plafond(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Plafond annuel de ressources pour l'éligibilité à l'ACS"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        cmu_c_plafond = simulation.calculate('cmu_c_plafond', period)
        P = simulation.legislation_at(period.start).cmu

        return period, cmu_c_plafond * (1 + P.majoration_plafond_acs)


@reference_formula
class cmu_base_ressources_i(SimpleFormulaColumn):
    column = FloatCol
    label = u"Base de ressources de l'individu prise en compte pour l'éligibilité à la CMU-C / ACS"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        previous_year = period.start.period('year').offset(-1)
        activite = simulation.calculate('activite', period)
        salnet = simulation.calculate('salnet', previous_year)
        chonet = simulation.calculate('chonet', previous_year)
        rstnet = simulation.calculate('rstnet', previous_year)
        pensions_alimentaires_percues = simulation.calculate('pensions_alimentaires_percues', previous_year)
        rsa_base_ressources_patrimoine_i = simulation.calculate('rsa_base_ressources_patrimoine_i', previous_year)
        aah = simulation.calculate('aah', previous_year)
        indemnites_journalieres_maternite = simulation.calculate('indemnites_journalieres_maternite', previous_year)
        indemnites_journalieres_maladie = simulation.calculate('indemnites_journalieres_maladie', previous_year)
        indemnites_journalieres_maladie_professionnelle = simulation.calculate('indemnites_journalieres_maladie_professionnelle', previous_year)
        indemnites_journalieres_accident_travail = simulation.calculate('indemnites_journalieres_accident_travail', previous_year)
        indemnites_stage = simulation.calculate('indemnites_stage', previous_year)
        revenus_stage_formation_pro = simulation.calculate('revenus_stage_formation_pro', previous_year)
        allocation_securisation_professionnelle = simulation.calculate('allocation_securisation_professionnelle', previous_year)
        prime_forfaitaire_mensuelle_reprise_activite = simulation.calculate('prime_forfaitaire_mensuelle_reprise_activite', previous_year)
        dedommagement_victime_amiante = simulation.calculate('dedommagement_victime_amiante', previous_year)
        prestation_compensatoire = simulation.calculate('prestation_compensatoire', previous_year)
        retraite_combattant = simulation.calculate('retraite_combattant', previous_year)
        pensions_invalidite = simulation.calculate('pensions_invalidite', previous_year)
        indemnites_chomage_partiel = simulation.calculate('indemnites_chomage_partiel', previous_year)
        bourse_enseignement_sup = simulation.calculate('bourse_enseignement_sup', previous_year)
        bourse_recherche = simulation.calculate('bourse_recherche', previous_year)
        gains_exceptionnels = simulation.calculate('gains_exceptionnels', previous_year)
        tns_total_revenus = simulation.calculate('tns_total_revenus', previous_year)
        P = simulation.legislation_at(period.start).cmu

        return period, ((salnet + revenus_stage_formation_pro + indemnites_chomage_partiel) * (1 - (activite == 1) * P.abattement_chomage) +
            indemnites_stage + aah + chonet + rstnet + pensions_alimentaires_percues + rsa_base_ressources_patrimoine_i + allocation_securisation_professionnelle +
            indemnites_journalieres_maternite + indemnites_journalieres_accident_travail + indemnites_journalieres_maladie + indemnites_journalieres_maladie_professionnelle +
            prime_forfaitaire_mensuelle_reprise_activite + dedommagement_victime_amiante + prestation_compensatoire +
            retraite_combattant + pensions_invalidite + bourse_enseignement_sup + bourse_recherche + gains_exceptionnels +
            tns_total_revenus)


@reference_formula
class cmu_base_ressources(SimpleFormulaColumn):
    column = FloatCol
    label = u"Base de ressources prise en compte pour l'éligibilité à la CMU-C / ACS"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        aspa = simulation.calculate('aspa', period)
        ass = simulation.calculate('ass', period)
        asi = simulation.calculate('asi', period)
        af = simulation.calculate('af', period)
        cf = simulation.calculate('cf', period)
        asf = simulation.calculate('asf', period)
        paje_clca = simulation.calculate('paje_clca', period)
        so_holder = simulation.compute('so', period)
        aide_logement = simulation.calculate('aide_logement', period)
        cmu_forfait_logement_base = simulation.calculate('cmu_forfait_logement_base', period)
        cmu_forfait_logement_al = simulation.calculate('cmu_forfait_logement_al', period)
        age_holder = simulation.compute('age', period)
        cmu_base_ressources_i_holder = simulation.compute('cmu_base_ressources_i', period)
        P = simulation.legislation_at(period.start).cmu

        so = self.cast_from_entity_to_roles(so_holder)
        so = self.filter_role(so, role = CHEF)

        cmu_br_i_par = self.split_by_roles(cmu_base_ressources_i_holder, roles = [CHEF, PART])
        cmu_br_i_pac = self.split_by_roles(cmu_base_ressources_i_holder, roles = ENFS)

        age_pac = self.split_by_roles(age_holder, roles = ENFS)

        res = (cmu_br_i_par[CHEF] + cmu_br_i_par[PART] +
            ((so == 2) + (so == 6)) * cmu_forfait_logement_base +
            (aide_logement > 0) * cmu_forfait_logement_al + aspa + ass + asi + af + cf + asf + paje_clca)

        for key, age in age_pac.iteritems():
            res += (0 <= age) * (age <= P.age_limite_pac) * cmu_br_i_pac[key]

        return period, res


@reference_formula
class cmu_nb_pac(SimpleFormulaColumn):
    column = PeriodSizeIndependentIntCol
    entity_class = Familles
    label = u"Nombre de personnes à charge au titre de la CMU"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        age_holder = simulation.compute('age', period)
        P = simulation.legislation_at(period.start).cmu

        ages = self.split_by_roles(age_holder, roles = ENFS)
        return period, nb_par_age(ages, 0, P.age_limite_pac)


@reference_formula
class cmu_c(SimpleFormulaColumn):
    '''
    Détermine si le foyer a droit à la CMU complémentaire
    '''
    column = BoolCol
    label = u"Éligibilité à la CMU-C"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        this_month = period.start.period('month')
        cmu_c_plafond = simulation.calculate('cmu_c_plafond', this_month)
        cmu_base_ressources = simulation.calculate('cmu_base_ressources', this_month)
        residence_mayotte = simulation.calculate('residence_mayotte', this_month)

        return period, not_(residence_mayotte) * (cmu_base_ressources <= cmu_c_plafond)


@reference_formula
class acs(SimpleFormulaColumn):
    '''
    Calcule le montant de l'ACS auquel le foyer a droit
    '''
    column = FloatCol
    label = u"Éligibilité à l'ACS"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        this_month = period.start.period('month')
        cmu_c = simulation.calculate('cmu_c', this_month)
        cmu_base_ressources = simulation.calculate('cmu_base_ressources', this_month)
        acs_plafond = simulation.calculate('acs_plafond', this_month)
        acs_montant = simulation.calculate('acs_montant', this_month)
        residence_mayotte = simulation.calculate('residence_mayotte', this_month)

        return period, not_(residence_mayotte) * not_(cmu_c) * (cmu_base_ressources <= acs_plafond) * acs_montant


############################################################################
# Helper functions
############################################################################


def forfait_logement(nbp_foyer, P, law_rsa):
    '''
    Calcule le forfait logement en fonction du nombre de personnes dans le "foyer CMU" et d'un jeu de taux
    '''
    return (12 * rsa_socle_base(nbp_foyer, law_rsa) *
        ((nbp_foyer == 1) * P.taux_1p + (nbp_foyer == 2) * P.taux_2p + (nbp_foyer > 2) * P.taux_3p_plus))


def nb_par_age(ages, min, max):
    '''
    Calcule le nombre d'individus ayant un âge compris entre min et max
    '''
    res = None
    for key, age in ages.iteritems():
        if res is None:
            res = zeros(len(age), dtype = int32)
        res += (min <= age) & (age <= max)
    return res


def rsa_socle_base(nbp, P):
    '''
    Calcule le RSA socle du foyer pour nombre de personnes donné
    '''
    return P.rmi * (1 + P.txp2 * (nbp >= 2) + P.txp3 * (nbp >= 3) + P.txps * max_(0, nbp - 3))
