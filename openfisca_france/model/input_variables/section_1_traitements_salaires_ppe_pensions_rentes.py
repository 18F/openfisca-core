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


from ..base import *  # noqa


build_column('cho_ld', BoolCol(label = u"Demandeur d'emploi inscrit depuis plus d'un an",
                   cerfa_field = {QUIFOY['vous']: u"1AI",
                                  QUIFOY['conj']: u"1BI",
                                  QUIFOY['pac1']: u"1CI",
                                  QUIFOY['pac2']: u"1DI",
                                  QUIFOY['pac3']: u"1EI",
                               }))  # Pour toutes les variables de ce type, les pac3 ne sont plus proposés après 2007

build_column('sali', IntCol(label = u"Revenus d'activité imposables",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"1AJ",
                               QUIFOY['conj']: u"1BJ",
                               QUIFOY['pac1']: u"1CJ",
                               QUIFOY['pac2']: u"1DJ",
                               QUIFOY['pac3']: u"1EJ",
                               }))  # (f1aj, f1bj, f1cj, f1dj, f1ej)

build_column('fra', IntCol(label = u"Frais réels",
               val_type = "monetary",
               cerfa_field = {QUIFOY['vous']: u"1AK",
                              QUIFOY['conj']: u"1BK",
                              QUIFOY['pac1']: u"1CK",
                              QUIFOY['pac2']: u"1DK",
                              QUIFOY['pac3']: u"1EK",
                              }))  # (f1ak, f1bk, f1ck, f1dk, f1ek)

build_column('alr', IntCol(label = u"Pensions alimentaires perçues",
               val_type = "monetary",
               cerfa_field = {QUIFOY['vous']: u"1AO",
                              QUIFOY['conj']: u"1BO",
                              QUIFOY['pac1']: u"1CO",
                              QUIFOY['pac2']: u"1DO",
                              QUIFOY['pac3']: u"1EO",
                              }))  # (f1ao, f1bo, f1co, f1do, f1eo)
build_column('alr_decl', BoolCol(label = u"Pension déclarée", default = True))

build_column('choi', IntCol(label = u"Autres revenus imposables (chômage, préretraite)",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"1AP",
                               QUIFOY['conj']: u"1BP",
                               QUIFOY['pac1']: u"1CP",
                               QUIFOY['pac2']: u"1DP",
                               QUIFOY['pac3']: u"1EP",
                               }))  # (f1ap, f1bp, f1cp, f1dp, f1ep)

build_column('rsti', IntCol(label = u"Pensions, retraites, rentes connues imposables",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"1AS",
                               QUIFOY['conj']: u"1BS",
                               QUIFOY['pac1']: u"1CS",
                               QUIFOY['pac2']: u"1DS",
                               QUIFOY['pac3']: u"1ES",
                               }))  # (f1as, f1bs, f1cs, f1ds, f1es)

build_column('hsup', IntCol(label = u"Heures supplémentaires : revenus exonérés connus",
                val_type = "monetary",
                start = date(2007, 1, 1),
                cerfa_field = {QUIFOY['vous']: u"1AU",
                               QUIFOY['conj']: u"1BU",
                               QUIFOY['pac1']: u"1CU",
                               QUIFOY['pac2']: u"1DU",
                               }))  # (f1au, f1bu, f1cu, f1du, f1eu)

# pour inv, il faut que tu regardes si tu es d'accord et si c'est bien la bonne case,
# la case P exsite déjà plus bas ligne 339 sous le nom caseP

build_column('inv', BoolCol(label = u'Invalide'))  # TODO: cerfa_field

build_column('ppe_du_sa', IntCol(label = u"Prime pour l'emploi des salariés: nombre d'heures payées dans l'année",
                     cerfa_field = {QUIFOY['vous']: u"1AV",
                                    QUIFOY['conj']: u"1BV",
                                    QUIFOY['pac1']: u"1CV",
                                    QUIFOY['pac2']: u"1DV",
                                    QUIFOY['pac3']: u"1QV",
                                    }))  # (f1av, f1bv, f1cv, f1dv, f1qv)

build_column('ppe_tp_sa', BoolCol(label = u"Prime pour l'emploi des salariés: indicateur de travail à temps plein sur l'année entière",
                      cerfa_field = {QUIFOY['vous']: u"1AX",
                                     QUIFOY['conj']: u"1BX",
                                     QUIFOY['pac1']: u"1CX",
                                     QUIFOY['pac2']: u"1DX",
                                     QUIFOY['pac3']: u"1QX",
                                     }))  # (f1ax, f1bx, f1cx, f1dx, f1qx)

# Rentes viagères
build_column('f1aw', IntCol(label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : Moins de 50 ans",
                entity = 'foy',
                val_type = "monetary",
                cerfa_field = u'1AW'))

build_column('f1bw', IntCol(label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : De 50 à 59 ans",
                entity = 'foy',
                val_type = "monetary",
                cerfa_field = u'1BW'))
build_column('f1cw', IntCol(label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : De 60 à 69 ans",
                entity = 'foy',
                val_type = "monetary",
                cerfa_field = u'1CW'))
build_column('f1dw', IntCol(label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : A partir de 70 ans",
                entity = 'foy',
                val_type = "monetary",
                cerfa_field = u'1DW'))

build_column('jour_xyz', IntCol(default = 360,
                    entity = "foy",
                    label = u"Jours décomptés au titre de cette déclaration"))

build_column('nbsala', EnumCol(label = u"Nombre de salariés dans l'établissement de l'emploi actuel",
                enum = Enum([u"Sans objet",
                            u"Aucun salarié",
                            u"1 à 4 salariés",
                            u"5 à 9 salariés",
                            u"10 à 19 salariés",
                            u"20 à 49 salariés",
                            u"50 à 199 salariés",
                            u"200 à 499 salariés",
                            u"500 à 999 salariés",
                            u"1000 salariés ou plus",
                            u"Ne sait pas",
                            ])))

build_column('tva_ent', BoolCol(label = u"L'entreprise employant le salarié paye de la TVA",
                    default = True))

#    build_column('code_risque', EnumCol(label = u"Code risque pour les accidents du travail"))  # TODO: Complete label, add enum and relevant default.

build_column('exposition_accident', EnumCol(label = u"Exposition au risque pour les accidents du travail",
                        enum = Enum([u"Faible",
                               u"Moyen",
                               u"Élevé",
                               u"Très élevé",
                               ])))

build_column('boursier', BoolCol(label = u"Élève ou étudiant boursier"))


build_column('rfr_n_1', IntCol(entity = 'foy', label = u"Revenu fiscal de référence année n - 1",
    val_type = "monetary"))
build_column('rfr_n_2', IntCol(entity = 'foy', label = u"Revenu fiscal de référence année n - 2",
    val_type = "monetary"))
build_column('nbptr_n_2', PeriodSizeIndependentIntCol(entity = 'foy', label = u"Nombre de parts année n - 2",
    val_type = "monetary"))


# Gain de levée d'options
# Bouvard: j'ai changé là mais pas dans le code, il faut chercher les f1uv
# et les mettre en f1tvm comme pour sali
# Il faut aussi le faire en amont dans les tables

# là je ne comprends pas pourquoi il faut changer les f1uv en f1tvm....
# du coups je n'ai pas changé et j'ai fait un dico comme pour sali

build_column('f1tv', IntCol(label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 1 et 2 ans",
                        entity = 'ind',
                        val_type = "monetary",
                        cerfa_field = {QUIFOY['vous']: u"1TV",
                                       QUIFOY['conj']: u"1UV",
                                       }))  # (f1tv,f1uv))

build_column('f1tw', IntCol(label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 2 et 3 ans",
                        entity = 'ind',
                        val_type = "monetary",
                        cerfa_field = {QUIFOY['vous']: u"1TW",
                                       QUIFOY['conj']: u"1UW",
                                       }))  # (f1tw,f1uw))

build_column('f1tx', IntCol(label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 3 et 4 ans",
                        entity = 'ind',
                        val_type = "monetary",
                        cerfa_field = {QUIFOY['vous']: u"1TX",
                                       QUIFOY['conj']: u"1UX",
                        }))  # (f1tx,f1ux))


# """
# CASES MANQUANTES PRESENTENT DANS LA DECLARATION DES REVENUS 2013 et 2012
# """
# # A CREER ET A INTEGRER DANS OF
#
# """
# ### VOS REVENUS
#
# #revenu de solidarité active
# pour le foyer:1BL
# 1ere PAC: 1CB
# 2ème PAC: 1DQ
#
# #pensions, retraites, rentes, rentes viagères à titre onéreux
# Pensions de retraite en capital taxables à 7.5%
# vous:1AT
# conj:1BT
#
# #gains de levée d'options, revenus éxonérés ou non imposables en France, revenus exceptionnels ou différés
#     #gains de levée d'options sur titres et gains d'acquisition d'actions gratuites attribuées à compter du 28/9/2012
#     imposables en salaires:
#     vous:1TT
#     conj:1UT
#
#     #gains et distributions provenant de parts ou actions de carried-interest, déclarés cases 1AJ ou 1BJ, soumis à la contribution salariale de 30 %
#     vous:1NY
#     conj:1OY
#
#     #agents d'assurance: salaires éxonérés
#     vous:1AQ
#     conj:1BQ
#
#     #salariés impatriés: salaires et primes éxonérés
#     vous:1DY
#     conj:1EY
#
#     #salaires imposables à l'étranger, non déclarés cases 1Aj ou 1BJ, retenus pour le calcul de la prime pour l'emploi
#     vous:1LZ
#     conj:1MZ
#
#     #sommes éxonérées transférées du CET au PERCO ou à un régime supplémentaire d'entreprise
#     vous: 1SM
#     conj:1DN
#
#     #fonctionnaires d'organisations internationales: rémunérations exonérées
#     vous: 1TY
#     conj:1UY
#     end = date(2012, 12, 31),
#
# #salaires et pensions exonérés de source étrangère retenus pour le calcul du taux effectif
# (n'indiquez pas ces revenus ligne 8TI (2042) ni ligne 1LZ et 1MZ).
#
#     #total de vos salaires

build_column('sal_pen_exo_etr', IntCol(entity = 'ind',
                     label = u"Salaires et pensions exonérés de source étrangère retenus pour le calcul du taux effectif",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"1AC",
                                    QUIFOY['conj']: u"1BC",
                                    QUIFOY['pac1']: u"1CC",
                                    QUIFOY['pac2']: u"1DC", },
                     start = date(2013, 1, 1),))

#     vous:1AC
#     conj:1BC
#     pac1:1CC
#     pac2:1DC
#     start = date(2013, 1, 1),
#
#     #montant de l'impôt acquitté à l'étranger
#     vous:1AD
#     conj:1BD
#     pac1:1CD
#     pac2:1DD
#     start = date(2013, 1, 1),
#
#     #frais rééls
#     vous:1AE
#     conj:1BE
#     pac1:1CE
#     pac2:1DE
#     start = date(2013, 1, 1),
#
#     #pour recevoir la PPE: activité à temps plein exercée à l'étranger toute l'année
#     vous:1AX
#     conj:1BX
#     pac1:1CX
#     pac2:1DX
#     start = date(2013, 1, 1),
#
#     #pour recevoir la PPE: sinon, nombre d'heures payées dans l'année
#     vous:1AG
#     conj:1BG
#     pac1:1CG
#     pac2:1DG
#     start = date(2013, 1, 1),
#
#     #pensions exonérées de source étrangère: total des pensions nettes encaissées
#     vous:1AH
#     conj:1BH
#     pac1:1CH
#     pac2:1DH
#     start = date(2013, 1, 1),
#
# #revenus exceptionnels ou différés à imposer selon le système du quotient
# montant total des revenus à imposer selon le système du quotient: 0XX
#
# #plus-values et gains divers
#     #gains de cession de bons de souscription de parts de créateurs d'entreprise taxable à 19 %:3SJ
#     #gains de cession de bons de souscription de parts de créateurs d'entreprise taxable à 30 %:3SK
#
#     #gains de cession de valeurs mobilières, de droits sociaux et assimilés:
#         #abattement net pour durée de détention appliquée:
#             #sur des plus-values:3SG
#             #sur des moins-values:3SH
#             start = date(2013, 1, 1),
#         #abattement net pour durée de détention renforcée appliquée:
#             #sur des plus-values:3SL
#             #sur des moins-values:3SM
#             start = date(2013, 1, 1),
#     #gains de levée d'options sur titres et gains d'acquisition d'actions gratuites attribuées à compter du 16.10.2007, soumis à la contribution salariale de 8 %
#         vous:3VO
#         conj:3SO
#         end = date(2012, 12, 31),
#     #gains de levée d'options sur titres et gains d'acquisition d'actions gratuites attribuées à compter du 16/10/2007, soumis à la contributin salariale de 10%:
#         vous:3VN
#         conj:3SN
#     #gains d'acquisition d'actions gratuites attribuées à compter du 16/10/2007, soumis à la contribution salariale de 2,5%
#         vous:3VS
#         conj:3SS
#         end = date(2012, 12, 31),
#     #impatriés: cessions de titres détenus à l'étranger (report de la déclaration 2047 IMP)
#         #plus-values exonérées (50 %):3VQ
#         #moins-values non imputables (50 %):3VR
#     #plus-values en report d'imposition (art 150-0 D ter du CGI):3WE
#         #plus-values taxables à 24 %:3SB
#     #plus-values en report d'imposition (art 150-0 B ter du CGI):3WH             start = date(2013, 1, 1),
#     #plus-values dont le report à expiré en 2012:
#         #plus-values taxables à 19 %:3SC    end = date(2012, 12, 31),
#     #transfert du domicile hors de France, report de la déclaration 2074 ET:
#         #plus-values et créances dont l'imposition est en sursis de paiement:
#             #plus-values imposables:3WA
#             #plus-values taxables à 19 %:3WF             start = date(2013, 1, 1),
#             #abattement pour durée de détention en cas de départ à la retraite d'un dirigeant:3WC    end = date(2012, 12, 31),
#         #plus-values et créances dont l'imposition ne bénéficie pas du sursis de paiement:
#             #plus-values imposables:3WB
#             #plus-values taxables à 19 %:3WG             start = date(2013, 1, 1),
#             #abattement pour durée de détention:3WD
#             #plus-values imposables (art 150-0 D ter bis du CGI):3WI            start = date(2013, 1, 1),
#             #plus-values taxables à 19 % (art 150-0 D ter bis du CGI):3WJ            start = date(2013, 1, 1),
#     #plus-values de cession de titres de jeunes entreprises innovantes exonérées:3VP
#     #plus-values exonérées de cession de participations supérieures à 25 % au sein du groupe familial:3VY
#     #plus-values de cession d'une résidence secondaire exonérée sous condition de remploi:3VW
#     #plus-values réalisées par les non-résidents:
#         #plus-values de cession de droits sociaux art 244 bis B du CGI et distributions de sociétés de capital-risque:3SE
#
# #revenus fonciers
#     #amortissement "Robien" et "Borloo neuf" déduit des revenus fonciers 2013 (investissements réalisés en 2009):4BY
#     #taxe sur les loyers élevés (report de la déclaration 2042 LE):4BH
#
# #revenus agricoles
#     #revenus des exploitants forestiers (régime du forfait)
#     vous:5HD
#     conj:5ID
#     pac1:5JD
#     #régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur:
#         #jeunes agriculteurs, abattement de 50% ou 100% :
#         vous:5HZ
#         conj:5IZ
#         pac1:5JZ
#     #déficits agricoles des années antérieures du foyer non encore déduits:
#     2007:5QF
#     2008:5QG
#     2009:5QN
#     2010:5QO
#     2011:5QP
#     2012:5QQ
#
# #revenus non commerciaux professionnels:
#     #régime de la déclaratin contrôlée, revenus bénéficiant de l'abattement association agrée ou viseur
#         #jeunes créateurs abattement 50 %:
#         vous:5QL
#         conj:5RL
#         pac1:5SL
#         #honoraires de prospection commerciale exonérs:
#         vous:5TF
#         conj:5UF
#         pac1:5VF
#     #régime de la déclaratin contrôlée, revenus ne bénéficiant pas de l'abattement association agrée
#         #honoraires de prospection commerciale exonérs:
#         vous:5TI
#         conj:5UI
#         pac1:5VI
#
# #revenus non commerciaux non professionnels
#     #régime déclaratif spécial ou micro BNC (recettes brutes sans déduction d'abattement)
#         #revenus nets exonérés
#         vous:5TH
#         conj:5UH
#         pac1:5VH
#     #régime de la déclaration contrôlée
#         #revenus imposables avec AA ou viseur
#         vous:5JG
#         conj:5RF
#         pac1:5SF
#         #déficits avec AA ou viseur
#         vous:5JJ
#         conj:5RG
#         pac1:5SG
#         #inventeurs et auteurs de logiciels: produits taxables à 16 % avec AA ou viseur
#         vous:5TC
#         conj:5UC
#         pac1:5VC
#         #jeunes créateurs abattement de 50 %, avec AA ou viseur
#         vous:5SV
#         conj:5SW
#         pac1:5SX
#     #déficits des années antérieures non encore déduite=s:
#     2007:5HT
#     2008:5IT
#     2009:5JT
#     2010:5KT
#     2011:5LT
#     2012:5MT
#
# #revenus à imposer aux prélèvements sociaux
#     #revenus nets:
#     vous:5HY
#     conj:5IY
#     pac1:5JY
#     #plus-values à long terme exonérées en cas de départ à la retraite
#     vous:5HG
#     conj:5IG
#
# #revenus industriels et commerciaux professionnels
#     #régime du bénéfice réel:
#         #locations meublées avec CGA ou viseur:
#         vous:5HA
#         conj:5IA
#         pac1:5JA
#         #locations meublées sans CGA:
#         vous:5KA
#         conj:5LA
#         pac1:5MA
#         #déficit locations meublées avec CGA ou viseur:
#         vous:5QA
#         conj:5RA
#         pac1:5SA
#
# #revenus industriels et commerciaux non professionnels
#     #déficits industriels et commerciaux non professionnels des années antérieures non encore déduits
#     2007:5RN
#     2008:5RO
#     2009:5RP
#     2010:5RQ
#     2011:5RR
#     2012:5RW
#
# #locations meublées non professionnelles
#     #régime du bénéfice réel
#         #revenus imposables avec CGA ou viseur:
#         vous:5NA
#         conj:5OA
#         pac1:5PA
#         #déficits avec CGA ou viseur:
#         vous:5NY
#         conj:5OY
#         pac1:5PY
#         #déficits sans CGA:
#         vous:5NZ
#         conj:5OZ
#         pac1:5PZ
#         #déficits des années antérieures non encore déduits:
#         2003:5GA
#         2004:5GB
#         2005:5GC
#         2006:5GD
#         2007:5GE
#         2008:5GF
#         2009:5GG
#         2010:5GH
#         2011:5GI
#         2012:5GJ
#
# ### CHARGES ET IMPUTATIONS DIVERSES
#
#     #epargne retraite PERP et produits assimilés (PREFON, COREM et C.G.O.S)
#         #vous souhaitez bénéficier du plafond de votre conjoint, cochez la case:6QR
#         #si vous êtes nouvellement domicilié en France en 2013 après avoir résidé à l'étranger au cours des 3 années précédentes:6QW
#         #Détermination du plafond de déduction pour les revenus 2013 au titre de l'Epargne Retraite (PERP, Préfon et assimilés):
#           Cotisations versées en 2013(ou 2012 pour les revenus 2012) aux régimes obligatoires d'entreprise de retraite  supplémentaire "article 83", PERCO et, pour leur montant total ou partiel,
#           celles versées aux régimes ou contrats facultatifs de retraite "Madelin" et "Madelin agricole":
#           vous:6QS
#           conj:6QT
#           pac1:6QU
#
# ### CHARGES OUVRANT DROIT A REDUCTION OU CREDIT D'IMPOT
#     #dons à des organismes d'intérêt général établis dans l'Etat européen:
#         #dons à des organismes d'aides aux personnes:7VA
#         #dons à des autres organismes:7VC
#     #dépenses en faveur de la qualité environnementale de l'habitation principale
#         #vous avez réalisé des dépenses d'isolation thermique des murs donnant sur l'extérieur, travaux effectués sur au moins la moitié de la surface totale des murs: 7WC
#         #vous avez réalisé des dépenses d'isolation thermique des toitures, travaux effectués sur la totalité de la toiture:7VG
#         #isolation thermique:
#             #matériaux d'isolation des murs (montant acquisition et pose):7SG
#             #matériaux d'isolation thermique des parois vitrées (montant):7SJ
#             #volets isolants (montant):7SK
#             #porte d'entrée donnant sur l'extérieur (montant):7SL
#         #equipement de production d'énergie utilisant une source d'énergie renouvelable
#             #Équipements de production d'électricité utilisant l'énergie radiative du soleil (panneaux photovoltaïques):7SM
#             #Appareils de chauffage au bois ou autres biomasses remplaçant un appareil équivalent:7SN
#             #Appareils de chauffage au bois ou autres biomasses ne remplaçant pas un appareil équivalent:7SO
#             #Pompes à chaleur autres que air/air et autres que géothermiques dont la finalité essentielle est la production de chaleur:7SP
#             #Pompes à chaleur géothermiques dont la finalité essentielle est la production de chaleur (y compris le coût de la pose de l'échangeur de chaleur souterrain):7SQ
#             #Pompes à chaleur (autres que air/air) dédiées à la production d'eau chaude sanitaire (chauffe-eaux thermodynamiques):7SR
#             #Équipements de fourniture d'eau chaude sanitaire fonctionnant à l'énergie solaire et dotés de capteurs solaires (chauffe-eaux solaires...):7SS
#             #Autres équipements de production d'énergie utilisant une source d'énergie renouvelable (énergie éolienne, hydraulique…):7ST
#         #Autres dépenses
#             # Équipements de récupération et de traitement des eaux pluviales:7SU
#             #Diagnostic de performance énergétique:7SV
#             #Équipements de raccordement à un réseau de chaleur:7SW
#     #dépenses en faveur de la qualité environnementale de l'habitation principale cases manquantes sur la déclaration des revenus 2012
#         #vous avez réalisé une seule catégorie de travaux dans votre habitation principale située dans un immeuble collectif, portez le montant des dépenses dans les rubriques 7TT à 7TY en fonction du taux du crédit d'impôt  applicable
#             #Dépenses ouvrant droit au crédit d'impôt au taux de 10%: 7TT    end = date(2012, 12, 31),
#             #Dépenses ouvrant droit au crédit d'impôt au taux de 11%: 7TU    end = date(2012, 12, 31),
#             #Dépenses ouvrant droit au crédit d'impôt au taux de 15%: 7TV    end = date(2012, 12, 31),
#             #Dépenses ouvrant droit au crédit d'impôt au taux de 17%: 7TW    end = date(2012, 12, 31),
#             #Dépenses ouvrant droit au crédit d'impôt au taux de 26%: 7TX    end = date(2012, 12, 31),
#             #Dépenses ouvrant droit au crédit d'impôt au taux de 32%: 7TY    end = date(2012, 12, 31),
#         #Vous avez réalisé un bouquet de travaux ou si votre habitation principale est une maison individuelle cochez les cases adéquates (7WH à 7VG) et portez le montant des dépenses aux rubriques concernées (7SD à 7SW)
#             #Vous avez réalisé des dépenses d'isolation thermique des parois vitrées
#                 #vous avez engagé les dépenses à compter du 4.4.2012: 7WS    end = date(2012, 12, 31),
#             #Vous avez réalisé des dépenses d'acquisition de volets isolants
#                 #vous avez engagé les dépenses (accepté un devis et versé un acompte) avant le 1.1.2012: 7WU    end = date(2012, 12, 31),
#                 #vous avez engagé les dépenses en 2012: 7WV    end = date(2012, 12, 31),
#             #Vous avez réalisé des dépenses d'acquisition de portes d'entrée donnant sur l'extérieur
#                 #vous avez engagé les dépenses (accepté un devis et versé un acompte) avant le 1.1.2012: 7WW    end = date(2012, 12, 31),
#                 #vous avez engagé les dépenses en 2012: 7WX    end = date(2012, 12, 31),
#             #Vous avez réalisé des dépenses d'isolation thermique des murs donnant sur l'extérieur
#                 #vous avez engagé les dépenses (accepté un devis et versé un acompte) avant le 4.4.2012: 7WA    end = date(2012, 12, 31),
#                 #vous avez engagé les dépenses du 4.4.2012 au 31.12.2012: 7WB    end = date(2012, 12, 31),
#             #Vous avez réalisé des dépenses d'isolation thermique des toitures
#                 #vous avez engagé les dépenses (accepté un devis et versé un acompte) avant le 4.4.2012: 7VE    end = date(2012, 12, 31),
#                 #vous avez engagé les dépenses du 4.4.2012 au 31.12.2012: 7VF    end = date(2012, 12, 31),
#     #dépenses en faveur de la qualité environnementale des habitations données en location
#         #montant du crédit d'impôt calculé:7SZ
#     #travaux de prévention des risques technologiques dans les logements données en location (report 2041 gr)
#         #dépenses réalisées en 2013:7WR
#     #travaux de restauration immobilière: loi Malraux
#         #opérations engagées avant le 1/1/2011:
#             #dans un secteur sauvegardé ou assimilé:7RD
#             #dans une zone de protection du patrimoine architectural, urbain et paysager (ZPPAUP) ou une aire de mise en valeur de l'architecture et du patrimoine (AMVAP):7RC
#         #opérations engagées en 2012:
#             #dans un secteur sauvegardé ou assimilé:7RF
#             #dans une zone de protection du patrimoine architectural, urbain et paysager (ZPPAUP) ou une aire de mise en valeur de l'architecture et du patrimoine (AMVAP):7RE
#         #opérations engagées en 2013:
#             #dans un secteur sauvegardé ou assimilé:7SY
#             #dans une zone de protection du patrimoine architectural, urbain et paysager (ZPPAUP) ou une aire de mise en valeur de l'architecture et du patrimoine (AMVAP):7SX
#     #dépenses de protection du patrimoine naturel
#         #report de réduction d'impôt non encore imputée de l'année 2010:7KB
#         #report de réduction d'impôt non encore imputée de l'année 2011:7KC
#         #report de réduction d'impôt non encore imputée de l'année 2012:7KD
#     #investissement locatifs: loi Duflot
#         #investissement réalisés et achevés en 2013:
#             #en métropole:7GH start = date(2013, 1, 1),
#             #outre-mer:7GI    start = date(2013, 1, 1),
#     #investissement locatifs neufs: loi Scellier
#         #investissement achevés ou acquis en 2013:
#             #investissements réalisés de 1/1/2013 au 31/03/2013 avec engagement de réalisation en 2012:
#                 #Métropole, logement BBC:7FA    start = date(2013, 1, 1),
#                 #Métropole, logement non-BBC:7FB    start = date(2013, 1, 1),
#                 #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7FC    start = date(2013, 1, 1),
#                 #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7FD    start = date(2013, 1, 1),
#             #investissements réalisés en 2012 avec engagement de réalisation de l'investissement à compter du 1/1/2012:
#                 #Métropole, logement BBC:7JA
#                 #Métropole, logement non-BBC:7JF
#                 #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7JK
#                 #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7JO
#             #investissements réalisés en 2012 avec engagement de réalisation de l'investissement en 2011:
#                 #Métropole, logement BBC:7JB
#                 #Métropole, logement non-BBC:7JG
#                 #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7JL
#                 #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7JP
#             #investissements réalisés en 2012, logement acquis en l'état de futur achévement avec contrat de réservation enregistré au plus tard le 31/12/2011:
#                 #investissements réalisés du 1/1/2012 au 31/3/2012:
#                     #Métropole, logement BBC:7JD
#                     #Métropole, logement non-BBC:7JH
#                     #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7JM
#                     #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7JQ
#                 #investissements réalisés du 1/4/2012 au 31/12/2012:
#                     #Métropole, logement BBC:7JE
#                     #Métropole, logement non-BBC:7JJ
#                     #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7JN
#                     #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7JR
#             #investissements réalisés en 2011 avec engagement de réalisation de l'investissement à compter du 1/1/2011:
#                 #Métropole, logement BBC:7NA
#                 #Métropole, logement non-BBC:7NF
#                 #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7NK
#                 #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7NP
#             #investissements réalisés en 2011 avec engagement de réalisation de l'investissement en 2010:
#                 #Métropole, logement BBC:7NB
#                 #Métropole, logement non-BBC:7NG
#                 #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7NL
#                 #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7NQ
#             #investissements réalisés en 2011, logement acquis en l'état de futur achévement avec contrat de réservation enregistré au plus tard le 31/12/2010:
#                 #investissements réalisés du 1/1/2011 au 31/1/2011:
#                     #Métropole, logement BBC:7NC
#                     #Métropole, logement non-BBC:7NH
#                     #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7NM
#                     #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7NR
#                 #investissements réalisés du 1/2/2011 au 31/3/2011:
#                     #Métropole, logement BBC:7ND
#                     #Métropole, logement non-BBC:7NI
#                     #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7NN
#                     #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7NS
#                 #investissements réalisés du 1/4/2011 au 31/12/2011:
#                     #Métropole, logement BBC:7NE
#                     #Métropole, logement non-BBC:7NJ
#                     #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7NO
#                     #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7NT
#             #report concernant les investissements achevés ou acquis au cours des années antérieures:
#                 #investissements achevés en 2012: report de 1/9 de la réduction d'impôt:
#                     #investissements réalisés en 2012:
#                         #investissements réalisés en 2012, en Métropole, dans les DOM, à St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7GJ    start = date(2013, 1, 1),
#                         #investissements réalisés en 2012 avec promesse d'achat en 2011, en Métropole, dans les DOM, à St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7GK    start = date(2013, 1, 1),
#                     #investissements réalisés en 2011:
#                         #investissements réalisés en 2011, en Métropole, dans les DOM, à St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7GL    start = date(2013, 1, 1),
#                         #investissements réalisés en 2011 avec promesse d'achat en 2010, en Métropole, dans les DOM, à St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7GP    start = date(2013, 1, 1),
#                     #investissements réalisés en 2010:
#                         #investissements réalisés en 2010, en Métropole, dans les DOM, à St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7GS
#                 #investissements achevés en 2011: report de 1/9 de la réduction d'impôt:
#                     #investissements réalisés en 2011:
#                         #investissements réalisés en 2011, en Métropole, dans les DOM, à St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7HA
#                         #investissements réalisés en 2011 avec promesse d'achat en 2010, en Métropole, dans les DOM, à St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7HB
#                     #investissements réalisés en 2010:
#                         #investissements réalisés en 2010, en Métropole et dans les DOM-COM:7HD
#                         #investissements réalisés en 2010 avec promesse d'achat avant le 1/1/2010, en Métropole et dans les DOM-COM:7HE
#                     #investissements réalisés en 2009, en Métropole et dans les DOM-COM:7HF
#                 #investissements réalisés et achevés en 2011: report de 1/5 de la réduction d'impôt:
#                     #investissement en Polynésie, Nouvelle Calédonie, dans les îles Wallis et Futuna:7HG
#                     #investissement en Polynésie, Nouvelle Calédonie, dans les îles Wallis et Futuna avec promesse d'achat en 2010:7HH
#             #investissements achevés en 2010:report de 1/9 de l'investissement:
#                 #investissement réalisés et achevés en 2010, en Métropole:7HV
#                 #investissement réalisés et achevés en 2010, dans les DOM-COM:7HW
#                 #investissement réalisés et achevés en 2010, en Métropole avec promesse d'achat avant le 1/1/2010:7HX
#                 #investissement réalisés et achevés en 2010, dans les DOM-COM avec promesse d'achat avant le 1/1/2010:7HZ
#             #investissements réalisés en 2009 et achevés en 2010:
#                 #investissement réalisés en 2009 et achevés en 2010, en Métropole en 2009, dans les DOM du 1/1/2009 au 26/5/2009, dans les DOM du 27/5/2009 au 30/12/2009 lorsqu'ils ne respectent pas les plafonds spécifiques:7HT
#                 #investissement réalisés et achevés en 2010, dans les DOM-COM du 27/5/2009 au 31/12/2009 respectant les plafonds spécifiques:7HU
#             #report du solde des réductions d'impôts non encore imputé
#                 #investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1/1/2010:
#                     #report de l'année 2010:7LB
#                     #report de l'année 2011:7LE
#                     #report de l'année 2012:7LM    start = date(2013, 1, 1),
#                 #investissements réalisés et achevés en 2010, ou réalisés en 2010 et achevés en 2011, ou rélisés et achevés en 2011 avec engagement en 2010:
#                     #report de l'année 2010:7LC
#                     #report de l'année 2011:7LD
#                     #report de l'année 2012:7LS    start = date(2013, 1, 1),
#                 #investissements réalisés et achevés en 2011: report du solde de réduction d'impôt de l'année 2011:7LF
#                 #investissements réalisés et achevés en 2011: report du solde de réduction d'impôt de l'année 2012:7LZ    start = date(2013, 1, 1),
#                 #investissements réalisés et achevés en 2012: report du solde de réduction d'impôt de l'année 2012:7MG    start = date(2013, 1, 1),
#     #investissement destinés à la location meublée non professionnelle: loi Censi-Bouvard
#             #investissement réalisés en 2013:
#                 #engagement de réalisation de l'investissement en 2013:7JT    start = date(2013, 1, 1),
#                 #engagement de réalisation de l'investissement en 2012:7JU    start = date(2013, 1, 1),
#             #investissement réalisés en 2012:
#                 #engagement de réalisation de l'investissement en 2012:7ID
#                 #promesse d'achat en 2011:7IE
#                 #logement acquis en l'état de futur achèvement avec contrat de réservation enregistré au plus tard le 31/12/2011:
#                     #investissement réalisé 1/1/2012 au 31/03/2012:7IF
#                     #investissement réalisé 1/4/2012 au 31/12/2012:7IG
#             #investissement réalisés en 2011:
#                 #logement acquis en l'état de futur achèvement avec contrat de réservation enregistré au plus tard le 31/12/2010:
#                     #investissement réalisé 1/1/2011 au 31/03/2011:7IN
#                     #investissement réalisé 1/4/2011 au 31/12/2011:7IV
#             #investissement réalisés en 2010:
#                 #promesse d'achat en 2009:7IW
#             #investissement réalisés en 2009:7IO
#     #report de 1/9 de la réduction d'impôt des:
#         #investissements réalisés et achevés en 2012
#             #réalisés en 2012:7JV    start = date(2013, 1, 1),
#             #réalisés en 2011 ou réalisés en 2012 avec promesse d'achat en 2011:7JW    start = date(2013, 1, 1),
#             #réalisés en 2011 avec promesse d'achat en 2010 ou réalisés en 2010:7JX    start = date(2013, 1, 1),
#         #investissements achevés en 2011: report de 1/9 de la réduction d'impôt:
#             #réalisés en 2011:7IA
#             #réalisés en 2011 avec promesse d'achat en 2010 ou réalisés en 2010:7IB
#             #réalisés en 2010 avec promesse d'achat en 2009 ou réalisés en 2009:7IC
#         #investissements achevés en 2010: report de 1/9 de l'investissement:
#             #réalisés en 2010:7IP
#             #réalisés en 2010 avec promesse d'achat en 2009:7IQ
#             #réalisés en 2009:7IR
#     #report du solde de réduction d'impôt non encore imputé:
#         #investissements réalisés et achevés en 2009, réalisés en 2009 et achevés en 2010, réalisés et achevés en 2010 avec engagement avant le 1/1/2010
#             #report du solde de réduction d'impôt de l'année 2010:7IU
#             #report du solde de réduction d'impôt de l'année 2011:7IX
#          #investissements réalisés et achevés en 2010, réalisés en 2010 et achevés en 2011, réalisés et achevés en 2011 avec engagement en 2010
#             #report du solde de réduction d'impôt de l'année 2010:7IT
#             #report du solde de réduction d'impôt de l'année 2011:7IH
#             #report du solde de réduction d'impôt de l'année 2012:7JC    start = date(2013, 1, 1),
#         #investissements réalisés et achevés en 2011, réalisés en 2011 et achevés en 2011 ou 2012, réalisés en 2012 avec promesse d'achat en 2011 et achevés en 2012
#             #report du solde de réduction d'impôt de l'année 2011:7IZ
#             #report du solde de réduction d'impôt de l'année 2012:7JI    start = date(2013, 1, 1),
#         #investissements réalisés et achevés en 2012
#             #report du solde de réduction d'impôt de l'année 2012:7JS    start = date(2013, 1, 1),
#     #Vos autres charges ouvrant droit à réduction d'impôt ou à crédit d'impôt
#         #sommes versées pour l'emploi d'un salarié à domicile
#             #si vous avez engagé les dépenses pour un ascendant bénéficiaire de l'APA:7DD
#             #souscription au capital de petites entreprises en phase  d'amorçage, de démarrage ou d'expansion: reports des versements 2012 (2011 pour la déclaration des revenus de 2012):7CQ
#             #investissements forestiers:
#                 #assurance:7UL
#                 #si les travaux sont consécutifs à un sinistre:7UT
#                 #report des dépenses de travaux de l'année 2009:
#                     #hors sinistre:7UU
#                     #après sinistre:7TE
#                 #report des dépenses de travaux de l'année 2010:
#                     #hors sinistre:7UV
#                     #après sinistre:7TF
#                 #report des dépenses de travaux de l'année 2011:
#                     #hors sinistre:7UW
#                     #après sinistre:7TG
#                 #report des dépenses de travaux de l'année 2012:
#                     #hors sinistre:7UX    start = date(2013, 1, 1),
#                     #après sinistre:7TH    start = date(2013, 1, 1),
#             #investissement locatif dans le secteur touristique:
#                 #acquisition d'un logement neuf:
#                     #report des dépenses d'investissement effectuées en 2010:7XP
#                     #report des dépenses d'investissement effectuées en 2012:7UY    start = date(2013, 1, 1),
#                 #réhabilitation d'un logement
#                     #report des dépenses d'investissement effectuées en 2010:7XQ
#                     #report des dépenses d'investissement effectuées en 2011:7XV
#                     #report des dépenses d'investissement effectuées en 2012:7UZ    start = date(2013, 1, 1),
#                 #Travaux de reconstruction, d'agrandissement, de réparation ou d'amélioration payés en 2012
#                     #Travaux engagés avant le 1.1.2011
#                         #Dans un village résidentiel de tourisme 7XA    end = date(2012, 12, 31),
#                         #Dans une résidence de tourisme classée ou un meublé tourisme 7XB    end = date(2012, 12, 31),
#                     #Travaux engagés à compter du 1.1.2012 :
#                         #Dans un village résidentiel de tourisme 7XX    end = date(2012, 12, 31),
#                         #Dans une résidence de tourisme classée ou un meublé tourisme 7XZ    end = date(2012, 12, 31),
#             #investissement locatif dans une résidence hôtelière à vocation sociale
#                 #report des dépenses d'investissement de 2010:7XR
#         #reprises de réductions d'impôt, autres imputations, conventions internationales, divers:
#             #crédit d'impôt compétitivité, emploi: montant non encore cédé:
#                 #entreprises bénéficiant de la restitution immédiate:8TL    start = date(2013, 1, 1),
#                 #autres entreprises:8UW    start = date(2013, 1, 1),
#             #investissement en Corse:
#                 #entreprises bénéficiant de le restitution immédiate:8TS
#             #élus locaux: indemnités de fonction soumises à la retenue à la source:
#                 vous:8BY
#                 conj:8CY
#              #Personnes domiciliées en France percevant des revenus de l'étranger
#                   #Revenus exonérés (y compris salaires et primes des détachés à l'étranger) retenus pour le calcul du taux effectif:8TI
#                   #Revenus d'activité et de remplacement de source étrangère:
#                       #Revenus imposables à la CSG et à la CRDS:
#                           #salaires au taux de 7,5 %:8TR
#                           #revenus non salariaux au taux de 7,5 %: 8TQ
#                           #pensions, indemnités de maladie, etc au taux de 6,6 %: 8TV
#                           #pensions, indemnités de maladie, etc au taux de 6.2 %: 8TW
#                           #pensions, indemnités de maladie, etc au taux de 3,8 %: 8TX
#                   #Revenus étrangers imposables en France, ouvrant droit à un crédit d'impôt égal au montant de l'impôt français:8TK
#              #Personnes non domiciliées en France:
#                   #Revenus de sources française et étrangère à prendre en compte pour le calcul du taux moyen d'imposition:8TM
#                   #Impôt sur plus-values en sursis de paiement en cas de transfert du domicile hors de france: 8TN
#              #Plus-values en report d'imposition non expiré: 8UT
#              #Crédit d'impôt égal aux prélèvements forfaitaires et retenues à la source non libératoires effectués à Mayotte en 2013: 8UV    start = date(2013, 1, 1),
#
# ###AUTRES CHARGES OUVRANT DROIT A REDUCTION D'IMPOT : Investissements outre-mer
# ###Pour la déclaration des revenus de 2013, les cases ont changé de nom, elles sont passées de 7.. à H.. (par ex:7QA à HQA)
#     #Vous optez pour le plafonnement des réductions d'impôt pour investissements outre-mer à 11% du revenu imposable (15% (1) ou 13% (2) pour certains investissements):HQA start = date(2013, 1, 1),
#                                                                                                                                                                         7QA end = date(2012, 12, 31),
#           (1).Investissements dans le logement social ; investissements immobiliers engagés avant le 1.1.2011 ; investissements dans le cadre d'une entreprise agréés avant le 5.12.2010.
#           (2).Investissements dans le logement (article 199 undecies A) engagés avant le 1.1.2012 et investissements dans le cadre d'une entreprise (article 199 undecies B) agréés avant le 28.9.2011.
#
#     #Investissements outre-mer dans le logement social : montant de la reduction d'impôt
#         #Investissements réalisés en 2013
#             #Investissements ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %
#                 #En 2010: HRA    start = date(2013, 1, 1),
#                 #En 2011: HRB    start = date(2013, 1, 1),
#                 #En 2012: HRC    start = date(2013, 1, 1),
#             #Autres investissements: HRD    start = date(2013, 1, 1),
#         #Report de réductions d'impôt non imputées les années antérieures:
#             #Investissements réalisés en 2009: HKG    start = date(2013, 1, 1),
#             #Investissements réalisés en 2009: 7KG    end = date(2012, 12, 31),
#             #Investissements réalisés en 2010:
#                 #Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%: HKH    start = date(2013, 1, 1),
#                                                                                                                                                                 7KH    end = date(2012, 12, 31),
#                 #Autres investissements: HKI    start = date(2013, 1, 1),
#                                          7KI    end = date(2012, 12, 31),
#             #Investissements réalisés en 2011:
#                 #Investissements ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                     #En 2009: HQN    start = date(2013, 1, 1),
#                               7QN    end = date(2012, 12, 31),
#                     #En 2010: HQU    start = date(2013, 1, 1),
#                               7QU    end = date(2012, 12, 31),
#             #Autres investissements: HQK    start = date(2013, 1, 1),
#                                      7QK    end = date(2012, 12, 31),
#             #Investissements réalisés en 2012:
#                 #Investissements ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %:
#                     #En 2009: HQJ    start = date(2013, 1, 1),
#                               7QJ    end = date(2012, 12, 31),
#                     #En 2010: HQS    start = date(2013, 1, 1),
#                               7QS    end = date(2012, 12, 31),
#                     #En 2011: HQW    start = date(2013, 1, 1),
#                               7QW    end = date(2012, 12, 31),
#                 #Autres investissements: HQX    start = date(2013, 1, 1),
#                                          7QX    end = date(2012, 12, 31),
#     #Investissements outre-mer dans le logement et autres secteurs d'activité : montant de la réduction d'impôt
#         #Investissements réalisés jusqu'au 31/12/2008: HQB    start = date(2013, 1, 1),
#                                                        7QB    end = date(2012, 12, 31),
#         #Investissements réalisés en 2009
#             #Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%: HQC    start = date(2013, 1, 1),
#                                                                                                                                                                7QC    end = date(2012, 12, 31),
#             #Autres investissements: HQL    start = date(2013, 1, 1),
#                                      7QL    end = date(2012, 12, 31),
#         #Investissements réalisés en 2010
#             #Investissements ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                 #Avant 2009: HQT    start = date(2013, 1, 1),
#                              7QT    end = date(2012, 12, 31),
#                 #En 2009: HQM    start = date(2013, 1, 1),
#                           7QM    end = date(2012, 12, 31),
#             #Autres investissements: HQD    start = date(2013, 1, 1),
#                                      7QD    end = date(2012, 12, 31),
#         #Investissements réalisés en 2011:
#             #Investissements immobiliers engagés avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                 #avant 2009: HOA    start = date(2013, 1, 1),
#                              7OA    end = date(2012, 12, 31),
#                 #en 2009: HOB    start = date(2013, 1, 1),
#                           7OB    end = date(2012, 12, 31),
#                 #en 2010: HOC    start = date(2013, 1, 1),
#                           7OC    end = date(2012, 12, 31),
#             #Investissements immobiliers engagés en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                 #avant 2009: HOH    start = date(2013, 1, 1),
#                              7OH    end = date(2012, 12, 31),
#                 #en 2009: HOI    start = date(2013, 1, 1),
#                           7OI    end = date(2012, 12, 31),
#                 #en 2010: HOJ    start = date(2013, 1, 1),
#                           7OJ    end = date(2012, 12, 31),
#             #Autres investissements: HOK    start = date(2013, 1, 1),
#                                      7OK    end = date(2012, 12, 31),
#         #Investissements réalisés en 2012:
#             #Investissements immobiliers  que vous avez engagé avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %:
#                 #avant 2009: HOL    start = date(2013, 1, 1),
#                              7OL    end = date(2012, 12, 31),
#                 #en 2009: HOM    start = date(2013, 1, 1),
#                           7OM    end = date(2012, 12, 31),
#                 #en 2010: HON    start = date(2013, 1, 1),
#                           7ON    end = date(2012, 12, 31),
#             #Investissements immobiliers  que vous avez engagé en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %:
#                 #avant 2009: HOO    start = date(2013, 1, 1),
#                              7OO    end = date(2012, 12, 31),
#                 #en 2009: HOP    start = date(2013, 1, 1),
#                           7OP    end = date(2012, 12, 31),
#                 #en 2010: HOQ    start = date(2013, 1, 1),
#                           7OQ    end = date(2012, 12, 31),
#                 #en 2011: HOR    start = date(2013, 1, 1),
#                           7OR    end = date(2012, 12, 31),
#             #Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %
#                 #avant 2009: HOS    start = date(2013, 1, 1),
#                              7OS    end = date(2012, 12, 31),
#                 #en 2009: HOT    start = date(2013, 1, 1),
#                           7OT    end = date(2012, 12, 31),
#                 #en 2010: HOU    start = date(2013, 1, 1),
#                           7OU    end = date(2012, 12, 31),
#                 #en 2011: HOV    start = date(2013, 1, 1),
#                           7OV    end = date(2012, 12, 31),
#             #Autres investissements: HOW    start = date(2013, 1, 1),
#                                      7OW    end = date(2012, 12, 31),
#         #Investissements réalisés en 2013:
#             #Investissements immobiliers engagés avant le 1.1.2011: HOD    start = date(2013, 1, 1),
#             #Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %:
#                 #en 2010: HOE    start = date(2013, 1, 1),
#                 #en 2011: HOF    start = date(2013, 1, 1),
#             #Investissements immobiliers engagés en 2012 ou 2013, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                 #en 2010  HOG    start = date(2013, 1, 1),
#                 #en 2011  HOX    start = date(2013, 1, 1),
#                 #en 2012  HOY    start = date(2013, 1, 1),
#             #Autres investissements: HOZ    start = date(2013, 1, 1),
#     #Investissements outre-mer dans le cadre de l'entreprise:
#         #Investissements réalisés en 2012
#             #Investissements agréés avant le 28/9/2011
#                 #Investissements ayant fait l’objet avant 2009 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50%:7PM    end = date(2012, 12, 31),
#                 #Investissements ayant fait l’objet en 2009 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50%:
#                     #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                         #à hauteur de 50%: 7PN    end = date(2012, 12, 31),
#                         #à hauteur de 60%: 7PO    end = date(2012, 12, 31),
#                 #Investissements dans votre entreprise:7PP    end = date(2012, 12, 31),
#                 #Investissements dans votre entreprise avec exploitation directe:
#                     #montant de la réduction d’impôt calculée:7PQ    end = date(2012, 12, 31),
#                     #montant de la réduction d’impôt dont vous demandez l’imputation en 2012:7PR    end = date(2012, 12, 31),
#                 #Investissements ayant fait l’objet en 2010 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50%:
#                     #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                         #à hauteur de 50%: 7PS    end = date(2012, 12, 31),
#                         #à hauteur de 60%: 7PT    end = date(2012, 12, 31),
#                 #Investissements dans votre entreprise:7PU    end = date(2012, 12, 31),
#                 #Investissements dans votre entreprise avec exploitation directe:
#                     #montant de la réduction d’impôt calculée:7PV    end = date(2012, 12, 31),
#                     #montant de la réduction d’impôt dont vous demandez l’imputation en 2012:7PW    end = date(2012, 12, 31),
#                 #Investissements ayant fait l’objet en 2011 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50%:
#                     #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                         #à hauteur de 52.63%: 7PX    end = date(2012, 12, 31),
#                         #à hauteur de 62.5%: 7PY    end = date(2012, 12, 31),
#                 #Investissements dans votre entreprise:7RG    end = date(2012, 12, 31),
#                 #Investissements dans votre entreprise avec exploitation directe:
#                     #montant de la réduction d’impôt calculée:7RH    end = date(2012, 12, 31),
#                     #montant de la réduction d’impôt dont vous demandez l’imputation en 2012:7RI    end = date(2012, 12, 31),
#                 #Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %: 7RJ    end = date(2012, 12, 31),
#                 #Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %:
#                     #investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                         #à hauteur de 52,63 %: 7RK    end = date(2012, 12, 31),
#                         #à hauteur de 62,5 %: 7RL     end = date(2012, 12, 31),
#                     #investissements dans votre entreprise: 7RM    end = date(2012, 12, 31),
#                     #investissements dans votre entreprise avec exploitation directe :
#                         #montant de la réduction d'impôt calculée: 7RN    end = date(2012, 12, 31),
#                         #montant de la réduction d'impôt dont vous demandez l'imputation en 2012: 7RO    end = date(2012, 12, 31),
#                 #Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %:
#                     #investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                         #à hauteur de 52,63 %: 7RP    end = date(2012, 12, 31),
#                         #à hauteur de 62,5 %: 7RQ    end = date(2012, 12, 31),
#                     #investissements dans votre entreprise: 7RR    end = date(2012, 12, 31),
#                     #investissements dans votre entreprise avec exploitation directe :
#                         #montant de la réduction d'impôt calculée: 7RS    end = date(2012, 12, 31),
#                         #montant de la réduction d'impôt dont vous demandez l'imputation en 2012: 7RT    end = date(2012, 12, 31),
#                 #Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %:
#                     #investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                         #à hauteur de 52,63 % 7RU    end = date(2012, 12, 31),
#                         #à hauteur de 62,5 % 7RV    end = date(2012, 12, 31),
#                     #investissements dans votre entreprise: 7RW    end = date(2012, 12, 31),
#                     #investissements dans votre entreprise avec exploitation directe :
#                         #montant de la réduction d'impôt calculée: 7RX    end = date(2012, 12, 31),
#                         #montant de la réduction d'impôt dont vous demandez l'imputation en 2012: 7RY    end = date(2012, 12, 31),
#                     #Investissements autres que ceux des lignes précédentes
#                         #investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                             #à hauteur de 52,63 %: 7NU    end = date(2012, 12, 31),
#                             #à hauteur de 62,5 %: 7NV    end = date(2012, 12, 31),
#                         #investissements dans votre entreprise: 7NW    end = date(2012, 12, 31),
#                         #investissements dans votre entreprise avec exploitation directe :
#                             #montant de la réduction d'impôt calculée: 7NX    end = date(2012, 12, 31),
#                             #montant de la réduction d'impôt dont vous demandez l'imputation en 2012: 7NY    end = date(2012, 12, 31),
#         #Investissements réalisés en 2013
#             #Investissements agréés du 5.12.2010 au 27.9.2011, Investissements ayant fait l’objet en 2010 ou 2011 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50%:
#                 #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                     #en 2010 à hauteur de 52,63%: HSA    start = date(2013, 1, 1),
#                     #en 2010 à hauteur de 62,5%: HSB    start = date(2013, 1, 1),
#                     #en 2011 à hauteur de 52,63%: HSF    start = date(2013, 1, 1),
#                     #en 2011 à hauteur de 62,5%: HSG    start = date(2013, 1, 1),
#                 #Investissements dans votre entreprise:
#                     #en 2010: HSC    start = date(2013, 1, 1),
#                     #en 2011: HSH    start = date(2013, 1, 1),
#                 #Investissements dans votre entreprise avec exploitation directe:
#                     #montant de la réduction d’impôt calculée:
#                         #en 2010: HSD    start = date(2013, 1, 1),
#                         #en 2011: HSI    start = date(2013, 1, 1),
#                     #montant de la réduction d’impôt dont vous demandez l’imputation en 2013:
#                         #en 2010: HSE    start = date(2013, 1, 1),
#                         #en 2011: HSJ    start = date(2013, 1, 1),
#         #Autres investissements:
#             #Investissements ayant fait l’objet en 2010 ou 2011 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt:
#                 #en 2010 à hauteur de 52,63%: HSK    start = date(2013, 1, 1),
#                 #en 2010 à hauteur de 62,5%: HSL    start = date(2013, 1, 1),
#                 #en 2011 à hauteur de 52,63%: HSP    start = date(2013, 1, 1),
#                 #en 2011 à hauteur de 62,5%: HSQ    start = date(2013, 1, 1),
#             #Investissements dans votre entreprise:
#                 #en 2010: HSM    start = date(2013, 1, 1),
#                 #en 2011: HSR    start = date(2013, 1, 1),
#             #Investissements dans votre entreprise avec exploitation directe:
#                 #montant de la réduction d’impôt calculée:
#                     #en 2010: HSN    start = date(2013, 1, 1),
#                     #en 2011: HSS    start = date(2013, 1, 1),
#                 #montant de la réduction d’impôt dont vous demandez l’imputation en 2013:
#                 #en 2010: HSO    start = date(2013, 1, 1),
#                 #en 2011: HST    start = date(2013, 1, 1),
#             #Investissements ayant fait l’objet en 2012 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %:
#                 #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt:
#                     #à hauteur de 52,63%: HSU    start = date(2013, 1, 1),
#                     #à hauteur de 62,5%: HSV    start = date(2013, 1, 1),
#                 #Investissements dans votre entreprise: HSW    start = date(2013, 1, 1),
#                 #Investissements dans votre entreprise avec exploitation directe :
#                     #montant de la réduction d’impôt calculé: HSX    start = date(2013, 1, 1),
#                     #montant de la réduction d’impôt dont vous demandez l’imputation en 2013: HSY    start = date(2013, 1, 1),
#         #Investissements autres que ceux des lignes précédentes
#             #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt:
#                 #à hauteur de 52,63%: HSZ    start = date(2013, 1, 1),
#                 #à hauteur de 62,5%: HTA    start = date(2013, 1, 1),
#             #Investissements dans votre entreprise:
#                 #Investissements dans votre entreprise avec exploitation directe : HTB    start = date(2013, 1, 1),
#                     #montant de la réduction d’impôt calculé: HTC    start = date(2013, 1, 1),
#                     #montant de la réduction d’impôt dont vous demandez l’imputation en 2013: HTD    start = date(2013, 1, 1),
#     #REPORT DE RÉDUCTIONS D'IMPÔT NON IMPUTÉES LES ANNEES ANTÉRIEURES
#         #Investissements réalisés en 2008: HQZ    start = date(2013, 1, 1),
#         #Investissements réalisés en 2009:
#             #Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%: HMM    start = date(2013, 1, 1),
#                                                                                                                                                                7MM    end = date(2012, 12, 31),
#             #Autres investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                 #à hauteur de 50%: HLG    start = date(2013, 1, 1),
#                                    7LG    end = date(2012, 12, 31),
#                 #à hauteur de 60%  HMA    start = date(2013, 1, 1),
#                                    7MA    end = date(2012, 12, 31),
#             #Autres investissements dans votre entreprise: HKS    start = date(2013, 1, 1),
#                                                            7KS    end = date(2012, 12, 31),
#         #Investissements réalisés en 2010:
#             #Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%: HMN    start = date(2013, 1, 1),
#                                                                                                                                                                7MN    end = date(2012, 12, 31),
#             #Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                 #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                     #à hauteur de 50%: HLH    start = date(2013, 1, 1),
#                                        7LH    end = date(2012, 12, 31),
#                     #à hauteur de 60%: HMB    start = date(2013, 1, 1),
#                                        7MB    end = date(2012, 12, 31),
#                 #Investissements dans votre entreprise: HKT    start = date(2013, 1, 1),
#                                                         7KT    end = date(2012, 12, 31),
#             #Autres investissements réalisés en 2010:
#                 #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                     #à hauteur de 50%: HLI    start = date(2013, 1, 1),
#                                        7LI    end = date(2012, 12, 31),
#                     #à hauteur de 60%:  HMC    start = date(2013, 1, 1),
#                                         7MC    end = date(2012, 12, 31),
#                 #Investissements dans votre entreprise: HKU    start = date(2013, 1, 1),
#                                                         7KU    end = date(2012, 12, 31),
#         #Investissements réalisés en 2011:
#             #Investissements immobliliers engagés avant le 1.1.2011 et investissements ayant reçu un agrément avant le 5.12.2010:
#                 #Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%: HQV    start = date(2013, 1, 1),
#                                                                                                                                                                    7QV    end = date(2012, 12, 31),
#                     #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                         #à hauteur de 50%: HQO    start = date(2013, 1, 1),
#                                            7QO    end = date(2012, 12, 31),
#                         #à hauteur de 60%: HQP    start = date(2013, 1, 1),
#                                            7QP    end = date(2012, 12, 31),
#                     #investissements dans votre entreprise: HQR    start = date(2013, 1, 1),
#                                                             7QR    end = date(2012, 12, 31),
#                 #Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                     #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                         #à hauteur de 50%: HQF    start = date(2013, 1, 1),
#                                            7QF    end = date(2012, 12, 31),
#                         #à hauteur de 60%: HQG    start = date(2013, 1, 1),
#                                            7QG    end = date(2012, 12, 31),
#                     #Investissements dans votre entreprise: HQI    start = date(2013, 1, 1),
#                                                             7QI    end = date(2012, 12, 31),
#         #Autres investissements:
#             #Investissements ayant fait l'objet avant 1.1.2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%: HQE    start = date(2013, 1, 1),
#                                                                                                                                                                    7QE    end = date(2012, 12, 31),
#             #Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                 #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                     #à hauteur de 52,63%: HPA    start = date(2013, 1, 1),
#                                           7PA    end = date(2012, 12, 31),
#                     #à hauteur de 62,5%: HPB    start = date(2013, 1, 1),
#                                          7PB    end = date(2012, 12, 31),
#                 #Investissements dans votre entreprise HPD    start = date(2013, 1, 1),
#                                                        7PD    end = date(2012, 12, 31),
#             #Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                 #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                     #à hauteur de 52,63%: HPE    start = date(2013, 1, 1),
#                                           7PE    end = date(2012, 12, 31),
#                     #à hauteur de 62,5%: HPF    start = date(2013, 1, 1),
#                                          7PF    end = date(2012, 12, 31),
#                 #Investissements dans votre entreprise: HPH    start = date(2013, 1, 1),
#                                                         7PH    end = date(2012, 12, 31),
#             #Investissements autres que ceux des lignes précédentes:
#                 #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                     #à hauteur de 52,63%: HPI    start = date(2013, 1, 1),
#                                           7PI    end = date(2012, 12, 31),
#                     #à hauteur de 62,5%: HPJ    start = date(2013, 1, 1),
#                                          7PJ    end = date(2012, 12, 31),
#             #Investissements dans votre entreprise: HPL    start = date(2013, 1, 1),
#                                                     7PL    end = date(2012, 12, 31),
#         #Investissements réalisés en 2012:
#             #Investissements agréés avant le 28.9.2011:
#                 #Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%: HPM    start = date(2013, 1, 1),
#                 #Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                     #investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                         #à hauteur de 50 %: HPN    start = date(2013, 1, 1),
#                         #à hauteur de 60 %: HPO    start = date(2013, 1, 1),
#                     #investissements dans votre entreprise: HPP    start = date(2013, 1, 1),
#                     #investissements dans votre entreprise avec exploitation directe : montant de la réduction d'impôt dont vous demandez l'imputation en 2012: HPR    start = date(2013, 1, 1),
#                 #Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                     #investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                         #à hauteur de 50 %: HPS    start = date(2013, 1, 1),
#                         #à hauteur de 60 %: HPT    start = date(2013, 1, 1),
#                     #investissements dans votre entreprise: HPU    start = date(2013, 1, 1),
#                     #investissements dans votre entreprise avec exploitation directe : montant de la réduction d'impôt dont vous demandez l'imputation en 2012: HPW    start = date(2013, 1, 1),
#                 #Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                     #investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                         #à hauteur de 52,63 %: HPX    start = date(2013, 1, 1),
#                         #à hauteur de 62,5 %: HPY    start = date(2013, 1, 1),
#                     #investissements dans votre entreprise: HRG    start = date(2013, 1, 1),
#                     #investissements dans votre entreprise avec exploitation directe : montant de la réduction d'impôt dont vous demandez l'imputation en 2012: HRI    start = date(2013, 1, 1),
#         #Autres investissements:
#             #Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %: HRJ    start = date(2013, 1, 1),
#             #Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %:
#                 #investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                     #à hauteur de 52,63 %: HRK    start = date(2013, 1, 1),
#                     #à hauteur de 62,5 %: HRL    start = date(2013, 1, 1),
#                 #investissements dans votre entreprise: HRM    start = date(2013, 1, 1),
#                 #investissements dans votre entreprise avec exploitation directe : montant de la réduction d'impôt dont vous demandez l'imputation en 2012: HRO    start = date(2013, 1, 1),
#             #Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %:
#                 #investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                     #à hauteur de 52,63 %: HRP    start = date(2013, 1, 1),
#                     #à hauteur de 62,5 %: HRQ    start = date(2013, 1, 1),
#                 #investissements dans votre entreprise: HRR    start = date(2013, 1, 1),
#                 #investissements dans votre entreprise avec exploitation directe : montant de la réduction d'impôt dont vous demandez l'imputation en 2012: HRT    start = date(2013, 1, 1),
#         #Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %:
#             #investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                 #à hauteur de 52,63 %: HRU    start = date(2013, 1, 1),
#                 #à hauteur de 62,5 %: HRV    start = date(2013, 1, 1),
#             #investissements dans votre entreprise: HRW    start = date(2013, 1, 1),
#             #investissements dans votre entreprise avec exploitation directe : montant de la réduction d'impôt dont vous demandez l'imputation en 2012: HRY    start = date(2013, 1, 1),
#         #Investissements autres que ceux des lignes précédentes:
#             #investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                #à hauteur de 52,63 %: HNU    start = date(2013, 1, 1),
#                #à hauteur de 62,5 %: HNV    start = date(2013, 1, 1),
#             #investissements dans votre entreprise: HNW    start = date(2013, 1, 1),
#             #investissements dans votre entreprise avec exploitation directe: HNY    start = date(2013, 1, 1),
