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

import csv
import json
import pkg_resources

from numpy import ceil, fromiter, int16, logical_not as not_, maximum as max_, minimum as min_, round

import openfisca_france
from .base import *  # noqa
from .pfam import nb_enf


zone_apl_by_depcom = None


@reference_formula
class al_pac(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Nombre de personne à charge au sens des allocations logement"

    def function(self, simulation, period):
        '''
        site de la CAF en 2011:

        # Enfant à charge
        Vous assurez financièrement l'entretien et asez la responsabilité
        affective et éducative d'un enfant, que vous ayez ou non un lien de
        parenté avec lui. Il est reconnu à votre charge pour le versement
        des aides au logement jusqu'au mois précédent ses 21 ans.
        Attention, s'il travaille, il doit gagner moins de 836,55 € par mois.

        # Parents âgés ou infirmes
        Sont à votre charge s'ils vivent avec vous et si leurs revenus 2009
        ne dépassent pas 10 386,59 € :
        * vos parents ou grand-parents âgés de plus de 65 ans ou d'au moins
        60 ans, inaptes au travail, anciens déportés,
        * vos proches parents infirmes âgés de 22 ans ou plus (parents,
        grand-parents, enfants, petits enfants, frères, soeurs, oncles,
        tantes, neveux, nièces).
        '''
        period = period.start.offset('first-of', 'month').period('month')
        age_holder = simulation.compute('age', period)
        smic55_holder = simulation.compute('smic55', period)
        nbR_holder = simulation.compute('nbR', period.start.offset('first-of', 'year').period('year'))
        D_enfch = simulation.legislation_at(period.start).al.autres.D_enfch
        af = simulation.legislation_at(period.start).fam.af
        cf = simulation.legislation_at(period.start).fam.cf

        age = self.split_by_roles(age_holder, roles = ENFS)
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

        # P_AL.D_enfch est une dummy qui vaut 1 si les enfants sont comptés à
        # charge (cas actuel) et zéro sinon.
        nbR = self.cast_from_entity_to_role(nbR_holder, role = VOUS)
        al_nbinv = self.sum_by_entity(nbR)

        age1 = af.age1
        age2 = cf.age2
        al_nbenf = nb_enf(age, smic55, age1, age2)
        al_pac = D_enfch * (al_nbenf + al_nbinv)  #  TODO: manque invalides
        # TODO: il faudrait probablement définir les AL pour un ménage et non
        # pour une famille
        return period, al_pac


@reference_formula
class br_al(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Base ressource des allocations logement"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        two_years_ago = period.start.offset('first-of', 'year').period('year').offset(-2)
        etu_holder = simulation.compute('etu', period)
        boursier_holder = simulation.compute('boursier', period)
        br_pf_i_holder = simulation.compute('br_pf_i', two_years_ago)
        rev_coll_holder = simulation.compute('rev_coll', two_years_ago)
        biact = simulation.calculate('biact', period)
        Pr = simulation.legislation_at(period.start).al.ressources

        boursier = self.split_by_roles(boursier_holder, roles = [CHEF, PART])
        br_pf_i = self.split_by_roles(br_pf_i_holder, roles = [CHEF, PART])
        etu = self.split_by_roles(etu_holder, roles = [CHEF, PART])
        rev_coll = self.sum_by_entity(rev_coll_holder)
        etuC = (etu[CHEF]) & (not_(etu[PART]))
        etuP = not_(etu[CHEF]) & (etu[PART])
        etuCP = (etu[CHEF]) & (etu[PART])
        # Boursiers
        # TODO: distinguer boursier foyer/boursier locatif
        etuCB = etu[CHEF] & boursier[CHEF]
        etuPB = etu[PART] & boursier[PART]
        # self.etu = (self.etu[CHEF]>=1)|(self.etuP>=1)
        revCatVous = max_(br_pf_i[CHEF], etuC * (Pr.dar_4 - (etuCB) * Pr.dar_5))
        revCatConj = max_(br_pf_i[PART], etuP * (Pr.dar_4 - (etuPB) * Pr.dar_5))
        revCatVsCj = (
            not_(etuCP) * (revCatVous + revCatConj) +
            etuCP * max_(br_pf_i[CHEF] + br_pf_i[PART], Pr.dar_4 - (etuCB | etuPB) * Pr.dar_5 + Pr.dar_7)
            )

        # TODO: ajouter les paramètres pour les étudiants en foyer (boursier et non boursier),
        # les inclure dans le calcul somme des revenus catégoriels après abatement
        revCat = revCatVsCj + rev_coll

        # TODO: charges déductibles : pension alimentaires et abatements spéciaux
        revNet = revCat

        # On ne considère pas l'abattement sur les ressources de certaines
        # personnes (enfant, ascendants ou grands infirmes).

        # abattement forfaitaire double activité
        abatDoubleAct = biact * Pr.dar_1

        # TODO: neutralisation des ressources
        # ...

        # TODO: abbattement sur les ressources
        # ...

        # TODO: évaluation forfaitaire des ressources (première demande)

        # TODO :double résidence pour raisons professionnelles

        # Base ressource des aides au logement (arrondies aux 100 euros supérieurs)

        br_al = ceil(max_(revNet - abatDoubleAct, 0) / 100) * 100

        return period, br_al


@reference_formula
class aide_logement_montant(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Formule des aides aux logements en secteur locatif"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        concub = simulation.calculate('concub', period)
        br_al = simulation.calculate('br_al', period)
        so_holder = simulation.compute('so', period)
        loyer_holder = simulation.compute('loyer', period)
        coloc_holder = simulation.compute('coloc', period)
        isol = simulation.calculate('isol', period)
        al_pac = simulation.calculate('al_pac', period)
        zone_apl_famille = simulation.calculate('zone_apl_famille', period)
        nat_imp_holder = simulation.compute('nat_imp', period.start.period(u'year').offset('first-of'))
        al = simulation.legislation_at(period.start).al
        fam = simulation.legislation_at(period.start).fam

        so = self.cast_from_entity_to_roles(so_holder)
        so = self.filter_role(so, role = CHEF)
        loyer = self.cast_from_entity_to_roles(loyer_holder)
        loyer = self.filter_role(loyer, role = CHEF)

        zone_apl = zone_apl_famille
        # Variables individuelles
        coloc = self.any_by_roles(coloc_holder)
        # Variables du foyer fiscal
        nat_imp = self.cast_from_entity_to_roles(nat_imp_holder)
        nat_imp = self.any_by_roles(nat_imp)

        # ne prend pas en compte les chambres ni les logements-foyers.
        # variables nécéssaires dans FA
        # isol : ménage isolé
        # concub: ménage en couple (rq : concub = ~isol.
        # al_pac : nb de personne à charge du ménage prise en compte pour les AL
        # zone_apl
        # loyer
        # br_al : base ressource des al après abattement.
        # coloc (1 si colocation, 0 sinon)
        # so : statut d'occupation du logement
        #   SO==1 : Accédant à la propriété
        #   SO==2 : Propriétaire (non accédant) du logement.
        #   SO==3 : Locataire d'un logement HLM
        #   SO==4 : Locataire ou sous-locataire d'un logement loué vie non-HLM
        #   SO==5 : Locataire ou sous-locataire d'un logement loué meublé ou d'une chambre d'hôtel.
        #   sO==6 : Logé gratuitement par des parents, des amis ou l'employeur

        loca = (3 <= so) & (5 >= so)
        acce = so == 1
        rmi = al.rmi
        bmaf = fam.af.bmaf_n_2

        # # aides au logement pour les locataires
        # loyer mensuel;
        L1 = loyer
        # loyer plafond;
        lp_taux = (not_(coloc)) * 1 + coloc * al.loyers_plafond.colocation

        z1 = al.loyers_plafond.zone1
        z2 = al.loyers_plafond.zone2
        z3 = al.loyers_plafond.zone3

        Lz1 = (
            isol * (al_pac == 0) * z1.L1 +
            concub * (al_pac == 0) * z1.L2 +
            (al_pac > 0) * z1.L3 +
            (al_pac > 1) * (al_pac - 1) * z1.L4
            ) * lp_taux
        Lz2 = (
            isol * (al_pac == 0) * z2.L1 +
            concub * (al_pac == 0) * z2.L2 +
            (al_pac > 0) * z2.L3 +
            (al_pac > 1) * (al_pac - 1) * z2.L4
            ) * lp_taux
        Lz3 = (
            isol * (al_pac == 0) * z3.L1 +
            concub * (al_pac == 0) * z3.L2 +
            (al_pac > 0) * z3.L3 +
            (al_pac > 1) * (al_pac - 1) * z3.L4
            ) * lp_taux

        L2 = Lz1 * (zone_apl == 1) + Lz2 * (zone_apl == 2) + Lz3 * (zone_apl == 3)
        # loyer retenu
        L = min_(L1, L2)

        # forfait de charges
        P_fc = al.forfait_charges
        C = (
            not_(coloc) * (P_fc.fc1 + al_pac * P_fc.fc2) +
            coloc * ((isol * 0.5 + concub) * P_fc.fc1 + al_pac * P_fc.fc2)
            )

        # dépense éligible
        E = L + C

        # ressources prises en compte
        R = br_al

        # Plafond RO
        R1 = (
            al.R1.taux1 * rmi * (isol) * (al_pac == 0) +
            al.R1.taux2 * rmi * (concub) * (al_pac == 0) +
            al.R1.taux3 * rmi * (al_pac == 1) +
            al.R1.taux4 * rmi * (al_pac >= 2) +
            al.R1.taux5 * rmi * (al_pac > 2) * (al_pac - 2)
            )

        R2 = (
            al.R2.taux4 * bmaf * (al_pac >= 2) +
            al.R2.taux5 * bmaf * (al_pac > 2) * (al_pac - 2)
            )

        Ro = round(12 * (R1 - R2) * (1 - al.autres.abat_sal))

        Rp = max_(0, R - Ro)

        # Participation personnelle
        Po = max_(al.pp.taux * E, al.pp.min)

        # Taux de famille
        TF = (
            al.TF.taux1 * (isol) * (al_pac == 0) +
            al.TF.taux2 * (concub) * (al_pac == 0) +
            al.TF.taux3 * (al_pac == 1) +
            al.TF.taux4 * (al_pac == 2) +
            al.TF.taux5 * (al_pac == 3) +
            al.TF.taux6 * (al_pac >= 4) +
            al.TF.taux7 * (al_pac > 4) * (al_pac - 4)
            )
        # Loyer de référence
        L_Ref = (
            z2.L1 * (isol) * (al_pac == 0) +
            z2.L2 * (concub) * (al_pac == 0) +
            z2.L3 * (al_pac >= 1) +
            z2.L4 * (al_pac > 1) * (al_pac - 1)
            )

        RL = L / L_Ref

        # TODO: paramètres en dur ??
        TL = max_(max_(0, al.TL.taux2 * (RL - 0.45)), al.TL.taux3 * (RL - 0.75) + al.TL.taux2 * (0.75 - 0.45))

        Tp = TF + TL

        PP = Po + Tp * Rp
        al_loc = max_(0, E - PP) * loca
        al_loc = al_loc * (al_loc >= al.autres.nv_seuil)

        # # TODO: APL pour les accédants à la propriété
        al_acc = 0 * acce
        # # APL (tous)
        al = al_loc + al_acc

        return period, al


@reference_formula
class alf(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Allocation logement familiale"
    url = u"http://vosdroits.service-public.fr/particuliers/F13132.xhtml"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        aide_logement_montant = simulation.calculate('aide_logement_montant', period)
        al_pac = simulation.calculate('al_pac', period)
        so_famille = simulation.calculate('so_famille', period)
        proprietaire_proche_famille = simulation.calculate('proprietaire_proche_famille', period)

        so = so_famille
        return period, (al_pac >= 1) * (so != 3) * not_(proprietaire_proche_famille) * aide_logement_montant


@reference_formula
class als_nonet(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Allocation logement sociale (non étudiante)"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        aide_logement_montant = simulation.calculate('aide_logement_montant', period)
        al_pac = simulation.calculate('al_pac', period)
        etu_holder = simulation.compute('etu', period)
        so_famille = simulation.calculate('so_famille', period)
        proprietaire_proche_famille = simulation.calculate('proprietaire_proche_famille', period)

        so = so_famille

        etu = self.split_by_roles(etu_holder, roles = [CHEF, PART])
        return period, (al_pac == 0) * (so != 3) * not_(proprietaire_proche_famille) * not_(etu[CHEF] | etu[PART]) * aide_logement_montant


@reference_formula
class alset(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Allocation logement sociale (non étudiante)"
    url = u"https://www.caf.fr/actualites/2012/etudiants-tout-savoir-sur-les-aides-au-logement"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        aide_logement_montant = simulation.calculate('aide_logement_montant', period)
        al_pac = simulation.calculate('al_pac', period)
        etu_holder = simulation.compute('etu', period)
        so_holder = simulation.compute('so', period)
        proprietaire_proche_famille = simulation.calculate('proprietaire_proche_famille', period)

        so = self.cast_from_entity_to_roles(so_holder)
        so = self.filter_role(so, role = CHEF)

        etu = self.split_by_roles(etu_holder, roles = [CHEF, PART])
        return period, (al_pac == 0) * (so != 3) * not_(proprietaire_proche_famille) * (etu[CHEF] | etu[PART]) * aide_logement_montant


@reference_formula
class als(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Allocation logement sociale"
    url = u"http://vosdroits.service-public.fr/particuliers/F1280.xhtml"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        als_nonet = simulation.calculate('als_nonet', period)
        alset = simulation.calculate('alset', period)

        return period, als_nonet + alset


@reference_formula
class apl(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u" Aide personnalisée au logement"
    # (réservée aux logements conventionné, surtout des HLM, et financé par le fonds national de l'habitation)"
    url = u"http://vosdroits.service-public.fr/particuliers/F12006.xhtml",

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        aide_logement_montant = simulation.calculate('aide_logement_montant', period)
        so_holder = simulation.compute('so', period)

        so = self.cast_from_entity_to_roles(so_holder)
        so = self.filter_role(so, role = CHEF)
        return period, aide_logement_montant * (so == 3)


@reference_formula
class aide_logement(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Aide au logement (tout type)"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        apl = simulation.calculate('apl', period)
        als = simulation.calculate('als', period)
        alf = simulation.calculate('alf', period)

        return period, max_(max_(apl, als), alf)


@reference_formula
class crds_lgtm(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"CRDS des allocations logement"
    url = u"http://vosdroits.service-public.fr/particuliers/F17585.xhtml"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        al = simulation.calculate('al', period)
        crds = simulation.legislation_at(period.start).fam.af.crds

        return period, -al * crds


@reference_formula
class so_individu(EntityToPersonColumn):
    entity_class = Individus
    label = u"Statut d'occupation de l'individu"
    variable = Menages.column_by_name["so"]


@reference_formula
class so_famille(PersonToEntityColumn):
    entity_class = Familles
    label = u"Statut d'occupation de la famille"
    role = CHEF
    variable = Individus.column_by_name["so_individu"]


@reference_formula
class zone_apl(SimpleFormulaColumn):
    column = EnumCol(
        enum = Enum([
            u"Non renseigné",
            u"Zone 1",
            u"Zone 2",
            u"Zone 3",
            ]),
        default = 2
        )
    entity_class = Menages
    label = u"Zone APL"

    def function(self, simulation, period):
        '''
        Retrouve la zone APL (aide personnalisée au logement) de la commune
        en fonction du depcom (code INSEE)
        '''
        period = period
        depcom = simulation.calculate('depcom', period)

        preload_zone_apl()
        default_value = 2
        return period, fromiter(
            (
                zone_apl_by_depcom.get(depcom_cell, default_value)
                for depcom_cell in depcom
                ),
            dtype = int16,
            )


def preload_zone_apl():
    global zone_apl_by_depcom
    if zone_apl_by_depcom is None:
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/apl/20110914_zonage.csv',
                ) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            zone_apl_by_depcom = {
                # Keep only first char of Zonage column because of 1bis value considered equivalent to 1.
                row['CODGEO']: int(row['Zonage'][0])
                for row in csv_reader
                }
        # Add subcommunes (arrondissements and communes associées), use the same value as their parent commune.
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/apl/commune_depcom_by_subcommune_depcom.json',
                ) as json_file:
            commune_depcom_by_subcommune_depcom = json.load(json_file)
            for subcommune_depcom, commune_depcom in commune_depcom_by_subcommune_depcom.iteritems():
                zone_apl_by_depcom[subcommune_depcom] = zone_apl_by_depcom[commune_depcom]


@reference_formula
class zone_apl_individu(EntityToPersonColumn):
    entity_class = Individus
    label = u"Zone apl de la personne"
    variable = zone_apl


@reference_formula
class zone_apl_famille(PersonToEntityColumn):
    entity_class = Familles
    label = u"Zone apl de la famille"
    role = CHEF
    variable = zone_apl_individu
