"""
Created on Mon May 30 09:48:18 2022.

This script handles the critical coupling sweep automation

@author: AlexTofini
"""
# Import dependencies
import math
import FDTD_SetUp as FDTD
import numpy as np
from scipy.interpolate import interp1d


def runSweep(parameters, simulation_setup):
    """
    Execute coupling region gap sweep in FDTD.

    Parameters
    ----------
    parameters : class
        Physical parameter class containing relevant about the physical parameters of the ring.
    simulation_setup : class
        Simulation class containing relevant information about the simulation settings.

    Returns
    -------
    Coupling_Coefficients : list
        List of coupling coefficient results for the swept gaps.
    coupler_IDs : list
        List of coupler IDs either returned via query or stored after simulation execution.

    """
    # Initialize lists
    Coupling_Coefficients = []
    coupler_IDs = []

    # Iterate through gaps and run FDTD coupling method that will either query results or simulate
    for ii in range(len(parameters.gap)):
        Coupling_Coefficient, coupler_ID = FDTD.calculate_coupling_coefficient(
            parameters, simulation_setup, gap=parameters.gap[ii])
        Coupling_Coefficients.append(Coupling_Coefficient)
        coupler_IDs.append(coupler_ID)
    return Coupling_Coefficients, coupler_IDs


def FindOptimalGap(gaps, sweep_results, simulation_setup, power_coupling):
    """
    Determine the optimal gap from the swept gap simulation and theoretical power coupling.

    Parameters
    ----------
    gaps : list
        List of gaps used in critical coupling sweep.
    sweep_results : list
        List containing sweep results from the coupling sweep.
    simulation_setup : class
        Simulation class containing relevant information about the simulation settings.
    power_coupling : float
        Theoretically required power coupling i.e. kappa value to achieve critical coupling.

    Returns
    -------
    optimal_gap : float
        Gap that will achieve critical coupling.

    """
    # Initialize list for power coupling coefficients
    power_coupling_coefficients = []

    # Defining speed of light to convert frequency to wavelength
    c = 299792458

    # Loading optical band and defining central wavelength to achieve critical coupling for
    band = simulation_setup.Band
    if band == 'CL':
        Center_wavl = 1550e-9
    else:
        Center_wavl = 1310e-9

    # Populate power coupling list with value corresponding closest to the central wavelength
    for ii in range(len(sweep_results)):
        frequencies = sweep_results[ii][0]
        wavelengths = [c/x for x in frequencies]
        indx = min(range(len(wavelengths)), key=lambda i: abs(wavelengths[i]-Center_wavl))
        power_coupling_coefficients.append(sweep_results[ii][1][indx])

    # Setting up interpolation function to get nm resolution for gaps
    f = interp1d(gaps, power_coupling_coefficients, kind='cubic')
    gaps_interp = np.linspace(min(gaps), max(gaps), round((max(gaps)-min(gaps))/1e-9)+1)

    # Enforcing rounding cause sometimes python has a slight rouding error
    for ii in range(len(gaps_interp)):
        gaps_interp[ii] = round(gaps_interp[ii], 9)

    # Interpolating power coupling coefficient results to higher resolution
    power_coupling_coefficients_interp = f(gaps_interp)

    # Determine index in interpolated power coupling that matches the theoretical value supplied
    critical_index = min(range(len(power_coupling_coefficients_interp)),
                         key=lambda i: abs(power_coupling_coefficients_interp[i]-power_coupling))

    # Determining the gap value at the critical index i.e. the critical gap
    optimal_gap = gaps_interp[critical_index]

    return optimal_gap


def EstimateCC_Condition(parameters, simulation_setup, saved_results):
    """
    Estimate required power coupling, i.e. Kappa to achieve critical coupling.

    This is based off the user provided propagation loss and the simulation absorption/bend loss.

    Parameters
    ----------
    parameters : class
        Physical parameter class containing relevant about the physical parameters of the ring.
    simulation_setup : class
        Simulation class containing relevant information about the simulation settings.
    saved_results : class
        Simulation class containing relevant results from previous simulation steps.

    Returns
    -------
    power_coupling : float
        Theoretically required power coupling, i.e. kappa, to achieve critical coupling.

    """
    alpha = saved_results.absorption_loss[0]/100 + simulation_setup.propagation_loss/100  # [dB/cm]
    RoundTrip = 2*math.pi*parameters.radius*100  # [cm]
    power_coupling = 1 - 10**(alpha*RoundTrip/-10)
    return power_coupling
