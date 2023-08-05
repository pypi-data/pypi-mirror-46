from __future__ import division, print_function

import sys
from pkg_resources import resource_filename

import numpy as np
import astropy.units as u
import astropy.constants as c
from scipy.optimize import fsolve
from scipy.interpolate import UnivariateSpline


def compute_isco(chi_bh):
    '''
    This function takes as input the aligned spin component of the BH and
    returns the innermost stable circular orbit radius normalized by the mass
    of the BH.
    '''
    try:
        assert np.all([np.abs(chi_bh) <= 1.0])
    except AssertionError:
        print('|chi1| must be less than 1.0')
        sys.exit(1)
    Z1 = 1.0 + ((1.0 - chi_bh**2)**(1./3.))*((1 + chi_bh)**(1./3.) +
                                             (1 - chi_bh)**(1./3.))
    Z2 = np.sqrt(3*chi_bh**2 + Z1**2)
    r_isco = 3 + Z2 - np.sign(chi_bh) * np.sqrt((3 - Z1)*(3 + Z1 + 2*Z2))
    return r_isco


def computeCompactness(M_ns, max_mass, R_ns=None, fromFile=False):
    '''
    This function takes as input the mass of the neutron star in solar mass
    and its radius in meters and returns the value of the compactness.
    '''
    if fromFile:
        eosfile = resource_filename(__name__, 'data/equil_2H.dat')
        M_g, M_b, Compactness = np.loadtxt(eosfile, unpack=True)
        s = UnivariateSpline(M_g, Compactness, k=5)
        s_b = UnivariateSpline(M_g, M_b, k=5)
        C_ns = s(M_ns)
        m2_b = s_b(M_ns)
    else:
        assert R_ns is not None, print('Radius must be supplied')
        C_ns = c.G * M_ns * c.M_sun/(R_ns * u.m * c.c**2)
        C_ns = C_ns.value

        d1 = 0.619
        d2 = 0.1359
        BE = (d1*C_ns + d2*C_ns*C_ns)*M_ns  # arXiv:1601.06083
        m2_b = M_ns + BE

    C_ns[M_ns > max_mass] = 0.5 ## BH compactness set to 0.5
    ### But Baryon mass is not zero, disk mass is. FIXME
    m2_b[M_ns > max_mass] = 0.0 ## BH baryon mass set to 0.0


    return [C_ns, m2_b]


'''
For Newtonian: Obtained from arXiv 1807.00011
alpha = 0.406
beta = 0.139
gamma = 0.255
delta = 1.761

For Kerr: Obtained from private message from F. Foucart
alpha = 0.24037857
beta = 0.15184471
gamma = 0.35607169
delta = 1.81491784
'''


def xi_implicit(xi, kappa, chi1, eta):
    xi_implicit = 3*(xi**2 - 2*kappa*xi + kappa**2*chi1**2)
    xi_implicit /= (xi**2 - 3*kappa*xi + 2*chi1*np.sqrt(kappa**3*xi))
    xi_implicit -= eta*xi**3
    return xi_implicit


def computeDiskMass(m1, m2, chi1, chi2, eosname='2H', kerr=False):
    '''
    This function computes the remnant disk mass after the coalescence using
    the equation (4) arXiv 1807.00011.
    '''
    ## Making sure that the supplied m1 >= m2 ##
    if (type(m1) == np.ndarray) and (type(m2) == np.ndarray):
        largerMass1 = m1 >= m2
        largerMass2 = m2 > m1
        m_primary = np.zeros_like(m1)
        m_secondary = np.zeros_like(m2)
        chi_primary = np.zeros_like(chi1)
        chi_secondary = np.zeros_like(chi2)

        m_primary[largerMass1] = m1[largerMass1]
        m_primary[~largerMass1] = m2[largerMass2]
        m_secondary[~largerMass2] = m2[~largerMass2]
        m_secondary[largerMass2] = m1[~largerMass1]

        chi_primary[largerMass1] = chi1[largerMass1]
        chi_primary[~largerMass1] = chi2[~largerMass1]
        chi_secondary[~largerMass2] = chi2[~largerMass2]
        chi_secondary[largerMass2] = chi1[~largerMass1]

    if (type(m1) == float) and (type(m2) == float):
        if m1 >= m2:
            m_primary = m1
            m_secondary = m2
            chi_primary = chi1
            chi_secondary = chi2
        else:
            m_primary = m2
            m_secondary = m1
            chi_primary = chi2
            chi_secondary = chi1

    if eosname == '2H':
        max_mass = 2.834648092299807
        [C_ns, m2_b] = computeCompactness(m_secondary, max_mass,
                                          fromFile=True)
        R_ns = c.G*m_secondary*c.M_sun/(C_ns*c.c**2)
    else:  # This is going to be for lalsimulation eos.
        import lal
        import lalsimulation as lalsim

        eos = lalsim.SimNeutronStarEOSByName(eosname)
        fam = lalsim.CreateSimNeutronStarFamily(eos)
        max_mass = lalsim.SimNeutronStarMaximumMass(fam)/c.M_sun.value
        print("Only 2H EoS is allowed currently...")
        sys.exit(0)
        [C_ns, m2_b] = computeCompactness(m_secondary, max_mass,
                                          R_ns, fromFile=False)
    eta = m_primary*m_secondary/(m_primary + m_secondary)**2
    BBH = m_secondary > max_mass
    BNS = m_primary < max_mass
    if type(BNS) == bool:
        if BNS or BBH:
            return float(not(BBH) or BNS)

    if not kerr:
        alpha = 0.406
        beta = 0.139
        gamma = 0.255
        delta = 1.761
        firstTerm = alpha*(1 - 2*C_ns)/(eta**(1/3))
        secondTerm = beta*compute_isco(chi1)*C_ns/eta
        thirdTerm = gamma
    else:
        alpha = 0.24037857
        beta = 0.15184471
        gamma = 0.35607169
        delta = 1.81491784
        kappa = (m_primary/m_secondary)*C_ns
        try:
            Num = len(kappa)
            xi = fsolve(xi_implicit, 100*np.ones(Num), args=(kappa, chi1, eta))
        except TypeError:
            xi = fsolve(xi_implicit, 100, args=(kappa, chi1, eta))

        firstTerm = alpha*xi*(1 - 2*C_ns)
        secondTerm = beta*compute_isco(chi1)*C_ns/eta
        thirdTerm = gamma
    combinedTerms = firstTerm - secondTerm + thirdTerm

    if type(combinedTerms) == float:
        if combinedTerms < 0.0:
            combinedTerms = 0.0
    if type(combinedTerms) == np.ndarray:
        lessthanzero = combinedTerms < 0.0
        combinedTerms[lessthanzero] = 0.0
    M_rem = (combinedTerms**delta)*m2_b
    if type(BNS) == np.ndarray:
        M_rem[BBH] = 0.0 # BBH is always EM-Dark
        M_rem[BNS] = 1.0 # Ad hoc value, assuming BNS is always EM-Bright


    return M_rem
