"""
Created on Wed Jul 21 11:23:33 2021.

This script sets up the FDTD simulation for the ring coupling region

@author: AlexTofini
"""

# Import dependencies
import lumerical_tools
import ConnectToDatabase as database


def calculate_coupling_coefficient(parameters, simulation_setup, **kwargs):
    """
    Set up the FDTD simulation pipeline in order to extract the coupling coefficient vs wavelength.

    Parameters
    ----------
    parameters : class
        Physical parameter class containing relevant about the physical parameters of the ring.
    simulation_setup : class
        Simulation class containing relevant information about the simulation settings.
    **kwargs : args
        key 1 (list0) : Lis of gaps used in critical coupling automation sweep.

    Returns
    -------
    Coupling_Coefficients : list
        List containing the coupling coefficient result.
        Index 0 : frequency component
        Index 1 : Coupling componennt
    coupler_ID : int
        Integer ID used to differentiate records in the coupler table.

    """
    # Optional arguement that controls wether the parameter class object is used to build the device
    # or if a gap override is used as a sweep parameter
    gap = kwargs.get('gap', None)
    if gap is not None:
        sweep = True
    else:
        sweep = False

    # Searching for exact file match to start prcoess
    if sweep:
        # Gap override is passed from sweep function
        result = database.QueryCouplers(parameters.radius, gap,
                                        parameters.coupling_length, parameters.slab_height,
                                        simulation_setup.Band)

        if result != []:
            # If matching record exists in the database, use that data
            print("Database contains a coupling record for current ring parameters")
            coupler_ID = result[0][0]
            f = database.ParseStringArray(result[0][7])
            CC = database.ParseStringArray(result[0][8])
        else:
            # If no matching record exists in the database, build the FDTD simulation
            print("Datase does not contain a coupling record for the current ring parameters")
            print("Executing FDTD simulation")

            # Call LumAPI to build FDTD simulation
            f, CC = lumerical_tools.run_FDTD(parameters, simulation_setup, gap=gap)

            # Determine the next ID in the coupler table for saving
            nextID = database.FindNextIndex('Coupler')

            # Now executing append query to  save the data
            database.WriteToCouplers(nextID, parameters.radius, gap,
                                     parameters.coupling_length, parameters.slab_height,
                                     simulation_setup.Band, f, CC)
            coupler_ID = nextID

    if not sweep:
        # No gap override present so using parameter class object to build entire coupler
        result = database.QueryCouplers(parameters.radius, parameters.gap,
                                        parameters.coupling_length, parameters.slab_height,
                                        simulation_setup.Band, parameters.wg_height, 
                                        parameters.wg_width)
        if result != []:
            print("Database contains a coupling record for current ring parameters")
            coupler_ID = result[0][0]
            f = database.ParseStringArray(result[0][7])
            CC = database.ParseStringArray(result[0][8])
        else:
            print("Datase does not contain a coupling record for the current ring parameters")
            print("Executing FDTD simulation")
            f, CC = lumerical_tools.run_FDTD(parameters, simulation_setup)

            nextID = database.FindNextIndex('Coupler')

            # Now executing append query to  save the data
            database.WriteToCouplers(nextID, parameters.radius, parameters.gap,
                                     parameters.coupling_length, parameters.slab_height,
                                     simulation_setup.Band, parameters.wg_height,
                                     parameters.wg_width, f, CC)
            coupler_ID = nextID

    # Combined results into list
    Coupling_Coefficients = [f, CC]

    return Coupling_Coefficients, coupler_ID
