"""
Created on Wed Jul 21 11:27:18 2021.

This script sets up the MODE simulation for the waveguide simulations

@author: AlexTofini
"""
# Import dependencies
import lumerical_tools
import ConnectToDatabase as database


def Active_Bent_Waveguide(parameters, simulation_setup, charge_setup):
    """
    Set up the MODE simulation pipeline in order to extract the mode profile in the form of a .LDF.

    Also run a voltage sweep to extract the change in effective index versus voltage

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
    dNeff : list
        2D list containing voltage, real dNeff, and imaginary dNeff components of waveguide data.
        Index 0 : voltage
        Index 1 : real dNeff
        Index 2 : imaginary dNeff
    absorption_loss_0Volt : float
        Absorption loss at 0 applied volts.
    waveguide_ID : int
        Integer ID used to differentiate different records in waveguide table.

    """
    # Determing CHARGE ID used to querry waveguide table
    charge_ID = database.FindChargeID(charge_setup.CHARGE_file,
                                      charge_setup.foundry)
    charge_ID = charge_ID[0][0]

    # Query waveguide table for matching record
    result = database.QueryWaveguides(simulation_setup.Band, charge_ID, charge_setup.foundry)
    if result != []:
        # If a matching record is found, parse the string array into useable values
        print("Database contains a waveguide record for current ring parameters")
        waveguide_ID = result[0][0]
        voltage = database.ParseStringArray(result[0][4])
        dneff_real = database.ParseStringArray(result[0][5])
        dneff_imag = database.ParseStringArray(result[0][6])
        absorption_losses = database.ParseStringArray(result[0][7])
        phase = database.ParseStringArray(result[0][8])
    else:
        # If no matching records are found, run simulation using LumAPI
        print("Datase does not contain a waveguide record for the current ring parameters")
        print("Executing FDTD simulation")
        nextID = database.FindNextIndex('Waveguide')

        # Call MODE simulation with LumAPI
        [voltage, dneff_real, dneff_imag,
         phase, absorption_losses] = lumerical_tools.run_active_bent_wg(
            parameters, simulation_setup, charge_setup, nextID)

        # Executing append query to save new record
        database.WriteToWaveguides(nextID, charge_ID, voltage, dneff_real, dneff_imag,
                                   absorption_losses, phase, charge_setup.foundry)
        waveguide_ID = nextID

    dNeff = [voltage, dneff_real, dneff_imag]
    phase_shift = [voltage, phase]
    return dNeff, absorption_losses, phase_shift, waveguide_ID
