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

#TODO: add start and end dates
import collections
from datetime import date

from openfisca_core.columns import BoolCol, IntCol

from base import QUIFOY, build_column_couple


column_by_name = collections.OrderedDict((

    # Dons à des organismes établis en France
    build_column_couple('f7ud', IntCol(entity = 'foy',
                    label = u"Dons à des organismes d'aide aux personnes en difficulté",
                    val_type = "monetary",
                    cerfa_field = u'7UD')),

    build_column_couple('f7uf', IntCol(entity = 'foy',
                    label = u"Dons à d'autres oeuvres d'utilité publique ou fiscalement assimilables aux oeuvres d'intérêt général",
                    val_type = "monetary",
                    cerfa_field = u'7UF')),

    build_column_couple('f7xs', IntCol(entity = 'foy',
                    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -5",
                    val_type = "monetary",
                    cerfa_field = u'7XS')),

    build_column_couple('f7xt', IntCol(entity = 'foy',
                    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -4",
                    val_type = "monetary",
                    cerfa_field = u'7XT')),

    build_column_couple('f7xu', IntCol(entity = 'foy',
                    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -3",
                    val_type = "monetary",
                    cerfa_field = u'7XU')),

    build_column_couple('f7xw', IntCol(entity = 'foy',
                    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -2",
                    val_type = "monetary",
                    cerfa_field = u'7XW')),

    build_column_couple('f7xy', IntCol(entity = 'foy',
                    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -1",
                    val_type = "monetary",
                    cerfa_field = u'7XY')),

    build_column_couple('f7va', IntCol(entity = 'foy',
                    label = u"Dons à des organismes d'aides aux personnes établis dans un Etat européen",
                    val_type = "monetary",
                    cerfa_field = u'7VA',
                    start = date(2011, 1, 1))),

    build_column_couple('f7vc', IntCol(entity = 'foy',
                    label = u"Dons à des autres organismes établis dans un Etat européen",
                    val_type = "monetary",
                    cerfa_field = u'7VC',
                    start = date(2011, 1, 1))),  # f7va, f7vc

    # Cotisations syndicales des salariées et pensionnés
    build_column_couple('f7ac', IntCol(entity = 'ind',
                    label = u"Cotisations syndicales des salariées et pensionnés",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"7AC",
                                   QUIFOY['conj']: u"7AE",
                                   QUIFOY['pac1']: u"7AG",
                                   })),  # f7ac, f7ae, f7ag

    # Salarié à domicile
    build_column_couple('f7db', IntCol(entity = 'foy',
                    label = u"Sommes versées pour l'emploi d'un salarié à domicile par les personnes ayant excercé une activité professionnelle ou ayant été demandeur d'emploi l'année de perception des revenus déclarés",
                    val_type = "monetary",
                    cerfa_field = u'7DB')),

    build_column_couple('f7df', IntCol(entity = 'foy',
                    label = u"Sommes versées pour l'emploi d'un salarié à domicile par les personnes retraités, ou inactives l'année de perception des revenus déclarés",
                    val_type = "monetary",
                    cerfa_field = u'7DF')),

    build_column_couple('f7dq', BoolCol(entity = 'foy',
                     label = u"Emploi direct pour la première fois d'un salarié à domicile durant l'année de perception des revenus déclarés",
                     cerfa_field = u'7DQ')),

    build_column_couple('f7dg', BoolCol(entity = 'foy',
                     label = u"Vous, votre conjoint ou une personne à votre charge à une carte d'invalidité d'au moins 80 % l'année de perception des revenus déclarés",
                     cerfa_field = u'7DG')),

    build_column_couple('f7dl', IntCol(entity = 'foy',
                    label = u"Nombre d'ascendants bénéficiaires de l'APA, âgés de plus de 65 ans, pour lesquels des dépenses ont été engagées l'année de perception des revenus déclarés",
                    cerfa_field = u'7DL')),

    # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale
    build_column_couple('f7vy', IntCol(entity = 'foy',
                    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): Première annuité",
                    val_type = "monetary",
                    cerfa_field = u'7VY')),

    build_column_couple('f7vz', IntCol(entity = 'foy',
                    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): annuités suivantes",
                    val_type = "monetary",
                    cerfa_field = u'7VZ')),

    build_column_couple('f7vx', IntCol(entity = 'foy',
                    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs BBC acquis ou construits du 01/01/2009 au 30/09/2011",
                    val_type = "monetary",
                    cerfa_field = u'7VX')),

    build_column_couple('f7vw', IntCol(entity = 'foy',
                    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2010 au 31/12/2010: première annuité",
                    val_type = "monetary",
                    cerfa_field = u'7VW')),

    build_column_couple('f7vv', IntCol(entity = 'foy',
                    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2010 au 31/12/2010: annuités suivantes",
                    val_type = "monetary",
                    cerfa_field = u'7VV')),  # TODO: variable non présente dans OF, à intégrer partout où c'est nécessaire

    build_column_couple('f7vu', IntCol(entity = 'foy',
                    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2011 au 30/09/2011: première annuité",
                    val_type = "monetary",
                    cerfa_field = u'7VU')),  # TODO: variable non présente dans OF, à intégrer partout où c'est nécessaire

    build_column_couple('f7vt', IntCol(entity = 'foy',
                    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2011 au 30/09/2011: annuités suivantes",
                    val_type = "monetary",
                    cerfa_field = u'7VT')),  # TODO: variable non présente dans OF, à intégrer partout où c'est nécessaire

    # Dépenses d'accueil dans un établissement pour personnes âgées dépendantes
    build_column_couple('f7cd', IntCol(entity = 'foy',
                    label = u"Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 1ere personne",
                    val_type = "monetary",
                    cerfa_field = u'7CD')),

    build_column_couple('f7ce', IntCol(entity = 'foy',
                    label = u"Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 2éme personne",
                    val_type = "monetary",
                    cerfa_field = u'7CE')),

    # Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus
    build_column_couple('f7ga', IntCol(entity = 'foy',
                    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 1er enfant à charge",
                    val_type = "monetary",
                    cerfa_field = u'7GA')),

    build_column_couple('f7gb', IntCol(entity = 'foy',
                    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 2ème enfant à charge",
                    val_type = "monetary",
                    cerfa_field = u'7GB')),

    build_column_couple('f7gc', IntCol(entity = 'foy',
                    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 3ème enfant à charge",
                    val_type = "monetary",
                    cerfa_field = u'7GC')),

    build_column_couple('f7ge', IntCol(entity = 'foy',
                    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 1er enfant à charge en résidence alternée",
                    val_type = "monetary",
                    cerfa_field = u'7GE')),

    build_column_couple('f7gf', IntCol(entity = 'foy',
                    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 2ème enfant à charge en résidence alternée",
                    val_type = "monetary",
                    cerfa_field = u'7GF')),

    build_column_couple('f7gg', IntCol(entity = 'foy',
                    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 3ème enfant à charge en résidence alternée",
                    val_type = "monetary",
                    cerfa_field = u'7GG')),

    # Nombre d'enfants à charge poursuivant leurs études
    build_column_couple('f7ea', IntCol(entity = 'foy',
                    label = u"Nombre d'enfants à charge poursuivant leurs études au collège",
                    cerfa_field = u'7EA')),

    build_column_couple('f7eb', IntCol(entity = 'foy',
                    label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études au collège",
                    cerfa_field = u'7EB')),

    build_column_couple('f7ec', IntCol(entity = 'foy',
                    label = u"Nombre d'enfants à charge poursuivant leurs études au lycée",
                    cerfa_field = u'7EC')),

    build_column_couple('f7ed', IntCol(entity = 'foy',
                    label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études au lycée",
                    cerfa_field = u'7ED')),

    build_column_couple('f7ef', IntCol(entity = 'foy',
                    label = u"Nombre d'enfants à charge poursuivant leurs études dans l'enseignement supérieur",
                    cerfa_field = u'7EF')),

    build_column_couple('f7eg', IntCol(entity = 'foy',
                    label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études dans l'enseignement supérieur",
                    cerfa_field = u'7EG')),

    # Intérêts des prêts étudiants
    build_column_couple('f7td', IntCol(entity = 'foy',
                    label = u"Intérêts des prêts étudiants versés avant l'année de perception des revenus déclarés",
                    val_type = "monetary",
                    cerfa_field = u'7TD')),

    build_column_couple('f7vo', IntCol(entity = 'foy',
                    label = u"Nombre d'années de remboursement du prêt étudiant avant l'année de perception des revenus déclarés",
                    cerfa_field = u'7VO')),

    build_column_couple('f7uk', IntCol(entity = 'foy',
                    label = u"Intérêts des prêts étudiants versés durant l'année de perception des revenus déclarés",
                    val_type = "monetary",
                    cerfa_field = u'7UK')),

    # Primes de rente survie, contrats d'épargne handicap
    build_column_couple('f7gz', IntCol(entity = 'foy',
                    label = u"Primes de rente survie, contrats d'épargne handicap",
                    val_type = "monetary",
                    cerfa_field = u'7GZ')),

    # Prestations compensatoires
    build_column_couple('f7wm', IntCol(entity = 'foy',
                    label = u"Prestations compensatoires: Capital fixé en substitution de rente",
                    val_type = "monetary",
                    cerfa_field = u'7WM')),

    build_column_couple('f7wn', IntCol(entity = 'foy',
                    label = u"Prestations compensatoires: Sommes versées l'année de perception des revenus déclarés",
                    val_type = "monetary",
                    cerfa_field = u'7WN')),

    build_column_couple('f7wo', IntCol(entity = 'foy',
                    label = u"Prestations compensatoires: Sommes totales décidées par jugement l'année de perception des revenus déclarés ou capital reconstitué",
                    val_type = "monetary",
                    cerfa_field = u'7WO')),

    build_column_couple('f7wp', IntCol(entity = 'foy',
                    label = u"Prestations compensatoires: Report des sommes décidées l'année de perception des revenus -1",
                    val_type = "monetary",
                    cerfa_field = u'7WP')),

    # Dépenses en faveur de la qualité environnementale de l'habitation principale
    build_column_couple('f7we', BoolCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: éco-prêt à taux zéro avec offre de prêt émise l'année de perception des revenus déclarés",
                    cerfa_field = u'7WE')),

    build_column_couple('f7wg', BoolCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: éco-prêt à taux zéro avec offre de prêt émise l'année de perception des revenus déclarés -1",
                    val_type = "monetary",
                    cerfa_field = u'7WG',
                    start = date(2012, 1, 1))),

    build_column_couple('f7wa', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique des murs avant le 03/04/2012",
                    cerfa_field = u'7WA')),

    build_column_couple('f7wb', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique des murs à compter du 04/04/2012",
                    cerfa_field = u'7WB')),

    build_column_couple('f7wc', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique sur plus de la moitié de la surface des murs extérieurs",
                    cerfa_field = u'7WC')),

    build_column_couple('f7ve', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique de la toiture avant le 04/04/2012",
                    cerfa_field = u'7VE')),

    build_column_couple('f7vf', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique de la toiture à compter du 04/04/2012",
                    cerfa_field = u'7VF')),

    build_column_couple('f7vg', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique de toute la toiture",
                    cerfa_field = u'7VG')),

    build_column_couple('f7sg', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Matériaux d'isolation thermique des murs (acquisitionn et pose)",
                    cerfa_field = u'7SG')),

    build_column_couple('f7sj', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Matériaux d'isolation thermique des parois vitrées",
                    cerfa_field = u'7SJ')),

    build_column_couple('f7sk', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Volets isolants",
                    cerfa_field = u'7SK')),

    build_column_couple('f7sl', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Portes d'entrées donnant sur l'extérieur",
                    cerfa_field = u'7SL')),

    build_column_couple('f7sm', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Équipements de production d'électricité utilisant l'énergie radiative du soleil",
                    cerfa_field = u'7SM')),

    build_column_couple('f7sn', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Appareils de chauffage au bois ou autres biomasses remplaçant un appareil équivalent",
                    cerfa_field = u'7SN')),

    build_column_couple('f7so', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Appareils de chauffage au bois ou autres biomasses ne remplaçant pas un appareil équivalent",
                    cerfa_field = u'7SO')),

    build_column_couple('f7sp', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Pompes à chaleur autres que air/air et autres que géothermiques dont la finalité essentielle est la production de chaleur",
                    cerfa_field = u'7SP')),

    build_column_couple('f7sq', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Pompes à chaleur géothermiques dont la finalité essentielle est la production de chaleur",
                    cerfa_field = u'7SQ')),

    build_column_couple('f7sr', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Pompes à chaleur (autres que air/air) dédiées à la production d'eau chaude sanitaire (chauffe-eaux thermodynamiques)",
                    cerfa_field = u'7SR')),

    build_column_couple('f7ss', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Équipements de fourniture d'eau chaude sanitaire fonctionnant à l'énergie solaire et dotés de capteurs solaires",
                    cerfa_field = u'7SS')),

    build_column_couple('f7st', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Autres équipements de production d'énergie utilisant une source d'énergie renouvelable (éolien, hydraulique)",
                    cerfa_field = u'7ST')),

    build_column_couple('f7su', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Équipements de récupération et de traitement des eaux pluviales",
                    cerfa_field = u'7SU')),

    build_column_couple('f7sv', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Diagnostic de performance énergétique",
                    cerfa_field = u'7SV')),

    build_column_couple('f7sw', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Équipements de raccordement à un réseau de chaleur",
                    cerfa_field = u'7SW')),

                  # TODO, nouvelle variable à intégrer dans OF (cf ancien nom déjà utilisé)
                                    # TODO vérifier pour les années précédentes
# TODO: CHECK
    # Intérêts d'emprunts
#     build_column_couple('f7wg', IntCol(entity = 'foy', label = u"Intérêts d'emprunts", val_type = "monetary", cerfa_field = u'7')), # cf pour quelle année
#
     build_column_couple('f7wq', BoolCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées du 01/01/2012 au 03/04/2012",
                    cerfa_field = u'7WQ')),

    build_column_couple('f7ws', BoolCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolations des parois vitrées à compter du 04/04/2012",
                    start = date(2013, 1, 1), # TODO vérifier année de début
                    cerfa_field = u'7WS')),

    build_column_couple('f7wt', BoolCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées réalisées sur au moins la moitié des fenêtres du logement ",
                    start = date(2013, 1, 1),
                    cerfa_field = u'7WT')),  # TODO vérifier année de début

    build_column_couple('f7wu', BoolCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: achat de volets avant 2012",
                    start = date(2013, 1, 1), # TODO vérifier année de début
                    cerfa_field = u'7WU')),

    build_column_couple('f7wv', BoolCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: achat de volets en 2012",
                    start = date(2013, 1, 1), # TODO vérifier année de début
                    cerfa_field = u'7WV')),

    build_column_couple('f7ww', BoolCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: achat de portes avant 2012",
                    start = date(2013, 1, 1), # TODO vérifier année de début
                    cerfa_field = u'7WW')),

    build_column_couple('f7wx', BoolCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: achat de portes en 2012",
                    start = date(2013, 1, 1), # TODO vérifier année de début
                    cerfa_field = u'7WX')),

    build_column_couple('f7wh', BoolCol(entity = 'foy', label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale (logement achevé depuis plus de 2 ans): bouquet de travaux réalisé pendant l'année de perception des revenus",
                    start = date(2013, 1, 1),
                    cerfa_field = u'7WH')),  # TODO vérifier année de début

    build_column_couple('f7wk', BoolCol(entity = 'foy',
                     label = u"Votre habitation principale est une maison individuelle",
                     cerfa_field = u'7WK')),

    build_column_couple('f7wf', BoolCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées avant le 01/01/n-1",
                    end = date(2012, 12, 31),
                    cerfa_field = u'7WF')),  # TODO vérifier les années précédentes

    # Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale
    build_column_couple('f7wi', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: Ascenseurs électriques à traction",
                    val_type = "monetary",
                    cerfa_field = u'7WI',
                    end = date(2012, 12, 31))),

    build_column_couple('f7wj', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: équipements spécialement conçus pour les personnes âgées ou handicapées",
                    val_type = "monetary",
                    cerfa_field = u'7WJ')),

    build_column_couple('f7wl', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: travaux de prévention des risques technologiques",
                    val_type = "monetary",
                    cerfa_field = u'7WL')),

    build_column_couple('f7wr', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de l'aide aux personnes réalisées dans des habitations données en location : travaux de prévention des risques technologiques",
                    val_type = "monetary",
                    cerfa_field = u'7WR')),

    # Investissements dans les DOM-TOM dans le cadre d'une entrepise
    build_column_couple('f7ur', IntCol(entity = 'foy',
                    label = u"Investissements réalisés en n-1, total réduction d’impôt",
                    val_type = "monetary",
                    cerfa_field = u'7UR',
                    end = date(2011, 12, 31))),  # TODO: vérifier les années antérieures

    build_column_couple('f7oz', IntCol(entity = 'foy',
                    label = u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-6",
                    val_type = "monetary",
                    cerfa_field = u'7OZ',
                    end = date(2011, 12, 31))),  # TODO: vérifier les années antérieures

    build_column_couple('f7pz', IntCol(entity = 'foy',
                    label = u"Investissements outre-mer réalisés en 2007 dans le cadre d'une entreprise: report de réduction d'impôt non imputée les années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7PZ',
                    end = date(2012, 12, 31))),  # TODO: vérifier les années antérieures

    build_column_couple('f7qz', IntCol(entity = 'foy',
                    label = u"Investissements outre-mer réalisés en 2008 dans le casdre d'une entreprise: report de réduction d'impôt non imputée les années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7QZ',
                    end = date(2012, 12, 31))),  # TODO: vérifier les années antérieures

    build_column_couple('f7rz', IntCol(entity = 'foy',
                    label = u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-3",
                    val_type = "monetary",
                    cerfa_field = u'7RZ',
                    end = date(2011, 12, 31))),  # TODO: vérifier années antérieures.

# TODO: 7sz se rapporte à des choses différentes en 2012 et 2013 par rapport aux années précédentes, cf pour les années antérieures

    build_column_couple('f7sz', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location",
                    val_type = "monetary",
                    cerfa_field = u'7SZ',
                    start = date(2012, 1, 1))),  # TODO: vérifier années <=2011

    # Aide aux créateurs et repreneurs d'entreprises
    build_column_couple('f7fy', IntCol(entity = 'foy',
                    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées avant l'année n-1 et ayant pris fin en année n-1",
                    cerfa_field = u'7FY',
                    end = date(2011, 12, 31))),  # TODO: vérifier date <=2011

    build_column_couple('f7gy', IntCol(entity = 'foy',
                    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées avant l'année n-1 et ayant pris fin en année n-1",
                    cerfa_field = u'7GY',
                    end = date(2011, 12, 31))),  # TODO: vérifier date <=2011


# TODO: 7jy réutilisée en 2013

     build_column_couple('f7jy', IntCol(entity = 'foy',
                    label = u"Report de 1/9 des investissements réalisés l'année de perception des revenus déclarés -3 ou -4",
                    cerfa_field = u'7JY',
                    start = date(2013, 1, 1))),

    build_column_couple('f7hy', IntCol(entity = 'foy',
                    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées en n-1 et n'ayant pas pris fin en n-1",
                    cerfa_field = u'7HY',
                    end = date(2011, 12, 31))),  # TODO: vérifier date <=2011

    build_column_couple('f7ky', IntCol(entity = 'foy',
                    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées en n-1 et ayant pris fin en n-1",
                    cerfa_field = u'7KY',
                    end = date(2011, 12, 31))),  # TODO: vérifier date <=2011

# 7iy réutilisée en 2013
#
#     build_column_couple('f7iy', IntCol(entity = 'foy',
#                     label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées en n-1 et n'ayant pas pris fin en n-1",
#                     cerfa_field = u'7IY',
#                     end = date(2011,12,31))),  # TODO: vérifier date <=2011

    build_column_couple('f7iy', IntCol(entity = 'foy',
                    label = u"Report du solde de réduction d'impôt non encore imputé sur les investissements réalisés",
                    cerfa_field = u'7IY',
                    start = date(2013, 1, 1))),

    build_column_couple('f7ly', IntCol(entity = 'foy',
                    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions ayant pas pris fin l'année de perception des revenus déclarés",
                    cerfa_field = u'7LY')),  # 2012 et 2013 ok

    build_column_couple('f7my', IntCol(entity = 'foy',
                    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions ayant pas pris fin l'année de perception des revenus déclarés",
                    cerfa_field = u'7MY')),  # 2012 et 2013 ok

    # Travaux de restauration immobilière
    build_column_couple('f7ra', IntCol(entity = 'foy',
                    label = u"Travaux de restauration immobilière dans une zone de protection du patrimoine architectural, urbain et paysager",
                    val_type = "monetary",
                    cerfa_field = u'7RA')),  # 2012 et 2013 ok

    build_column_couple('f7rb', IntCol(entity = 'foy',
                    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé",
                    val_type = "monetary",
                    cerfa_field = u'7RB')),

    build_column_couple('f7rc', IntCol(entity = 'foy',
                    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé",
                    val_type = "monetary",
                    cerfa_field = u'7RC')),

    build_column_couple('f7rd', IntCol(entity = 'foy',
                    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé",
                    val_type = "monetary",
                    cerfa_field = u'7RD')),

    build_column_couple('f7re', IntCol(entity = 'foy',
                    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé",
                    val_type = "monetary",
                    cerfa_field = u'7RE')),

    build_column_couple('f7rf', IntCol(entity = 'foy',
                    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé",
                    val_type = "monetary",
                    cerfa_field = u'7RF')),

    build_column_couple('f7sx', IntCol(entity = 'foy',
                    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé",
                    val_type = "monetary",
                    cerfa_field = u'7SX')),

    build_column_couple('f7sy', IntCol(entity = 'foy',
                    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé",
                    val_type = "monetary",
                    cerfa_field = u'7SY')), # 2012 et 2013 ok

    build_column_couple('f7gw', IntCol(entity = 'foy',
                    label = u"Investissements achevés en n-2 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna : report de 1/5 de la réduction d'impôt",
                    cerfa_field = u'7GW',
                    start = date(2013, 1, 1))),

    build_column_couple('f7gx', IntCol(entity = 'foy',
                    label = u"Investissements achevés en n-2 avec promesse d'achat en n-3 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna : report de 1/5 de la réduction d'impôt",
                    cerfa_field = u'7GX',
                    start = date(2013, 1, 1))),

    # Investissements locatifs dans le secteur de touristique
    build_column_couple('f7xa', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique: travaux engagés avant 2011 dans un village résidentiel de tourisme",
                    val_type = "monetary",
                    cerfa_field = u'7XA',
                    start = date(2011, 1, 1),
                    end = date(2012, 12, 31))),

    build_column_couple('f7xb', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique: travaux engagés avant 2011 dans une résidence de tourisme classée ou meublée",
                    val_type = "monetary",
                    cerfa_field = u'7XB',
                    start = date(2011, 1, 1),
                    end = date(2012, 12, 31))),

    build_column_couple('f7xc', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique: prix d'acquisition ou de revient d'un logement neuf acquis ou achevé en n-1",
                    val_type = "monetary",
                    cerfa_field = u'7XC',
                    end = date(2012, 12, 31))),

    build_column_couple('f7xd', BoolCol(entity = 'foy',
                     label = u"Investissements locatifs dans le secteur de touristique: logement neuf, demande d'étalement du solde de la réduction d'impôt sur 6 ans",
                     cerfa_field = u'7XD',
                     end = date(2012, 12, 31))),

    build_column_couple('f7xe', BoolCol(entity = 'foy',
                     label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, demande d'étalement du solde de la réduction d'impôt sur 6 ans",
                     cerfa_field = u'7XE',
                     end = date(2012, 12, 31))),

    build_column_couple('f7xf', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XF')),

    build_column_couple('f7xh', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique: travaux de reconstruction, agrandissement, réparation dans une résidence de tourisme classée ou un meublé de tourisme",
                    val_type = "monetary",
                    cerfa_field = u'7XH',
                    end = date(2012, 12, 31))),

    build_column_couple('f7xi', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XI')),

    build_column_couple('f7xj', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XJ')),

    build_column_couple('f7xk', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XK')),

    build_column_couple('f7xl', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, prix de revient d'un logement réhabilité en n-1 et achevé depuis moins de 15 ans",
                    val_type = "monetary",
                    cerfa_field = u'7XL',
                    end = date(2012, 12, 31))),

    build_column_couple('f7xm', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, report de dépenses des travaux de réhabilitation achevés les années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XM')),

# TODO: f7xn cf années <= à 2011 (possible erreur dans le label pour ces dates, à vérifier)
    build_column_couple('f7xn', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XN',
                    start = date(2012, 1, 1))),

    build_column_couple('f7xo', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XO')),

    build_column_couple('f7xp', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XP')),

    build_column_couple('f7xq', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XQ')),

    build_column_couple('f7xr', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
cerfa_field = u'7XR')),

    build_column_couple('f7xv', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique: Report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XV',
                    start = date(2012, 1, 1))),

    build_column_couple('f7xx', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique: travaux engagés après 2012 dans un village résidentiel de tourisme",
                    val_type = "monetary",
                    cerfa_field = u'7XX',
                    start = date(2012, 1, 1))),

    build_column_couple('f7xz', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique: travaux engagés après 2012 dans une résidence de tourisme classée ou un meublé tourisme",
                    val_type = "monetary",
                    cerfa_field = u'7XZ',
                    start = date(2012, 1, 1))),

    build_column_couple('f7uy', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique: Report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7UY',
                    start = date(2013, 1, 1))),

    build_column_couple('f7uz', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique: Report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7UZ',
                    start = date(2013, 1, 1))),

    # Souscriptions au capital des PME
    build_column_couple('f7cf', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital des PME non cotées, petites entreprises en phase de démarrage, ou d'expansion",
                    val_type = "monetary",
                    cerfa_field = u'7CF')),

    build_column_couple('f7cl', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -4",
                    val_type = "monetary",
                    cerfa_field = u'7CL')),

    build_column_couple('f7cm', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -3",
                    val_type = "monetary",
                    cerfa_field = u'7CM')),

    build_column_couple('f7cn', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -2",
                    val_type = "monetary",
                    cerfa_field = u'7CN')),

    build_column_couple('f7cc', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -1",
                    val_type = "monetary",
                    cerfa_field = u'7CC')),

    build_column_couple('f7cq', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -1pour les start-up",
                    val_type = "monetary",
                    cerfa_field = u'7CQ')),

    build_column_couple('f7cu', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital des PME non cotées, montant versé au titre de souscriptions antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7CU')),

# TODO: en 2013 et 2012 plus de sofipêche (pourtant présent dans param à ces dates...), case 7gs réutilisée

    build_column_couple('f7gs', IntCol(entity = 'foy',
                    label = u"Reports concernant les investissements achevés ou acquis au cours des années antérieures: Investissements réalisés en n-3 en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon",
                    val_type = "monetary",
                    cerfa_field = u'7GS',
                    start = date(2013, 1, 1))),

    # Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
    build_column_couple('f7ua', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UA', end = date(2011, 12, 31))),  # vérifier <=2011
    build_column_couple('f7ub', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UB', end = date(2011, 12, 31))),  # vérifier <=2011

# en 2013 et 2012, 7uc se rapporte à autre chose, réutilisation de la case
#    build_column_couple('f7uc', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UC', end = date(2011,12,31))),  # vérifier <=2011

    build_column_couple('f7uc', IntCol(entity = 'foy',
                    label = u"Cotisations pour la défense des forêts contre l'incendie ",
                    val_type = "monetary",
                    cerfa_field = u'7UC',
                    start = date(2012, 1, 1))),

    build_column_couple('f7ui', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UI', end = date(2011, 12, 31))),  # vérifier <=2011
    build_column_couple('f7uj', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UJ', end = date(2011, 12, 31))),  # vérifier <=2011
    build_column_couple('f7qb', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QB', end = date(2011, 12, 31))),  # vérifier <=2011
    build_column_couple('f7qc', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QC', end = date(2011, 12, 31))),  # vérifier <=2011
    build_column_couple('f7qd', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QD', end = date(2011, 12, 31))),  # vérifier <=2011
    build_column_couple('f7ql', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QL', end = date(2011, 12, 31))),  # vérifier <=2011
    build_column_couple('f7qt', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QT', end = date(2011, 12, 31))),  # vérifier <=2011
    build_column_couple('f7qm', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QM', end = date(2011, 12, 31))),  # vérifier <=2011

    # Souscription de parts de fonds communs de placement dans l'innovation,
    # de fonds d'investissement de proximité
    build_column_couple('f7gq', IntCol(entity = 'foy',
                    label = u"Souscription de parts de fonds communs de placement dans l'innovation",
                    val_type = "monetary",
                    cerfa_field = u'7GQ')),

    build_column_couple('f7fq', IntCol(entity = 'foy',
                    label = u"Souscription de parts de fonds d'investissement de proximité",
                    val_type = "monetary",
                    cerfa_field = u'7FQ')),

    build_column_couple('f7fm', IntCol(entity = 'foy',
                    label = u"Souscription de parts de fonds d'investissement de proximité investis en Corse",
                    val_type = "monetary",
                    cerfa_field = u'7FM')),

    build_column_couple('f7fl', IntCol(entity = 'foy',
                    label = u"Souscription de parts de fonds d'investissement de proximité investis outre-mer par des personnes domiciliées outre-mer",
                    val_type = "monetary",
                    cerfa_field = u'7FL')),

    # Souscriptions au capital de SOFICA
    build_column_couple('f7gn', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital de SOFICA 36 %",
                    val_type = "monetary",
                    cerfa_field = u'7GN',
                    start = date(2012, 1, 1))),

    build_column_couple('f7fn', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital de SOFICA 30 %",
                    val_type = "monetary",
                    cerfa_field = u'7FN',
                    start = date(2012, 1, 1))),

    # Intérêts d'emprunt pour reprise de société
    build_column_couple('f7fh', IntCol(entity = 'foy',
                    label = u"Intérêts d'emprunt pour reprise de société",
                    val_type = "monetary", cerfa_field = u'7FH')),

    # Frais de comptabilité et d'adhésion à un CGA (centre de gestion agréée) ou à une AA (association agréée)),
    build_column_couple('f7ff', IntCol(entity = 'foy',
                    label = u"Frais de comptabilité et d'adhésion à un CGA (centre de gestion agréée) ou à une AA (association agréée)",
                    val_type = "monetary",
                    cerfa_field = u'7FF')),

    build_column_couple('f7fg', IntCol(entity = 'foy',
                    label = u"Frais de comptabilité et d'adhésion à un CGA ou à une AA: nombre d'exploitations",
                    cerfa_field = u'7FG')),

    # Travaux de conservation et de restauration d’objets classés monuments historiques
    build_column_couple('f7nz', IntCol(entity = 'foy',
                    label = u"Travaux de conservation et de restauration d’objets classés monuments historiques",
                    val_type = "monetary" ,
                    cerfa_field = u'7NZ')),

    # Dépenses de protection du patrimoine naturel
    build_column_couple('f7ka', IntCol(entity = 'foy',
                    label = u"Dépenses de protection du patrimoine naturel",
                    val_type = "monetary",
                    cerfa_field = u'7KA',
                    start = date(2010, 1, 1))),
    build_column_couple('f7kb', IntCol(entity = 'foy',
                    label = u"Dépenses de protection du patrimoine naturel (excédent de réduction d’impôt d’années antérieures qui n’a pu être imputé)",
                    val_type = "monetary",
                    cerfa_field = u'7KB',
                    start = date(2011, 1, 1))),
    build_column_couple('f7kc', IntCol(entity = 'foy',
                    label = u"Dépenses de protection du patrimoine naturel (excédent de réduction d’impôt d’années antérieures qui n’a pu être imputé)",
                    val_type = "monetary",
                    cerfa_field = u'7KC',
                    start = date(2012, 1, 1))),
    build_column_couple('f7kd', IntCol(entity = 'foy',
                    label = u"Dépenses de protection du patrimoine naturel (excédent de réduction d’impôt d’années antérieures qui n’a pu être imputé)",
                    val_type = "monetary",
                    cerfa_field = u'7KD',
                    start = date(2013, 1, 1))),

    build_column_couple('f7uh', IntCol(entity = 'foy',
                    label = u"Dons et cotisations versés aux partis politiques",
                    val_type = "monetary",
                    cerfa_field = u'7UH',
                    start = date(2013, 1, 1))),

    # Investissements forestiers
    build_column_couple('f7un', IntCol(entity = 'foy',
                    label = u"Investissements forestiers: acquisition",
                    val_type = "monetary",
                    cerfa_field = u'7UN')),

    build_column_couple('f7ul', IntCol(entity = 'foy',
                    label = u"Investissements forestiers",
                    val_type = "monetary",
                    cerfa_field = u'7UL')),

    build_column_couple('f7uu', IntCol(entity = 'foy',
                    label = u"Investissements forestiers",
                    val_type = "monetary",
                    cerfa_field = u'7UU')),

    build_column_couple('f7uv', IntCol(entity = 'foy',
                    label = u"Investissements forestiers",
                    val_type = "monetary",
                    cerfa_field = u'7UV')),

    build_column_couple('f7uw', IntCol(entity = 'foy',
                    label = u"Investissements forestiers",
                    val_type = "monetary",
                    cerfa_field = u'7UW')),

    build_column_couple('f7th', IntCol(entity = 'foy',
                    label = u"Investissements forestiers",
                    val_type = "monetary",
                    cerfa_field = u'7TH')),

    build_column_couple('f7ux', IntCol(entity = 'foy',
                    label = u"Investissements forestiers",
                    val_type = "monetary",
                    cerfa_field = u'7UX')),

    build_column_couple('f7tg', IntCol(entity = 'foy',
                    label = u"Investissements forestiers",
                    val_type = "monetary",
                    cerfa_field = u'7TG')),

    build_column_couple('f7tf', IntCol(entity = 'foy',
                    label = u"Investissements forestiers",
                    val_type = "monetary",
                    cerfa_field = u'7TF')),

    build_column_couple('f7ut', IntCol(entity = 'foy',
                    label = u"Investissements forestiers",
                    val_type = "monetary",
                    cerfa_field = u'7UT')),

    # Intérêts pour paiement différé accordé aux agriculteurs
    build_column_couple('f7um', IntCol(entity = 'foy',
                    label = u"Intérêts pour paiement différé accordé aux agriculteurs",
                    val_type = "monetary",
                    cerfa_field = u'7UM')),

    # Investissements locatifs neufs : Dispositif Scellier:
    build_column_couple('f7hj', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 en métropole",
                    val_type = "monetary",
                    cerfa_field = u'7HJ')),

    build_column_couple('f7hk', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 dans les DOM-COM",
                    val_type = "monetary",
                    cerfa_field = u'7HK')),

    build_column_couple('f7hn', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 en métropole avec promesse d'achat avant le 1er janvier 2010",
                    val_type = "monetary",
                    cerfa_field = u'7HN')),

    build_column_couple('f7ho', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 dans les DOM-COM avec promesse d'achat avant le 1er janvier 2010",
                    val_type = "monetary",
                    cerfa_field = u'7HO')),

    build_column_couple('f7hl', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2009 (métropole et DOM ne respectant pas les plafonds)",
                    val_type = "monetary",
                    cerfa_field = u'7HL')),

    build_column_couple('f7hm', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2009 dans les DOM et respectant les plafonds",
                    val_type = "monetary",
                    cerfa_field = u'7HM')),

    build_column_couple('f7hr', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés et achevés en 2009, en métropole en 2009; dans les DOM du 1.1.2009 au 26.5.2009 ; dans les DOM du 27.5.2009 au 30.12.2009 lorsqu'ils ne respectent pas les plafonds spécifiques",
                    val_type = "monetary",
                    cerfa_field = u'7HR')),

    build_column_couple('f7hs', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés et achevés en 2009 dans les DOM COM du 27.5.2009 au 31.12.2009 respectant les plafonds spécifiques",
                    val_type = "monetary",
                    cerfa_field = u'7HS')),

    build_column_couple('f7la', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1.1.2010, Report de l'année 2009",
                    val_type = "monetary",
                    cerfa_field = u'7LA')),

    build_column_couple('f7lb', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1.1.2010, Report de l'année 2010",
                    val_type = "monetary",
                    cerfa_field = u'7LB',
                    start = date(2011, 1, 1))),

    build_column_couple('f7lc', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010, Report de l'année 2010",
                    val_type = "monetary",
                    cerfa_field = u'7LC',
                    start = date(2011, 1, 1))),

    build_column_couple('f7ld', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010, Report de l'année 2011",
                    val_type = "monetary",
                    cerfa_field = u'7LD',
                    start = date(2012, 1, 1))),

    build_column_couple('f7le', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1.1.2010, Report de l'année 2011",
                    val_type = "monetary",
                    cerfa_field = u'7LE',
                    start = date(2012, 1, 1))),

    build_column_couple('f7lf', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2011 : report du solde de réduction d'impôt de l'année 2011",
                    val_type = "monetary",
                    cerfa_field = u'7LF',
                    start = date(2012, 1, 1))),

    build_column_couple('f7ls', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010",
                    val_type = "monetary",
                    cerfa_field = u'7LS',
                    start = date(2013, 1, 1))),

    build_column_couple('f7lm', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1.1.2010",
                    val_type = "monetary",
                    cerfa_field = u'7LM',
                    start = date(2013, 1, 1))),

    build_column_couple('f7lz', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Report du solde de réduction d'impôt de l'année 2012",
                    val_type = "monetary",
                    cerfa_field = u'7LZ',
                    start = date(2013, 1, 1))),

    build_column_couple('f7mg', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2012 : report du solde de réduction d'impôt de l'année 2012",
                    val_type = "monetary",
                    cerfa_field = u'7MG',
                    start = date(2013, 1, 1))),

    build_column_couple('f7na', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2011, métropole, BBC",
                    val_type = "monetary",
                    cerfa_field = u'7NA',
                    start = date(2011, 1, 1))),

    build_column_couple('f7nb', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2010, réalisés en 2011, ",
                    val_type = "monetary",
                    cerfa_field = u'7NB',
                    start = date(2011, 1, 1))),

    build_column_couple('f7nc', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.1.2011 au 31.1.2011, métropole, BBC",
                    val_type = "monetary",
                    cerfa_field = u'7NC',
                    start = date(2011, 1, 1))),

    build_column_couple('f7nd', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.2.2011 au 31.3.2011, métropole, BBC",
                    val_type = "monetary",
                    cerfa_field = u'7ND',
                    start = date(2011, 1, 1))),

    build_column_couple('f7ne', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.4.2011 au 31.12.2011, métropole, BBC",
                    val_type = "monetary",
                    cerfa_field = u'7NE',
                    start = date(2011, 1, 1))),

    build_column_couple('f7nf', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2011, ",
                    val_type = "monetary",
                    cerfa_field = u'7NF',
                    start = date(2011, 1, 1))),

    build_column_couple('f7ng', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2010, réalisés en 2011, ",
                    val_type = "monetary",
                    cerfa_field = u'7NG',
                    start = date(2011, 1, 1))),

    build_column_couple('f7nh', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.1.2011 au 31.1.2011, Investissement réalisé du 1.1.2011 au 31.1.2011, métropole, non-BBC",
                    val_type = "monetary",
                    cerfa_field = u'7NH',
                    start = date(2011, 1, 1))),

    build_column_couple('f7ni', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.2.2011 au 31.3.2011, métropole, non-BBC",
                    val_type = "monetary",
                    cerfa_field = u'7NI',
                    start = date(2011, 1, 1))),

    build_column_couple('f7nj', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.4.2011 au 31.12.2011, métropole, non-BBC",
                    val_type = "monetary",
                    cerfa_field = u'7NJ',
                    start = date(2011, 1, 1))),

    build_column_couple('f7nk', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon",
                    val_type = "monetary",
                    cerfa_field = u'7NK',
                    start = date(2011, 1, 1))),

    build_column_couple('f7nl', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2010, réalisés en 2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon",
                    val_type = "monetary",
                    cerfa_field = u'7NL',
                    start = date(2011, 1, 1))),

    build_column_couple('f7nm', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.1.2011 au 31.1.2011, Investissement réalisé du 1.1.2011 au 31.1.2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon",
                    val_type = "monetary",
                    cerfa_field = u'7NM',
                    start = date(2011, 1, 1))),

    build_column_couple('f7nn', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.2.2011 au 31.3.2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon",
                    val_type = "monetary",
                    cerfa_field = u'7NN',
                    start = date(2011, 1, 1))),

    build_column_couple('f7no', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.4.2011 au 31.12.2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon",
                    val_type = "monetary",
                    cerfa_field = u'7NO',
                    start = date(2011, 1, 1))),

    build_column_couple('f7np', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna",
                    val_type = "monetary",
                    cerfa_field = u'7NP',
                    start = date(2011, 1, 1))),

    build_column_couple('f7nq', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2010, réalisés en 2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna",
                    val_type = "monetary",
                    cerfa_field = u'7NQ',
                    start = date(2011, 1, 1))),

    build_column_couple('f7nr', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.1.2011 au 31.1.2011, Investissement réalisé du 1.1.2011 au 31.1.2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna",
                    val_type = "monetary",
                    cerfa_field = u'7NR',
                    start = date(2011, 1, 1))),

    build_column_couple('f7ns', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.2.2011 au 31.3.2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna",
                    val_type = "monetary",
                    cerfa_field = u'7NS',
                    start = date(2011, 1, 1))),

    build_column_couple('f7nt', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.4.2011 au 31.12.2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna",
                    val_type = "monetary",
                    cerfa_field = u'7NT',
                    start = date(2011, 1, 1))),

    build_column_couple('f7hv', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2010 en métropole",
                    val_type = "monetary",
                    cerfa_field = u'7HV',
                    start = date(2011, 1, 1))),

    build_column_couple('f7hw', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2010 dans les DOM COM",
                    val_type = "monetary",
                    cerfa_field = u'7HW',
                    start = date(2011, 1, 1))),

    build_column_couple('f7hx', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2010 en métropole avec promesse d'achat avant le 1.1.2010",
                    val_type = "monetary",
                    cerfa_field = u'7HX',
                    start = date(2011, 1, 1))),

    build_column_couple('f7hz', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2010 dans les DOM COM avec promesse d'achat avant le 1.1.2010",
                    val_type = "monetary",
                    cerfa_field = u'7HZ',
                    start = date(2011, 1, 1))),

    build_column_couple('f7ht', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2009, Investissements réalisés en 2009 et achevés en 2010, en métropole en 2009; dans les DOM du 1.1.2009 au 26.5.2009 ; dans les DOM du 27.5.2009 au 30.12.2009 lorsqu'ils ne respectent pas les plafonds spécifiques",
                    val_type = "monetary",
                    cerfa_field = u'7HT',
                    start = date(2011, 1, 1))),

    build_column_couple('f7hu', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2009, Investissements réalisés en 2009 et achevés en 2010, dans les DOM COM du 27.5.2009 au 31.12.2009 respectant les plafonds spécifiques",
                    val_type = "monetary",
                    cerfa_field = u'7HU',
                    start = date(2011, 1, 1))),

    build_column_couple('f7ha', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: Investissements achevés et réalisés en 2011",
                    val_type = "monetary",
                    cerfa_field = u'7HA',
                    start = date(2012, 1, 1))),

    build_column_couple('f7hb', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: Investissements achevés et réalisés en 2011, avec promesse d'achat en 2010",
                    val_type = "monetary",
                    cerfa_field = u'7HB',
                    start = date(2012, 1, 1))),

    build_column_couple('f7hg', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2011 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna",
                    val_type = "monetary",
                    cerfa_field = u'7HG',
                    start = date(2012, 1, 1))),

    build_column_couple('f7hh', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2011 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna avec promesse d'achat en 2010",
                    val_type = "monetary",
                    cerfa_field = u'7HH',
                    start = date(2012, 1, 1))),

    build_column_couple('f7hd', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: Investissements achevés en 2011, réalisés en 2010, en métropole et dans les DOM-COM",
                    val_type = "monetary",
                    cerfa_field = u'7HD',
                    start = date(2012, 1, 1))),

    build_column_couple('f7he', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: Investissements achevés en 2011, en métropole et dans les DOM-COM avec promesse d'achat avant le 1.1.2010",
                    val_type = "monetary",
                    cerfa_field = u'7HE',
                    start = date(2012, 1, 1))),

    build_column_couple('f7hf', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: Investissements achevés en 2011, Investissements réalisés en 2009 en métropole et dans les DOM-COM",
                    val_type = "monetary",
                    cerfa_field = u'7HF',
                    start = date(2012, 1, 1))),

    build_column_couple('f7ja', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2012, métropole, BBC",
                    val_type = "monetary",
                    cerfa_field = u'7JA',
                    start = date(2012, 1, 1))),

    build_column_couple('f7jb', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, métropole, BBC",
                    val_type = "monetary",
                    cerfa_field = u'7JB',
                    start = date(2012, 1, 1))),

    build_column_couple('f7jd', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.1.2012 au 31.3.2012, métropole, BBC",
                    val_type = "monetary",
                    cerfa_field = u'7JD',
                    start = date(2012, 1, 1))),

    build_column_couple('f7je', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.4.2012 au 31.12.2012, métropole, BBC ",
                    val_type = "monetary",
                    cerfa_field = u'7JE',
                    start = date(2012, 1, 1))),

    build_column_couple('f7jf', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2012, métropole, non-BBC",
                    val_type = "monetary",
                    cerfa_field = u'7JF',
                    start = date(2012, 1, 1))),

    build_column_couple('f7jg', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, métropole, non-BBC",
                    val_type = "monetary",
                    cerfa_field = u'7JG',
                    start = date(2012, 1, 1))),

    build_column_couple('f7jh', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.1.2012 au 31.3.2012, métropole, non-BBC",
                    val_type = "monetary",
                    cerfa_field = u'7JH',
                    start = date(2012, 1, 1))),

    build_column_couple('f7jj', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.4.2012 au 31.12.2012, métropole, non-BBC",
                    val_type = "monetary",
                    cerfa_field = u'7JJ',
                    start = date(2012, 1, 1))),

    build_column_couple('f7jk', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon",
                    val_type = "monetary",
                    cerfa_field = u'7JK',
                    start = date(2012, 1, 1))),

    build_column_couple('f7jl', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon",
                    val_type = "monetary",
                    cerfa_field = u'7JL',
                    start = date(2012, 1, 1))),

    build_column_couple('f7jm', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.1.2012 au 31.3.2012, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon",
                    val_type = "monetary",
                    cerfa_field = u'7JM',
                    start = date(2012, 1, 1))),

    build_column_couple('f7jn', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.4.2012 au 31.12.2012, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon",
                    val_type = "monetary",
                    cerfa_field = u'7JN',
                    start = date(2012, 1, 1))),

    build_column_couple('f7jo', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna",
                    val_type = "monetary",
                    cerfa_field = u'7JO',
                    start = date(2012, 1, 1))),

    build_column_couple('f7jp', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna",
                    val_type = "monetary",
                    cerfa_field = u'7JP',
                    start = date(2012, 1, 1))),

    build_column_couple('f7jq', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.1.2012 au 31.3.2012, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna",
                    val_type = "monetary",
                    cerfa_field = u'7JQ',
                    start = date(2012, 1, 1))),

    build_column_couple('f7jr', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.4.2012 au 31.12.2012, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna",
                    val_type = "monetary",
                    cerfa_field = u'7JR',
                    start = date(2012, 1, 1))),

    build_column_couple('f7gj', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Reports concernant les investissements achevés ou acquis au cours des années antérieures, Investissements achevés et réalisés en 2012, en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon",
                    val_type = "monetary",
                    cerfa_field = u'7GJ',
                    start = date(2013, 1, 1))),

    build_column_couple('f7gk', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Reports concernant les investissements achevés ou acquis au cours des années antérieures, Investissements achevés et réalisés en 2012, en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon, avec promesse d'achat en 2011",
                    val_type = "monetary",
                    cerfa_field = u'7GK',
                    start = date(2013, 1, 1))),

    build_column_couple('f7gl', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Reports concernant les investissements achevés ou acquis au cours des années antérieures, Investissements achevés en 2012 et réalisés en 2011, en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon",
                    val_type = "monetary",
                    cerfa_field = u'7GL',
                    start = date(2013, 1, 1))),

    build_column_couple('f7gp', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Reports concernant les investissements achevés ou acquis au cours des années antérieures, Investissements achevés en 2012 et réalisés en 2011, en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon, avec promesse d'achat en 2010s",
                    val_type = "monetary",
                    cerfa_field = u'7GP',
                    start = date(2013, 1, 1))),

    build_column_couple('f7fa', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Investissements achevés ou acquis en 2013, réalisés du 1.1.2013 au 31.3.2013, métropole, BBC",
                    val_type = "monetary",
                    cerfa_field = u'7FA',
                    start = date(2013, 1, 1))),

    build_column_couple('f7fb', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Investissements achevés ou acquis en 2013, réalisés du 1.1.2013 au 31.3.2013, métropole, non-BBC",
                    val_type = "monetary",
                    cerfa_field = u'7FB',
                    start = date(2013, 1, 1))),

    build_column_couple('f7fc', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Investissements achevés ou acquis en 2013, réalisés du 1.1.2013 au 31.3.2013, DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon",
                    val_type = "monetary",
                    cerfa_field = u'7FC',
                    start = date(2013, 1, 1))),

    build_column_couple('f7fd', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier : Investissements achevés ou acquis en 2013, réalisés du 1.1.2013 au 31.3.2013 en Polynésie, en Nouvelle Calédonie et à Wallis et Futuna",
                    val_type = "monetary",
                    cerfa_field = u'7FD',
                    start = date(2013, 1, 1))),

    # Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
    build_column_couple('f7ij', IntCol(entity = 'foy',
                    label = u"Investissement destinés à la location meublée non professionnelle: engagement de réalisation de l'investissement en 2011",
                    val_type = "monetary",
                    cerfa_field = u'7IJ')),

    build_column_couple('f7il', IntCol(entity = 'foy',
                    label = u"Investissement destinés à la location meublée non professionnelle: promesse d'achat en 2010",
                    val_type = "monetary",
                    cerfa_field = u'7IL')),

    build_column_couple('f7im', IntCol(entity = 'foy',
                    label = u"Investissement destinés à la location meublée non professionnelle: investissement réalisés en 2010 avec promesse d'achat en 2009",
                    val_type = "monetary",
                    cerfa_field = u'7IM')),

    build_column_couple('f7ik', IntCol(entity = 'foy',
                    label = u"Reports de 1/9 de l'investissement réalisé et achevé en 2009",
                    val_type = "monetary",
                    cerfa_field = u'7IK')),

    build_column_couple('f7is', IntCol(entity = 'foy',
                    label = u"Report du solde de réduction d'impôt non encore imputé: année  n-4",
                    val_type = "monetary",
                    cerfa_field = u'7IS')),

    # Investissements locatifs dans les résidences de tourisme situées dans une zone de
    # revitalisation rurale

# """
# réutilisation de cases en 2013
# """

    build_column_couple('f7gt', IntCol(entity = 'foy',
                    label = u"Scellier: report de 1/9 de la réduction d'impôt des investissements achevés en 2012 avec promesse d'achat en 2010",
                    val_type = "monetary",
                    cerfa_field = u'7GT',
                    start = date(2013, 1, 1))),  # vérif <=2012

    build_column_couple('f7gu', IntCol(entity = 'foy',
                    label = u"Scellier: report de 1/9 de la réduction d'impôt des investissements achevés en 2012 avec promesse d'achat en 2009",
                    val_type = "monetary",
                    cerfa_field = u'7GU',
                    start = date(2013, 1, 1))),  # vérif <=2012

    build_column_couple('f7gv', IntCol(entity = 'foy',
                    label = u"Scellier: report de 1/5 de la réduction d'impôt des investissements réalisés et achevés en 2012 en Polynésie, en Nouvelle Calédonie et à Wallis et Futuna ",
                    val_type = "monetary",
                    cerfa_field = u'7GV',
                    start = date(2013, 1, 1))),  # vérif <=2012

    build_column_couple('f7xg', IntCol(entity = 'foy', label = u"Investissement locatif dans le secteur touristique, travaux réalisés dans un village résidentiel de tourisme",
                    val_type = "monetary",
                    cerfa_field = u'7XG',
                    end = date(2012, 12, 1))),  # vérif <=2012

    # Crédits d'impôts en f7
    # Acquisition de biens culturels
    build_column_couple('f7uo', IntCol(entity = 'foy',
                    label = u"Acquisition de biens culturels",
                    val_type = "monetary",
                    cerfa_field = u'7UO')),

    # Mécénat d'entreprise
    build_column_couple('f7us', IntCol(entity = 'foy',
                    label = u"Réduction d'impôt mécénat d'entreprise",
                    val_type = "monetary",
                    cerfa_field = u'7US')),

    # Crédits d’impôt pour dépenses en faveur de la qualité environnementale

    build_column_couple('f7sb', IntCol(entity = 'foy',
                   label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 25 %",
                   val_type = "monetary",
                   cerfa_field = u'7SB',
                   end = date(2012, 12, 1))),  # TODO: verif<=2012

    build_column_couple('f7sc', IntCol(entity = 'foy',
                   label = u"Crédits d’impôt pour dépenses en faveur de la qualité environnementale",
                   val_type = "monetary",
                   cerfa_field = u'7SC',
                   end = date(2012, 12, 1))),  # TODO: verif<=2012

# """
# réutilisation de case pour 2013
# """

    build_column_couple('f7sd', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale, économie d'énergie: chaudières à condensation",
                    val_type = "monetary",
                    cerfa_field = u'7SD',
                    start = date(2013, 1, 1))),  # TODO: verif<=2012 et vérifier autres prog comportant f7sd

    build_column_couple('f7se', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale, économie d'énergie: chaudières à micro-cogénération gaz",
                    val_type = "monetary",
                    cerfa_field = u'7SE',
                    start = date(2013, 1, 1))),  # TODO: verif<=2012

    build_column_couple('f7sh', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale, isolation thermique: matériaux d'isolation des toitures (acquisition et pose)",
                    val_type = "monetary",
                    cerfa_field = u'7SH',
                    start = date(2013, 1, 1))),  # TODO: verif<=2012

    # ('f7wg', IntCol() déjà disponible

    # Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte en 2007 et investissements forestiers aprés ???

    build_column_couple('f7up', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt pour investissements forestiers: travaux",
                    val_type = "monetary",
                    cerfa_field = u'7UP',
                    start = date(2008, 1, 1))),  # TODO: vérif date début, ok pour 13

    build_column_couple('f7uq', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt pour investissements forestiers: contrat de gestion",
                    val_type = "monetary",
                    cerfa_field = u'7UQ',
                    start = date(2008, 1, 1))),  # TODO: vérif date début, ok pour 13

    # Déclaration de déménagement correspondant à un crédit d'impôt aide à la mobilité
    build_column_couple('f1ar', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt aide à la mobilité",
                    cerfa_field = u'1AR',
                    end = date(2012, 12, 31))),  # TODO: vérifier <=2012

    build_column_couple('f1br', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt aide à la mobilité",
                    cerfa_field = u'1BR',
                    end = date(2012, 12, 31))),  # TODO: vérifier <=2012

    build_column_couple('f1cr', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt aide à la mobilité",
                    cerfa_field = u'1CR',
                    end = date(2012, 12, 31))),  # TODO: vérifier <=2012

    build_column_couple('f1dr', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt aide à la mobilité",
                    cerfa_field = u'1DR',
                    end = date(2012, 12, 31))),  # TODO: vérifier <=2012

    build_column_couple('f1er', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt aide à la mobilité",
                    cerfa_field = u'1ER',
                    end = date(2012, 12, 31))),  # TODO: vérifier <=2012

    # Crédit d’impôt représentatif de la taxe additionnelle au droit de bail
    build_column_couple('f4tq', IntCol(entity = 'foy',
                    label = u"Crédit d’impôt représentatif de la taxe additionnelle au droit de bail",
                    val_type = "monetary",
                    cerfa_field = u'4TQ')),  # vérif libéllé, en 2013=Montant des loyers courus du 01/01/1998 au 30/09/1998 provenant des immeubles
                                           # pour lesquels la cessation ou l'interruption de la location est intervenue en 2013 et qui ont été
                                           # soumis à la taxe additionnelle au droit de bail

    # Crédits d’impôt pour dépenses en faveur de l’aide aux personnes

    build_column_couple('f7sf', IntCol(entity = 'foy',
                    label = u"Appareils de régulation du chauffage, matériaux de calorifugeage",
                    val_type = "monetary",
                    cerfa_field = u'7SF')),

    build_column_couple('f7si', IntCol(entity = 'foy',
                    label = u"Matériaux d’isolation des planchers bas sur sous-sol, sur vide sanitaire ou sur passage couvert (acquisition et pose)",
                    val_type = "monetary",
                    cerfa_field = u'7SI')),

    build_column_couple('f7te', IntCol(entity = 'foy',
                    label = u"Dépenses d'investissement forestier",
                    val_type = "monetary",
                    cerfa_field = u'7TE')),

    build_column_couple('f7tu', IntCol(entity = 'foy',
                    label = u"Dépenses de travaux dans l'habitation principale",
                    val_type = "monetary",
                    cerfa_field = u'7TU')),

    build_column_couple('f7tt', IntCol(entity = 'foy',
                    label = u"Dépenses de travaux dans l'habitation principale",
                    val_type = "monetary",
                    cerfa_field = u'7TT')),

    build_column_couple('f7tv', IntCol(entity = 'foy',
                    label = u"Dépenses de travaux dans l'habitation principale",
                    val_type = "monetary",
                    cerfa_field = u'7TV')),

    build_column_couple('f7tx', IntCol(entity = 'foy',
                    label = u"Dépenses de travaux dans l'habitation principale",
                    val_type = "monetary",
                    cerfa_field = u'7TX')),

    build_column_couple('f7ty', IntCol(entity = 'foy',
                    label = u"Dépenses de travaux dans l'habitation principale",
                    val_type = "monetary",
                    cerfa_field = u'7TY')),

    build_column_couple('f7tz', IntCol(entity = 'foy',
                    label = u"Dépenses de travaux dans l'habitation principale",
                    val_type = "monetary",
                    cerfa_field = u'7TZ')),

    build_column_couple('f7tw', IntCol(entity = 'foy',
                    label = u"Dépenses de travaux dans l'habitation principale",
                    val_type = "monetary",
                    cerfa_field = u'7TW')),

    # Réduction d'impôts sur les investissements locatifs intermédiaires (loi Duflot)

    build_column_couple('f7gh', IntCol(entity = 'foy',
                    label = u"Investissements locatifs intermédiaires en métropole",
                    val_type = "monetary",
                    cerfa_field = u'7GH')),

    build_column_couple('f7gi', IntCol(entity = 'foy',
                    label = u"Investissements locatifs intermédiaires outre-mer",
                    val_type = "monetary",
                    cerfa_field = u'7GI')),

    ))
    # ('f7wf', IntCol() déjà disponible
    # ('f7wh', IntCol() déjà disponible
    # ('f7wk', IntCol() déjà disponible
    # ('f7wq', IntCol() déjà disponible