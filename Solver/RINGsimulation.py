"""
Created on Wed Sep  1 17:38:54 2021.

This file contains the classes and constructors that allow for interaction between the
GUI and the scripts

@author: AlexTofini
"""
import Mode_SetUp
import FDTD_SetUp
import Interconnect_SetUp
import CHARGE_SetUp
import ConnectToDatabase as database
import CriticalCoupling_Solver as CCs


class Physical_Parameters():
    """
    A class to represent the physical paramters of the micro-ring modulator.

    ...

    """

    def __init__(self, *args):
        """
        Initialize Phyisical_Parameters class with all the necessary physical attributes.

        Parameters
        ----------
            radius : float
                Ring radius
            gap : float
                Ring gap
            coupling_length : float
                Ring coupling length, >0 for racetrack ring resonator
            wg_width : float
                Waveguide width
            thick_Si : float
                Thickness of waveguide, this never changes from 220 nm
            slab_height : float
                Slab height
        """
        self.radius = 0
        self.gap = 0
        self.coupling_length = 0
        self.wg_width = 0
        self.wg_height = 0
        self.slab_height = 0


# %% simulation parameters class constructor
class Simulation_Parameters():
    """
    A class to represent the simulation paramters of the micro-ring modulator.

    ...

    """

    def __init__(self, *args):
        """
        Initialize Simulation_Parameters class with all the necessary simulation settings.

        Parameters
        ----------
            lambda_start : float
                Starting wavelength for the ring simulation.
            lambda_end : float
                Ending wavelength for the ring simulation.
            Band : str
                Optical band
                Options: [CL, O]
            laser_wavl : float
                Laser wavelength for eye diagram simualtions.
            eye_type : str
                Eye diagram type.
                Options: [NRZ, PAM4].
            bitrate : float
                slab height.
            eye_vmin : float
                Minimum voltage used for the eye diagram simulation.
            eye_vmax : float
                Maximum voltage used for the eye diagram simulation.
            staticNonLinCorrec : str
                Static non-linearity correction setting.
                Options: [no, yes, N/A]
            propagation_loss : float
                Excess propagation loss supplied by the user.
        """
        self.lambda_start = 0
        self.lambda_end = 0
        self.Band = ''
        self.laser_wavl = 0
        self.eye_type = ''
        self.bitrate = 0
        self.eye_vmin = 0
        self.eye_vmax = 0
        self.staticNonLinCorrec = ''
        self.propagation_loss = 0

# %% Charge parameters class constructor


class charge_params():
    """
    A class to represent the charge paramters of the PN-junction.

    ...

    """

    def __init__(self, *args):
        """
        Initialize Simulation_Parameters class with all the necessary simulation settings.

        Parameters
        ----------
            vmin : float
                Minimum voltage used for the CHARGE simulation.
            vmax : float
                Maximum voltage used for the CHARGE simulation.
            charge_datapoints : float
                Number of voltage steps used, i.e. resolution.
            p_width_core : float
                Width of the P doping inside the core
                Note: this can be for P or P1Al or P2Al depending on the foundry and PN type.
            n_width_core : float
                Width of the N doping inside the core.
                Note: this can be for N or N1Al depending on the foundry.
            p_width_slab : float
                Width of the P doping inside the slab.
                Note: this can be for P or P1Al or P1Al+P2Al depending on the foundry and PN type.
            n_width_slab : float
                Width of the N doping inside the slab
                Note: this can be for N or N1AL depending on the foundry.
            pp_width : float
                Width of the P+ doping inside the slab
                Note: this can be for P+ or P4Al depending on the foundry.
            np_width : float
                Width of the N+ doping inside the slab
                Note: this can be for N+ or N3Al depending on the foundry.
            ppp_width : float
                Width of the P++ doping inside the slab
                Note: this can be for P++ or P5Al depending on the foundry.
            npp_width : float
                Width of the N++ doping inside the slab
                Note: this can be for N++ or N5Al depending on the foundry.
            CHARGE_file : WindowsPath
                Path object pointing to to CHARGE file used for the ring simulation.
            save_name : str
                Filename for saving if the PN-junction is being created by the user.
            PN_type : str
                PN-junction type.
                Options: [Lateral, L-Shaped].
            bias : str
                PN-junction modulation bias.
                Options: [Forward, Reverse].
            foundry : str
                Foundry control for the PN-junction definition.
                Options: [AMF, AIM].
        """
        self.vmin = 0
        self.vmax = 0
        self.charge_datapoints = 0
        self.p_width_core = 0
        self.n_width_core = 0
        self.p_width_slab = 0
        self.n_width_slab = 0
        self.pp_width = 0
        self.np_width = 0
        self.ppp_width = 0
        self.npp_width = 0
        self.CHARGE_file = ''
        self.save_name = ''
        self.PN_type = ''
        self.bias = ''
        self.foundry = ''

# %% saved results class constructor


class results():
    """
    A class to represent the results to be saved and utilized across the rest of the scripts.

    ...

    """

    def __init__(self, *args):
        """
        Initialize Simulation_Parameters class with all the necessary simulation settings.

        Parameters
        ----------
            coupler_ID : int
                Starting wavelength for the ring simulation.
            waveguide_ID : int
                Ending Wavelength for the ring simulation.
            absorption_loss : float
                Aborption/bend loss returned from the MODE simualtion.
            f : array
                Array containing the frequency component of the coupling result.
            CC : array
                Array containing the coupling coefficient component of the coupling result.
            dNeff : array
                Array containing the results for the change in effective index v.s. voltage.
            wavelength : array
                Array containing the results for the wavl. component of the transmission spectra.
            T : array
                Array containing the results for the power component of the transmission spectra.
            NonLinVoltages : array
                Array containing the non-linear voltages returns from the static non-linearity fix.
            CriticalCoupleGap : float
                Critical gap results from the critical coupling sweep.
            phase_shift : list
                List containing phase shift values w.r.t voltage
            capacitance : list
                List containing averaged capacitance values v.s. voltage across ssac signal sweep
            resistance : list
                List containing averaged resistance values v.s. voltage across ssac signal sweep
            bandwidth : list
                List containing averaged bandwidth values v.s. voltage across ssac signal sweep
        """
        self.coupler_ID = 0
        self.waveguide_ID = 0
        self.absorption_loss = 0
        self.f = []
        self.CC = []
        self.dNeff = []
        self.wavelength = []
        self.T = []
        self.NonLinVoltages = []
        self.CriticalCoupleGap = 0
        self.resonances = []
        self.FSRs = []
        self.bandwidths_3dB = []
        self.QFactors = []
        self.InsertionLosses = []
        self.phase_shift = []
        self.capacitance = []
        self.resistance = []
        self.bandwidth = []


def runSimulation(Radius, Gap, Slab_Height, CouplingLength, LambdaStart, LambdaEnd, Band,
                  CHARGE_file, prop_loss, Waveguide_Height, Waveguide_Width):
    """
    Execute simulation pipeline to create requested micro-ring modulator.

    Parameters
    ----------
    Radius : float
        Ring radius.
    Gap : float
        Ring gap.
    Slab_Height : float
        Slab height.
    CouplingLength : float
        Ring coupling length, >0 for racetrack ring resonator.
    LambdaStart : float
        Start wavelength for ring simulation.
    LambdaEnd : float
        End wavelength for ring simulation.
    Band : str
        Optical band.
        Options: [CL, O].
    CHARGE_file : WindowsPath
        Path object pointing to to CHARGE file used for the ring simulation.
    prop_loss : float
        Excess propagation loss supplied by the user.

    Returns
    -------
    saved_results : result class
        Populated saved_result class with results from the ring simulation process.

    """
    # Initializing classes
    parameters = Physical_Parameters()
    simulation_setup = Simulation_Parameters()
    charge_setup = charge_params()
    saved_results = results()

    # Populating physical parameters
    parameters.radius = Radius
    parameters.gap = Gap
    parameters.slab_height = Slab_Height
    parameters.coupling_length = CouplingLength
    parameters.wg_width = Waveguide_Width
    parameters.wg_height = Waveguide_Height

    # Populating simulation settings
    # if Band == 'CL':
    #    parameters.wg_width = 0.5e-6
    # else:
    #    parameters.wg_width = 0.35e-6
    simulation_setup.lambda_start = LambdaStart
    simulation_setup.lambda_end = LambdaEnd
    simulation_setup.Band = Band
    simulation_setup.propagation_loss = prop_loss

    # Querying charge file to populate charge_setup, searching both foundries for the record
    charge_file = str(CHARGE_file).split('\\')[-1]
    charge_file = charge_file.split('.')[0]
    result_check = database.QueryChargeFile(charge_file, 'AMF')
    if result_check == []:
        result = database.QueryChargeFile(charge_file, 'AIM')
        charge_setup.foundry = 'AIM'
    else:
        result = result_check
        charge_setup.foundry = 'AMF'

    # Populating CHARGE settings
    charge_setup.PN_type = result[0][1]
    charge_setup.p_width_core = result[0][7]
    charge_setup.n_width_core = result[0][8]
    charge_setup.p_width_slab = result[0][9]
    charge_setup.n_width_slab = result[0][10]
    charge_setup.pp_width = result[0][11]
    charge_setup.np_width = result[0][12]
    charge_setup.ppp_width = result[0][13]
    charge_setup.npp_width = result[0][14]
    charge_setup.vmin = result[0][16]
    charge_setup.vmax = result[0][17]
    charge_setup.charge_datapoints = result[0][18]
    charge_setup.bias = result[0][19]
    saved_results.capacitance = database.ParseStringArray(result[0][21])
    saved_results.resistance = database.ParseStringArray(result[0][22])
    saved_results.bandwidth = database.ParseStringArray(result[0][23])
    charge_setup.CHARGE_file = str(CHARGE_file)

    # Executing coupling region simulation in FDTD and saving results to result class
    coupling_coefficient, coupler_ID = FDTD_SetUp.calculate_coupling_coefficient(
        parameters, simulation_setup)
    saved_results.f = coupling_coefficient[0]
    saved_results.CC = coupling_coefficient[1]
    saved_results.coupler_ID = coupler_ID

    # Executing waveguide simulation in MODE and saving results to result class
    dNeff, absorption_loss, phase_shift, waveguide_ID = Mode_SetUp.Active_Bent_Waveguide(
        parameters, simulation_setup, charge_setup)
    saved_results.dNeff = dNeff
    saved_results.waveguide_ID = waveguide_ID
    saved_results.absorption_loss = absorption_loss
    saved_results.phase_shift = phase_shift

    # Executing combined ring simulation in Interconnect and saving results to result class
    [wavelength, T] = Interconnect_SetUp.Build_Ring(
        parameters, simulation_setup, charge_setup, saved_results)
    saved_results.wavelength = wavelength
    saved_results.T = T

    return saved_results


def runPNJunctionSimulator(p_width_core, n_width_core, p_width_slab, n_width_slab,
                           pp_width, np_width, ppp_width, npp_width, slab_height,
                           radius, coupling_length, vmin, vmax, save_name, bias,
                           band, foundry, PN_type, wg_height, wg_width):
    """
    Execute CHARGE simulation process for defined PN-junction.

    Parameters
    ----------
    p_width_core : float
        Width of the P doping inside the core
        Note: this can be for P or P1Al or P2Al depending on the foundry and PN type.
    n_width_core : float
        Width of the N doping inside the core
        Note: this can be for N or N1Al depending on the foundry.
    p_width_slab : float
        Width of the P doping inside the slab
        Note: this can be for P or P1Al or P1Al+P2Al depending on the foundry and PN type.
    n_width_slab : float
        Width of the N doping inside the slab
        Note: this can be for N or N1AL depending on the foundry.
    pp_width : float
        Width of the P+ doping inside the slab
        Note: this can be for P+ or P4Al depending on the foundry.
    np_width : float
        Width of the N+ doping inside the slab
        Note: this can be for N+ or N3Al depending on the foundry.
    ppp_width : float
        Width of the P++ doping inside the slab
        Note: this can be for P++ or P5Al depending on the foundry.
    npp_width : float
        Width of the N++ doping inside the slab
        Note: this can be for N++ or N5Al depending on the foundry.
    slab_height : float
        Slab height.
    radius : float
        Radius of ring composing the PN junction.
    coupling_length : float
        Straight coupling region in ring if it is present.
    vmin : float
        Minimum voltage used in the CHARGE simulation.
    vmax : float
        Maximum voltage used in the CHARGE simulation.
    save_name : str
        Filename for saving if the PN-junction is being created by the user.
    bias : str
        PN-junction modulation bias.
        Options: [Forward, Reverse]
    band : str
        Optical band.
        Options: [CL, O]
    foundry : str
        Foundry control for the PN-junction definition.
        Options: [AMF, AIM]
    PN_type : str
        PN-junction type.
        Options: [Lateral, L-Shaped]
    wg_height : float
        Height of waveguide
    wg_width : float
        Width of waveguide

    Returns
    -------
    CHARGE_FILE : str
        Filaname associated with the .mat file result, either return by querry or simulated.
    SimRun : TYPE
        DESCRIPTION.

    """
    # Initializing classes
    parameters = Physical_Parameters()
    simulation_setup = Simulation_Parameters()
    charge_setup = charge_params()

    # Populating physical parameters
    parameters.slab_height = slab_height
    parameters.radius = radius
    parameters.coupling_length = coupling_length
    parameters.wg_height = wg_height
    parameters.wg_width = wg_width

    # Populating simulation settions
    simulation_setup.Band = band

    # Caculating number of voltage steps based off fixed resolution of .25 Volts
    N = (vmax - vmin)/0.25 + 1

    # Populating charge settings
    charge_setup.p_width_core = p_width_core
    charge_setup.n_width_core = n_width_core
    charge_setup.p_width_slab = p_width_slab
    charge_setup.n_width_slab = n_width_slab
    charge_setup.pp_width = pp_width
    charge_setup.np_width = np_width
    charge_setup.ppp_width = ppp_width
    charge_setup.npp_width = npp_width
    charge_setup.vmin = vmin
    charge_setup.vmax = vmax
    charge_setup.charge_datapoints = N
    charge_setup.save_name = save_name
    charge_setup.PN_type = PN_type
    charge_setup.bias = bias
    charge_setup.foundry = foundry

    # Executing simulation depending on PN junction type
    if PN_type == 'Lateral':
        CHARGE_FILE, SimRun = CHARGE_SetUp.simulateLateral(
            parameters, simulation_setup, charge_setup)
    elif PN_type == 'L-Shaped':
        CHARGE_FILE, SimRun = CHARGE_SetUp.simulateLShaped(
            parameters, simulation_setup, charge_setup)

    return CHARGE_FILE, SimRun


def runEye(Eye_type, Vmax, Vmin, Laser_Wavl, Radius, CouplingLength, LambdaStart, LambdaEnd,
           bitrate, staticNonLinCorrec, CHARGE_file, saved_results, prop_loss):
    """
    Execute eye diagram simulation process.

    Parameters
    ----------
    Eye_type : str
        Eye diagram type.
        Options: [NRZ, PAM4].
    Vmax : float
        Maximum wavelength boundary condition for eye diagram simulation.
    Vmin : float
        Minimum wavelength boundary condition for eye diagram simulation.
    Laser_Wavl : float
        Operating wavelength for laser used for the eye diagram.
    Radius : float
        Ring radius.
    CouplingLength : float
        Ring coupling length, >0 for racetrack ring resonator
    LambdaStart : float
        Start wavelenth from the ring simulation.
    LambdaEnd : float
        End wavelength from the ring simulation.
    bitrate : float
        Bitrate used for eye diagram simulation.
    staticNonLinCorrec : str
        Static non-linearity correction setting.
        Options: [no, yes, N/A]
    CHARGE_file : WindowsPath
        Path object pointing to to CHARGE file used for the ring simulation.
    saved_results : class
        Result class with results from previous simulations.
    prop_loss : float
        Excess propagation loss supplied by the user.

    Returns
    -------
    amplitude : TYPE
        DESCRIPTION.
    time : TYPE
        DESCRIPTION.
    Voltage_levels : TYPE
        DESCRIPTION.

    """
    # Checking CHARGE file to determine what foundry it is associated with
    foundry_check = str(CHARGE_file).split('\\')[-2]
    if foundry_check == 'Charge_AMF':
        foundry = 'AMF'
    elif foundry_check == 'Charge_AIM':
        foundry = 'AIM'

    # Querrying CHARGE data to determine relevant info to use as limitations on eye diagrams
    charge_file = str(CHARGE_file).split('\\')[-1]
    charge_file = charge_file.split('.')[0]
    charge_query = database.QueryChargeFile(charge_file, foundry)

    # Initializing classes
    simulation_setup = Simulation_Parameters()
    parameters = Physical_Parameters()
    charge_setup = charge_params()

    # Populating physical parameters
    parameters.radius = Radius
    parameters.coupling_length = CouplingLength

    # Populating simulation settings
    simulation_setup.lambda_start = LambdaStart
    simulation_setup.lambda_end = LambdaEnd
    simulation_setup.eye_vmax = Vmax
    simulation_setup.eye_vmin = Vmin
    simulation_setup.laser_wavl = Laser_Wavl
    simulation_setup.eye_type = Eye_type
    simulation_setup.bitrate = bitrate
    simulation_setup.staticNonLinCorrec = staticNonLinCorrec
    simulation_setup.propagation_loss = prop_loss

    # Populating CHARGE settings
    charge_setup.vmin = charge_query[0][14]
    charge_setup.vmax = charge_query[0][15]
    charge_setup.charge_datapoints = charge_query[0][16]

    # Determining voltage levels depending on eye type
    if Eye_type == 'PAM4':
        Voltage_levels = Interconnect_SetUp.PAM4_Voltage(simulation_setup,
                                                         saved_results,
                                                         charge_setup)
        saved_results.NonLinVoltages = Voltage_levels
    elif Eye_type == 'NRZ':
        Voltage_levels = [simulation_setup.eye_vmin, simulation_setup.eye_vmax]

    # Running eye diagram simulation in Interconnect
    [amplitude, time] = Interconnect_SetUp.Eye_Diagrams(parameters, simulation_setup, saved_results)

    return amplitude, time, Voltage_levels


def CriticalCouplingAutomation(Radius, Gaps, Slab_Height, CouplingLength, LambdaStart, LambdaEnd,
                               Band, CHARGE_file, prop_loss):
    """
    Execute critical coupling automation.

    Parameters
    ----------
    Radius : float
        Ring radius.
    Gaps : float
        Ring gap.
    Slab_Height : float
        Slab height.
    CouplingLength : float
        Ring coupling length, >0 for racetrack ring resonator.
    LambdaStart : float
        Start wavelength for ring simulation.
    LambdaEnd : float
        End wavelength for ring simulation.
    Band : str
        Optical band.
        Options: [CL, O].
    CHARGE_file : WindowsPath
        Path object pointing to to CHARGE file used for the ring simulation.
    prop_loss : flaot
        Excess propagation loss supplied by the user.
    saved_charge_results : class
        Result class with only populated charge data

    Returns
    -------
    saved_results : class
        Populated class with saved results to be used in the rest of the simulation.

    """
    # Initializing classes
    parameters = Physical_Parameters()
    simulation_setup = Simulation_Parameters()
    saved_results = results()
    charge_setup = charge_params()

    # Populating physical parameters
    parameters.radius = Radius
    parameters.gap = Gaps
    parameters.slab_height = Slab_Height
    parameters.coupling_length = CouplingLength
    if Band == 'CL':
        parameters.wg_width = 0.5e-6
    else:
        parameters.wg_width = 0.35e-6

    # Populating simulation settings
    simulation_setup.lambda_start = LambdaStart
    simulation_setup.lambda_end = LambdaEnd
    simulation_setup.Band = Band
    simulation_setup.propagation_loss = prop_loss

    # Querying charge file to populate charge_setup
    charge_file = str(CHARGE_file).split('\\')[-1]
    charge_file = charge_file.split('.')[0]

    result_check = database.QueryChargeFile(charge_file, 'AMF')
    if result_check == []:
        result = database.QueryChargeFile(charge_file, 'AIM')
        charge_setup.foundry = 'AIM'
    else:
        result = result_check
        charge_setup.foundry = 'AMF'

    # Populating CHARGE settings
    charge_setup.PN_type = result[0][1]
    charge_setup.p_width_core = result[0][7]
    charge_setup.n_width_core = result[0][8]
    charge_setup.p_width_slab = result[0][9]
    charge_setup.n_width_slab = result[0][10]
    charge_setup.pp_width = result[0][11]
    charge_setup.np_width = result[0][12]
    charge_setup.ppp_width = result[0][13]
    charge_setup.npp_width = result[0][14]
    charge_setup.vmin = result[0][16]
    charge_setup.vmax = result[0][17]
    charge_setup.charge_datapoints = result[0][18]
    charge_setup.bias = result[0][19]
    saved_results.capacitance = database.ParseStringArray(result[0][21])
    saved_results.resistance = database.ParseStringArray(result[0][22])
    saved_results.bandwidth = database.ParseStringArray(result[0][23])
    charge_setup.CHARGE_file = str(CHARGE_file)

    # Begining critical coupling automation sequence

    # Step 1 determine the loss of the current waveguide and charge configuration
    dNeff, absorption_losses, phase_shift, waveguide_ID = Mode_SetUp.Active_Bent_Waveguide(
        parameters, simulation_setup, charge_setup)
    saved_results.dNeff = dNeff
    saved_results.waveguide_ID = waveguide_ID
    saved_results.absorption_loss = absorption_losses
    saved_results.phase_shift = phase_shift

    # Step 2 estimate critical coupling condition
    power_coupling = CCs.EstimateCC_Condition(parameters, simulation_setup, saved_results)

    # Step 3 Sweeping to find critical coupling condition
    sweep_results, coupler_IDs = CCs.runSweep(parameters, simulation_setup)
    optimal_gap = CCs.FindOptimalGap(
        Gaps, sweep_results, simulation_setup, power_coupling)

    # Step 4 Setting class object gap to critically coupled result above
    parameters.gap = optimal_gap
    saved_results.CriticalCoupleGap = optimal_gap

    # Step 5 Running final coupler simulation at critically coupled gap
    coupling_coefficient, coupler_ID = FDTD_SetUp.calculate_coupling_coefficient(
        parameters, simulation_setup, gap=optimal_gap)
    saved_results.f = coupling_coefficient[0]
    saved_results.CC = coupling_coefficient[1]
    saved_results.coupler_ID = coupler_ID

    # Step 6 Running transmission sweep for the previous settings
    [wavelength, T] = Interconnect_SetUp.Build_Ring(
        parameters, simulation_setup, charge_setup, saved_results)
    saved_results.wavelength = wavelength
    saved_results.T = T

    return saved_results
