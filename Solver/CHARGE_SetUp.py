"""
Created on Mon Sep 26 16:37:28 2022.

This scrip sets up the CHARGE simulation for the PN junction simulations

@author: AlexTofini
"""
# Import dependencies
import lumerical_tools
import os
import ConnectToDatabase as database


def simulateForAMF(parameters, simulation_setup, charge_setup):
    """
    Simulate PN junction for the AMF foundry.

    Parameters
    ----------
    parameters : class
        Physical parameter class containing relevant about the physical parameters of the ring.
    simulation_setup : class
        Simulation class containing relevant information about the simulation settings.
    charge_setup : class
        Charge class containing relevant information about the CHARGE simulation.

    Returns
    -------
    filename : str
        Filename associated with .mat result file.
    SimRun : bool
        Boolean stating if simulation succesfully executed.

    """
    # Query AMF CHARGE table for matching record
    result = database.QueryChargeSims(charge_setup.PN_type, parameters.slab_height,
                                      parameters.radius, parameters.coupling_length,
                                      charge_setup.p_width_core, charge_setup.n_width_core,
                                      charge_setup.p_width_slab, charge_setup.n_width_slab,
                                      charge_setup.pp_width, charge_setup.np_width,
                                      charge_setup.ppp_width, charge_setup.npp_width,
                                      charge_setup.vmin, charge_setup.vmax, charge_setup.bias,
                                      simulation_setup.Band, charge_setup.foundry)
    if result != []:
        # If matching record exists, use the results
        print("Database contains a record for current PN Junction")
        # Recording the previously user-specified filename
        filename = result[0][13]
        capacitance_avg = result[0][19]
        resistance_avg = result[0][20]
        bandwidth_avg = result[0][21]
        SimRun = False
    else:
        # If no matching record exists, use LumAPI to create the CHARGE simulation
        print("Database does not contains a record for current PN Junction")

        # Execute simulation using LumAPI
        capacitance_avg, resistance_avg, bandwidth_avg = lumerical_tools.run_charge(
            parameters, simulation_setup, charge_setup)

        # Determine next identification ID in the table to save the new record to
        nextID = database.FindNextIndex('Charge_AMF')

        # Execute append querry to save new record
        database.WriteChargeSims(nextID, charge_setup.PN_type, parameters.slab_height,
                                 parameters.radius, parameters.coupling_length,
                                 charge_setup.p_width_core, charge_setup.n_width_core,
                                 charge_setup.p_width_slab, charge_setup.n_width_slab,
                                 charge_setup.pp_width, charge_setup.np_width,
                                 charge_setup.ppp_width, charge_setup.npp_width,
                                 charge_setup.save_name, charge_setup.vmin,
                                 charge_setup.vmax, charge_setup.charge_datapoints,
                                 charge_setup.bias, simulation_setup.Band,
                                 charge_setup.foundry, capacitance_avg, resistance_avg,
                                 bandwidth_avg)

        # Cleaning up charge database temporary save files
        cwd = os.getcwd()
        if os.path.exists(cwd + "\\Database\\Charge_AMF\\ChargeSim.ldev"):
            os.remove(cwd + "\\Database\\Charge_AMF\\ChargeSim.ldev")
        if os.path.exists(cwd + "\\Database\\Charge_AMF\\ChargeSim_p0.log"):
            os.remove(cwd + "\\Database\\Charge_AMF\\ChargeSim_p0.log")

        # User specified the file name
        filename = charge_setup.save_name
        SimRun = True

    return filename, SimRun


def simulateForAIM(parameters, simulation_setup, charge_setup):
    """
    Simulate PN junction for the AIM foundry.

    Parameters
    ----------
    parameters : class
        Physical parameter class containing relevant about the physical parameters of the ring.
    simulation_setup : class
        Simulation class containing relevant information about the simulation settings.
    charge_setup : class
        Charge class containing relevant information about the CHARGE simulation.

    Returns
    -------
    filename : str
        Filename associated with .mat result file.
    SimRun : bool
        Boolean stating if simulation succesfully executed.

    """
    # Query AIM CHARGE table for matching record
    result = database.QueryChargeSims(charge_setup.PN_type, parameters.slab_height,
                                      parameters.radius, parameters.coupling_length,
                                      charge_setup.p_width_core, charge_setup.n_width_core,
                                      charge_setup.p_width_slab, charge_setup.n_width_slab,
                                      charge_setup.pp_width, charge_setup.np_width,
                                      charge_setup.ppp_width, charge_setup.npp_width,
                                      charge_setup.vmin, charge_setup.vmax, charge_setup.bias,
                                      simulation_setup.Band, charge_setup.foundry)
    if result != []:
        # If matching record exists, use the results
        print("Database contains a record for current PN Junction")
        # Recording the previously user-specified filename
        filename = result[0][13]
        SimRun = False
    else:
        # If no matching record exists, use LumAPI to create the CHARGE simulation
        print("Database does not contains a record for current PN Junction")

        # Execute simulation using LumAPI
        capacitance_avg, resistance_avg, bandwidth_avg = lumerical_tools.run_charge(
            parameters, simulation_setup, charge_setup)

        # Determine next identification ID in the table to save the new record to
        nextID = database.FindNextIndex('Charge_AIM')

        # Execute append querry to save new record
        database.WriteChargeSims(nextID, charge_setup.PN_type, parameters.slab_height,
                                 parameters.radius, parameters.coupling_length,
                                 charge_setup.p_width_core, charge_setup.n_width_core,
                                 charge_setup.p_width_slab, charge_setup.n_width_slab,
                                 charge_setup.pp_width, charge_setup.np_width,
                                 charge_setup.ppp_width, charge_setup.npp_width,
                                 charge_setup.save_name, charge_setup.vmin,
                                 charge_setup.vmax, charge_setup.charge_datapoints,
                                 charge_setup.bias, simulation_setup.Band,
                                 charge_setup.foundry, capacitance_avg, resistance_avg,
                                 bandwidth_avg)
        # Cleaning up charge database temporary save files
        cwd = os.getcwd()
        if os.path.exists(cwd + "\\Database\\Charge_AIM\\ChargeSim.ldev"):
            os.remove(cwd + "\\Database\\Charge_AIM\\ChargeSim.ldev")
        if os.path.exists(cwd + "\\Database\\Charge_AIM\\ChargeSim_p0.log"):
            os.remove(cwd + "\\Database\\Charge_AIM\\ChargeSim_p0.log")

        # User specified the file name
        filename = charge_setup.save_name
        SimRun = True

    return filename, SimRun


def simulateLShaped(parameters, simulation_setup, charge_setup):
    """
    Execute simulation proceedure for L-Shaped PN junction.

    Parameters
    ----------
    parameters : class
        Physical parameter class containing relevant about the physical parameters of the ring.
    simulation_setup : class
        Simulation class containing relevant information about the simulation settings.
    charge_setup : class
        Charge class containing relevant information about the CHARGE simulation.

    Returns
    -------
    filename : str
        Filename associated with .mat result file.
    SimRun : bool
        Boolean stating if simulation succesfully executed.

    """
    # Only AIM has the capability of L-Shaped so only 1 option here
    filename, SimRun = simulateForAIM(
        parameters, simulation_setup, charge_setup)
    return filename, SimRun


def simulateLateral(parameters, simulation_setup, charge_setup):
    """
    Execute simulation procedure for Lateral PN junction.

    Parameters
    ----------
    parameters : class
        Physical parameter class containing relevant about the physical parameters of the ring.
    simulation_setup : class
        Simulation class containing relevant information about the simulation settings.
    charge_setup : class
        Charge class containing relevant information about the CHARGE simulation.

    Returns
    -------
    filename : str
        Filename associated with .mat result file.
    SimRun : bool
        Boolean stating if simulation succesfully executed.

    """
    # Call different simulation scripts depending on foundry
    if charge_setup.foundry == 'AMF':
        filename, SimRun = simulateForAMF(
            parameters, simulation_setup, charge_setup)
    elif charge_setup.foundry == 'AIM':
        filename, SimRun = simulateForAIM(
            parameters, simulation_setup, charge_setup)
    return filename, SimRun
