"""
Created on Tue Sep 27 08:58:37 2022.

This script contains all the queries to connect to the SQL database, and has the integrity system

@author: AlexTofini
"""

# Importing relevant packages
import pyodbc
import os
import shutil

# Defining connection to database (This will have to be changed when hosted at UBC)
cnn_string = (
    r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Users\AlexTofini\Documents\GitHub\Ring-Modulator-Automation-GUI\Solver\Database'
    r'\Database.accdb '
)
cnn = pyodbc.connect(cnn_string)
cursor = cnn.cursor()


def QueryCouplers(radius, gap, coupling_length, slab_height, band, wg_height, wg_width):
    """
    Query coupler table for matching record.

    Parameters
    ----------
    radius : float
        Radius of ring.
    gap : float
        Gap used for ring.
    coupling_length : float
        Coupling length of ring.
    slab_height : float
        Slab height of waveguide.
    band : str
        Optical band
        Options : [CL, O].
    wg_height : float
        Height of waveguide
    wg_width : float
        Width of waveguide

    Returns
    -------
    result : list
        Query results from coupler table.

    """
    # Defining SQL command
    sql = (
        'SELECT [Coupler Table].*'
        'FROM [Coupler Table]'
        'WHERE ((([Coupler Table].Radius)=%s) AND (([Coupler Table].Gap)=%s) '
        'AND (([Coupler Table].Coupling_Length)=%s) AND (([Coupler Table].Slab_Height)=%s) '
        'AND (([Coupler Table].Optical_Band)=\'%s\') AND (([Coupler Table].Waveguide_Height)=%s) '
        'AND (([Coupler Table].Waveguide_Width)=%s));'
    ) % (radius, gap, coupling_length, slab_height, band, wg_height, wg_width)

    # Executing querry and fetching reults
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def WriteToCouplers(ID, radius, gap, coupling_length, slab_height, band, wg_height, wg_width,
                    f, CC):
    """
    Append query used to add record to coupler table.

    Parameters
    ----------
    ID : int
        Integer ID used to differentiate records in coupelr table.
    radius : float
        Radius of ring.
    gap : float
        Gap used for ring.
    coupling_length : float
        Coupling length of ring.
    slab_height : float
        Slab height of waveguide.
    band : str
        Optical band
        Options : [CL, O].
    wg_height : float
        Height of waveguide
    wg_width : float
        Width of waveguid
    f : list
        List containing frequency component of coupling coefficient simulation.
    CC : list
        Power coupling componeny of the coupling coefficient simulation.

    Returns
    -------
    None.

    """
    # Defining SQL command
    sql = (
        'INSERT INTO [Coupler Table] ( Coupler_ID, Radius, Gap, Coupling_Length, Slab_Height, '
        'Optical_Band, Waveguide_Height, Waveguide_Width, Frequency, Coupling_Coefficient )'
        'SELECT %s AS Expr1, %s AS Expr2, %s AS Expr3, %s AS Expr4, \'%s\' AS Expr5, '
        '\'%s\' AS Expr6, %s AS Expr7, %s AS Expr8, \'%s\' AS Expr9, \'%s\' AS Expr10;'
    ) % (ID, radius, gap, coupling_length, slab_height, band, wg_height, wg_width, f, CC)

    # Executing querry and commiting to table
    cursor.execute(sql)
    cursor.commit()
    return


def QueryWaveguides(band, charge_ID, foundry):
    """
    Query waveguide table for matching record.

    Parameters
    ----------
    charge_ID : int
        Integer ID used to link waveguide record with corresponding CHARGE record.
    foundry : str
        Foundry that the device is being simulated for.
        Options : [AMF, AIM]

    Returns
    -------
    result : list
        Query results from waveguide table.

    """
    # Defining SQL command depending on foundry
    if foundry == 'AMF':
        sql = (
            'SELECT [Waveguide Table].* '
            'FROM [Charge AMF Table] LEFT JOIN [Waveguide Table] ON '
            '[Charge AMF Table].Charge_ID = [Waveguide Table].Charge_ID_AMF '
            'WHERE (([Waveguide Table].Charge_ID_AMF)=%s); '
        ) % (charge_ID)
    elif foundry == 'AIM':
        sql = (
            'SELECT [Waveguide Table].* '
            'FROM [Charge AIM Table] LEFT JOIN [Waveguide Table] ON '
            '[Charge AIM Table].Charge_ID = [Waveguide Table].Charge_ID_AIM '
            'WHERE (([Waveguide Table].Charge_ID_AIM)=%s); '
        ) % (charge_ID)

    # Executing querry and fetching reults
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def WriteToWaveguides(ID, charge_ID, voltage,
                      dneff_real, dneff_imag, absorp_loss, phase, foundry):
    """
    Append query used to add record to waveguide table.

    Parameters
    ----------
    ID : int
        Integer ID used to differentiate records inside the waveguide table.
    charge_ID : int
        Integer ID used to link waveguide record with corresponding CHARGE record.
    voltage : list
        Voltage component of effective index versus voltage sweep result.
    dneff_real : list
        Real component of effective index versus voltage sweep result.
    dneff_imag : list
        Imaginary component of effective index versus voltage sweep result.
    absorp_loss : float
        Absorption loss versus voltage
    phase : float
        Phase shift versus voltage
    foundry : str
        Foundry that the device is being simulated for.
        Options : [AMF, AIM]

    Returns
    -------
    None.

    """
    # Defining waveguide filename based off integer ID
    waveguide_filename = 'Waveguide_' + str(ID)

    # Defining SQL command based of the foundry
    if foundry == 'AMF':
        sql = (
            'INSERT INTO [Waveguide Table] ( Waveguide_ID, '
            'Charge_ID_AMF, Charge_ID_AIM, Filename, Voltage, Real_Neff, Imag_Neff, '
            'Absorption_Loss, Phase )'
            'SELECT %s AS Expr1, %s AS Expr2, '
            '%s AS Expr3, \'%s\' AS Expr4, \'%s\' AS Expr5, \'%s\' AS Expr6, \'%s\' AS Expr7, '
            '\'%s\' AS Expr8, \'%s\' AS Expr9;'
        ) % (ID, charge_ID, 'Null', waveguide_filename, voltage,
             dneff_real, dneff_imag, absorp_loss, phase)
    elif foundry == 'AIM':
        sql = (
            'INSERT INTO [Waveguide Table] ( Waveguide_ID, '
            'Charge_ID_AMF, Charge_ID_AIM, Filename, Voltage, Real_Neff, Imag_Neff, '
            'Absorption_Loss, Phase )'
            'SELECT %s AS Expr1, %s AS Expr2, '
            '%s AS Expr3, \'%s\' AS Expr4, \'%s\' AS Expr5, \'%s\' AS Expr6, \'%s\' AS Expr7, '
            '\'%s\' AS Expr8, \'%s\' AS Expr9;'
        ) % (ID, 'Null', charge_ID, waveguide_filename, voltage,
             dneff_real, dneff_imag, absorp_loss, phase)

    # Executing querry and commiting results
    cursor.execute(sql)
    cursor.commit()

    return


def FindNextIndex(Table_name):
    """
    Find the next integer ID in the passed in table for appending.

    Parameters
    ----------
    Table_name : str
        Name of table to determine the next integer ID for the primary key.

    Returns
    -------
    nextID : TYPE
        DESCRIPTION.

    """
    # Creating list of options for table names and their corresponding field and table name syntax
    if Table_name == 'Eye_Data':
        field = 'Eye_Data_ID'
        table = 'Eye Data'
    elif Table_name == 'Charge_AMF':
        field = 'Charge_ID'
        table = 'Charge AMF Table'
    elif Table_name == 'Charge_AIM':
        field = 'Charge_ID'
        table = 'Charge AIM Table '
    else:
        field = Table_name + '_ID'
        table = Table_name + ' Table'

    # Defining SQL command
    sql = (
        'SELECT [%s].%s '
        'FROM [%s];'
    ) % (table, field, table)

    # Executing query and fetching results
    cursor.execute(sql)
    result = cursor.fetchall()

    # Initializing ID tracker
    max_ID = 0

    # If result is not empty, determine maximum ID. NextID is max +1
    if result != []:
        for ii in range(len(result)):
            if result[ii][0] > max_ID:
                max_ID = result[ii][0]
        nextID = max_ID + 1
    else:
        nextID = 1

    return nextID


def QueryChargeSims(PN_type, slab_height, wg_height, wg_width, radius, coupling_length,
                    p_width_core, n_width_core, p_width_slab, n_width_slab, pp_width,
                    np_width, ppp_width, npp_width, v_min, v_max, bias, band, foundry):
    """
    Query CHARGE tables for matching record.

    Parameters
    ----------
    PN_type : str
        Type of PN junction.
        Options : [Lateral, L-Shaped]
    slab_height : float
        Slab height.
    wg_height : float
        Height of waveguide
    wg_width : float
        Width of waveguide
    radius : float
        Radius of ring composing the PN junction.
    coupling_length : float
        Straight coupling region in ring if it is present.
    p_width_core : float
        Width of P doping type in waveguide core.
    n_width_core : float
        Width of N doping type in waveguide core.
    p_width_slab : float
        Width of P doping type in waveguide slab.
    n_width_slab : float
        Width of N doping type in waveguide slab.
    pp_width : float
        Width of P+ doping type in waveguide slab.
    np_width : float
        Width of N+ doping type in waveguide slab.
    ppp_width : float
        Width of P++ doping type in waveguide slab.
    npp_width : float
        Width of N++ doping type in waveguide slab.
    v_min : float
        Minimum voltage used in CHARGE simulation.
    v_max : float
        Maximum voltage used in CHARGE simulation.
    bias : str
        Voltage bias used in simualtion.
        Options : [Reverse, Forward]
    band : str
        Optical band.
        Options : [CL, O]
    foundry : str
        Foundry that the PN junction is created for.
        Options : [AMF, AIM]

    Returns
    -------
    result : TYPE
        Query results from CHARGE table.

    """
    # Defining SQL command based off foundry
    if foundry == 'AMF':
        sql = (
            'SELECT [Charge AMF Table].*'
            'FROM [Charge AMF Table]'
            'WHERE ((([Charge AMF Table].Type)=\'%s\') AND (([Charge AMF Table].Slab_Height)=%s) '
            'AND (([Charge AMF Table].Waveguide_Height)=%s) '
            'AND (([Charge AMF Table].Waveguide_Width)=%s) '
            'AND (([Charge AMF Table].Radius)=%s) AND (([Charge AMF Table].Coupling_Length)=%s) '
            'AND (([Charge AMF Table].P_Width_Core)=%s) AND (([Charge AMF Table].N_Width_Core)=%s) '
            'AND (([Charge AMF Table].P_Width_Slab)=%s) AND (([Charge AMF Table].N_Width_Slab)=%s) '
            'AND (([Charge AMF Table].[P+_Width])=%s) AND (([Charge AMF Table].[N+_Width])=%s) '
            'AND (([Charge AMF Table].[P++_Width])=%s) AND (([Charge AMF Table].[N++_Width])=%s) '
            'AND (([Charge AMF Table].Min_Voltage)=%s) AND (([Charge AMF Table].Max_Voltage)=%s) '
            'AND (([Charge AMF Table].Bias)=\'%s\') '
            'AND (([Charge AMF Table].Optical_Band)=\'%s\'));'
        ) % (PN_type, slab_height, wg_height, wg_width, radius, coupling_length, p_width_core,
             n_width_core, p_width_slab, n_width_slab, pp_width, np_width, ppp_width, npp_width,
             v_min, v_max, bias, band)
    elif foundry == 'AIM':
        sql = (
            'SELECT [Charge AIM Table].*'
            'FROM [Charge AIM Table]'
            'WHERE ((([Charge AIM Table].Type)=\'%s\') AND (([Charge AIM Table].Slab_Height)=%s) '
            'AND (([Charge AMF Table].Waveguide_Height)=%s) '
            'AND (([Charge AMF Table].Waveguide_Width)=%s) '
            'AND (([Charge AIM Table].Radius)=%s) AND (([Charge AIM Table].Coupling_Length)=%s) '
            'AND (([Charge AIM Table].P1Al_Width_Core)=%s) '
            'AND (([Charge AIM Table].N1Al_Width_Core)=%s) '
            'AND (([Charge AIM Table].P1Al_Width_Slab)=%s) '
            'AND (([Charge AIM Table].N1Al_Width_Slab)=%s) '
            'AND (([Charge AIM Table].P4Al_Width)=%s) '
            'AND (([Charge AIM Table].N3Al_Width)=%s) '
            'AND (([Charge AIM Table].P5Al_Width)=%s) '
            'AND (([Charge AIM Table].N5Al_Width)=%s) '
            'AND (([Charge AIM Table].Min_Voltage)=%s) '
            'AND (([Charge AIM Table].Max_Voltage)=%s) '
            'AND (([Charge AIM Table].Bias)=\'%s\') '
            'AND (([Charge AIM Table].Optical_Band)=\'%s\'));'
        ) % (PN_type, slab_height, wg_height, wg_width, radius, coupling_length, p_width_core,
             n_width_core, p_width_slab, n_width_slab, pp_width, np_width, ppp_width, npp_width,
             v_min, v_max, bias, band)

    # Executing query and fetching results
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def QueryChargeFile(charge_file, foundry):
    """
    Query CHARGE table for matching .mat filename.

    Parameters
    ----------
    charge_file : str
        Filename of a CHARGE record dataset.
    foundry : str
        Foundry that the PN junction is created for.
        Options : [AMF, AIM]

    Returns
    -------
    result : TYPE
        Query results from CHARGE table matching specified filename.

    """
    # Defining SQL command based off foundry
    if foundry == 'AMF':
        sql = (
            'SELECT [Charge AMF Table].*'
            'FROM [Charge AMF Table]'
            'WHERE ((([Charge AMF Table].Filename)=\'%s\'));'
        ) % (charge_file)
    elif foundry == 'AIM':
        sql = (
            'SELECT [Charge AIM Table].*'
            'FROM [Charge AIM Table]'
            'WHERE ((([Charge AIM Table].Filename)=\'%s\'));'
        ) % (charge_file)

    # Executing query and fetching results
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def WriteChargeSims(ID, PN_type, slab_height, wg_height, wg_width, radius, coupling_length,
                    p_width_core, n_width_core, p_width_slab, n_width_slab, pp_width, np_width,
                    ppp_width, npp_width, save_name, v_min, v_max, N, bias, band, foundry,
                    capacitance, resistance, bandwidth):
    """
    Append query used to add a record to the CHARGE tables.

    Parameters
    ----------
    ID : int
        Integer ID used to differentiate records in CHARGE table.
    PN_type : str
        Type of PN junction.
        Options : [Lateral, L-Shaped]
    slab_height : float
        Slab height.
    wg_height : float
        Height of waveguide
    wg_width : float
        Width of waveguide
    radius : float
        Radius of ring composing the PN junction.
    coupling_length : float
        Straight coupling region in ring if it is present.
    p_width_core : float
        Width of P doping type in waveguide core.
    n_width_core : float
        Width of N doping type in waveguide core.
    p_width_slab : float
        Width of P doping type in waveguide slab.
    n_width_slab : float
        Width of N doping type in waveguide slab.
    pp_width : float
        Width of P+ doping type in waveguide slab.
    np_width : float
        Width of N+ doping type in waveguide slab.
    ppp_width : float
        Width of P++ doping type in waveguide slab.
    npp_width : float
        Width of N++ doping type in waveguide slab.
    save_name : str
        Filename associated with CHARGE simulation results.
    v_min : float
        Minimum voltage used in CHARGE simulation.
    v_max : float
        Maximum voltage used in CHARGE simulation.
    N : int
        Number of voltage steps used in CHARGE simulation.
    bias : str
        Voltage bias used in simualtion.
        Options : [Reverse, Forward]
    band : str
        Optical band.
        Options : [CL, O]
    foundry : str
        Foundry that the PN junction is created for.
        Options : [AMF, AIM]
    capacitance_avg : list
        List containing averaged capacitance values v.s. voltage across ssac signal sweep
    resistance_avg : list
        List containing averaged resistance values v.s. voltage across ssac signal sweep
    bandwidth_avg : list
        List containing averaged bandwidth values v.s. voltage across ssac signal sweep

    Returns
    -------
    None.

    """
    if foundry == 'AMF':
        sql = (
            'INSERT INTO [Charge AMF Table] ( Charge_ID, Type, Slab_Height, Waveguide_Height, '
            'Waveguide_Width, Radius, '
            'Coupling_Length, P_Width_Core, N_Width_Core, P_Width_Slab, N_Width_Slab, '
            '[P+_Width], [N+_Width], [P++_Width], [N++_Width], Filename, Min_Voltage, Max_Voltage, '
            'N, Bias, Optical_Band, Capacitance, Resistance, Bandwidth )'
            'SELECT %s AS Expr1, \'%s\' AS Expr2, %s AS Expr3, %s AS Expr4, %s AS Expr5, '
            '%s AS Expr6, %s AS Expr7, '
            '%s AS Expr8, %s AS Expr9, %s AS Expr10, %s AS Expr11, %s AS Expr12, %s AS Expr13, '
            '%s AS Expr14, %s AS Expr15, \'%s\' AS Expr16, %s AS Expr17, %s AS Expr18, '
            '%s AS Expr19, \'%s\' AS Expr20, \'%s\' AS Expr21, \'%s\' AS Expr22, \'%s\' AS Expr23, '
            '\'%s\' AS Expr24;'
        ) % (ID, PN_type, slab_height, wg_height, wg_width, radius, coupling_length, p_width_core,
             n_width_core, p_width_slab, n_width_slab, pp_width, np_width, ppp_width,
             npp_width, save_name, v_min, v_max, N, bias, band, capacitance, resistance, bandwidth)
    elif foundry == 'AIM':
        sql = (
            'INSERT INTO [Charge AIM Table] ( Charge_ID, Type, Slab_Height, Waveguide_Height, '
            'Waveguide_Width, Radius, '
            'Coupling_Length, P1Al_Width_Core, N1Al_Width_Core, P1Al_Width_Slab, N1Al_Width_Slab, '
            'P4Al_Width, N3Al_Width, P5Al_Width, N5Al_Width, Filename, Min_Voltage, Max_Voltage, '
            'N, Bias, Optical_Band, Capacitance, Resistance, Bandwidth )'
            'SELECT %s AS Expr1, \'%s\' AS Expr2, %s AS Expr3, %s AS Expr4, %s AS Expr5, '
            '%s AS Expr6, %s AS Expr7, '
            '%s AS Expr8, %s AS Expr9, %s AS Expr10, %s AS Expr11, %s AS Expr12, %s AS Expr13, '
            '%s AS Expr14, %s AS Expr15, \'%s\' AS Expr16, %s AS Expr17, %s AS Expr18, '
            '%s AS Expr19, \'%s\' AS Expr20, \'%s\' AS Expr21, \'%s\' AS Expr22, \'%s\' AS Expr23, '
            '\'%s\' AS Expr24;'
        ) % (ID, PN_type, slab_height, wg_height, wg_width, radius, coupling_length, p_width_core,
             n_width_core, p_width_slab, n_width_slab, pp_width, np_width, ppp_width,
             npp_width, save_name, v_min, v_max, N, bias, band, capacitance, resistance, bandwidth)
    cursor.execute(sql)
    cursor.commit()
    return


def QueryTransmission(waveguide_ID, coupler_ID, prop_loss):
    """
    Query transmission table for matching record.

    Parameters
    ----------
    waveguide_ID : int
        Integer ID of waveguide table data used in simulation.
    coupler_ID : int
        Integer ID of coupler table data used in simulation.
    prop_loss : float
        Propgation loss specified by the user.

    Returns
    -------
    result : TYPE
        Query results from transmission table.

    """
    sql = (
        'SELECT [Transmission Table].Transmission_ID, [Transmission Table].Filename '
        'FROM [Transmission Table] '
        'WHERE ((([Transmission Table].Waveguide_ID)=%s) '
        'AND (([Transmission Table].Coupler_ID)=%s) '
        'AND (([Transmission Table].Propagation_loss)=%s));'
    ) % (waveguide_ID, coupler_ID, prop_loss)

    # Executing query and fetching results
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def WriteTransmission(waveguide_ID, coupler_ID, transmission_ID, transmission_file, prop_loss,
                      resonances, FSRs, bandwidths_3dB, QFactors, InsertionLosses):
    """
    Append query used to add a record to the transmission table.

    Parameters
    ----------
    waveguide_ID : int
        Integer ID of waveguide table data used in simulation.
    coupler_ID : int
        Integer ID of coupler table data used in simulation.
    transmission_ID : int
        Integer ID of transmission data used to differentiate records.
    transmission_file : str
        Filename of transmission data based off transmission ID.
    prop_loss : float
        Propgation loss specified by the user.
    resonances : list
        List of resonances present in transmission spectra, units of nm
    FSRs : list
        List of the FSRs for each resonance in the spectrum, units of nm
    bandwidths_dB : list
        List of 3dB bandwidths associated with each resonance in the spectrum, units nm
    QFactors : list
        List of quality factors associated with each resonance in the spectrum
    InsertionLosses : list
        List of insertion losses assocaited with each resonance in the spectrum, units dBm

    Returns
    -------
    None.

    """
    sql = (
        'INSERT INTO [Transmission Table] (Waveguide_ID, Coupler_ID, Transmission_ID, Filename, '
        'Propagation_Loss, Resonances, FSRs, 3dB_Bandwidths, Q_Factors, Insertion_Losses ) '
        'SELECT %s AS Expr1, %s AS Expr2, %s AS Expr3, \'%s\' AS Expr4, %s AS Expr5, '
        '\'%s\' AS Expr6, \'%s\' AS Expr7, \'%s\' AS Expr8, \'%s\' AS Expr9, \'%s\' AS Expr10;'
    ) % (waveguide_ID, coupler_ID, transmission_ID, transmission_file, prop_loss, resonances, FSRs,
         bandwidths_3dB, QFactors, InsertionLosses)

    # Executing query and commiting results
    cursor.execute(sql)
    cursor.commit()
    return


def FindChargeID(charge_file, foundry):
    """
    Query CHARGE table for integer ID corresponding to passed in charge file.

    Parameters
    ----------
    charge_file : str
        Charge filename.
    foundry : str
        Foundry that the PN junction is created for.
        Options : [AMF, AIM]

    Returns
    -------
    result : list
        Query results from CHARGE table based off supplied charge filename.

    """
    # Defining filename based off supplied charge_file
    file = charge_file.split('\\')[-1]
    file = file.split('.')[0]

    # Defining SQL command based of foundry
    if foundry == 'AMF':
        sql = (
            'SELECT [Charge AMF Table].Charge_ID '
            'FROM [Charge AMF Table]'
            'WHERE ((([Charge AMF Table].Filename)=\'%s\'));'
        ) % (file)
    elif foundry == 'AIM':
        sql = (
            'SELECT [Charge AIM Table].Charge_ID '
            'FROM [Charge AIM Table]'
            'WHERE ((([Charge AIM Table].Filename)=\'%s\'));'
        ) % (file)

    # Executing query and fetching results
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def QueryEyeTable(waveguide_ID, coupler_ID, prop_loss):
    """
    Query eye table for matching record.

    Parameters
    ----------
    waveguide_ID : int
        Integer ID of waveguide table data used in simulation.
    coupler_ID : int
        Integer ID of coupler table data used in simulation.
    prop_loss : float
        Propgation loss specified by the user.

    Returns
    -------
    result : list
        Query results from eye table.

    """
    # Defining SQL command
    sql = (
        'SELECT [Eye Table].Eye_ID '
        'FROM [Eye Table] '
        'WHERE ((([Eye Table].Waveguide_ID)=%s) AND (([Eye Table].Coupler_ID)=%s) '
        'AND (([Eye Table].Propagation_Loss)=%s));'
    ) % (waveguide_ID, coupler_ID, prop_loss)

    # Executing query and fetching results
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def WriteToEyeTable(ID, waveguide_ID, coupler_ID, prop_loss):
    """
    Append query used to add a record to the eye table.

    Parameters
    ----------
    ID : int
        Integer ID used to differentiate records in the eye table.
    waveguide_ID : int
        Integer ID of waveguide table data used in simulation.
    coupler_ID : int
        Integer ID of coupler table data used in simulation.
    prop_loss : float
        Propgation loss specified by the user.

    Returns
    -------
    None.

    """
    # Defining SQL command
    sql = (
        'INSERT INTO [Eye Table] ( Eye_ID, Waveguide_ID, Coupler_ID, Propagation_Loss ) '
        'SELECT %s AS Expr1, %s AS Expr2, %s AS Expr3, %s AS Expr4;'
    ) % (ID, waveguide_ID, coupler_ID, prop_loss)

    # Executing query and fetching results
    cursor.execute(sql)
    cursor.commit()
    return


def QueryEyeData(eye_ID, laser_wavelength, vmin, vmax, bitrate, eye_type, SNLC):
    """
    Query eye data table for matching records associated with the eye table.

    Parameters
    ----------
    eye_ID : int
        Integer ID associated with matching data in eye table.
    laser_wavelength : float
        Operating laser wavelength used in eye diagram simulation.
    vmin : float
        Minimum modulation voltage used in eye diagram simulation.
    vmax : float
        Maximum modulation voltage used in eye diagram simulation.
    bitrate : float
        Bitrate used in eye diagram simulation.
    eye_type : str
        Eye diagram modulation type.
        Options : [NRZ, PAM4]
    SNLC : str
        Static non-linearity correction option.
        Options : [yes, no, N/A]

    Returns
    -------
    result : list
        Query results from eye data table.

    """
    # Defining SQL command
    sql = (
        'SELECT [Eye Data].* '
        'FROM [Eye Data] '
        'WHERE ((([Eye Data].Eye_ID)=%s) AND (([Eye Data].Laser_Wavelength)=%s) '
        'AND (([Eye Data].Min_Voltage)=%s) AND (([Eye Data].Max_Voltage)=%s) '
        'AND (([Eye Data].Bitrate)=%s) AND (([Eye Data].Type)=\'%s\') '
        'AND (([Eye Data].SNLC)=\'%s\'));'
    ) % (eye_ID, laser_wavelength, vmin, vmax, bitrate, eye_type, SNLC)

    # Executing querry and fetching results
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def WriteToEyeData(eye_ID, laser_wavelength, vmin, vmax, bitrate,
                   filename, eye_type, SNLC, eye_data_ID):
    """
    Append query used to add a record to eye data table.

    Parameters
    ----------
    eye_ID : int
        Integer ID associated with matching data in eye table.
    laser_wavelength : float
        Operating laser wavelength used in eye diagram simulation.
    vmin : float
        Minimum modulation voltage used in eye diagram simulation.
    vmax : float
        Maximum modulation voltage used in eye diagram simulation.
    bitrate : float
        Bitrate used in eye diagram simulation.
    filename : str
        Filename associated with eye diagram simulation results.
    eye_type : str
        Eye diagram modulation type.
        Options : [NRZ, PAM4]
    SNLC : str
        Static non-linearity correction option.
        Options : [yes, no, N/A]
    eye_data_ID : int
        Integer ID used to differentiate records in the eye data table.

    Returns
    -------
    None.

    """
    # Defining SQL command
    sql = (
        'INSERT INTO[Eye Data](Eye_ID, Laser_Wavelength, Min_Voltage, Max_Voltage, Bitrate, '
        'Filename, Type, SNLC, EYE_Data_ID) '
        'SELECT %s AS Expr1, %s AS Expr2, %s AS Expr3, %s AS Expr4, %s AS Expr5, \'%s\' AS Expr6, '
        '\'%s\' AS Expr7, \'%s\' AS Expr8, %s AS Expr9;'
    ) % (eye_ID, laser_wavelength, vmin, vmax, bitrate, filename, eye_type, SNLC, eye_data_ID)

    # Executing query and committing results
    cursor.execute(sql)
    cursor.commit()
    return


def ParseStringArray(strArray):
    """
    Parse the inputed string array into a array floats.

    Parameters
    ----------
    strArray : array [str]
        Array of characters to be parsed into array of floats.

    Returns
    -------
    array : array [floats]
        Parsed array.

    """
    # Replacing bounding characters and separating by delimeter comma
    strArray = strArray.replace('[', '')
    strArray = strArray.replace(']', '')
    strArray = strArray.split(',')

    # Initialize array
    array = []

    # Populating the array
    for ii in range(len(strArray)):
        array.append(float(strArray[ii]))
    return array


def CreateTempInterconnectData(freq, CC, dNeff, coupler_ID, waveguide_ID, folder):
    """
    Create temporary datafiles for Interconnect to load into the components forming the ring.

    Parameters
    ----------
    freq : list
        List containing frequency component of the coupling coefficient data.
    CC : list
        List containing coupling data component of the coupling coefficient data.
    dNeff : list
        2D list containing voltage, real dNeff, and imaginary dNeff components of waveguide data.
        Index 0 : voltage
        Index 1 : real dNeff
        Index 2 : imaginary dNeff
    coupler_ID : int
        Integer ID of coupler table data used in simulation.
    waveguide_ID : int
        Integer ID of waveguide table data used in simulation.
    folder : WindowsPath
        Path to folder where temporary data will be created.

    Returns
    -------
    None.

    """
    # Saving current working directory and defining path to folder
    cwd = os.getcwd()
    path = cwd + "\\Database\\" + folder

    # Initialize empty list of lines for temporary coupler datafile
    lines_coupler = []

    # Iterate through data to create list of lines for temporary coupler datafile
    for ii in range(len(freq)):
        lines_coupler.append(str(freq[ii]) + ' ' + str(CC[ii]))

    # Creating temporary coupler datafile
    with open(path + '\\coupler_' + str(coupler_ID) + '.txt', 'w') as f:
        for line in lines_coupler:
            f.write(line)
            f.write('\n')

    # Initialize empty list of lines for temporary waveguide datafile
    lines_waveguide = []

    # Iterate through data to create list of lines for temporary waveguide datafile
    for ii in range(len(dNeff[0])):
        lines_waveguide.append(str(dNeff[0][ii]) + ' ' +
                               str(dNeff[1][ii]) + ' ' + str(dNeff[2][ii]))

    # Creating temporary waveguide datafile
    with open(path + '\\waveguide_' + str(waveguide_ID) + '.txt', 'w') as f:
        for line in lines_waveguide:
            f.write(line)
            f.write('\n')

    return


def DestroyTempInterconnectData(coupler_ID, waveguide_ID, transmission_ID, folder):
    """
    Remove all temporary datafiles created by CreateTempInterconnectData().

    Parameters
    ----------
    coupler_ID : int
        Integer ID of coupler table data used in simulation.
    waveguide_ID : int
        Integer ID of waveguide table data used in simulation.
    transmission_ID : int
        Integer ID of transmission table data used in the simulation.
    folder : WindowsPath
        Path to folder where temporary data will be created.

    Returns
    -------
    None.

    """
    # Both the folder and filename share the same naming convention
    filename = folder

    # Saving current working directory
    cwd = os.getcwd()

    # Cleaning up all temporary files
    if os.path.exists(cwd + "\\Database\\" + folder + "\\coupler_" + str(coupler_ID) + '.txt'):
        os.remove(cwd + "\\Database\\" + folder + "\\coupler_" + str(coupler_ID) + '.txt')
    if os.path.exists((cwd + "\\Database\\" + folder + "\\waveguide_"
                       + str(waveguide_ID) + '.txt')):
        os.remove((cwd + "\\Database\\" + folder + "\\waveguide_"
                   + str(waveguide_ID) + '.txt'))
    if os.path.exists((cwd + "\\Database\\" + folder + "\\" + filename + '_'
                       + str(transmission_ID) + '.icp')):
        os.remove(cwd + "\\Database\\" + folder + "\\" + filename + '_' +
                  str(transmission_ID) + '.icp')
    if os.path.exists((cwd + "\\Database\\" + folder + "\\" + filename + '_'
                       + str(transmission_ID) + '.ich')):
        os.remove(cwd + "\\Database\\" + folder + "\\" + filename + '_' +
                  str(transmission_ID) + '.ich')

    # If folder is transmission, remove the sweep results
    if folder == 'Transmission':
        # Deleting voltage sweep folder to save space and keep database clean
        sweepfolder = cwd + "\\Database\\" + folder + "\\" + filename + '_' + \
            str(transmission_ID) + '_voltage_sweep'
        try:
            shutil.rmtree(sweepfolder)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    return


def CheckDatabaseIntegrity():
    """
    Integrity checker than manages the information matching between Access and the folders.

    Returns
    -------
    None.

    """
    def IntegrityCore(name):
        """
        Integrity system for core ring simulation.

        Parameters
        ----------
        name : str
            Name of result type to inforce integrity on.

        Returns
        -------
        None.

        """
        # Pseudo dictionairy to defirentiate different database tables
        if name == 'Transmission':
            directory = 'Transmission'
            filetype = '.mat'
            file_database_index = 0
        elif name == 'Waveguide':
            directory = 'Mode'
            filetype = '.ldf'
            file_database_index = 3
        elif name == 'Charge AMF':
            directory = 'Charge_AMF'
            filetype = '.mat'
            file_database_index = 15
        elif name == 'Charge AIM':
            directory = 'Charge_AIM'
            filetype = '.mat'
            file_database_index = 15
        else:
            return

        # Saving current working directory
        cwd = os.getcwd()

        # Defining generic SQL command to grab table results
        sql = (
            'SELECT [%s Table].*'
            'FROM [%s Table];'
        ) % (name, name)

        # Executing querry and saving results
        cursor.execute(sql)
        result = cursor.fetchall()

        # Iterating through all transmission records and searching for matching file in folders
        for ii in range(len(result)):
            filename = result[ii][file_database_index]
            # Searching folder for following file name
            if os.path.exists(cwd + "\\Database\\" + directory + "\\" + filename + filetype):
                print(name + " integrity check 1 passed")
            else:
                print("Missing " + name + " datafile for: " + filename)
                print("Deleting corresponding database record")
                # Defining delete querry to clean up database
                sql = (
                    'DELETE [%s Table].*, [%s Table].Filename '
                    'FROM [%s Table] '
                    'WHERE ((([%s Table].Filename)=\'%s\'));'
                ) % (name, name, name, name, filename)
                # Executing querry and commiting results
                cursor.execute(sql)
                cursor.commit()

        # Now iterating through all files in transmission folder and searching for matching record
        for root, dirs, files in os.walk(cwd + "\\Database\\" + directory):
            # Iterating through all files found
            for file in files:
                if file.endswith(filetype):
                    filename = file.split('.')[0]
                    # Defining querry to search database directory for matching file
                    sql = (
                        'SELECT [%s Table].* '
                        'FROM [%s Table] '
                        'WHERE ((([%s Table].Filename)=\'%s\'));'
                    ) % (name, name, name, filename)

                    # Executing querry and fetching results
                    cursor.execute(sql)
                    result = cursor.fetchall()

                    # If no matching record is present, delete the files
                    if result == []:
                        print("Missing " + name + " database record for: " + file)
                        print("Deleting corresponding datafile")
                        os.remove(cwd + "\\Database\\" + directory + "\\" + file)
                    else:
                        print(name + " integrity check 2 passed")

    def IntegrityEye(name):
        """
        Integrity system for eye diagram simulations.

        Parameters
        ----------
        name : str
            Name of eye type to inforce integrity on.

        Returns
        -------
        None.

        """
        # Pseudo dictionairy to defirentiate different database tables
        directory = name
        filetype = '.mat'
        file_database_index = 5
        if name == 'Eye_NRZ':
            Eye_type = 'NRZ'
        elif name == 'Eye_PAM4':
            Eye_type = 'PAM4'
        else:
            return

        # Saving current working directory
        cwd = os.getcwd()

        # Defining querry to search for all eye data
        sql = (
            'SELECT [Eye Data].* '
            'FROM [Eye Data] '
            'WHERE ((([Eye Data].Type)=\'%s\'));'
        ) % (Eye_type)

        # Executing querry and fetching resultsi
        cursor.execute(sql)
        result = cursor.fetchall()

        # Iterating through all transmission records and searching for matching file in folders
        for ii in range(len(result)):
            filename = result[ii][file_database_index]
            # Searching folder for following file name
            if os.path.exists(cwd + "\\Database\\" + directory + "\\" + filename + filetype):
                print(name + " integrity check 1 passed")
            else:
                print("Missing " + name + " datafile for: " + filename)
                print("Deleting corresponding database record")

                # Defining querry to delete results from eye table and data table
                sql = (
                    'DELETE [Eye Data].*, [Eye Data].Filename '
                    'FROM [Eye Data] '
                    'WHERE ((([Eye Data].Filename)=\'%s\'));'
                ) % (filename)

                # Executing querry and commiting results
                cursor.execute(sql)
                cursor.commit()

        # Now iterating through all files in transmission folder and searching for matching record
        for root, dirs, files in os.walk(cwd + "\\Database\\" + directory):
            # Iterating through all files found
            for file in files:
                if file.endswith(filetype):
                    # Searching database directory for matching file
                    filename = file.split('.')[0]

                    # Defining querry to grab all data from eye data table
                    sql = (
                        'SELECT [Eye Data].* '
                        'FROM [Eye Data] '
                        'WHERE ((([Eye Data].Filename)=\'%s\'));'
                    ) % (filename)

                    # Executing querry and fetching results
                    cursor.execute(sql)
                    result = cursor.fetchall()

                    # If no record is present, then deleete the corresponding data in the folders
                    if result == []:
                        print("Missing " + name + " database record for: " + file)
                        print("Deleting corresponding datafile")
                        os.remove(cwd + "\\Database\\" + directory + "\\" + file)
                    else:
                        print(name + " integrity check 2 passed")

    # Calling integrity scripts to inforce integrity
    IntegrityCore('Transmission')
    IntegrityCore('Waveguide')
    IntegrityCore('Charge AMF')
    IntegrityCore('Charge AIM')
    IntegrityEye('Eye_NRZ')
    IntegrityEye('Eye_PAM4')

    return
