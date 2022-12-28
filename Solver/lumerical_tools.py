"""
Created on Wed Jul 21 11:27:18 2021.

This script contains all the LumAPI communication functions to execute all the required simulations.

@author: AlexTofini
"""

# Import dependenciess
import sys
import os
import platform
import numpy as np


# Saving current working directory
cwd = os.getcwd()

# Searching for Lumerical API location
if platform.system() == 'Windows':
    # try:
    lumapi_path = 'C:/Program Files/Lumerical/v212/api/python'
    os.chdir(lumapi_path)
    import lumapi

else:
    lumapi_path = '/CMC/tools/lumerical/v211/api/python'
    os.chdir(lumapi_path)
    temp = os.getcwd()
    print("Searching for lumapi in the following directory: "+temp)
    import lumapi

dir_path = os.path.dirname(os.path.realpath(__file__))
if os.path.exists(os.path.join(lumapi_path, 'lumapi.py')):
    print('Found lumapi path at' + ': ' + lumapi_path)
    sys.path.append(lumapi_path)
else:
    print('lumapi path does not exist, edit lumapi_path variable')

# Returning to original directory
os.chdir(cwd)
# %%  Simulation methods


def run_FDTD(parameters, simulation_setup, close=True, **kwargs):
    """
    Execute FDTD simulation to create coupling region and simulate coupling efficiency.

    Parameters
    ----------
    parameters : class
        Physical parameter class containing relevant about the physical parameters of the ring.
    simulation_setup : class
        Simulation class containing relevant information about the simulation settings.
    close : bool, optional
        Boolean to control if simulation closes after execution. The default is True.
    **kwargs : args
        key 1 (list0) : Lis of gaps used in critical coupling automation sweep.

    Returns
    -------
    f : list
        Frequency result of coupling result.
    CC : list
        Power coupling component of coupling result.
    """
    # Optional arguement that controls wether the parameter class object is used to build the device
    # or if a gap override is used as a sweep parameter
    gap = kwargs.get('gap', None)
    if gap is not None:
        sweep = True
    else:
        sweep = False

    # Saving current working directory
    cwd = os.getcwd()

    # Opening blank FDTD simulation
    print('Current Directory Before Openning' + ': ' + cwd)
    fdtd = lumapi.open('fdtd')

    # Loading .FSP file containing model for coupling region
    print('Current Directory After Openning' + ': ' + cwd)
    filename = 'DirectionalCoupler.fsp'

    # Changing back to initial directory
    lumapi.evalScript(fdtd, "cd('%s');"
                      % (cwd))

    if sweep:
        # If critical coupling sweep is being done use gap override
        lumapi.evalScript(fdtd, ("load('%s'); setnamed('::model','gap',%s); "
                                 "setnamed('::model','radius',%s); "
                                 "setnamed('::model','coupling_length',%s);")
                          % (filename, gap,  parameters.radius, parameters.coupling_length))
    if not sweep:
        # If critical coupling sweep is not being done use gap in the parameter class
        lumapi.evalScript(fdtd, ("load('%s'); setnamed('::model','gap',%s); "
                                 "setnamed('::model','radius',%s); "
                                 "setnamed('::model','coupling_length',%s);")
                          % (filename, parameters.gap,  parameters.radius,
                             parameters.coupling_length))

    # Pass waveguide parameters to simulation
    lumapi.evalScript(fdtd, ("setnamed('::model','wg_width',%s); "
                             "setnamed('::model','wg_height',%s); "
                             "setnamed('::model','slab_height',%s);")
                      % (parameters.wg_width, parameters.wg_height, parameters.slab_height))

    # Due to how lumerical handles the port object I manually set it via the console for simplicity
    command = ("switchtolayout; setglobalsource('wavelength start', %s); "
               "setglobalsource('wavelength stop', %s);")
    lumapi.evalScript(fdtd, command
                      % (simulation_setup.lambda_start, simulation_setup.lambda_end))

    # Running analysis script to extract results from monitors
    lumapi.evalScript(fdtd, 'ExtractCouplingCoefficient;')

    # Exporting results from FDTD
    f = lumapi.getVar(fdtd, 'f')
    CC = lumapi.getVar(fdtd, 'power_coupling')

    # Converting result arrays to lists
    f = f.tolist()
    CC = CC.tolist()

    # Cleaning up lists
    for ii in range(len(f)):
        f[ii] = f[ii][0]
        CC[ii] = CC[ii][0]

    # Closing FDTD simulation if close is True
    if close:
        lumapi.close(fdtd)

    return f, CC


def run_active_bent_wg(parameters, simulation_setup, charge_setup, waveguide_ID, close=True):
    """
    Run MODE simulation to extract Mode profile in form of .LDF and run voltage sweep.

    Parameters
    ----------
    parameters : class
        Physical parameter class containing relevant about the physical parameters of the ring.
    simulation_setup : class
        Simulation class containing relevant information about the simulation settings.
        DESCRIPTION.
    charge_setup : class
        Charge class containing relevant information about the CHARGE simulation.
    waveguide_ID : int
        Integer ID used to differentiate between records in the waveguide table.
    close : bool, optional
        Boolean to control if simulation closes after execution. The default is True.

    Returns
    -------
    voltage_cleaned : list
        List of voltages from the change in effective index voltage sweep.
    dneff_real_cleaned : list
        List of real components of dNeff from the change in effective index voltage sweep.
    dneff_imag_cleaned : list
        List of imaginary components of dNeff from the change in effective index voltage sweep.
    loss_cleaned : list
        List of losses from the change in effective index voltage sweep.

    """
    # Saving current working directory
    cwd = os.getcwd()
    print('Current Directory Before Openning' + ': ' + cwd)

    # Loading blank MODE simulation
    mode = lumapi.open('mode')
    print('Current Directory After Openning' + ': ' + cwd)

    # Chaning directory back to starting location
    lumapi.evalScript(mode, "cd('%s');"
                      % (cwd))
    # Defining waveguide model name to load
    filename = 'Waveguide.lms'

    # Loading waveguide model
    lumapi.evalScript(mode, "load('%s'); "
                      % (filename))

    # Defining physical parameters
    command = "wg_height = %s; wg_width = %s; Radius = %s; slab_height = %s; Coupling_Length = %s;"
    lumapi.evalScript(mode, command
                      % (parameters.wg_height, parameters.wg_width, parameters.radius,
                         parameters.slab_height, parameters.coupling_length))

    # Defining simulation paramters
    command = "Band = '%s'; Waveguide_ID = '%s';"
    lumapi.evalScript(mode, command
                      % (simulation_setup.Band, waveguide_ID))

    # Passing CHARGE data to waveguide model
    command = ("CHARGE_filename = '%s'; V_start = %s; V_stop = %s; N = %s; p_width_slab = %s; "
               "n_width_slab = %s; pp_width = %s; np_width = %s; ppp_width =%s; npp_width = %s; "
               "bias = '%s';")
    lumapi.evalScript(mode, command
                      % (charge_setup.CHARGE_file, charge_setup.vmin,
                         charge_setup.vmax, charge_setup.charge_datapoints,
                         charge_setup.p_width_slab, charge_setup.n_width_slab,
                         charge_setup.pp_width, charge_setup.np_width,
                         charge_setup.ppp_width, charge_setup.npp_width,
                         charge_setup.bias))

    # Loading analysis script
    lumapi.evalScript(mode, 'ActiveBentWaveguide;')

    # Extracting data from completed simulation
    voltage = lumapi.getVar(mode, 'V')
    dneff_real = lumapi.getVar(mode, 'dneff_real')
    dneff_imag = lumapi.getVar(mode, 'dneff_imag')
    phase = lumapi.getVar(mode, 'phase')
    loss = lumapi.getVar(mode, 'loss')

    # Initializing new areas for cleaned up data
    dneff_real_cleaned = []
    dneff_imag_cleaned = []
    voltage_cleaned = []
    phase_cleaned = []
    loss_cleaned = []

    # Cleaning data
    for ii in range(len(dneff_real)):
        voltage_cleaned.append(voltage[ii][0])
        dneff_real_cleaned.append(dneff_real[ii][0])
        dneff_imag_cleaned.append(dneff_imag[ii][0])
        phase_cleaned.append(phase[ii][0])
        loss_cleaned.append(loss[ii][0])

    # Closing simulation if close is True
    if close:
        lumapi.close(mode)

    return [voltage_cleaned, dneff_real_cleaned, dneff_imag_cleaned, phase_cleaned, loss_cleaned]


def run_charge(parameters, simulation_setup, charge_params, close=True):
    """
    Run CHARGE simulation to get .mat file corresponding to PN junction results.

    Parameters
    ----------
    parameters : class
        Physical parameter class containing relevant about the physical parameters of the ring.
    simulation_setup : class
        Simulation class containing relevant information about the simulation settings.
        DESCRIPTION.
    charge_setup : class
        Charge class containing relevant information about the CHARGE simulation.
    close : bool, optional
        Boolean to control if simulation closes after execution. The default is True.

    Returns
    -------
    capacitance_avg : list
        List containing averaged capacitance values v.s. voltage across ssac signal sweep
    resistance_avg : list
        List containing averaged resistance values v.s. voltage across ssac signal sweep
    bandwidth_avg : list
        List containing averaged bandwidth values v.s. voltage across ssac signal sweep

    """
    # Saving current working directory
    cwd = os.getcwd()
    print('Current Directory Before Openning' + ': ' + cwd)

    # Opening blank CHARGE simulation
    device = lumapi.open('device')
    print('Current Directory After Openning' + ': ' + cwd)

    # Returning to previous path in case it changed
    lumapi.evalScript(device, "cd('%s');"
                      % (cwd))

    # Passing doping dimensions to simulation
    command = ("p_width_core =%s; n_width_core =%s; p_width_slab =%s; n_width_slab =%s; "
               "pp_width = %s; np_width = %s; ppp_width = %s; npp_width = %s;")
    lumapi.evalScript(device, command
                      % (charge_params.p_width_core, charge_params.n_width_core,
                         charge_params.p_width_slab, charge_params.n_width_slab,
                         charge_params.pp_width, charge_params.np_width,
                         charge_params.ppp_width, charge_params.npp_width))

    # Passing in simulation parameters
    command = ("slab_height = %s; radius = %s; coupling_length = %s; band = '%s'; wg_height = %s; "
               "wg_width = %s;")
    lumapi.evalScript(device, command %
                      (parameters.slab_height, parameters.radius, parameters.coupling_length,
                       simulation_setup.Band, parameters.wg_height, parameters.wg_width))

    # Passing in charge settings
    command = "v_min = %s; v_max =%s; N =%s; bias = '%s'; save_name = '%s';"
    lumapi.evalScript(device, command
                      % (charge_params.vmin, charge_params.vmax, charge_params.charge_datapoints,
                         charge_params.bias, charge_params.save_name))

    # Select and use PN junction build script depending on foundry and PN type
    if charge_params.foundry == 'AMF':
        lumapi.evalScript(device, 'Build_Lateral_AMF;')
    elif charge_params.foundry == 'AIM':
        if charge_params.PN_type == 'Lateral':
            lumapi.evalScript(device, 'Build_Lateral_AIM;')
        elif charge_params.PN_type == 'L-Shaped':
            lumapi.evalScript(device, 'Build_LSHaped_AIM;')

    # Exporting results from FDTD
    capacitance_avg = lumapi.getVar(device, 'cap_avg')
    resistance_avg = lumapi.getVar(device, 'res_avg')
    bandwidth_avg = lumapi.getVar(device, 'bw_avg')

    # Converting result arrays to lists
    capacitance_avg = capacitance_avg.tolist()
    resistance_avg = resistance_avg.tolist()
    bandwidth_avg = bandwidth_avg.tolist()

    # Cleaning up lists

    capacitance_avg = capacitance_avg[0]
    resistance_avg = resistance_avg[0]
    bandwidth_avg = bandwidth_avg[0]

    # Close simualtion if close is True
    if close:
        lumapi.close(device)
    return capacitance_avg, resistance_avg, bandwidth_avg


def run_interconnect(parameters, simulation_setup, charge_setup,
                     saved_results, transmission_ID, close=True):
    """
    Run Interconnect simulation for ring transmission simulation.

    Parameters
    ----------
    parameters : class
        Physical parameter class containing relevant about the physical parameters of the ring.
    simulation_setup : class
        Simulation class containing relevant information about the simulation settings.
        DESCRIPTION.
    charge_setup : class
        Charge class containing relevant information about the CHARGE simulation.
    saved_results : class
        Result class containing relevant results from previous simulations.
    transmission_ID : int
        Integer ID used to differentiate records in transmission table.
    close : bool, optional
        Boolean to control if simulation closes after execution. The default is True.

    Returns
    -------
    None.

    """
    # Defining file names to load, these are created by the temporary file system
    coupler_file = 'coupler_' + str(saved_results.coupler_ID)
    waveguide_file = 'waveguide_' + str(saved_results.waveguide_ID)

    # Saving current working directory
    cwd = os.getcwd()
    print('Current Directory Before Openning' + ': ' + cwd)

    # Opening empty Interconnect simulation
    interc = lumapi.open('interconnect')
    print('Current Directory After Openning' + ': ' + cwd)

    # Changing back to previous path in case it changed.
    lumapi.evalScript(interc, "cd('%s');"
                      % (cwd))

    # Specifying filename to load, PAM4 is complicated so a model is used
    filename = 'TransmissionSpectrum.icp'

    # Loading model into simulation
    lumapi.evalScript(interc, "load('%s');"
                      % (filename))

    # Passing physical parameters to simulation
    command = "radius =%s; gap =%s; L = %s; slab_height = %s;"
    lumapi.evalScript(interc, command
                      % (parameters.radius, parameters.gap, parameters.coupling_length,
                         parameters.slab_height))

    # Passing loss parameters to simulation
    # First taking the difference between the 0 volt case and the rest
    voltage_dependent_loss = [0.0]
    for ii in range(len(saved_results.absorption_loss) - 1):
        voltage_dependent_loss.append(saved_results.absorption_loss[ii+1] -
                                      saved_results.absorption_loss[ii])

    command = "propagation_loss = %s; absorption_loss = %s;"
    lumapi.evalScript(interc, command
                      % (simulation_setup.propagation_loss, voltage_dependent_loss))

    # Passing voltage information to simulation
    command = "vmin = %s; vmax = %s; N = %s;"
    lumapi.evalScript(interc, command
                      % (charge_setup.vmin, charge_setup.vmax, charge_setup.charge_datapoints))

    # Passing file names to simulation
    command = "waveguide_file = '%s'; coupler_file = '%s';"
    lumapi.evalScript(interc, command
                      % (waveguide_file, coupler_file))

    # Passing wavelength and transmission file ID to simulation
    command = "start_wavelength = %s; stop_wavelength =%s; transmission_ID = %s;"
    lumapi.evalScript(interc, command
                      % (simulation_setup.lambda_start, simulation_setup.lambda_end,
                         transmission_ID))
    # Running ring building script and executing transmission sweep
    # lumapi.evalScript(interc, 'Transmission;')
    lumapi.evalScript(interc, 'SimulateSpectrum;')

    # Closing simulation if close is True
    if close:
        lumapi.close(interc)
    return


def run_interconnect_EYE_NRZ(parameters, simulation_setup, saved_results, eye_ID, close=True):
    """
    Execute NRZ eye diagram.

    Parameters
    ----------
    parameters : class
        Physical parameter class containing relevant about the physical parameters of the ring.
    simulation_setup : class
        Simulation class containing relevant information about the simulation settings.
    saved_results : class
        Result class containing relevant results from previous simulations.
    eye_ID : int
        Integer ID used to differentiate the data in the eye data table.
    close : bool, optional
        Boolean to control if simulation closes after execution. The default is True.

    Returns
    -------
    None.

    """
    # Defining file names to load, these are created by the temporary file system
    coupler_file = 'coupler_' + str(saved_results.coupler_ID)
    waveguide_file = 'waveguide_' + str(saved_results.waveguide_ID)

    # Saving current working directory
    cwd = os.getcwd()
    print('Current Directory Before Openning' + ': ' + cwd)

    # Opening empty Interconnect simulation
    interc = lumapi.open('interconnect')
    print('Current Directory After Openning' + ': ' + cwd)

    # Changing back to previous path in case it changed.
    lumapi.evalScript(interc, "cd('%s');"
                      % (cwd))

    # This command used to state automation is being used, this is for debugging the script
    command = "Running_Script = %s;"
    lumapi.evalScript(interc, command
                      % (1))

    # Passing in simulation parameters
    command = ("radius =%s; L = %s;  Eye_Data_ID = %s; propagation_loss = %s; "
               "start_wavelength = %s; stop_wavelength =%s; bitrate = %s; "
               "Vmin = %s; Vmax =%s; laser_lambda =%s;")
    lumapi.evalScript(interc, command
                      % (parameters.radius, parameters.coupling_length, eye_ID,
                         simulation_setup.propagation_loss, simulation_setup.lambda_start,
                         simulation_setup.lambda_end, simulation_setup.bitrate,
                         simulation_setup.eye_vmin, simulation_setup.eye_vmax,
                         simulation_setup.laser_wavl))

    # Passing wavelength and transmission file ID to simulationi
    command = "waveguide_file = '%s'; coupler_file = '%s';"
    lumapi.evalScript(interc, command
                      % (waveguide_file, coupler_file))

    # Executing NRZ eye diagram building script and running simulation
    lumapi.evalScript(interc, 'NRZ_Eye_Analysis;')

    # Closing simulation if close is True
    if close:
        lumapi.close(interc)
    return


def run_interconnect_EYE_PAM4(parameters, simulation_setup, saved_results, eye_ID, close=True):
    """
    Execute PAM4 eye diagram.

    Parameters
    ----------
    parameters : class
        Physical parameter class containing relevant about the physical parameters of the ring.
    simulation_setup : class
        Simulation class containing relevant information about the simulation settings.
    saved_results : class
        Result class containing relevant results from previous simulations.
    eye_ID : int
        Integer ID used to differentiate the data in the eye data table.
    close : bool, optional
        Boolean to control if simulation closes after execution. The default is True.

    Returns
    -------
    None.

    """
    # Defining file names to load, these are created by the temporary file system
    coupler_file = 'coupler_' + str(saved_results.coupler_ID)
    waveguide_file = 'waveguide_' + str(saved_results.waveguide_ID)

    # Saving current working directory
    cwd = os.getcwd()
    print('Current Directory Before Openning' + ': ' + cwd)

    # Opening empty Interconnect simulationi
    interc = lumapi.open('interconnect')
    print('Current Directory After Openning' + ': ' + cwd)

    # Changing back to previous path in case it changed.
    lumapi.evalScript(interc, "cd('%s');"
                      % (cwd))

    # Specifying filename to load, PAM4 is complicated so a model is used
    filename = 'PAM4_Eye_Diagram.icp'

    # This command used to state automation is being used, this is for debugging the script
    command = "Running_Script = %s;"
    lumapi.evalScript(interc, command
                      % (1))

    # Loading model into simulation
    lumapi.evalScript(interc, "load('%s');"
                      % (filename))

    # Passing in simulation parameters
    command = ("radius =%s; L = %s;  Eye_Data_ID = %s; propagation_loss = %s; "
               "start_wavelength = %s; stop_wavelength =%s; bitrate = %s;")
    lumapi.evalScript(interc, command
                      % (parameters.radius, parameters.coupling_length,
                         eye_ID,  simulation_setup.propagation_loss, simulation_setup.lambda_start,
                         simulation_setup.lambda_end, simulation_setup.bitrate))

    # Passing in voltage levels for PAM4
    if simulation_setup.staticNonLinCorrec == 'yes':
        v_space = np.array(saved_results.NonLinVoltages)
    else:
        v_space = np.linspace(simulation_setup.eye_vmin, simulation_setup.eye_vmax, 4)
    command = "V0 = %s; V1 =%s; V2 = %s; V3 =%s; laser_lambda =%s; "
    lumapi.evalScript(interc, command
                      % (v_space[0], v_space[1],
                         v_space[2], v_space[3],
                         simulation_setup.laser_wavl))

    # Pasing in filenames for temporary data loading
    command = "waveguide_file = '%s'; coupler_file = '%s';"
    lumapi.evalScript(interc, command
                      % (waveguide_file, coupler_file))

    # Executing anysis script
    lumapi.evalScript(interc, 'PAM4_Eye_Analysis;')

    # Closing simulation if close is True
    if close:
        lumapi.close(interc)
    return
