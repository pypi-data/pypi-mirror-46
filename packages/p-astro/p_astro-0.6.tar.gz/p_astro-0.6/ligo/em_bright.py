"""Module containing tools for EM-Bright classification of
compact binaries using trained supervised classifier
"""

import pickle
from os import path

import pkg_resources

from .computeDiskMass import compute_isco


def mchirp(m1, m2):
    return(m1 * m2)**(3./5.)/(m1 + m2)**(1./5.)


def q(m1, m2):
    return m2/m1 if m2 < m1 else m1/m2


def source_classification(m1, m2, chi1, chi2, snr,
                          ns_classifier=None,
                          emb_classifier=None,
                          scaler=None):
    """
    Returns the predicted probability of whether a
    compact binary either has an EM counterpart or
    has a NS as one of its components

    Parameters
    ----------
    m1 : float
        primary mass
    m2 : float
        secondary mass
    chi1 : float
        dimensionless primary spin
    chi2 : float
        dimensionless secondary spin
    snr : float
        signal to noise ratio of the signal
    ns_classifier : object
        pickled object for NS classification
    emb_classifier : object
        pickled object for EM brightness classification
    scaler : object
        pickle object storing `StandardScaler`
        instance with which to scale input parameters

    Returns
    -------
    tuple
        (P_NS, P_EMB) predicted values.

    Notes
    -----
    By default the classifiers and scaler provided in the package
    data is used to make predictions. All three `ns_classifier`,
    `emb_classifier` and `scaler` must be supplied
    when not using defaults for sensible results.

    Examples
    --------
    >>> from ligo import em_bright
    >>> em_bright.source_classification(2.0 ,1.0 ,0. ,0. ,10.0)
    (1.0, 1.0)
    """
    if not ns_classifier:
        ns_classifier = pickle.load(open(pkg_resources.resource_filename(
            __name__, 'data/RF_classifier_ns_complete_set.pkl'), 'rb'))
    if not emb_classifier:
        emb_classifier = pickle.load(open(pkg_resources.resource_filename(
            __name__, 'data/RF_classifier_emb_complete_set.pkl'), 'rb'))
    if not scaler:
        scaler = pickle.load(open(pkg_resources.resource_filename(
            __name__, 'data/scaler_set_all.pkl'), 'rb'))

    mc = mchirp(m1, m2)
    mass_ratio = q(m1, m2)
    isco = compute_isco(chi1)

    features = [[m1, m2, mc, mass_ratio, chi1, chi2, isco, snr]]
    prediction_em, prediction_ns = \
        emb_classifier.predict_proba(scaler.transform(features)).T[1], \
        ns_classifier.predict_proba(scaler.transform(features)).T[1]
    return prediction_ns[0], prediction_em[0]
