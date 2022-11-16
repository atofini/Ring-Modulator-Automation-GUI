"""
Created on Wed Jul 21 11:27:18 2021.

This script sets up the Interconnect simulation for the completed ring transmission and eye diagrams

@author: AlexTofini
"""
# Import dependencies
import lumerical_tools
import os
import numpy as np
import h5py
import ConnectToDatabase as database
from scipy.interpolate import interp1d
from scipy.signal import find_peaks


def Build_Ring(parameters, simulation_setup, charge_setup, saved_results):
    """
    Combine simulation results for coupling region, PN junction and waveguide to form ring.

    Transmission spectra is the end result of this function.

    Parameters
    ----------
    parameters : class
        Physical parameter class containing relevant about the physical parameters of the ring.
    simulation_setup : class
        Simulation class containing relevant information about the simulation settings.
    charge_setup : class
        Charge class containing relevant information about the CHARGE simulation.
    saved_results : class
        Class object containing previous simulation results from component simulations.

    Returns
    -------
    list
        DESCRIPTION.

    """
    # Saving current working directory
    cwd = os.getcwd()

    # Defining paths to where data is stored
    folder = 'Transmission'
    transmission_path = '/Database/' + folder
    directory = cwd+transmission_path

    # Querying transmission table for matching record
    result = database.QueryTransmission(saved_results.waveguide_ID, saved_results.coupler_ID,
                                        simulation_setup.propagation_loss)

    if result != []:
        # If a transmission record exists, use the results instead of simulating
        print("Database contains a transmission record for current ring parameters")
        transmission_ID = result[0][0]
        transmission_file = result[0][1]
    else:
        # If a transmission record does not exists, call LumAPI to run simulation
        print("Database does not contain a transmission record for the current ring parameters")
        print("Executing Interconnect simulation")

        # Determine the next ID in the transmission table to store data with
        nextID = database.FindNextIndex('Transmission')
        transmission_ID = nextID
        transmission_file = 'transmission_' + str(transmission_ID)

        # Creating temporary files to be read in from Interconnect
        database.CreateTempInterconnectData(saved_results.f, saved_results.CC, saved_results.dNeff,
                                            saved_results.coupler_ID, saved_results.waveguide_ID,
                                            folder)

        # Running simulation
        lumerical_tools.run_interconnect(parameters, simulation_setup, charge_setup,
                                         saved_results, nextID)

        # Deleting temporary files
        database.DestroyTempInterconnectData(
            saved_results.coupler_ID, saved_results.waveguide_ID,
            transmission_ID, folder)

    # Analyzing results and storing in lists
    data = h5py.File(directory+'/'+transmission_file + '.mat', 'r')
    raw = data.get('result')
    raw = np.array(raw)
    wavelength = data.get('result/wavelength')
    wavelength = np.array(wavelength)
    wavelength = np.squeeze(wavelength)
    voltage = data.get('result/voltage')
    voltage = np.array(voltage)
    voltage = np.squeeze(voltage)
    T = data.get('result/TE_gain__dB_')
    T = np.array(T)
    T = np.squeeze(T)

    # Extracting FOMs to display to save to database and display to the user

    # Isolating non biased data, aka 0V
    non_biased_T = T[0, :]
    wavelength = wavelength*1e9

    # Solving list of resonances
    height = 0.01
    [indx, peaks] = find_peaks(-1*non_biased_T, height)
    # plt.plot(wavelength[indx], non_biased_T[indx], "x")
    resonance_array = wavelength[indx]
    for ii in range(len(resonance_array)):
        resonance_array[ii] = round(resonance_array[ii], 3)
    saved_results.resonances = str(resonance_array.tolist())

    # Solving list of FSRs
    FSR_list = [0] * (len(resonance_array)-1)
    for i in range(len(FSR_list)):
        FSR_list[i] = abs(round(resonance_array[i+1]-resonance_array[i], 2))

    saved_results.FSRs = str(FSR_list)

    # Solving list of 3dB bandwidths
    three_dB_bandwidth = [0] * (len(resonance_array))
    three_dB_line = [-3]*len(non_biased_T)
    idx = np.argwhere(np.diff(np.sign(three_dB_line - non_biased_T))).flatten()
    three_dB_intersections = wavelength[idx]
    for i in range(int(len(three_dB_intersections)/2)):
        three_dB_bandwidth[i] = round(
            np.abs(three_dB_intersections[2*i+1] - three_dB_intersections[2*i]), 3)
    saved_results.bandwidths_3dB = str(three_dB_bandwidth)

    # Getting quality factors
    Qfactor = resonance_array/three_dB_bandwidth
    Qfactor = np.around(Qfactor, decimals=-2)
    Qfactor = Qfactor.astype(int)
    saved_results.QFactors = str(Qfactor.tolist())

    # Getting insertion loss Results
    ILs = np.round(np.array(peaks['peak_heights']), 2)
    saved_results.InsertionLosses = str(ILs.tolist())

    # Saving to database if the simulation was executed
    if result == []:
        # Saving to database
        database.WriteTransmission(saved_results.waveguide_ID,
                                   saved_results.coupler_ID, transmission_ID,
                                   transmission_file, simulation_setup.propagation_loss,
                                   saved_results.resonances, saved_results.FSRs,
                                   saved_results.bandwidths_3dB, saved_results.QFactors,
                                   saved_results.InsertionLosses)

    return [wavelength, T]


def Eye_Diagrams(parameters, simulation_setup, saved_results):
    """
    Create eye diagram simulations based off user specified values.

    Parameters
    ----------
    parameters : class
        Physical parameter class containing relevant about the physical parameters of the ring.
    simulation_setup : class
        Simulation class containing relevant information about the simulation settings.
    saved_results : class
        Class object containing previous simulation results from component simulations.

    Returns
    -------
    list
        List containing : [amplitude, time].
            amplitude : list
                List of current values that represent the eye diagram amplitude
            time : list
                List of time values that form the eye diagram

    """
    # Saving current working directory
    cwd = os.getcwd()

    # Using eye type to determine folder location for saving
    Eye_type = simulation_setup.eye_type
    if Eye_type == 'NRZ':
        folder = 'Eye_NRZ'
    else:
        folder = 'Eye_PAM4'

    # Defining path to folder
    path = '/Database/' + folder
    data_directory = cwd + path

    # Query eye table for matching IDs for the waveguide and coupler in addition to propagation loss
    Eye_result = database.QueryEyeTable(saved_results.waveguide_ID, saved_results.coupler_ID,
                                        simulation_setup.propagation_loss)

    if Eye_result != []:
        # If an eye table record does exists, query the eye data with the acquired eye_ID
        Eye_ID = Eye_result[0][0]
        result = database.QueryEyeData(Eye_ID,
                                       simulation_setup.laser_wavl, simulation_setup.eye_vmin,
                                       simulation_setup.eye_vmax, simulation_setup.bitrate,
                                       simulation_setup.eye_type,
                                       simulation_setup.staticNonLinCorrec)
    else:
        # If an eye table record does not exists, create one by finding next ID
        nextID = database.FindNextIndex('Eye')
        Eye_ID = nextID
        database.WriteToEyeTable(Eye_ID, saved_results.waveguide_ID, saved_results.coupler_ID,
                                 simulation_setup.propagation_loss)
        # no need to querry eye data table since we know it is empty
        result = []

    if result != []:
        # If an eye data record is present, use it instead of simulating
        print("Database contains a matching " + Eye_type + " eye record for the current parameters")
        Eye_file = result[0][5]
    else:
        # If no eye data record is present, prepare to simulate using LumAPI
        print("Database does not contain a " + Eye_type + " eye record for the current parameters")
        print("Executing " + Eye_type + " eye diagram in Interconnect")

        # Determine next ID in eye data table for the new record
        nextID = database.FindNextIndex('Eye_Data')
        Eye_Data_ID = nextID
        Eye_file = 'Eye_' + Eye_type + '_' + str(Eye_Data_ID)

        # Creating temporary files to be read in from Interconnect
        database.CreateTempInterconnectData(saved_results.f, saved_results.CC, saved_results.dNeff,
                                            saved_results.coupler_ID, saved_results.waveguide_ID,
                                            folder)

        # Run corresponding LumAPI simulation script depending on eye type
        if Eye_type == 'NRZ':
            lumerical_tools.run_interconnect_EYE_NRZ(
                parameters, simulation_setup, saved_results, nextID)
        elif Eye_type == 'PAM4':
            lumerical_tools.run_interconnect_EYE_PAM4(
                parameters, simulation_setup, saved_results, nextID)

        # Deleting temporary files
        database.DestroyTempInterconnectData(
            saved_results.coupler_ID, saved_results.waveguide_ID,
            Eye_Data_ID, folder)

        # Create new record in eye data table
        database.WriteToEyeData(Eye_ID,
                                simulation_setup.laser_wavl, simulation_setup.eye_vmin,
                                simulation_setup.eye_vmax, simulation_setup.bitrate,
                                Eye_file, Eye_type, simulation_setup.staticNonLinCorrec,
                                Eye_Data_ID)

    # Extract results from .mat file and convert to lists
    data = h5py.File(data_directory+'/'+Eye_file + '.mat', 'r')
    raw = data.get('result')
    raw = np.array(raw)
    amplitude = data.get('result/amplitude__a.u._')
    amplitude = np.array(amplitude)
    amplitude = np.squeeze(amplitude)
    time = data.get('result/time')
    time = np.array(time)
    time = np.squeeze(time)

    return [amplitude, time]


def PAM4_Voltage(simulation_setup, saved_results, charge_setup):
    """
    Determine voltage levels used in the PAM4 modulation.

    Parameters
    ----------
    simulation_setup : class
        Simulation class containing relevant information about the simulation settings.
    saved_results : class
        Class object containing previous simulation results from component simulations.
        DESCRIPTION.
    charge_setup : class
        Charge class containing relevant information about the CHARGE simulation.

    Returns
    -------
    None.

    """
    # Import depencendies

    # The are the requested voltage levels for the eye diagram
    eye_vmin = simulation_setup.eye_vmin
    eye_vmax = simulation_setup.eye_vmax

    # These are the voltage levels present in the imported charge sweep.
    charge_vmin = charge_setup.vmin
    charge_vmax = charge_setup.vmax
    charge_N = charge_setup.charge_datapoints
    voltage = np.linspace(charge_vmin, charge_vmax, charge_N)

    # Populating simulation class settings
    SNLC = simulation_setup.staticNonLinCorrec
    laser = simulation_setup.laser_wavl*1e-9

    # Extracting results from saved results class
    T = saved_results.T
    wavelength = saved_results.wavelength

    if SNLC == 'no':
        # No correction, create simple equidistant linspace
        v_space = np.linspace(eye_vmin, eye_vmax, 4)
        V0 = v_space[0]
        V1 = v_space[1]
        V2 = v_space[2]
        V3 = v_space[3]
    else:
        # Yes correction, use automation algorithm to create non-linear voltages
        indx = min(range(len(wavelength)), key=lambda i: abs(wavelength[i]-laser))
        shift_curve = []
        for ii in range(len(T)):
            shift_curve.append(T[ii, indx])

        # Interpolating to high res
        f = interp1d(voltage, shift_curve, kind='cubic')
        voltage_interp = np.linspace(voltage[0], voltage[-1], num=10000, endpoint=True)
        shift_curve_interp = f(voltage_interp)

        # restricting data within the boundaries of the eye diagram voltages
        shift_curve_trunc = []
        voltage_trunc = []
        for ii in range(len(voltage_interp)):
            if voltage_interp[ii] >= eye_vmin and voltage_interp[ii] <= eye_vmax:
                voltage_trunc.append(voltage_interp[ii])
                shift_curve_trunc.append(shift_curve_interp[ii])

        max_shift = max(shift_curve_trunc)
        min_shift = min(shift_curve_trunc)
# =============================================================================
#         max_index = shift_curve_trunc.index(max_shift)
#         min_index = shift_curve_trunc.index(min_shift)
#
#         # Determining voltage levels for equidistant transmission
#         shift_range = max_shift - min_shift
# =============================================================================
        shift_levels = np.linspace(min_shift, max_shift, 4)

        # Finding voltage levels
        voltage_levels = []
        for ii in range(len(shift_levels)):
            indx = min(range(len(shift_curve_trunc)), key=lambda j: abs(
                shift_curve_trunc[j]-shift_levels[ii]))
            voltage_levels.append(round(voltage_trunc[indx], 3))

        V0 = voltage_levels[0]
        V1 = voltage_levels[1]
        V2 = voltage_levels[2]
        V3 = voltage_levels[3]

        # TODO(REMOVE THIS ) since it is for thesis plotting only

# =============================================================================

# =============================================================================
#         plt.plot(voltage, shift_curve, label='Transmission @ Laser Wavelength')
#         plt.xlim([min(voltage), max(voltage)])
#         #plt.ylim([-27.5, 0])
#         plt.axvline(x=eye_vmin, color='r', label='Min.Request Eye Voltage')
#         plt.axvline(x=eye_vmax, color='r', label='Max. Requested Eye Voltage')
#         plt.xlabel("Voltage [V]", fontsize=14)
#         plt.ylabel('Transmission [dBm]', fontsize=14)
#         plt.xticks(fontsize=14)
#         plt.yticks(fontsize=14)
#         plt.title("Non-Linearity Visualization (Case 1)", fontsize=14)
#         for ii in range(len(voltage_levels)):
#             plt.scatter(voltage_levels[ii], shift_levels[ii], color='k')
#
#
#         for ii in range(len(shift_levels)):
#             if ii == 0:
#                 plt.axhline(y=shift_levels[ii], color='k', linestyle='dashed',
#                             label='Equidistant Transmission Levels')
#             else:
#                 plt.axhline(y=shift_levels[ii], color='k', linestyle='dashed',
#                             label='_nolegend_')
#         plt.legend(loc='lower right')
#         plt.savefig('case1.svg')
#
#
#         plt.figure()
#         laser_nm = laser/1e-6
#         wavelength_nm=wavelength/1e-6
#         for ii in range(len(T)):
#             plt.plot(wavelength_nm, T[ii, :], label='_nolegend_')
#         plt.axvline(x=laser_nm, color='r', label='Laser Wavelength')
#         xrange = 0.00025
#         plt.xlim([laser_nm-xrange/2, laser_nm+xrange/2])
#         plt.ylim([-40, 0])
#         plt.xticks(fontsize=14)
#         plt.yticks(fontsize=14)
#         plt.title("Transmission Shifts (Case 2)", fontsize=14)
#         plt.xlabel('Wavelength [um]', fontsize=14)
#         plt.ylabel("Transmission [dBm]", fontsize=14)
#         plt.legend(loc = 'lower right')
#         plt.savefig('case2_laser.svg')
# =============================================================================
# =============================================================================

    return [V0, V1, V2, V3]
