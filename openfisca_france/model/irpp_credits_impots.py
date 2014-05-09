# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)


from __future__ import division

import logging

from numpy import logical_not as not_, maximum as max_, minimum as min_

from .input_variables.base import QUIFOY

log = logging.getLogger(__name__)
VOUS = QUIFOY['vous']


def _credits_impot_2002(creimp, accult, prlire, aidper, acqgpl, drbail):
    """ Crédits d'impôt pour l'impôt sur les revenus de 2002 """
    return creimp + accult + prlire + aidper + acqgpl + drbail


def _credits_impot_2003_2004(creimp, accult, mecena, prlire, aidper, acqgpl, drbail):
    """ Crédits d'impôt pour l'impôt sur les revenus de 2003 et 2004 """
    return creimp + accult + mecena + prlire + aidper + acqgpl + drbail


def _credits_impot_2005_2006(creimp, divide, direpa, accult, mecena, prlire, aidper,
    quaenv, acqgpl, drbail, ci_garext, preetu, assloy, aidmob, jeunes):
    """ Crédits d'impôt pour l'impôt sur les revenus de 2005 et 2006 """
    return (creimp + divide + direpa + accult + mecena + prlire + aidper +
        quaenv + acqgpl + drbail + ci_garext + preetu + assloy + aidmob + jeunes)


def _credits_impot_2007(creimp, divide, direpa, accult, mecena, prlire, aidper,
        quaenv, acqgpl, drbail, ci_garext, preetu, saldom2, inthab, assloy, aidmob, jeunes):
    """ Crédits d'impôt pour l'impôt sur les revenus de 2007 """
    return (creimp + divide + direpa + accult + mecena + prlire + aidper +
        quaenv + acqgpl + drbail + ci_garext + preetu + saldom2 + inthab + assloy +
        aidmob + jeunes)


def _credits_impot_2008(creimp, divide, direpa, accult, mecena, prlire, aidper,
    quaenv, drbail, ci_garext, preetu, saldom2, inthab, assloy, aidmob, jeunes):
    """ Crédits d'impôt pour l'impôt sur les revenus de 2008 """
    return (creimp + divide + direpa + accult + mecena + prlire + aidper +
        quaenv + drbail + ci_garext + preetu + saldom2 + inthab + assloy + aidmob + jeunes)


def _credits_impot_2009(creimp, divide, direpa, accult, mecena, prlire, aidper,
    quaenv, drbail, ci_garext, preetu, saldom2, inthab, assloy, autent):
    """ Crédits d'impôt pour l'impôt sur les revenus de 2009 """
    return (creimp + divide + direpa + accult + mecena + prlire + aidper +
        quaenv + drbail + ci_garext + preetu + saldom2 + inthab + assloy + autent)


def _credits_impot_2010(creimp, accult, percvm, direpa, mecena, prlire, aidper,
    quaenv, drbail, ci_garext, preetu, saldom2, inthab, assloy, autent):
    """ Crédits d'impôt pour l'impôt sur les revenus de 2010 """
    return (creimp + accult + percvm + direpa + mecena + prlire + aidper +
        quaenv + drbail + ci_garext + preetu + saldom2 + inthab + assloy + autent)


def _credits_impot_2011(prlire, creimp, accult, preetu ):  # TODO: check because totally unchecked
    """ Crédits d'impôt pour l'impôt sur les revenus de 2011 """
    log.warning("TODO: totally unchecked")
    return prlire + creimp + accult + preetu


def _credits_impot_2012(prlire, creimp, accult, preetu ):
    """ Crédits d'impôt pour l'impôt sur les revenus de 2012 """
    log.warning("TODO: incomplete")
    return prlire + creimp + accult + preetu


def _credits_impot_2013(prlire, creimp, accult, preetu ):
#TODO: missing 1 niche
#TODO: create new function for f3VV (new legislation : non-resident_45%)
    """ Crédits d'impôt crédités l'impôt sur les revenus de 2013 """
    log.warning("TODO: not complete")
    return prlire + creimp + accult + preetu





def _nb_pac2(nbF, nbJ, nbR, nbH):
    return nbF + nbJ + nbR + nbH / 2


def _creimp_2002(f2ab, f8ta, f8tb, f8tc, f8td, f8te, f8tf, f8tg, f8th):
    '''Avoir fiscaux et crédits d'impôt 2002 '''
    return (f2ab + f8ta + f8tb + f8tc + f8td + f8te - f8tf + f8tg + f8th)

def _creimp_2003(f2ab, f8ta, f8tb, f8tc, f8td, f8te, f8tf, f8tg, f8th, f8to, f8tp):
    '''Avoir fiscaux et crédits d'impôt 2003 '''
    return (f2ab + f8ta + f8tb + f8tc + f8td + f8te - f8tf + f8tg + f8th + f8to - f8tp)

def _creimp_2004(f2ab, f8ta, f8tb, f8tc, f8td, f8te, f8tf, f8tg, f8th, f8to, f8tp, f8uz, f8tz):
    '''Avoir fiscaux et crédits d'impôt 2004 '''
    return (f2ab + f8ta + f8tb + f8tc + f8td + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8uz + f8tz)

def _creimp_2005(f2ab, f8ta, f8tb, f8tc, f8td, f8te, f8tf, f8tg, f8th, f8to, f8tp, f8uz, f8tz, f8wa, f8wb, f8wc,
                   f8we):
    '''Avoir fiscaux et crédits d'impôt 2005 '''
    return  (f2ab + f8ta + f8tb + f8tc + f8td + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8uz + f8tz + f8wa + f8wb +
    f8wc + f8we)

def _creimp_2006(f2ab, f8ta, f8tb, f8tc, f8te, f8tf, f8tg, f8th, f8to, f8tp, f8uz, f8tz, f8wa, f8wb, f8wc, f8wd, f8we,
                  f8wr, f8ws, f8wt, f8wu):
    '''Avoir fiscaux et crédits d'impôt 2006 '''
    return  (f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8uz + f8tz + f8wa + f8wb + f8wc +
            f8wd + f8we + f8wr + f8ws + f8wt + f8wu)

def _creimp_2007(f2ab, f8ta, f8tb, f8tc, f8te, f8tf, f8tg, f8th, f8to, f8tp, f8uz, f8tz, f8wa, f8wb, f8wc, f8wd, f8wr,
                   f8ws, f8wt, f8wu, f8wv, f8wx):
    '''Avoir fiscaux et crédits d'impôt 2007 '''
    return  (f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8uz + f8tz + f8wa + f8wb + f8wc +
            f8wd + f8wr + f8ws + f8wt + f8wu + f8wv + f8wx)

def _creimp_2008(f2ab, f8ta, f8tb, f8tc, f8te, f8tf, f8tg, f8th, f8to, f8tp, f8uz, f8tz, f8wa, f8wb, f8wc,
                  f8wd, f8we, f8wr, f8ws, f8wt, f8wu, f8wv, f8wx):
    '''Avoir fiscaux et crédits d'impôt 2008'''
    return  (f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8uz + f8tz + f8wa + f8wb + f8wc +

            f8wd + f8wr + f8ws + f8wt + f8wu + f8wv + f8wx)
def _creimp_2009(f2ab, f8ta, f8tb, f8tf, f8tg, f8th, f8to, f8tp, f8uz, f8tz, f8wa, f8wb, f8wd, f8we, f8wr, f8ws, f8wt,
                  f8wu, f8wv, f8wx, f8wy):
    '''Avoir fiscaux et crédits d'impôt 2009'''
    return  (f2ab + f8ta + f8tb - f8tf + f8tg + f8th + f8to - f8tp + f8uz + f8tz + f8wa + f8wb + f8wd + f8we + f8wr +
            f8ws + f8wt + f8wu + f8wv + f8wx + f8wy)

def _creimp_2010_2011(f2ab, f8ta, f8tb, f8tc, f8tf, f8tg, f8th, f8to, f8tp, f8uz, f8tz, f8wa, f8wb, f8wd,
                  f8we, f8wr, f8wt, f8wu, f8wv):
    '''Avoir fiscaux et crédits d'impôt 2011 '''
    return (f2ab + f8ta + f8tb + f8tc - f8tf + f8tg + f8th + f8to - f8tp + f8uz + f8tz + f8wa + f8wb + f8wd + f8we +
           f8wr + f8wt + f8wu + f8wv)













#def _creimp(f2ab, f8ta, f8tb, f8tf, f8tg, f8th, f8tc, f8td, f8te, f8to, f8tp, f8uz, f8tz, f8wa, f8wb, f8wc, f8wd, f8we, f8wr, f8ws, f8wt, f8wu, f8wv, f8wx, f8wy, _P):
#    '''
#    Avoir fiscaux et crédits d'impôt
#    2002-
#    '''
#
#    if _P.datesim.year == 2002:
#        return (f2ab + f8ta + f8tb + f8tc + f8td + f8te - f8tf + f8tg + f8th)
#
#    elif _P.datesim.year == 2003:
#        return (f2ab + f8ta + f8tb + f8tc + f8td + f8te - f8tf + f8tg + f8th + f8to - f8tp)
#
#    elif _P.datesim.year == 2004:
#        return (f2ab + f8ta + f8tb + f8tc + f8td + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8uz + f8tz)
#
#    elif _P.datesim.year == 2005:
#        return (f2ab + f8ta + f8tb + f8tc + f8td + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8uz + f8tz + f8wa + f8wb + f8wc + f8we)
#
#
#
#    elif _P.datesim.year == 2006:
#        return (f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th
#                   + f8to - f8tp + f8uz + f8tz + f8wa + f8wb + f8wc + f8wd + f8we + f8wr + f8ws + f8wt + f8wu)
#
#    elif _P.datesim.year == 2007:
#        return (f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8thhttp://www3.finances.gouv.fr/calcul_impot/2012/complet/index.htm
#                   + f8to - f8tp + f8uz + f8tz + f8wa + f8wb + f8wc + f8wd + f8wr + f8ws + f8wt + f8wu + f8wv + f8wx)
#
#
#
#    elif _P.datesim.year == 2008:
#        return (f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th
#                   + f8to - f8tp + f8uz + f8tz + f8wa + f8wb + f8wc + f8wd + f8we + f8wr + f8ws + f8wt + f8wu + f8wv + f8wx)
#
#
#    elif _P.datesim.year == 2009:
#        return (f2ab + f8ta + f8tb - f8tf + f8tg + f8th + f8to - f8tp
#                   + f8uz + f8tz + f8wa + f8wb + f8wd + f8we + f8wr + f8ws + f8wt + f8wu + f8wv + f8wx + f8wy)
#
#
#    elif _P.datesim.year == 2010:
#        return (f2ab + f8ta + f8tb + f8tc - f8tf + f8tg + f8th + f8to - f8tp + f8uz + f8tz + f8wa + f8wb + f8wd + f8we + f8wr + f8wt + f8wu + f8wv)
#
#
#
#    elif _P.datesim.year == 2011:
#        log.warning("TODO: totally unchecked")
#        return (f2ab + f8ta + f8tb + f8tc - f8tf + f8tg + f8th + f8to - f8tp + f8uz + f8tz + f8wa + f8wb + f8wd + f8we + f8wr + f8wt + f8wu + f8wv)
#
#
#    else:
#        log.warning("TODO: not implemented, returns 0")
#        return f2ab * 0  # TODO: 2012

def _divide(marpac, f2dc, f2gr, _P):
    '''
    Crédit d'impôt dividendes
    2005-2009
    '''
    P = _P.ir.credits_impot.divide

    max1 = P.max * (marpac + 1)
    return min_(P.taux * (f2dc + f2gr), max1)

def _percvm(f3vv_end_2010, _P):
    '''
    Crédit d’impôt pertes sur cessions de valeurs mobilières (3VV)
    -2010
    '''
    # TODO: check when it starts
    return _P.ir.credits_impot.percvm.taux * f3vv_end_2010

def _direpa(f2bg):
    '''
    Crédit d’impôt directive « épargne » (case 2BG)
    '''
    return f2bg

def _accult(f7uo, _P):
    '''
    Acquisition de biens culturels (case 7UO)
    2002-
    '''
    P = _P.ir.credits_impot.accult
    return P.taux * f7uo

def _mecena(f7us):
    '''
    Mécénat d'entreprise (case 7US)
    2003-
    '''
    return f7us

def _prlire(f2dh, f2ch, marpac, _P):
    '''
    Prélèvement libératoire à restituer (case 2DH)
    2002-2013
    '''
    plaf_resid = max_(_P.ir.rvcm.abat_assvie - f2ch, 0)
    return _P.ir.credits_impot.prlire.taux * min_(f2dh, plaf_resid)

def _quaenv_2005(marpac, nb_pac2, f7wf, f7wh, f7wg, _P):
    '''
    Crédits d’impôt pour dépenses en faveur de la qualité environnementale
    (cases 7WF, 7WH, 7WK, 7WQ, 7SB, 7SD, 7SE et 7SH)
    2005-
    '''
    P = _P.ir.credits_impot.quaenv

    n = nb_pac2
    max0 = P.max * (1 + marpac) + P.pac1 * (n >= 1) + P.pac2 * (n >= 2) + P.pac2 * (max_(n - 2, 0))

    max1 = max_(0, max0 - f7wf)
    max2 = max_(0, max1 - f7wg)
    return (P.taux_wf * min_(f7wf, max0) +
		P.taux_wg * min_(f7wg, max1) +
		P.taux_wh * min_(f7wh, max2))


def _quaenv_2006_2008(marpac, nb_pac2, f7wf, f7wh, f7wq, f7wg, _P):
    '''
    Crédits d’impôt pour dépenses en faveur de la qualité environnementale
    (cases 7WF, 7WH, 7WK, 7WQ, 7SB, 7SD, 7SE et 7SH)
    2005-
    '''
    P = _P.ir.credits_impot.quaenv

    n = nb_pac2

    max0 = P.max * (1 + marpac) + P.pac1 * n

    max1 = max_(0, max0 - f7wf)
    max2 = max_(0, max1 - f7wg)
    max3 = max_(0, max2 - f7wh)
    return (P.taux_wf * min_(f7wf, max0) +
                P.taux_wg * min_(f7wg, max1) +
                P.taux_wh * min_(f7wh, max2) +
                P.taux_wq * min_(f7wq, max3))


def _quaenv_2009(marpac, nb_pac2, f7wf, f7wh, f7wk, f7sb, f7sd, f7se, f7wg, f7sc, _P):
    '''
    Crédits d’impôt pour dépenses en faveur de la qualité environnementale
    (cases 7WF, 7WH, 7WK, 7WQ, 7SB, 7SD, 7SE et 7SH)
    2005-
    '''
    P = _P.ir.credits_impot.quaenv

    n = nb_pac2

    max0 = P.max * (1 + marpac) + P.pac1 * n

    max1 = max_(0, max0 - f7wf)
    max2 = max_(0, max1 - f7se)
    max3 = max_(0, max2 - f7wk)
    max4 = max_(0, max3 - f7sd)
    max5 = max_(0, max4 - f7wg)
    max6 = max_(0, max5 - f7sc)
    max7 = max_(0, max6 - f7wh)
    return (P.taux_wf * min_(f7wf, max0) +
                P.taux_se * min_(f7se, max1) +
                P.taux_wk * min_(f7wk, max2) +
                P.taux_sd * min_(f7sd, max3) +
                P.taux_wg * min_(f7wg, max4) +
                P.taux_sc * min_(f7sc, max5) +
                P.taux_wh * min_(f7wh, max6) +
                P.taux_sb * min_(f7sb, max7))


def _quaenv_2010(marpac, nb_pac2, f7wf, f7wh, f7wk, f7wq, f7sb, f7sd, f7se, f7sh, _P):
    '''
    Crédits d’impôt pour dépenses en faveur de la qualité environnementale
    (cases 7WF, 7WH, 7WK, 7WQ, 7SB, 7SD, 7SE et 7SH)
    2005-
    '''
    P = _P.ir.credits_impot.quaenv

    n = nb_pac2
    max0 = P.max * (1 + marpac) + P.pac1 * n

    max1 = max_(0, max0 - f7wf)
    max2 = max_(0, max1 - f7se)
    max3 = max_(0, max2 - f7wk)
    max4 = max_(0, max3 - f7sd)
    max5 = max_(0, max4 - f7wh)
    max6 = max_(0, max5 - f7sb)
    max7 = max_(0, max6 - f7wq)
    return (P.taux_wf * min_(f7wf, max0) +
                P.taux_se * min_(f7se, max1) +
                P.taux_wk * min_(f7wk, max2) +
                P.taux_sd * min_(f7sd, max3) +
                P.taux_wh * min_(f7wh, max4) +
                P.taux_sb * min_(f7sb, max5) +
                P.taux_wq * min_(f7wq, max6) +
                P.taux_sh * min_(f7sh, max7))


def _quaenv_2011_(f7wf, _P):
    '''
    Crédits d’impôt pour dépenses en faveur de la qualité environnementale
    (cases 7WF, 7WH, 7WK, 7WQ, 7SB, 7SD, 7SE et 7SH)
    2005-
    '''
    P = _P.ir.credits_impot.quaenv
# TODO: Check 2011 formula and plaf in param

    return f7wf * 0

def _aidper_2002_2003(marpac, nb_pac2, f7wi, _P):
    '''
    Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
    (cases 7WI, 7WJ, 7WL et 7SF).
    2002-2003
    '''
    P = _P.ir.credits_impot.aidper

    n = nb_pac2
    max0 = P.max * (1 + marpac) + P.pac1 * (n >= 1) + P.pac2 * (n >= 2) + P.pac2 * (max_(n - 2, 0))

    return P.taux_wi * min_(f7wi, max0)  # TODO: enfant en résidence altérnée

def _aidper_2004_2005(marpac, nb_pac2, f7wi, f7wj, _P):
    '''
    Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
    (cases 7WI, 7WJ, 7WL et 7SF).
    2004-2005
    '''
    P = _P.ir.credits_impot.aidper

    n = nb_pac2
    max0 = P.max * (1 + marpac) + P.pac1 * (n >= 1) + P.pac2 * (n >= 2) + P.pac2 * (max_(n - 2, 0))

    max1 = max_(0, max0 - f7wj)
    return (P.taux_wj * min_(f7wj, max0) +
                P.taux_wi * min_(f7wi, max1))

def _aidper_2006_2009(marpac, nb_pac2, f7wi, f7wj, _P):
    '''
    Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
    (cases 7WI, 7WJ, 7WL et 7SF).
    2002-
    '''
    P = _P.ir.credits_impot.aidper

    n = nb_pac2
    max0 = P.max * (1 + marpac) + P.pac1 * n

    max1 = max_(0, max0 - f7wj)
    return (P.taux_wj * min_(f7wj, max0) +
                P.taux_wi * min_(f7wi, max1))

def _aidper_2010(marpac, nb_pac2, f7wj, f7wl, f7sf, f7si, _P):
    '''
    Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
    (cases 7WI, 7WJ, 7WL et 7SF).
    2002-
    '''
    P = _P.ir.credits_impot.aidper

    n = nb_pac2
    max0 = P.max * (1 + marpac) + P.pac1 * n

    max1 = max_(0, max0 - f7wl)
    max2 = max_(0, max1 - f7sf)
    max3 = max_(0, max2 - f7wj)
    return (P.taux_wl * min_(f7wl, max0) +
                P.taux_sf * min_(f7sf, max1) +
                P.taux_wj * min_(f7wj, max2) +
                P.taux_wi * min_(f7si, max3))

def _aidper_2011_(marpac, _P):
    '''
    Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
    (cases 7WI, 7WJ, 7WL et 7SF).
    2002-
    '''
    P = _P.ir.credits_impot.aidper

    return 0 * marpac  # TODO 2011, 2012, 2013

def _acqgpl(f7up, f7uq, _P):
    '''
    Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte
    2002-2007
    '''
    P = _P.ir.credits_impot.acqgpl

    if 2002 <= _P.datesim.year <= 2007:
        return f7up * P.mont_up + f7uq * P.mont_uq

def _drbail(f4tq, _P):
    '''
    Crédit d’impôt représentatif de la taxe additionnelle au droit de bail (case 4TQ)
    2002-
    '''
    P = _P.ir.credits_impot.drbail
    return P.taux * f4tq

def _ci_garext(f7ga, f7gb, f7gc, f7ge, f7gf, f7gg, _P):
    '''
    Frais de garde des enfants à l’extérieur du domicile (cases 7GA à 7GC et 7GE à 7GG)
    2005-
    '''
    P = _P.ir.credits_impot.garext
    max1 = P.max
    return P.taux * (min_(f7ga, max1) +
                          min_(f7gb, max1) +
                          min_(f7gc, max1) +
                          min_(f7ge, max1 / 2) +
                          min_(f7gf, max1 / 2) +
                          min_(f7gg, max1 / 2))

def _preetu_2005(f7uk, _P):
    '''
    Crédit d’impôt pour souscription de prêts étudiants (cases 7UK, 7VO et 7TD)
    2005
    '''
    P = _P.ir.credits_impot.preetu

    return P.taux * min_(f7uk, P.max)

def _preetu_2006_2007(f7uk, f7vo, _P):
    '''
    Crédit d’impôt pour souscription de prêts étudiants (cases 7UK, 7VO et 7TD)
    2006-2007
    '''
    P = _P.ir.credits_impot.preetu

    max1 = P.max * (1 + f7vo)  # TODO check if it is not (f7vo) instead for ALL OR SOME YEARS (2011 for example)
    return P.taux * min_(f7uk, max1)

def _preetu_2008_(f7uk, f7vo, f7td, _P):
    '''
    Crédit d’impôt pour souscription de prêts étudiants (cases 7UK, 7VO et 7TD)
    2008-
    '''
    P = _P.ir.credits_impot.preetu

    max1 = P.max * f7vo  # TODO check if it is not (f7vo) instead for ALL OR SOME YEARS (2011 for example)
    return P.taux * min_(f7uk, P.max) + P.taux * min_(f7td, max1)  # TODO:

def _saldom2_2007_2008(nb_pac2, f7db, f7dg, f7dl, _P):
    '''
    Crédit d’impôt emploi d’un salarié à domicile (cases 7DB, 7DG)
    2007-2008
    '''
    P = _P.ir.reductions_impots.saldom

    isinvalid = f7dg

    nbpacmin = nb_pac2 + f7dl
    maxBase = P.max1
    maxDuMaxNonInv = P.max2
    maxNonInv = min_(maxBase + P.pac * nbpacmin, maxDuMaxNonInv)
    maxEffectif = maxNonInv * not_(isinvalid) + P.max3 * isinvalid

    return P.taux * min_(f7db, maxEffectif)

def _saldom2_2009_2010(nb_pac2, f7db, f7dg, f7dl, f7dq, _P):
    '''
    Crédit d’impôt emploi d’un salarié à domicile (cases 7DB, 7DG)
    2009-2010
    '''
    P = _P.ir.reductions_impots.saldom

    isinvalid = f7dg

    annee1 = f7dq
    nbpacmin = nb_pac2 + f7dl
    maxBase = P.max1 * not_(annee1) + P.max1_1ereAnnee * annee1
    maxDuMaxNonInv = P.max2 * not_(annee1) + P.max2_1ereAnnee * annee1
    maxNonInv = min_(maxBase + P.pac * nbpacmin, maxDuMaxNonInv)
    maxEffectif = maxNonInv * not_(isinvalid) + P.max3 * isinvalid

    return P.taux * min_(f7db, maxEffectif)

def _saldom2_2011_(f7db, f7dg,_P):
    '''
    Crédit d’impôt emploi d’un salarié à domicile (cases 7DB, 7DG)
    2011-
    '''
    P = _P.ir.reductions_impots.saldom

    isinvalid = f7dg

    maxEffectif = 0

    return P.taux * min_(f7db, maxEffectif)

def _inthab_2007(marpac, nb_pac2, caseP, caseF, nbG, nbR, _P):
    '''
    Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
    2007
    '''
    P = _P.ir.credits_impot.inthab

    invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
    nb = nb_pac2
    max0 = P.max * (marpac + 1) * (1 + invalide) + nb * P.add

    return 0 * nb  # TODO
    
def _inthab_2008(marpac, nb_pac2, caseP, caseF, nbG, nbR, f7vy, f7vz, _P):
    '''
    Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
    2008
    '''
    P = _P.ir.credits_impot.inthab

    invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
    nb = nb_pac2
    max0 = P.max * (marpac + 1) * (1 + invalide) + nb * P.add

    max1 = max_(max0 - f7vy, 0)
    return (P.taux1 * min_(f7vy, max0) +
                P.taux3 * min_(f7vz, max1))


def _inthab_2009(marpac, nb_pac2, caseP, caseF, nbG, nbR, f7vx, f7vy, f7vz, _P):
    '''
    Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
    2009
    '''
    P = _P.ir.credits_impot.inthab

    invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
    nb = nb_pac2
    max0 = P.max * (marpac + 1) * (1 + invalide) + nb * P.add

    max1 = max_(max0 - f7vx, 0)
    max2 = max_(max1 - f7vy, 0)
    return (P.taux1 * min_(f7vx, max0) +
                P.taux1 * min_(f7vy, max1) +
                P.taux3 * min_(f7vz, max2))

def _inthab_2010(marpac, nb_pac2, caseP, caseF, nbG, nbR, f7vw, f7vx, f7vy, f7vz, _P):
    '''
    Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
    2010
    '''
    P = _P.ir.credits_impot.inthab

    invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
    nb = nb_pac2
    max0 = P.max * (marpac + 1) * (1 + invalide) + nb * P.add

    max1 = max_(max0 - f7vx, 0)
    max2 = max_(max1 - f7vy, 0)
    max3 = max_(max2 - f7vw, 0)
    return (P.taux1 * min_(f7vx, max0) +
                P.taux1 * min_(f7vy, max1) +
                P.taux2 * min_(f7vw, max2) +
                P.taux3 * min_(f7vz, max3))

def _inthab_2011(marpac, nb_pac2, caseP, caseF, nbG, nbR, f7vw, f7vx, f7vy, f7vz, _P):
    '''
    Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
    2011
    '''
    P = _P.ir.credits_impot.inthab

    invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
    nb = nb_pac2
    max0 = P.max * (marpac + 1) * (1 + invalide) + nb * P.add

    max1 = max_(max0 - f7vx, 0)
    max2 = max_(max1 - f7vy, 0)
    max3 = max_(max2 - f7vw, 0)
    return (P.taux1 * min_(f7vx, max0) +
                P.taux1 * min_(f7vy, max1) +
                P.taux2 * min_(f7vw, max2) +
                P.taux3 * min_(f7vz, max3))

def _inthab_2012_(f7vx,_P):
    '''
    Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
    2012-
    '''

    return f7vx * 0

def _assloy(f4bf, _P):
    '''
    Crédit d’impôt primes d’assurance pour loyers impayés (case 4BF)
    2005-
    '''
    return _P.ir.credits_impot.assloy.taux * f4bf

def _autent(f8uy):
    '''
    Auto-entrepreneur : versements d’impôt sur le revenu (case 8UY)
    2009-
    '''
    return f8uy

def _aidmob(f1ar, f1br, f1cr, f1dr, f1er, _P):
    '''
    Crédit d'impôt aide à la mobilité
    2005-2008
    '''
    return (f1ar + f1br + f1cr + f1dr + f1er) * _P.ir.credits_impot.aidmob.montant

def _jeunes(self, age_holder, nbptr, rfr, marpac, _P):  # TODO: Replace VOUS in age with personnes à charge.
    '''
    Crédit d'impôt en faveur des jeunes
    2005-2008
    TODO: What is rev?
    rfr de l'année où jeune de moins de 26 à travaillé six mois
    '''
    age = self.filter_role(age_holder, role = VOUS)

    rev = 0
    P = _P.ir.credits_impot.jeunes
    elig = (age > P.age) * (rfr > P.rfr_plaf * (marpac * P.rfr_mult + not_(marpac)) + max_(0, nbptr - 2) * .5 * P.rfr_maj)
    montant = (P.min >= rev > P.int) * P.montant + (P.int >= rev >= P.max) * P.taux
    return  elig * montant  # D'après  le document num. 2041 GY
                                # somme calculée sur formulaire 2041
