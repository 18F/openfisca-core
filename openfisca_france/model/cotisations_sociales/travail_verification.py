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
import math

from numpy import logical_not as not_, zeros

from ..base import *  # noqa


DEBUG_SAL_TYPE = 'public_titulaire_hospitaliere'
log = logging.getLogger(__name__)
taux_versement_transport_by_localisation_entreprise = None


@reference_formula
class cotisations_patronales_contributives_old(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation sociales patronales contributives"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        rafp_employeur = simulation.calculate('rafp_employeur', period)
        pension_civile_employeur = simulation.calculate('pension_civile_employeur', period)
        _P = simulation.legislation_at(period.start)

        pat = _P.cotsoc.cotisations_employeur.__dict__
        cotisations_patronales = zeros(len(salbrut))
        for category in CAT:
            iscat = (type_sal == category[1])  # category[1] is the numerical index
            if category[0] in pat.keys():
                for bar in pat[category[0]].itervalues():
                    if category[0] in [
                        "prive_cadre",
                        "prive_non_cadre",
                        "public_non_titulaire",
                        "public_titulaire_hospitaliere",
                        ]: #  TODO: move up
                        is_contrib = (bar.option == "contrib") & (bar.name not in ['cnracl', 'rafp', 'pension'])
                        temp = -(
                            iscat * bar.calc(
                                salbrut + (category[0] == 'public_non_titulaire') * (
                                    indemnite_residence + primes_fonction_publique
                                    )
                                )
                            ) * is_contrib
                        cotisations_patronales += temp

        cotisations_patronales += rafp_employeur + pension_civile_employeur
        return period, cotisations_patronales


@reference_formula
class cotisations_patronales_non_contributives_old(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation sociales patronales non contributives"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        cotisations_patronales_accident = simulation.calculate('cotisations_patronales_accident', period)
        _P = simulation.legislation_at(period.start)

        pat = _P.cotsoc.cotisations_employeur.__dict__
        cotisations_patronales = zeros(len(salbrut))
        for category in CAT:
            iscat = (type_sal == category[1])
            if category[0] in pat.keys():
                for bar in pat[category[0]].itervalues():
                    is_noncontrib = (bar.option == "noncontrib")
                    temp = -(iscat
                             * bar.calc(salbrut + (category[0] == 'public_non_titulaire') * (
                                 indemnite_residence + primes_fonction_publique))
                             * is_noncontrib)
                    cotisations_patronales += temp
        return period, cotisations_patronales + cotisations_patronales_accident


@reference_formula
class cotisations_patronales_transport(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales patronales: versement transport"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        _P = simulation.legislation_at(period.start)

        pat = _P.cotsoc.cotisations_employeur.__dict__
        transport = zeros(len(salbrut))
        for category in CAT:
            iscat = (type_sal == category[1])  # category[1] is the numerical index of the category
            if category[0] in pat.keys():  # category[0] is the name of the category
                if 'transport' in pat[category[0]]:
                    bar = pat[category[0]]['transport']
                    temp = -bar.calc(salbrut + (category[0] == 'public_non_titulaire') * (
                        indemnite_residence + primes_fonction_publique)) * iscat  # check
                    transport += temp
        return period, transport


@reference_formula
class cotisations_patronales_main_d_oeuvre_old(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation sociales patronales main d'oeuvre"
    # TODO: A discriminer selon la taille de l'entreprise
    # Il s'agit de prélèvements sur les salaires que la CN ne classe pas dans les cotisations sociales
    #  En particulier, la CN classe:
    #     - D291: taxe sur les salaire, versement transport, FNAL, CSA, taxe d'apprentissage, formation continue
    #     - D993: participation à l'effort de construction

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        cotisations_patronales_transport = simulation.calculate('cotisations_patronales_transport', period)
        _P = simulation.legislation_at(period.start)

        pat = _P.cotsoc.cotisations_employeur.__dict__
        cotisations_patronales = zeros(len(salbrut))
        for category in CAT:
            iscat = (type_sal == category[1])  # category[1] is the numerical index
            if category[0] in pat.keys():
                for bar in pat[category[0]].itervalues():
                    is_mo = (bar.option == "main-d-oeuvre")
                    temp = -(iscat
                             * bar.calc(salbrut + (category[0] == 'public_non_titulaire') * (
                                 indemnite_residence + primes_fonction_publique))
                             * is_mo)
                    cotisations_patronales += temp
        return period, cotisations_patronales + cotisations_patronales_transport
class cotisations_patronales_old(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales patronales"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        cotisations_patronales_contributives = simulation.calculate('cotisations_patronales_contributives', period)
        cotisations_patronales_non_contributives_old = simulation.calculate('cotisations_patronales_non_contributives_old', period)
        cotisations_patronales_main_d_oeuvre_old = simulation.calculate('cotisations_patronales_main_d_oeuvre_old', period)

        return period, cotisations_patronales_contributives + cotisations_patronales_non_contributives_old + cotisations_patronales_main_d_oeuvre_old


def seuil_fds(_P):
    ind_maj_ref = _P.cotsoc.sal.fonc.commun.ind_maj_ref
    pt_ind = _P.cotsoc.sal.fonc.commun.pt_ind
    seuil_mensuel = math.floor((pt_ind * ind_maj_ref) / 12)
    return seuil_mensuel


@reference_formula
class cotisations_salariales_contributives_old(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales salariales contributives"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        rafp_employe = simulation.calculate('rafp_employe', period)
        pension_civile_employe = simulation.calculate('pension_civile_employe', period)
        _P = simulation.legislation_at(period.start)

        sal = _P.cotsoc.cotisations_salarie.__dict__
        cotisations_salariales = zeros(len(salbrut))
        for category in CAT:
            iscat = (type_sal == category[1])
            if category[0] in sal:
                for bar in sal[category[0]].itervalues():
                    is_contrib = (bar.option == "contrib") & (
                        bar.name not in ["rafp", "pension", "cnracl1", "cnracl2"])  # dealed by pension civile and rafp
                    temp = -(iscat * bar.calc(
                        salbrut - hsup + (category[0] == 'public_non_titulaire') * (
                            indemnite_residence + primes_fonction_publique
                            )
                        )
                    ) * is_contrib
                    cotisations_salariales += temp
        public_titulaire = (
            (type_sal == CAT['public_titulaire_etat'])
            + (type_sal == CAT['public_titulaire_territoriale'])
            + (type_sal == CAT['public_titulaire_hospitaliere']))

        return period, cotisations_salariales + (pension_civile_employe + rafp_employe) * public_titulaire


@reference_formula
class cotisations_salariales_non_contributives_old(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales salariales non-contributives"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        rafp_employe = simulation.calculate('rafp_employe', period)
        pension_civile_employe = simulation.calculate('pension_civile_employe', period)
        cotisations_salariales_contributives_old = simulation.calculate('cotisations_salariales_contributives_old', period)
        _P = simulation.legislation_at(period.start)

        sal = _P.cotsoc.cotisations_salarie.__dict__
        cotisations_salariales = zeros(len(salbrut))
        seuil_assuj_fds = seuil_fds(_P)
    #    log.info("seuil assujetissement FDS %i", seuil_assuj_fds)
        for category in CAT:
            iscat = (type_sal == category[1])
            if category[0] in sal:
                for bar in sal[category[0]].itervalues():
                    is_exempt_fds = (category[0] in ['public_titulaire_etat', 'public_titulaire_territoriale', 'public_titulaire_hospitaliere']) * (bar.name == 'solidarite') * ((salbrut - hsup) <= seuil_assuj_fds)  # TODO: check assiette voir IPP
                    is_noncontrib = (bar.option == "noncontrib")  # and (bar.name in ["famille", "maladie"])
                    temp = -(iscat * bar.calc(
                        salbrut + primes_fonction_publique + indemnite_residence -
                        hsup + rafp_employe + pension_civile_employe +
                        cotisations_salariales_contributives_old * (
                            category[0] == 'public_non_titulaire'
                            ) * (bar.name == "excep_solidarite")
                        )  # * (category[0] == 'public_non_titulaire')
                        * is_noncontrib * not_(is_exempt_fds)
                        )
                    cotisations_salariales += temp
        return period, cotisations_salariales


@reference_formula
class cotisations_salariales_old(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales salariales"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        cotisations_salariales_contributives_old = simulation.calculate('cotisations_salariales_contributives_old', period)
        cotisations_salariales_non_contributives_old = simulation.calculate('cotisations_salariales_non_contributives_old', period)

        return period, cotisations_salariales_contributives_old + cotisations_salariales_non_contributives_old


@reference_formula
class cotisations_patronales_accident(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations patronales accident du travail et maladie professionelle"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')  # TODO month ?
        salbrut = simulation.calculate('salbrut', period)
        taux_accident_travail = simulation.calculate('taux_accident_travail', period)
        type_sal = simulation.calculate('type_sal', period)

        prive = (type_sal == CAT['prive_cadre']) + (type_sal == CAT['prive_non_cadre'])
        return period, -salbrut * taux_accident_travail * prive  # TODO: check public

