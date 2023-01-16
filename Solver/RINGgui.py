"""
Created on Wed Aug 25 11:20:06 2021.

This script contains the GUI code that creates the interactable visualization of the automation
system

@author: AlexTofini

"""
import textwrap
import PySimpleGUI as sg
import numpy as np
import RINGsimulation as sim
from scipy.signal import find_peaks
import InputVerification as verify
import Draw as draw
import ConnectToDatabase as database
import matplotlib.pyplot as plt
import math
import matplotlib
from pathlib import Path
# Setting the interactive plot window
matplotlib.use('TkAgg')

# set the theme for the screen/window
sg.theme("DarkTanBlue")


def enable_result_buttons():
    """
    Enable result tab option for user.

    Returns
    -------
    None.

    """
    CC_button.Update(disabled=False)
    NEFF_button.Update(disabled=False)
    Tranmission_button.Update(disabled=False)
    NRZ_button.Update(disabled=False)
    PAM4_button.Update(disabled=False)
    Phase_button.Update(disabled=False)


def toggle_PN_Plot_Options(show):
    """
    Toggle the plot options for the PN junction result tab.

    Parameters
    ----------
    show : bool
        Boolean control to dictate whether the plot options are visible in the PN junction results.

    Returns
    -------
    None.

    """
    Phase_plot_button.update(visible=show)
    Capacitance_plot_button.update(visible=show)
    Resistance_plot_button.update(visible=show)
    Bandwidth_plot_button.update(visible=show)


def toggle_Corner_Analysis_Results(show):
    """
    Toggle the corner analysis result optionsin the result tab.

    Parameters
    ----------
    show : bool
        Boolean control to dictate whether the corner analysis results should be visible

    Returns
    -------
    None.

    """
    Nominal_plot.update(visible=show)
    BL_plot.update(visible=show)
    BR_plot.update(visible=show)
    TL_plot.update(visible=show)
    TR_plot.update(visible=show)


def update_text_results(str1, str2, str3, str4, str5):
    """
    Display text results for transmission window to user.

    Parameters
    ----------
    str1 : str
        string to display as first text result.
    str2 : str
        string to display as second text result.
    str3 : str
        string to display as third text result.
    str4 : str
        string to display as fourth text result.
    str5 : str
        string to display as fifth text result.

    Returns
    -------
    None.

    """
    Result1.Update(str1, visible=True)
    Result2.Update(str2, visible=True)
    Result3.Update(str3, visible=True)
    Result4.Update(str4, visible=True)
    Result5.Update(str5, visible=True)


def enable_secondary_inputs():
    """
    Enable visiblity for eye diagram inputs to user.

    Returns
    -------
    None.

    """
    Laser_Input.Update(visible=True)
    VMin_Input.Update(visible=True)
    VMax_Input.Update(visible=True)
    Bitrate_Input.Update(visible=True)
    Eye_button.Update(visible=True)


def disable_secondary_inputs():
    """
    Disable visibility of eye diagram inputs to user.

    Returns
    -------
    None.

    """
    Laser_Input.Update(visible=False)
    VMin_Input.Update(visible=False)
    VMax_Input.Update(visible=False)
    Bitrate_Input.Update(visible=False)
    Eye_button.Update(visible=False)
    non_linearity_correction.Update(visible=False)
    non_linearity_correction.Update(visible=False)


def plot_CC(saved_results, identifier='Nominal'):
    """
    Plot coupling coefficient i.e the power coupling coefficient.

    Returns
    -------
    None.

    """
    # Disable secondary inputs in case the user has previously selected a tab with them
    disable_secondary_inputs()

    # Enable PN junction plot option buttons
    toggle_PN_Plot_Options(False)

    # Creating plot in separate window to reduce lag
    fig = plt.figure(1)
    fig.clear()
    #  Plotting power coupling results in figure
    CC = saved_results.CC
    CC_f = saved_results.f
    c = 299792458
    wavl = [c/x/1e-9 for x in CC_f]
    x = wavl
    y = CC
    plt.plot(x, y)
    plt.title('[' + identifier + '] Coupling Efficiency vs. Wavelength')
    plt.xlabel('Wavelength [nm]')
    plt.ylabel('Efficiency [%]')
    plt.grid()
    fig = plt.gcf()
    fig.canvas.manager.window.attributes('-topmost', 1)

    # Cleaning up text_results since they are not applicable here
    update_text_results('', '', '', '', '')


def plot_NEFF(saved_results, identifier='Nominal'):
    """
    Plot change in effective index versus voltage.

    Returns
    -------
    None.

    """
    # Disable secondary inputs in case the user has previously selected a tab with them
    disable_secondary_inputs()

    # Enable PN junction plot option buttons
    toggle_PN_Plot_Options(False)

    # Creating Matplotlib figure
    plt.figure(1)
    plt.figure(1).clear()

    # Plotting change in effective index plot
    dNeff = saved_results.dNeff
    x = dNeff[0]
    y1 = dNeff[1]
    y2 = dNeff[2]
    plt.plot(x, y1, label="Real")
    plt.plot(x, y2, label="Imaginary")
    plt.title('Delta Neff vs. Voltage')
    plt.xlabel('Voltage [V]')
    plt.ylabel('Delta Neff')
    plt.legend(loc="upper right")
    plt.grid()
    fig = plt.gcf()
    fig.canvas.manager.window.attributes('-topmost', 1)

    # Cleaning up text_results since they are not applicable here
    update_text_results('', '', '', '', '')


def plot_T(saved_results, identifier='Nominal'):
    """
    Plot transmission spectra of the ring modulator.

    Returns
    -------
    None.

    """
    # Disable secondary inputs in case the user has previously selected a tab with them
    disable_secondary_inputs()

    # Enable PN junction plot option buttons
    toggle_PN_Plot_Options(False)

    # Creating Matplotlib figure
    plt.figure(1)
    plt.figure(1).clear()

    # Plotting transmission spectra and shift w.r.t voltage
    dNeff = saved_results.dNeff
    wavelength = saved_results.wavelength
    wavelength = wavelength  # *1e9
    T = saved_results.T
    V = dNeff[0]
    dV = abs(V[len(V)-1] - V[0])/(len(V)-1)
    for i in range(len(T)):
        plt.plot(wavelength, T[i, :])

    plt.title('Transmission Spectra for V= ' +
              str(V[0]) + " to " + str(V[len(V)-1]) + "in steps of " + str(dV))
    plt.xlabel('Wavleength [nm]')
    plt.ylabel('Transmission [dB]')
    plt.legend(loc="upper right")
    plt.grid()
    fig = plt.gcf()
    fig.canvas.manager.window.attributes('-topmost', 1)

    # Extracting FOMs to display to user

    # Isolating non biased data, aka 0V
    non_biased_T = T[0, :]

    # Solving list of resonances
    height = 0.01
    [indx, peaks] = find_peaks(-1*non_biased_T, height)
    plt.plot(wavelength[indx], non_biased_T[indx], "x")
    resonance_list = wavelength[indx]
    result1_str = 'Resonance [nm]: [ '
    for i in range(len(resonance_list)):
        result1_str = result1_str + str(round(resonance_list[i], 3)) + ', '
    result1_str = result1_str + ']'
    result1_str = textwrap.wrap(result1_str, 40)

    # Solving list of FSRs
    FSR_list = [0] * (len(resonance_list)-1)
    result2_str = 'FSR [nm]: [ '
    for i in range(len(FSR_list)):
        FSR_list[i] = round(resonance_list[i+1]-resonance_list[i], 2)
        result2_str = result2_str + str(FSR_list[i]) + ', '

    result2_str = result2_str + ']'

    # Solving list of 3dB bandwidths
    three_dB_bandwidth = [0] * (len(resonance_list))
    three_dB_line = [-3]*len(non_biased_T)
    idx = np.argwhere(np.diff(np.sign(three_dB_line - non_biased_T))).flatten()
    three_dB_intersections = wavelength[idx]
    result3_str = '3 dB Bandwidth [nm]: [ '
    for i in range(int(len(three_dB_intersections)/2)):
        print(i)
        three_dB_bandwidth[i] = round(
            np.abs(three_dB_intersections[2*i+1] - three_dB_intersections[2*i]), 3)
        result3_str = result3_str + str(three_dB_bandwidth[i]) + ', '

    result3_str = result3_str + ']'

    # Solving list of quality factors
    Qfactor = resonance_list/three_dB_bandwidth
    Qfactor = np.around(Qfactor, decimals=-2)
    Qfactor = Qfactor.astype(int)
    result4_str = 'Q: [ '
    for i in range(len(Qfactor)):
        result4_str = result4_str + str(Qfactor[i]) + ', '

    result4_str = result4_str + ']'

    # Getting insertion loss Results
    result5_str = 'Insertion Loss [dB]: [ '
    ILs = np.round(np.array(peaks['peak_heights']), 2)
    result5_str = result5_str + str(ILs) + ' ]'

    # Updating the displayed results
    update_text_results(result1_str, result2_str, result3_str, result4_str, result5_str)


def plot_Phase(saved_results, identifier='Nominal'):
    """
    Plot PN junction phase chnage.

    Returns
    -------
    None.

    """
    # Creating Matplotlib figure
    plt.figure(1)
    plt.figure(1).clear()

    # Plotting change in effective index plot
    phase_shift = saved_results.phase_shift
    x = phase_shift[0]
    y1 = phase_shift[1]
    plt.plot(x, y1, label="Phase")
    plt.title('Phase Shift vs. Voltage')
    plt.xlabel('Voltage [V]')
    plt.ylabel('Phase [rads]')
    plt.legend(loc="upper right")
    plt.grid()
    fig = plt.gcf()
    fig.canvas.manager.window.attributes('-topmost', 1)

    # Determining if Vpi has been resolved
    max_shift = max(phase_shift[1])
    if max_shift < math.pi:
        result_str1 = 'Vpi was not resolved'
    else:
        indx = min(range(len(phase_shift[1])), key=lambda i: abs(phase_shift[1][i]-math.pi))
        Vpi = phase_shift[0][indx]
        result_str1 = "Vpi = " + str(Vpi) + " Volts"
    # Updating result strings
    update_text_results(result_str1, '', '', '', '')


def plot_Capacitance(saved_results, identifier='Nominal'):
    """
    Plot PN junction capacitance versus voltage.

    Returns
    -------
    None.

    """
    # Creating Matplotlib figure
    plt.figure(1)
    plt.figure(1).clear()

    # Plotting change in effective index plot
    capacitance = saved_results.capacitance
    phase_shift = saved_results.phase_shift
    voltage = phase_shift[0]
    x = voltage
    capacitance_scaled = [x/1e-10 for x in capacitance]
    y1 = capacitance_scaled
    plt.plot(x, y1, label="Average Capacitance")
    plt.title('Capacitance vs. Voltage')
    plt.xlabel('Voltage [V]')
    plt.ylabel('Capacitance [pf/cm]')
    plt.legend(loc="upper right")
    plt.grid()
    fig = plt.gcf()
    fig.canvas.manager.window.attributes('-topmost', 1)

    # Updating result strings
    update_text_results('', '', '', '', '')


def plot_Resistance(saved_results, identifier='Nominal'):
    """
    Plot PN junction resistance versus voltage.

    Returns
    -------
    None.

    """
    # Creating Matplotlib figure
    plt.figure(1)
    plt.figure(1).clear()

    # Plotting change in effective index plot
    resistance = saved_results.resistance
    phase_shift = saved_results.phase_shift
    voltage = phase_shift[0]
    x = voltage
    resistance_scaled = [x/100 for x in resistance]
    y1 = resistance_scaled
    plt.plot(x, y1, label="Average Resistance")
    plt.title('Resistance vs. Voltage')
    plt.xlabel('Voltage [V]')
    plt.ylabel('Resistance [Ohm.cm]')
    plt.legend(loc="upper right")
    plt.grid()
    fig = plt.gcf()
    fig.canvas.manager.window.attributes('-topmost', 1)

    # Updating result strings
    update_text_results('', '', '', '', '')


def plot_Bandwidth(saved_results, identifier='Nominal'):
    """
    Plot PN junction bandwidth versus voltage.

    Returns
    -------
    None.

    """
    # Creating Matplotlib figure
    plt.figure(1)
    plt.figure(1).clear()

    # Plotting change in effective index plot
    capacitance = saved_results.capacitance
    resistance = saved_results.resistance
    phase_shift = saved_results.phase_shift
    voltage = phase_shift[0]
    x = voltage
    capacitance_scaled = [x/1e-10 for x in capacitance]
    resistance_scaled = [x/100 for x in resistance]
    bandwidth_scaled = [1/(2*math.pi*x*y)/1e-12/1e9 for x,
                        y in zip(resistance_scaled, capacitance_scaled)]

    y1 = bandwidth_scaled
    plt.plot(x, y1, label="Average Bandwidth")
    plt.title('Bandwidth vs. Voltage')
    plt.xlabel('Voltage [V]')
    plt.ylabel('Bandwidth [GHz]')
    plt.legend(loc="upper right")
    plt.grid()
    fig = plt.gcf()
    fig.canvas.manager.window.attributes('-topmost', 1)

    # Updating result strings
    update_text_results('', '', '', '', '')


# Dimensions for drawing are hard coded as pixels and indifferent to physical provided size
# Defining Size Of Canvas
canvas_width = 1100
canvas_height = 1000
# Defining center point Of ring
x0 = -75
y0 = 40
# Defining radius and coupling region
drawing_radius = 250
coupling_region = 250
# Defining bus waveguide parameters
bus_width = 15
bus_extra = 100
bus_length = 2 * drawing_radius + bus_extra
drawing_gap = 125

# Setting up all elements on the window
# Defining parameters that dictate placing and size of objects on window
spacing = 20
box_size = 10
warning_size = 40
eye_pading = 0

# Creating elements on main GUI window
main_tab = [
    [sg.Text('Ring Parameters',
             font='Helvitica 16 bold underline')],
    [sg.Text('Radius [um]:',
             size=(spacing, 1)),
     sg.Input(key='-RADIUS-',
              s=(box_size, 1)),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-RADIUS_WARNING-')],
    [sg.Text('Gap [nm]:',
             size=(spacing, 1)),
     sg.Input(key='-GAP-',
              s=(box_size, 1),
              readonly=False,
              use_readonly_for_disable=False),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-GAP_WARNING-')],
    [sg.Text('Slab Height [nm]:',
             size=(spacing, 1)),
     sg.Input(key='-SLAB-',
              s=(box_size, 1)),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-SLAB_WARNING-')],
    [sg.Text('Coupling Length [um]:',
             size=(spacing, 1)),
     sg.Input(0, key='-COUPLING_LENGTH-',
              s=(box_size, 1)),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-COUPLING_LENGTH_WARNING-')],
    [sg.Text('Waveguide Height [nm]:',
             size=(spacing, 1)),
     sg.Input(key='-WAVEGUIDE_HEIGHT-',
              s=(box_size, 1)),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-WAVEGUIDE_HEIGHT_WARNING-')],
    [sg.Text('Waveguide Width [nm]:',
             size=(spacing, 1)),
     sg.Input(key='-WAVEGUIDE_WIDTH-',
              s=(box_size, 1)),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-WAVEGUIDE_WIDTH_WARNING-')],
    [sg.Text('Simulation Parameters',
             font='Helvitica 16 bold underline')],
    [sg.Radio('CL Band (1500-1600)nm',
              "RADIO1",
              default=True,
              key='-CL_BAND-')],
    [sg.Radio('O Band (1260-1400)nm',
              "RADIO1",
              default=False,
              key='-O_BAND-')],
    [sg.Checkbox('Critical Coupling',
                 default=False,
                 visible=True,
                 change_submits=True,
                 key='-CRITICAL_COUPLE-')],
    [sg.Checkbox('Perform Corner Analysis',
                 default=False,
                 visible=True,
                 change_submits=True,
                 key='-CORNER_ANALYSIS-'),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-CORNER_ANALYSIS_WARNING-')],
    [sg.Text('Propagation Loss [dB/cm]'),
     sg.Input('2.5',
              s=(box_size, 1),
              key='-PROP_LOSS-'),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-PROP_LOSS_WARNING-')],
    [sg.Radio('Define CHARGE',
              "RADIO2",
              default=False,
              enable_events=True,
              key='-DEFINE_CHARGE-'),
     sg.Radio('Import CHARGE',
              "RADIO2",
              default=True,
              enable_events=True,
              key='-IMPORT_CHARGE-'),
     sg.Text('Filename:'),
     sg.Input(key='-CHARGE_FILE-',
              s=(box_size, 1)),
     sg.FileBrowse(key='-BROWSE-'),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-CHARGE_FILE_WARNING-')],
    [sg.Graph(canvas_size=(canvas_width/2,
                           canvas_height/2),
              graph_bottom_left=(-canvas_width/2, -canvas_height/2),
              graph_top_right=(400, 400),
              background_color='white',
              key='-GRAPH-')],
    [sg.Button('Update Ring Parameters'),
     sg.Button("Run Simulation",
               visible=False,
               key='-RUN-')]


]

# Creating elements on CHARGE window
charge_tab = [
    [sg.Text('Select Foundry',
             font='Helvitica 16 bold underline')],
    [sg.Radio('AMF',
              "RADIO5",
              default=True,
              enable_events=True,
              key='-AMF-')],
    [sg.Radio('AIM',
              "RADIO5",
              default=False,
              enable_events=True,
              key='-AIM-')],
    [sg.Text('Select PN-Junction Type',
             font='Helvitica 16 bold underline')],
    [sg.Radio('Lateral',
              "RADIO3",
              default=True,
              enable_events=True,
              key='-LATERAL-')],
    [sg.Radio('L-Shaped',
              "RADIO3",
              default=False,
              enable_events=True,
              visible=False,
              key='-L_SHAPED-')],
    [sg.Text('Input Parameters',
             font='Helvitica 16 bold underline')],
    [sg.Text('P Width (Core) [nm]:',
             size=(spacing, 1),
             key='-P_WIDTH_CORE_TEXT-'),
     sg.Input(key='-P_WIDTH_CORE-',
              s=(box_size, 1)),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-P_WIDTH_CORE_WARNING-')],
    [sg.Text('N Width (Core) [nm]:',
             size=(spacing, 1),
             key='-N_WIDTH_CORE_TEXT-'),
     sg.Input(key='-N_WIDTH_CORE-',
              s=(box_size, 1)),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-N_WIDTH_CORE_WARNING-')],
    [sg.Text('P Width (Slab) [nm]:',
             size=(spacing, 1),
             key='-P_WIDTH_SLAB_TEXT-'),
     sg.Input(key='-P_WIDTH_SLAB-',
              s=(box_size, 1)),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-P_WIDTH_SLAB_WARNING-')],
    [sg.Text('N Width (Slab) [nm]:',
             size=(spacing, 1),
             key='-N_WIDTH_SLAB_TEXT-'),
     sg.Input(key='-N_WIDTH_SLAB-',
              s=(box_size, 1)),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-N_WIDTH_SLAB_WARNING-')],
    [sg.Text('P+ Width [nm]:',
             size=(spacing, 1),
             key='-P+_WIDTH_TEXT-'),
     sg.Input(key='-P+_WIDTH-',
              s=(box_size, 1)),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-P+_WIDTH_WARNING-')],
    [sg.Text('N+ Width [nm]:',
             size=(spacing, 1),
             key='-N+_WIDTH_TEXT-'),
     sg.Input(key='-N+_WIDTH-',
              s=(box_size, 1)),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-N+_WIDTH_WARNING-')],
    [sg.Text('P++ Width [nm]:',
             size=(spacing, 1),
             key='-P++_WIDTH_TEXT-'),
     sg.Input(key='-P++_WIDTH-',
              s=(box_size, 1)),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-P++_WIDTH_WARNING-')],
    [sg.Text('N++ Width [nm]:',
             size=(spacing, 1),
             key='-N++_WIDTH_TEXT-'),
     sg.Input(key='-N++_WIDTH-',
              s=(box_size, 1)),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-N++_WIDTH_WARNING-')],
    [sg.Text('Min Voltage [V]]:',
             size=(spacing, 1)),
     sg.Input(key='-VMIN_CHARGE-',
              s=(box_size, 1)),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-VMIN_CHARGE_WARNING-')],
    [sg.Text('Max Voltage [V]]:',
             size=(spacing, 1)),
     sg.Input(key='-VMAX_CHARGE-',
              s=(box_size, 1)),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-VMAX_CHARGE_WARNING-')],
    [sg.Radio('Forward Bias',
              "RADIO4",
              default=False,
              key='-FORWARD-')],
    [sg.Radio('Reverse Bias',
              "RADIO4",
              default=True,
              key='-REVERSE-')],
    [sg.Text('Filename for saving:',
             size=(spacing, 1)),
     sg.Input(key='-SAVE_NAME-',
              s=(box_size, 1)),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-SAVE_NAME_WARNING-')],
    [sg.Graph(canvas_size=(800,
                           200),
              graph_bottom_left=(0, 0),
              graph_top_right=(200, 800),
              background_color='white',
              key='-GRAPH_CHARGE-')],
    [sg.Button('Update CHARGE Parameters'),
     sg.Button("Run CHARGE Simulation",
               visible=False,
               key='-RUN_CHARGE-')]
]
# Creating elements on the variability window
sz = (10, 20)
col1_color = 'grey',
col2_color = 'green',
col1 = [
    [sg.Text("Select 2 Desired Variables & Specify Variability")],
    [sg.Checkbox('Waveguide Height',
                 default=False,
                 visible=True,
                 enable_events=True,
                 key='-VARIABILITY_WAVEGUIDE_HEIGHT-'),
     sg.Text('+- '),
     sg.Input(key='-WAVEGUIDE_HEIGHT_RANGE-', s=(box_size, 1),
              visible=True),
     sg.Text(' [nm]'),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-WAVEGUIDE_HEIGHT_RANGE_WARNING-')
     ],
    [sg.Checkbox('Waveguide Width',
                 default=False,
                 visible=True,
                 enable_events=True,
                 key='-VARIABILITY_WAVEGUIDE_WIDTH-'),
     sg.Text('+- '),
     sg.Input(key='-WAVEGUIDE_WIDTH_RANGE-', s=(box_size, 1),
              visible=True),
     sg.Text(' [nm]'),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-WAVEGUIDE_WIDTH_RANGE_WARNING-')
     ],
    [sg.Checkbox('Slab Height',
                 default=False,
                 visible=True,
                 enable_events=True,
                 key='-VARIABILITY_SLAB_HEIGHT-'),
     sg.Text('+- '),
     sg.Input(key='-SLAB_HEIGHT_RANGE-', s=(box_size, 1),
              visible=True),
     sg.Text(' [nm]'),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-SLAB_HEIGHT_RANGE_WARNING-')
     ],
    [sg.Checkbox('Doping Cocentration % Error',
                 default=False,
                 visible=True,
                 enable_events=True,
                 key='-VARIABILITY_DOPING_CONCENTRATION-'),
     sg.Text('+- '),
     sg.Input(key='-DOPING_CONCENTRATION_RANGE-', s=(box_size, 1),
              visible=True),
     sg.Text(' [%]'),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-DOPING_CONCENTRATION_RANGE_WARNING-')
     ],
    [sg.Button('Update',
               visible=True,
               button_color=('black', 'green'),
               key='-UPDATE_VARIABILITY-')],
    [sg.Text("Current Selected Variability Analysis Settings:",
             key='-CURRENT_VARIABLES-')],
]


variability_tab = [[sg.Column(col1, element_justification='c')]]

# Creating elements on result window
results_tab = [
    [sg.Radio('Nominal',
              "RADIO_Corner",
              default=True,
              visible=False,
              enable_events=False,
              key='-NOMINAL-'),
     sg.Radio('Bottom Left Corner',
              "RADIO_Corner",
              default=False,
              visible=False,
              enable_events=False,
              key='-CORNER_BL-'),
     sg.Radio('Bottom Right Corner',
              "RADIO_Corner",
              default=False,
              visible=False,
              enable_events=False,
              key='-CORNER_BR-'),
     sg.Radio('Top Left Corner',
              "RADIO_Corner",
              default=False,
              visible=False,
              enable_events=False,
              key='-CORNER_TL-'),
     sg.Radio('Top Right Corner',
              "RADIO_Corner",
              default=False,
              visible=False,
              enable_events=False,
              key='-CORNER_TR-')],
    [sg.B('Coupling Coefficient',
          disabled=True,
          key='-CC-'),
     sg.B('Delta Neff',
          disabled=True,
          key='-NEFF-'),
     sg.B('PN Junction',
          disabled=True,
          key='-PN_RESULT-'),
     sg.B('Transmission Spectra',
          disabled=True,
          key='-T-'),
     sg.B('NRZ Eye Diagram',
          disabled=True,
          key='-NRZ-'),
     sg.B('PAM4 Eye Diagram',
          disabled=True,
          key='-PAM4-')],
    [sg.Button('Plot Phase Shift',
               visible=False,
               button_color=('black', 'yellow'),
               key='-PHASE-'),
     sg.Button('Plot Capacitance',
               visible=False,
               button_color=('black', 'yellow'),
               key='-CAPACITANCE-'),
     sg.Button('Plot Resistance',
               visible=False,
               button_color=('black', 'yellow'),
               key='-RESISTANCE-'),
     sg.Button('Plot Bandwidth',
               visible=False,
               button_color=('black', 'yellow'),
               key='-BANDWIDTH-')],
    # =============================================================================
    #     [sg.T('Controls:')],
    #     [sg.Canvas(key='controls_cv')],
    #     [sg.T('Figure:')],
    #     [sg.Column(
    #         layout=[
    #             [sg.Canvas(key='fig_cv',
    #                        # it's important that you set this size
    #                        size=(400 * 2, 400)
    #                        )]
    #         ],
    #         background_color='#DAE0E6',
    #         pad=(0, 0)
    #     )],
    # =============================================================================
    [sg.Text('Placeholder text:',
             size=(100,
                   None),
             visible=False,
             key='-RESULT1-')],
    [sg.Text('Placeholder text:',
             size=(100, 1),
             visible=False,
             key='-RESULT2-'),
     sg.Input(key='-LASER-',
              s=(box_size, 1),
              visible=False),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-LASER_WARNING-',
             pad=(eye_pading, 0))],
    [sg.Text('Placeholder text:',
             size=(100, 1),
             visible=False,
             key='-RESULT3-'),
     sg.Input(key='-VMIN-',
              s=(box_size, 1),
              visible=False),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-VMIN_WARNING-',
             pad=(eye_pading, 0))],
    [sg.Text('Placeholder text:',
             size=(100, 1),
             visible=False,
             key='-RESULT4-'),
     sg.Input(key='-VMAX-',
              s=(box_size, 1),
              visible=False),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-VMAX_WARNING-',
             pad=(eye_pading, 0))],
    [sg.Text('Placeholder text:',
             size=(100, 1),
             visible=False,
             key='-RESULT5-'),
     sg.Input(key='-BITRATE-',
              s=(box_size, 1),
              visible=False),
     sg.Text('Warning Message: ',
             size=(warning_size, 1),
             text_color='yellow',
             visible=False,
             key='-BITRATE_WARNING-',
             pad=(eye_pading, 0))],
    [sg.Checkbox('Correct Static Non-linearity',
                 default=False,
                 visible=False,
                 key='-STATIC_NONLIN-')],
    [sg.B('Update Eye',
          visible=False,
          key='-EYEBUTTON-')]

]
# Defining tab groups to handle each different window as described above
tabgrp = [[sg.TabGroup([[sg.Tab('Simulation',
                                main_tab,
                                title_color='Red',
                                border_width=10,
                                tooltip='Personal details',
                                element_justification='center'),
                         sg.Tab('Variability Analysis',
                                variability_tab, title_color='Blue',
                                visible=False,
                                key='-VARIABILITY_TAB-',
                                element_justification='center'),
                         sg.Tab('CHARGE',
                                charge_tab, title_color='Blue',
                                visible=False,
                                key='-CHARGE_TAB-',
                                element_justification='center'),
                         sg.Tab('Results',
                                results_tab,
                                title_color='Blue',
                                visible=False,
                                key='-RESULTS_TAB-',
                                element_justification='center')]],
                       tab_location='centertop',
                       title_color='Red',
                       tab_background_color='Purple',
                       selected_title_color='Green',
                       selected_background_color='Gray',
                       border_width=5)]]

# Naming and creating Window
window = sg.Window('Ring Modulator Simulator', tabgrp, finalize=True)

# Creating handles for main window objects to manipulate
graph = window['-GRAPH-']
graph_charge = window['-GRAPH_CHARGE-']
radius_warning = window['-RADIUS_WARNING-']
gap_warning = window['-GAP_WARNING-']
slab_warning = window['-SLAB_WARNING-']
wg_height_warning = window['-WAVEGUIDE_HEIGHT_WARNING-']
wg_width_warning = window['-WAVEGUIDE_WIDTH_WARNING-']
coupling_length_warning = window['-COUPLING_LENGTH_WARNING-']
coupling_box = window['-COUPLING_LENGTH-']
run_sim = window['-RUN-']
charge_window = window['-CHARGE_TAB-']
variability_window = window['-VARIABILITY_TAB-']
results_window = window['-RESULTS_TAB-']
charge_file = window['-CHARGE_FILE-']
browse_button = window['-BROWSE-']
run_charge = window['-RUN_CHARGE-']
corner_analysis = window['-CORNER_ANALYSIS-']
propagation_loss_box = window['-PROP_LOSS-']
propagation_loss_warning = window['-PROP_LOSS_WARNING-']
corner_analysis_warning = window['-CORNER_ANALYSIS_WARNING-']
gap_box = window['-GAP-']

# Creating handles for result tabs
CC_button = window['-CC-']
NEFF_button = window['-NEFF-']
Tranmission_button = window['-T-']
NRZ_button = window['-NRZ-']
PAM4_button = window['-PAM4-']
Phase_button = window['-PN_RESULT-']

# Creating handles for the PN junction plot options
Phase_plot_button = window['-PHASE-']
Capacitance_plot_button = window['-CAPACITANCE-']
Resistance_plot_button = window['-RESISTANCE-']
Bandwidth_plot_button = window['-BANDWIDTH-']

# Creating handels for the corner analysis result options
Nominal_plot = window['-NOMINAL-']
BL_plot = window['-CORNER_BL-']
BR_plot = window['-CORNER_BR-']
TL_plot = window['-CORNER_TL-']
TR_plot = window['-CORNER_TR-']

# Creating handles for variability checkboxes
waveguide_height_var_box = window['-VARIABILITY_WAVEGUIDE_HEIGHT-']
waveguide_width_var_box = window['-VARIABILITY_WAVEGUIDE_WIDTH-']
slab_height_var_box = window['-VARIABILITY_SLAB_HEIGHT-']
doping_concentration_var_box = window['-VARIABILITY_DOPING_CONCENTRATION-']

# Creating handle for variability list text
variability_variables_text = window['-CURRENT_VARIABLES-']

# Creating handles for variability input warnings
wg_height_range_warning = window['-WAVEGUIDE_HEIGHT_RANGE_WARNING-']
wg_width_range_warning = window['-WAVEGUIDE_WIDTH_RANGE_WARNING-']
slab_height_range_warning = window['-SLAB_HEIGHT_RANGE_WARNING-']
doping_concentration_range_warning = window['-DOPING_CONCENTRATION_RANGE_WARNING-']


# Creating handles for the scalar result displays
Result1 = window['-RESULT1-']
Result2 = window['-RESULT2-']
Result3 = window['-RESULT3-']
Result4 = window['-RESULT4-']
Result5 = window['-RESULT5-']

# creating handle for Eye diagram update button, inputs and warnings
Eye_button = window['-EYEBUTTON-']
Laser_Input = window['-LASER-']
VMin_Input = window['-VMIN-']
VMax_Input = window['-VMAX-']
Bitrate_Input = window['-BITRATE-']
laser_warning = window['-LASER_WARNING-']
vmin_warning = window['-VMIN_WARNING-']
vmax_warning = window['-VMAX_WARNING-']
bitrate_warning = window['-BITRATE_WARNING-']
charge_file_warning = window['-CHARGE_FILE_WARNING-']
non_linearity_correction = window['-STATIC_NONLIN-']

# Creating handles for CHARGE
p_width_core_warning = window['-P_WIDTH_CORE_WARNING-']
n_width_core_warning = window['-N_WIDTH_CORE_WARNING-']
p_width_slab_warning = window['-P_WIDTH_SLAB_WARNING-']
n_width_slab_warning = window['-N_WIDTH_SLAB_WARNING-']
pp_width_warning = window['-P+_WIDTH_WARNING-']
np_width_warning = window['-N+_WIDTH_WARNING-']
ppp_width_warning = window['-P++_WIDTH_WARNING-']
npp_width_warning = window['-N++_WIDTH_WARNING-']
vmin_charge_warning = window['-VMIN_CHARGE_WARNING-']
vmax_charge_warning = window['-VMAX_CHARGE_WARNING-']
save_name_warning = window['-SAVE_NAME_WARNING-']
p_width_core_box = window['-P_WIDTH_CORE-']
n_width_core_box = window['-N_WIDTH_CORE-']
p_width_slab_box = window['-P_WIDTH_SLAB-']
n_width_slab_box = window['-N_WIDTH_SLAB-']
pp_width_box = window['-P+_WIDTH-']
np_width_box = window['-N+_WIDTH-']
ppp_width_box = window['-P++_WIDTH-']
npp_width_box = window['-N++_WIDTH-']
p_width_core_text = window['-P_WIDTH_CORE_TEXT-']
n_width_core_text = window['-N_WIDTH_CORE_TEXT-']
p_width_slab_text = window['-P_WIDTH_SLAB_TEXT-']
n_width_slab_text = window['-N_WIDTH_SLAB_TEXT-']
pp_width_text = window['-P+_WIDTH_TEXT-']
np_width_text = window['-N+_WIDTH_TEXT-']
ppp_width_text = window['-P++_WIDTH_TEXT-']
npp_width_text = window['-N++_WIDTH_TEXT-']
lateral_button = window['-LATERAL-']
L_shapped_PN_button = window['-L_SHAPED-']

# Drawing placeholder ring to illustrate what the user is attempting to fill out

# Drawing Circle
circle = graph.DrawCircle((x0, y0), drawing_radius, fill_color='',
                          line_color='black', line_width=bus_width/2*1.25)

# Drawing Bus
bus = graph.DrawRectangle((x0-bus_length/2, y0-bus_width/2-drawing_radius-drawing_gap),
                          (x0 + bus_length/2, y0+bus_width/2-drawing_radius-drawing_gap),
                          fill_color='black', line_color="black")

# Drawing measurement lines and displays, coupler length deleted since not the default view
radius_line = graph.DrawLine((x0, y0), (x0+drawing_radius, y0), color="blue", width=5)
radius_text = graph.DrawText('?? [um]', (x0+120, y0+25), color="blue",
                             font=None, angle=0, text_location="center")
gap_line = graph.DrawLine((x0, y0-drawing_radius),
                          (x0, y0-drawing_radius-drawing_gap), color="blue", width=5)
gap_text = graph.DrawText('?? [nm]', (x0+75, y0-drawing_radius-drawing_gap/2),
                          color="blue", font=None, angle=0, text_location="center")
coupling_length_line = graph.DrawLine(
    (x0, y0-drawing_radius), (x0, y0-drawing_radius), color="blue", width=5)
coupling_length_text = graph.DrawText(
    '?? [um]', (x0+50, y0-drawing_radius), color="blue", font=None, angle=0, text_location="center")
graph.delete_figure(coupling_length_line)
graph.delete_figure(coupling_length_text)

# Drawing Arc and deleting it since it is not the default view
left_arc = graph.DrawArc((x0-coupling_region/2-drawing_radius, y0-drawing_radius-1),
                         (x0+coupling_region / 3, y0+drawing_radius+1), 180, 90, style='arc',
                         arc_color="black", line_width=9, fill_color=None)
right_arc = graph.DrawArc((x0+coupling_region/2+drawing_radius, y0-drawing_radius-1),
                          (x0-coupling_region / 3, y0+drawing_radius+1), 180, -90, style='arc',
                          arc_color="black", line_width=9, fill_color=None)
graph.delete_figure(right_arc)
graph.delete_figure(left_arc)

# Drawing coupler region extension and deleting since they are not the default view
top_coupling = graph.DrawRectangle((x0-coupling_region/2, y0-bus_width/2+drawing_radius),
                                   (x0+coupling_region/2, y0+bus_width/2+drawing_radius),
                                   fill_color='black', line_color="black")
bot_coupling = graph.DrawRectangle((x0-coupling_region/2, y0-bus_width/2-drawing_radius),
                                   (x0+coupling_region/2, y0+bus_width/2-drawing_radius),
                                   fill_color='black', line_color="black")
graph.delete_figure(top_coupling)
graph.delete_figure(bot_coupling)

# Updating graph to display what I have just added to the canvas
graph.Update()

# Creating empty PN-junction drawing to show user what they are filling in
draw.CreateWaveguideCrosssection(graph_charge)
draw.CreateWaveguideMeasurementLines(graph_charge)
draw.CreateWaveguideMeasurementLabels(graph_charge)
draw.CreateWaveguideDopantLabels_AMF(graph_charge)


# Creating boolea Boolean trackers to see what data is correctly provided

# Physical parameters
bool_radius = 0
bool_gap = 0
bool_slab = 0
bool_coupling_length = 1
bool_critical_couple = 0


# Simualtion parameters
bool_define_charge = 0
bool_charge_file = 0
bool_charge_params = 0

# Variability analysis booleans
bool_variability = 0
bool_waveguide_height_variability = 0
bool_waveguide_width_variability = 0
bool_slab_height_variability = 0
bool_doping_concentration_variability = 0
bool_corner_analyis_ready = 0

# Creating Variability Dictionairy
Variability_Dict = {}

# Adding variability counter to limit simulation space to 2 currently
variability_dimensions = 2
selected_dimensions = 0
setting1 = ''
setting2 = ''

# Secondary inputs
bool_laser = 0
bool_vmin = 0
bool_vmax = 0
bool_bitrate = 0
bool_NRZ = 0
bool_PAM4 = 0

# Foundry tracker to prevent radio button double input
foundry_tracker = 'AMF'

# Before starting the app, database integrity is inforced
database.CheckDatabaseIntegrity()


# Creating the event handler
while True:
    # Constantly tracks events and displays for debugging
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Update Ring Parameters':
        # This event handles the verification process then displays the run button if it passes

        # Verifying radius
        bool_radius, Radius, radius_text = verify.CheckRadius(
            x0, y0, values, graph, radius_text, radius_warning)

        # Verifying gap
        bool_gap, Gap, gap_text = verify.CheckGap(
            x0, y0, values, graph, gap_text, gap_warning,
            drawing_radius, drawing_gap, bool_critical_couple, gap_box)

        # Verifying slab height
        bool_slab, slab_height = verify.CheckSlab(values, slab_warning)

        # Verifying coupling length
        [bool_coupling_length, CouplingLength, circle, left_arc, right_arc, top_coupling,
         bot_coupling, radius_text, radius_line] = verify.CheckCouplingLength(
            x0, y0, values, graph, coupling_length_text, coupling_length_line,
            coupling_region, drawing_radius, coupling_length_warning, circle, top_coupling,
            bot_coupling, bus_width, left_arc, right_arc, radius_text, radius_line, radius_warning,
            bool_radius, bool_gap, Radius, coupling_box, bool_critical_couple)

        # Verify waveguide height
        bool_wg_height, wg_height = verify.CheckWaveguideHeight(values, wg_height_warning)

        # Verify waveguide width
        bool_wg_width, wg_width = verify.CheckWaveguideWidth(values, wg_width_warning)

        # Verifying optical band
        LambdaStart, LambdaEnd, band = verify.CheckBand(values)

        # Verifying charge selection type
        bool_define_charge = verify.CheckCharge(values)

        # Verifying charge file
        bool_load_charge, CHARGE_file = verify.CheckChargeFile(
            values, charge_file_warning, bool_define_charge)

        # Verify if variability analysis is being performed
        bool_variability = verify.check_for_variability_analysis(
            values, corner_analysis_warning)

        # Verify if PN junction results are present for each corner in the simulation space
        if bool_variability:
            (bool_charge_corner_BL,
             bool_charge_corner_BR,
             bool_charge_corner_TL,
             bool_charge_corner_TR,
             CHARGE_file_BL,
             CHARGE_file_BR,
             CHARGE_file_TL,
             CHARGE_file_TR) = verify.check_for_variability_analysis_charge(values)

        # Verifying propagation loss
        bool_prop_loss, prop_loss = verify.CheckPropLoss(
            values, propagation_loss_warning)

        # Using different name for clarity, this determines if the charge is ready to use
        # Regardless if it is loaded or defined
        if bool_load_charge == 1:
            bool_charge = 1
        else:
            bool_charge = 0

        results_window.Update(visible=False)

    elif event == 'Update CHARGE Parameters':
        # This event handles verifying the charge parameters and enabling the run button

        # Verifying charge paramters
        [bool_charge_params, p_width_core, n_width_core, p_width_slab, n_width_slab,
         pp_width, np_width, ppp_width, npp_width, vmin_charge, vmax_charge, save_name,
         bias, foundry, PN_Type] = verify.CheckChargeParameters(values, graph_charge,
                                                                p_width_core_warning,
                                                                n_width_core_warning,
                                                                p_width_slab_warning,
                                                                n_width_slab_warning,
                                                                pp_width_warning,
                                                                np_width_warning,
                                                                ppp_width_warning,
                                                                npp_width_warning,
                                                                vmin_charge_warning,
                                                                vmax_charge_warning,
                                                                save_name_warning)

        # If parameters are supplied properly, then enable the charge run button
        if bool_charge_params == 1:
            run_charge.Update(visible=True)
        else:
            run_charge.Update(visible=False)

    elif event == '-VARIABILITY_WAVEGUIDE_HEIGHT-':
        if bool_waveguide_height_variability:
            bool_waveguide_height_variability = 0
            selected_dimensions -= 1
            wg_height_range_warning.Update('', visible=False)
        else:
            if selected_dimensions < variability_dimensions:
                bool_waveguide_height_variability = 1
                selected_dimensions += 1
            else:
                waveguide_height_var_box.Update(False)
    elif event == '-VARIABILITY_WAVEGUIDE_WIDTH-':
        if bool_waveguide_width_variability:
            bool_waveguide_width_variability = 0
            selected_dimensions -= 1
            wg_width_range_warning.Update('', visible=False)
        else:
            if selected_dimensions < variability_dimensions:
                bool_waveguide_width_variability = 1
                selected_dimensions += 1
            else:
                waveguide_width_var_box.Update(False)
    elif event == '-VARIABILITY_SLAB_HEIGHT-':
        if bool_slab_height_variability:
            bool_slab_height_variability = 0
            selected_dimensions -= 1
            slab_height_range_warning.Update('', visible=False)
        else:
            if selected_dimensions < variability_dimensions:
                bool_slab_height_variability = 1
                selected_dimensions += 1
            else:
                slab_height_var_box.Update(False)
    elif event == '-VARIABILITY_DOPING_CONCENTRATION-':
        if bool_doping_concentration_variability:
            bool_doping_concentration_variability = 0
            selected_dimensions -= 1
            doping_concentration_range_warning.Update('', visible=False)
        else:
            if selected_dimensions < variability_dimensions:
                bool_doping_concentration_variability = 1
                selected_dimensions += 1
            else:
                doping_concentration_var_box.Update(False)
    elif event == '-UPDATE_VARIABILITY-':

        # Creating Dictionary for variability analysis for easy reading and manipulation
        # Convention is to put ID for each new variable so the system detects it
        # Then supply the Range, Warning text, and units after Using the same name as in the ID
        Variability_Dict = {
            "[ID] Waveguide Height": bool_waveguide_height_variability,
            "Waveguide Height Range": 0,
            "Waveguide Height Warning": wg_height_range_warning,
            "Waveguide Height Units": 'nm',
            "[ID] Waveguide Width": bool_waveguide_width_variability,
            "Waveguide Width Range": 0,
            "Waveguide Width Warning": wg_width_range_warning,
            "Waveguide Width Units": 'nm',
            "[ID] Slab Height": bool_slab_height_variability,
            "Slab Height Range": 0,
            "Slab Height Warning": slab_height_range_warning,
            "Slab Height Units": 'nm',
            "[ID] Doping Concentration": bool_doping_concentration_variability,
            "Doping Concentration Range": 0,
            "Doping Concentration Warning": doping_concentration_range_warning,
            "Doping Concentration Units": '%',
        }

        Variability_Dict = verify.check_variability_range(
            values, Variability_Dict)

        # Checking which variability setting has been seelcted and updating display
        variability_display_text, bool_corner_analyis_ready = verify.update_variability(
            values, Variability_Dict, selected_dimensions, corner_analysis_warning)

        # Updating warning message for variability analysis checkbox
        variability_variables_text.Update(variability_display_text)

        # Defining variables to either be used in the charge simulation or ring

    elif event == '-RUN_CHARGE-':
        # This event handles the charge simulation execution

        # Converting to SI units in case it wasnt already done
        Radius_SI = round(Radius*1e-6, 10)
        slab_height_SI = round(slab_height*1e-9, 10)
        CouplingLength_SI = round(CouplingLength*1e-6, 10)
        wg_width_SI = round(wg_width*1e-9, 10)
        wg_height_SI = round(wg_height*1e-9, 10)

        try:
            # Simulating charge distribution
            CHARGE_FILE, SimRun = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                             p_width_slab, n_width_slab,
                                                             pp_width, np_width,
                                                             ppp_width, npp_width,
                                                             slab_height_SI, Radius_SI,
                                                             CouplingLength_SI, vmin_charge,
                                                             vmax_charge, save_name,
                                                             bias, band, foundry, PN_Type,
                                                             wg_height_SI, wg_width_SI)
            if values['-CORNER_ANALYSIS-']:
                # Repeating 4 times for all corners
                if not SimRun:
                    save_name = CHARGE_FILE

                # Intializing variability analysis variables that can be passed to charge solver
                var_wg_height_SI = [round(wg_height_SI -
                                          Variability_Dict['Waveguide Height Range']*1e-9, 10),
                                    round(wg_height_SI +
                                          Variability_Dict['Waveguide Height Range']*1e-9, 10)]
                var_wg_width_SI = [round(wg_width_SI -
                                         Variability_Dict['Waveguide Width Range']*1e-9, 10),
                                   round(wg_width_SI +
                                         Variability_Dict['Waveguide Width Range']*1e-9, 10)]
                var_slab_height_SI = [round(slab_height_SI -
                                            Variability_Dict['Slab Height Range']*1e-9, 10),
                                      round(slab_height_SI +
                                            Variability_Dict['Slab Height Range']*1e-9, 10)]
                var_doping_error = [-Variability_Dict['Doping Concentration Range'],
                                    Variability_Dict['Doping Concentration Range']]

                # Since there are 4 variables possible for the variability analysis and we are doing
                # subsets of 2, there exists 6 possible combinations, therefore six cases are shown
                # This could be coded in a cleaner way if the functions were rewritten, TODO()

                # Listing cases.
                # Case: 1 = wg_height x wg_width
                # Case: 2 = wg_height x slab_height
                # Case: 3 = wg_height x doping_concentration
                # Case: 4 = wg_width x slab_height
                # Case: 5 = wg_width x doping_concentration
                # Case: 6 = slab_height x doping_concentration

                # Case 1
                if (Variability_Dict['[ID] Waveguide Height'] and
                        Variability_Dict['[ID] Waveguide Width']):

                    # Constructing bottom left corner
                    identifier_BL = ('_wg_height-' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_wg_width-' + str(Variability_Dict['Waveguide Width Range']) +
                                     Variability_Dict['Waveguide Width Units'])
                    identifier_BL = identifier_BL.replace('.', 'p')
                    CHARGE_FILE_BL, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   slab_height_SI, Radius_SI,
                                                                   CouplingLength_SI,
                                                                   vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_BL,
                                                                   bias, band, foundry,
                                                                   PN_Type,
                                                                   var_wg_height_SI[0],
                                                                   var_wg_width_SI[0])

                    # Constructing bottom right corner
                    identifier_BR = ('_wg_height+' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_wg_width-' + str(Variability_Dict['Waveguide Width Range']) +
                                     Variability_Dict['Waveguide Width Units'])
                    identifier_BR = identifier_BR.replace('.', 'p')
                    CHARGE_FILE_BR, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   slab_height_SI, Radius_SI,
                                                                   CouplingLength_SI, vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_BR,
                                                                   bias, band, foundry, PN_Type,
                                                                   var_wg_height_SI[0],
                                                                   var_wg_width_SI[1])

                    # Constructing bottom left corner
                    identifier_TL = ('_wg_height-' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_wg_width+' + str(Variability_Dict['Waveguide Width Range']) +
                                     Variability_Dict['Waveguide Width Units'])
                    identifier_TL = identifier_TL.replace('.', 'p')
                    CHARGE_FILE_TL, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   slab_height_SI, Radius_SI,
                                                                   CouplingLength_SI, vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_TL,
                                                                   bias, band, foundry, PN_Type,
                                                                   var_wg_height_SI[1],
                                                                   var_wg_width_SI[0])

                    # Constructing bottom left corner
                    identifier_TR = ('_wg_height+' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_wg_width+' + str(Variability_Dict['Waveguide Width Range']) +
                                     Variability_Dict['Waveguide Width Units'])
                    identifier_TR = identifier_TR.replace('.', 'p')
                    CHARGE_FILE_TR, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   slab_height_SI, Radius_SI,
                                                                   CouplingLength_SI, vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_TR,
                                                                   bias, band, foundry, PN_Type,
                                                                   var_wg_height_SI[1],
                                                                   var_wg_width_SI[1])
                # Case 2
                elif (Variability_Dict['[ID] Waveguide Height'] and
                        Variability_Dict['[ID] Slab Height']):

                    # Constructing bottom left corner
                    identifier_BL = ('_wg_height-' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_slab_height-' + str(Variability_Dict['Slab Height Range']) +
                                     Variability_Dict['Slab Height Units'])
                    identifier_BL = identifier_BL.replace('.', 'p')
                    CHARGE_FILE_BL, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   var_slab_height_SI[0], Radius_SI,
                                                                   CouplingLength_SI,
                                                                   vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_BL,
                                                                   bias, band, foundry,
                                                                   PN_Type,
                                                                   var_wg_height_SI[0],
                                                                   wg_width_SI)

                    # Constructing bottom right corner
                    identifier_BR = ('_wg_height+' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_slab_height-' + str(Variability_Dict['Slab Height Range']) +
                                     Variability_Dict['Slab Height Units'])
                    identifier_BR = identifier_BR.replace('.', 'p')
                    CHARGE_FILE_BR, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   var_slab_height_SI[1], Radius_SI,
                                                                   CouplingLength_SI, vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_BR,
                                                                   bias, band, foundry, PN_Type,
                                                                   var_wg_height_SI[0],
                                                                   wg_width_SI)

                    # Constructing bottom left corner
                    identifier_TL = ('_wg_height-' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_slab_height+' + str(Variability_Dict['Slab Height Range']) +
                                     Variability_Dict['Slab Height Units'])
                    identifier_TL = identifier_TL.replace('.', 'p')
                    CHARGE_FILE_TL, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   var_slab_height_SI[0], Radius_SI,
                                                                   CouplingLength_SI, vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_TL,
                                                                   bias, band, foundry, PN_Type,
                                                                   var_wg_height_SI[1],
                                                                   wg_width_SI)

                    # Constructing bottom left corner
                    identifier_TR = ('_wg_height+' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_slab_height+' + str(Variability_Dict['Slab Height Range']) +
                                     Variability_Dict['Slab Height Units'])
                    identifier_TR = identifier_TR.replace('.', 'p')
                    CHARGE_FILE_TR, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   var_slab_height_SI[1], Radius_SI,
                                                                   CouplingLength_SI, vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_TR,
                                                                   bias, band, foundry, PN_Type,
                                                                   var_wg_height_SI[1],
                                                                   wg_width_SI)
                # Case 3
                elif (Variability_Dict['[ID] Waveguide Height'] and
                        Variability_Dict['[ID] Doping Concentration']):

                    # Constructing bottom left corner
                    identifier_BL = ('_wg_height-' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_doping-' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])
                    identifier_BL = identifier_BL.replace('.', 'p')
                    CHARGE_FILE_BL, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   slab_height_SI, Radius_SI,
                                                                   CouplingLength_SI,
                                                                   vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_BL,
                                                                   bias, band, foundry,
                                                                   PN_Type,
                                                                   var_wg_height_SI[0],
                                                                   wg_width_SI,
                                                                   var_doping_error[0])

                    # Constructing bottom right corner
                    identifier_BR = ('_wg_height+' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_doping-' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])
                    identifier_BR = identifier_BR.replace('.', 'p')
                    CHARGE_FILE_BR, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   slab_height_SI, Radius_SI,
                                                                   CouplingLength_SI, vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_BR,
                                                                   bias, band, foundry, PN_Type,
                                                                   var_wg_height_SI[0],
                                                                   wg_width_SI,
                                                                   var_doping_error[1])

                    # Constructing bottom left corner
                    identifier_TL = ('_wg_height-' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_doping+' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])
                    identifier_TL = identifier_TL.replace('.', 'p')
                    CHARGE_FILE_TL, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   slab_height_SI, Radius_SI,
                                                                   CouplingLength_SI, vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_TL,
                                                                   bias, band, foundry, PN_Type,
                                                                   var_wg_height_SI[1],
                                                                   wg_width_SI,
                                                                   var_doping_error[0])

                    # Constructing bottom left corner
                    identifier_TR = ('_wg_height+' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_doping+' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])
                    identifier_TR = identifier_TR.replace('.', 'p')
                    CHARGE_FILE_TR, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   slab_height_SI, Radius_SI,
                                                                   CouplingLength_SI, vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_TR,
                                                                   bias, band, foundry, PN_Type,
                                                                   var_wg_height_SI[1],
                                                                   wg_width_SI,
                                                                   var_doping_error[1])
                # Case 4
                elif (Variability_Dict['[ID] Waveguide Width'] and
                        Variability_Dict['[ID] Slab Height']):

                    # Constructing bottom left corner
                    identifier_BL = ('_wg_width-' + str(Variability_Dict['Waveguide Width Range'])
                                     + Variability_Dict['Waveguide Width Units'] +
                                     '_slab_height-' + str(Variability_Dict['Slab Height Range']) +
                                     Variability_Dict['Slab Height Units'])
                    identifier_BL = identifier_BL.replace('.', 'p')
                    CHARGE_FILE_BL, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   var_slab_height_SI[0], Radius_SI,
                                                                   CouplingLength_SI,
                                                                   vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_BL,
                                                                   bias, band, foundry,
                                                                   PN_Type,
                                                                   wg_height_SI,
                                                                   var_wg_width_SI[0])

                    # Constructing bottom right corner
                    identifier_BR = ('_wg_width+' + str(Variability_Dict['Waveguide Width Range'])
                                     + Variability_Dict['Waveguide Width Units'] +
                                     '_slab_height-' + str(Variability_Dict['Slab Height Range']) +
                                     Variability_Dict['Slab Height Units'])
                    identifier_BR = identifier_BR.replace('.', 'p')
                    CHARGE_FILE_BR, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   var_slab_height_SI[1], Radius_SI,
                                                                   CouplingLength_SI, vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_BR,
                                                                   bias, band, foundry, PN_Type,
                                                                   wg_height_SI,
                                                                   var_wg_width_SI[0])

                    # Constructing bottom left corner
                    identifier_TL = ('_wg_width-' + str(Variability_Dict['Waveguide Width Range'])
                                     + Variability_Dict['Waveguide Width Units'] +
                                     '_slab_height+' + str(Variability_Dict['Slab Height Range']) +
                                     Variability_Dict['Slab Height Units'])
                    identifier_TL = identifier_TL.replace('.', 'p')
                    CHARGE_FILE_TL, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   var_slab_height_SI[0], Radius_SI,
                                                                   CouplingLength_SI, vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_TL,
                                                                   bias, band, foundry, PN_Type,
                                                                   wg_height_SI,
                                                                   var_wg_width_SI[1])

                    # Constructing bottom left corner
                    identifier_TR = ('_wg_width+' + str(Variability_Dict['Waveguide Width Range'])
                                     + Variability_Dict['Waveguide Width Units'] +
                                     '_slab_height+' + str(Variability_Dict['Slab Height Range']) +
                                     Variability_Dict['Slab Height Units'])
                    identifier_TR = identifier_TR.replace('.', 'p')
                    CHARGE_FILE_TR, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   var_slab_height_SI[1], Radius_SI,
                                                                   CouplingLength_SI, vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_TR,
                                                                   bias, band, foundry, PN_Type,
                                                                   wg_height_SI,
                                                                   var_wg_width_SI[1])
                # Case 5
                elif (Variability_Dict['[ID] Waveguide Width'] and
                        Variability_Dict['[ID] Doping Concentration']):

                    # Constructing bottom left corner
                    identifier_BL = ('_wg_width-' + str(Variability_Dict['Waveguide Width Range'])
                                     + Variability_Dict['Waveguide Width Units'] +
                                     '_doping-' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])
                    identifier_BL = identifier_BL.replace('.', 'p')
                    CHARGE_FILE_BL, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   slab_height_SI, Radius_SI,
                                                                   CouplingLength_SI,
                                                                   vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_BL,
                                                                   bias, band, foundry,
                                                                   PN_Type,
                                                                   wg_height_SI,
                                                                   var_wg_width_SI[0],
                                                                   var_doping_error[0])

                    # Constructing bottom right corner
                    identifier_BR = ('_wg_width+' + str(Variability_Dict['Waveguide Width Range'])
                                     + Variability_Dict['Waveguide Width Units'] +
                                     '_doping-' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])
                    identifier_BR = identifier_BR.replace('.', 'p')
                    CHARGE_FILE_BR, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   slab_height_SI, Radius_SI,
                                                                   CouplingLength_SI, vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_BR,
                                                                   bias, band, foundry, PN_Type,
                                                                   wg_height_SI,
                                                                   var_wg_width_SI[0],
                                                                   var_doping_error[1])

                    # Constructing bottom left corner
                    identifier_TL = ('_wg_width-' + str(Variability_Dict['Waveguide Width Range'])
                                     + Variability_Dict['Waveguide Width Units'] +
                                     '_doping+' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])
                    identifier_TL = identifier_TL.replace('.', 'p')
                    CHARGE_FILE_TL, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   slab_height_SI, Radius_SI,
                                                                   CouplingLength_SI, vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_TL,
                                                                   bias, band, foundry, PN_Type,
                                                                   wg_height_SI,
                                                                   var_wg_width_SI[1],
                                                                   var_doping_error[0])

                    # Constructing bottom left corner
                    identifier_TR = ('_wg_width+' + str(Variability_Dict['Waveguide Width Range'])
                                     + Variability_Dict['Waveguide Width Units'] +
                                     '_doping+' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])
                    identifier_TR = identifier_TR.replace('.', 'p')
                    CHARGE_FILE_TR, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   slab_height_SI, Radius_SI,
                                                                   CouplingLength_SI, vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_TR,
                                                                   bias, band, foundry, PN_Type,
                                                                   wg_height_SI,
                                                                   var_wg_width_SI[1],
                                                                   var_doping_error[1])
                # Case 6
                elif (Variability_Dict['[ID] Slab Height'] and
                        Variability_Dict['[ID] Doping Concentration']):

                    # Constructing bottom left corner
                    identifier_BL = ('_slab_height-' + str(Variability_Dict['Slab Height Range'])
                                     + Variability_Dict['Slab Height Units'] +
                                     '_doping-' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])
                    identifier_BL = identifier_BL.replace('.', 'p')
                    CHARGE_FILE_BL, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   var_slab_height_SI[0], Radius_SI,
                                                                   CouplingLength_SI,
                                                                   vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_BL,
                                                                   bias, band, foundry,
                                                                   PN_Type,
                                                                   wg_height_SI,
                                                                   wg_width_SI,
                                                                   var_doping_error[0])

                    # Constructing bottom right corner
                    identifier_BR = ('_slab_height+' + str(Variability_Dict['Slab Height Range'])
                                     + Variability_Dict['Slab Height Units'] +
                                     '_doping-' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])
                    identifier_BR = identifier_BR.replace('.', 'p')
                    CHARGE_FILE_BR, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   var_slab_height_SI[0], Radius_SI,
                                                                   CouplingLength_SI, vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_BR,
                                                                   bias, band, foundry, PN_Type,
                                                                   wg_height_SI,
                                                                   wg_width_SI,
                                                                   var_doping_error[1])

                    # Constructing bottom left corner
                    identifier_TL = ('_slab_height-' + str(Variability_Dict['Slab Height Range'])
                                     + Variability_Dict['Slab Height Units'] +
                                     '_doping+' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])
                    identifier_TL = identifier_TL.replace('.', 'p')
                    CHARGE_FILE_TL, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   var_slab_height_SI[1], Radius_SI,
                                                                   CouplingLength_SI, vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_TL,
                                                                   bias, band, foundry, PN_Type,
                                                                   wg_height_SI,
                                                                   wg_width_SI,
                                                                   var_doping_error[0])

                    # Constructing bottom left corner
                    identifier_TR = ('_slab_height+' + str(Variability_Dict['Slab Height Range'])
                                     + Variability_Dict['Slab Height Units'] +
                                     '_doping+' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])
                    identifier_TR = identifier_TR.replace('.', 'p')
                    CHARGE_FILE_TR, _ = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                                   p_width_slab, n_width_slab,
                                                                   pp_width, np_width,
                                                                   ppp_width, npp_width,
                                                                   var_slab_height_SI[1], Radius_SI,
                                                                   CouplingLength_SI, vmin_charge,
                                                                   vmax_charge,
                                                                   save_name + identifier_TR,
                                                                   bias, band, foundry, PN_Type,
                                                                   wg_height_SI,
                                                                   wg_width_SI,
                                                                   var_doping_error[1])

            # Set bool to false to allow for verifcation process to double check it is correct
            bool_charge = 0

            # Display pop-up window to user explaining results
            if SimRun:
                sg.Popup(
                    'PN junction succesffuly simulated. Select the file in "Import CHARGE" in the'
                    ' "Simulation" tab to use', keep_on_top=True)

            else:
                sg.Popup(
                    'Database record already exists for this configuration under the following'
                    ' filename: ' + CHARGE_FILE + ".mat", keep_on_top=True)

        except ValueError as e:
            print("Encountered the following error while attempting to simulate the PN junction")
            print(e)

    elif event == '-RUN-':
        try:

            # This event runs the simulation depending on the supplied settings
            print("Running Simulation")
            print("Current Physical Parameters: R=" + str(Radius) +
                  "[um]_G=" + str(Gap) + "[nm]_Slab=" + str(slab_height) +
                  "[nm]_L=" + str(CouplingLength) + "[um]")

            # Converting to SI units for saving
            Radius_SI = round(Radius*1e-6, 10)
            slab_height_SI = round(slab_height*1e-9, 10)
            CouplingLength_SI = round(CouplingLength*1e-6, 10)
            wg_width_SI = round(wg_width*1e-9, 10)
            wg_height_SI = round(wg_height*1e-9, 10)

            # Gap is unique since it can be swept for critical coupling
            if bool_critical_couple == 1:
                Gap_SI = np.linspace(100e-9, 600e-9, 11)

                # This executes the critical coupling sweep
                saved_results = sim.CriticalCouplingAutomation(
                    Radius_SI, Gap_SI, slab_height_SI,
                    CouplingLength_SI, LambdaStart, LambdaEnd,
                    band, CHARGE_file, prop_loss,
                    wg_height_SI, wg_width_SI)

                gap_box.update(str(round(saved_results.CriticalCoupleGap/1e-9)))
            else:
                Gap_SI = round(Gap*1e-9, 10)

                # This executes a single iteration of the script
                saved_results = sim.runSimulation(
                    Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                    LambdaStart, LambdaEnd, band, CHARGE_file, prop_loss,
                    wg_height_SI, wg_width_SI)

            if values['-CORNER_ANALYSIS-']:
                # Executing 4 extra simulations
                # The 2 paramters varied are depicted in the the variability dictionairy
                # Intializing variability analysis variables that can be passed to charge solver
                var_wg_height_SI = [round(wg_height_SI -
                                          Variability_Dict['Waveguide Height Range']*1e-9, 10),
                                    round(wg_height_SI +
                                          Variability_Dict['Waveguide Height Range']*1e-9, 10)]
                var_wg_width_SI = [round(wg_width_SI -
                                         Variability_Dict['Waveguide Width Range']*1e-9, 10),
                                   round(wg_width_SI +
                                         Variability_Dict['Waveguide Width Range']*1e-9, 10)]
                var_slab_height_SI = [round(slab_height_SI -
                                            Variability_Dict['Slab Height Range']*1e-9, 10),
                                      round(slab_height_SI +
                                            Variability_Dict['Slab Height Range']*1e-9, 10)]
                var_doping_error = [-Variability_Dict['Doping Concentration Range'],
                                    Variability_Dict['Doping Concentration Range']]

                # Since there are 4 variables possible for the variability analysis and we are doing
                # subsets of 2, there exists 6 possible combinations, therefore six cases are shown
                # This could be coded in a cleaner way if the functions were rewritten, TODO()

                # Listing cases.
                # Case: 1 = wg_height x wg_width
                # Case: 2 = wg_height x slab_height
                # Case: 3 = wg_height x doping_concentration
                # Case: 4 = wg_width x slab_height
                # Case: 5 = wg_width x doping_concentration
                # Case: 6 = slab_height x doping_concentration

                # Case 1
                if (Variability_Dict['[ID] Waveguide Height'] and
                        Variability_Dict['[ID] Waveguide Width']):

                    # Defining identifiers to locate charge simulation files for corners
                    identifier_BL = ('_wg_height-' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_wg_width-' + str(Variability_Dict['Waveguide Width Range']) +
                                     Variability_Dict['Waveguide Width Units'])

                    identifier_BR = ('_wg_height+' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_wg_width-' + str(Variability_Dict['Waveguide Width Range']) +
                                     Variability_Dict['Waveguide Width Units'])

                    identifier_TL = ('_wg_height-' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_wg_width+' + str(Variability_Dict['Waveguide Width Range']) +
                                     Variability_Dict['Waveguide Width Units'])

                    identifier_TR = ('_wg_height+' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_wg_width+' + str(Variability_Dict['Waveguide Width Range']) +
                                     Variability_Dict['Waveguide Width Units'])

                    identifier_BL = identifier_BL.replace('.', 'p')
                    identifier_BR = identifier_BR.replace('.', 'p')
                    identifier_TL = identifier_TL.replace('.', 'p')
                    identifier_TR = identifier_TR.replace('.', 'p')

                    # Constucting path to file from name, this got a little convoluted
                    charge_file = str(CHARGE_file).split('\\')[-1]
                    charge_file = charge_file.split('.')[0]
                    CHARGE_file_BL = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_BL))
                    CHARGE_file_BR = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_BR))
                    CHARGE_file_TL = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_TL))
                    CHARGE_file_TR = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_TR))

                    if bool_critical_couple == 1:
                        saved_results_BL = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            var_wg_height_SI[0], var_wg_width_SI[0])
                        Gap_BL = round(saved_results_BL.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_BL = sim.runSimulation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            var_wg_height_SI[0], var_wg_width_SI[0])
                    if bool_critical_couple == 1:
                        saved_results_BR = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            var_wg_height_SI[0], var_wg_width_SI[1])
                        Gap_BR = round(saved_results_BR.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_BR = sim.runSimulation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BR, prop_loss,
                            var_wg_height_SI[0], var_wg_width_SI[1])
                    if bool_critical_couple == 1:
                        saved_results_TL = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            var_wg_height_SI[1], var_wg_width_SI[0])
                        Gap_TL = round(saved_results_TL.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_TL = sim.runSimulation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_TL, prop_loss,
                            var_wg_height_SI[1], var_wg_width_SI[0])
                    if bool_critical_couple == 1:
                        saved_results_TR = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            var_wg_height_SI[1], var_wg_width_SI[1])
                        Gap_TR = round(saved_results_TR.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_TR = sim.runSimulation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_TR, prop_loss,
                            var_wg_height_SI[1], var_wg_width_SI[1])
                # Case 2
                elif (Variability_Dict['[ID] Waveguide Height'] and
                        Variability_Dict['[ID] Slab Height']):

                    # Defining identifiers to locate charge simulation files for corners
                    identifier_BL = ('_wg_height-' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_slab_height-' + str(Variability_Dict['Slab Height Range']) +
                                     Variability_Dict['Slab Height Units'])

                    identifier_BR = ('_wg_height+' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_slab_height-' + str(Variability_Dict['Slab Height Range']) +
                                     Variability_Dict['Slab Height Units'])

                    identifier_TL = ('_wg_height-' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_slab_height+' + str(Variability_Dict['Slab Height Range']) +
                                     Variability_Dict['Slab Height Units'])

                    identifier_TR = ('_wg_height+' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_slab_height+' + str(Variability_Dict['Slab Height Range']) +
                                     Variability_Dict['Slab Height Units'])

                    identifier_BL = identifier_BL.replace('.', 'p')
                    identifier_BR = identifier_BR.replace('.', 'p')
                    identifier_TL = identifier_TL.replace('.', 'p')
                    identifier_TR = identifier_TR.replace('.', 'p')

                    # Constucting path to file from name, this got a little convoluted
                    charge_file = str(CHARGE_file).split('\\')[-1]
                    charge_file = charge_file.split('.')[0]
                    CHARGE_file_BL = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_BL))
                    CHARGE_file_BR = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_BR))
                    CHARGE_file_TL = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_TL))
                    CHARGE_file_TR = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_TR))

                    if bool_critical_couple == 1:
                        saved_results_BL = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, var_slab_height_SI[0], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            var_wg_height_SI[0], wg_width_SI)
                        Gap_BL = round(saved_results_BL.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_BL = sim.runSimulation(
                            Radius_SI, Gap_SI, var_slab_height_SI[0], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            var_wg_height_SI[0], wg_width_SI)
                    if bool_critical_couple == 1:
                        saved_results_BR = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, var_slab_height_SI[1], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            var_wg_height_SI[0], wg_width_SI)
                        Gap_BR = round(saved_results_BR.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_BR = sim.runSimulation(
                            Radius_SI, Gap_SI, var_slab_height_SI[1], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BR, prop_loss,
                            var_wg_height_SI[0], wg_width_SI)
                    if bool_critical_couple == 1:
                        saved_results_TL = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, var_slab_height_SI[0], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            var_wg_height_SI[1], wg_width_SI)
                        Gap_TL = round(saved_results_TL.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_TL = sim.runSimulation(
                            Radius_SI, Gap_SI, var_slab_height_SI[0], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_TL, prop_loss,
                            var_wg_height_SI[1], wg_width_SI)
                    if bool_critical_couple == 1:
                        saved_results_TR = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, var_slab_height_SI[1], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            var_wg_height_SI[1], wg_width_SI)
                        Gap_TR = round(saved_results_TR.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_TR = sim.runSimulation(
                            Radius_SI, Gap_SI, var_slab_height_SI[1], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_TR, prop_loss,
                            var_wg_height_SI[1], wg_width_SI)
                # Case 3
                elif (Variability_Dict['[ID] Waveguide Height'] and
                        Variability_Dict['[ID] Doping Concentration']):

                    # Defining identifiers to locate charge simulation files for corners
                    identifier_BL = ('_wg_height-' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_doping-' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])

                    identifier_BR = ('_wg_height+' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_doping-' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])

                    identifier_TL = ('_wg_height-' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_doping+' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])

                    identifier_TR = ('_wg_height+' + str(Variability_Dict['Waveguide Height Range'])
                                     + Variability_Dict['Waveguide Height Units'] +
                                     '_doping+' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])

                    identifier_BL = identifier_BL.replace('.', 'p')
                    identifier_BR = identifier_BR.replace('.', 'p')
                    identifier_TL = identifier_TL.replace('.', 'p')
                    identifier_TR = identifier_TR.replace('.', 'p')

                    # Constucting path to file from name, this got a little convoluted
                    charge_file = str(CHARGE_file).split('\\')[-1]
                    charge_file = charge_file.split('.')[0]
                    CHARGE_file_BL = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_BL))
                    CHARGE_file_BR = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_BR))
                    CHARGE_file_TL = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_TL))
                    CHARGE_file_TR = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_TR))

                    if bool_critical_couple == 1:
                        saved_results_BL = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            var_wg_height_SI[0], wg_width_SI)
                        Gap_BL = round(saved_results_BL.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_BL = sim.runSimulation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            var_wg_height_SI[0], wg_width_SI)
                    if bool_critical_couple == 1:
                        saved_results_BR = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            var_wg_height_SI[0], wg_width_SI)
                        Gap_BR = round(saved_results_BR.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_BR = sim.runSimulation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BR, prop_loss,
                            var_wg_height_SI[0], wg_width_SI)
                    if bool_critical_couple == 1:
                        saved_results_TL = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            var_wg_height_SI[1], wg_width_SI)
                        Gap_TL = round(saved_results_TL.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_TL = sim.runSimulation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_TL, prop_loss,
                            var_wg_height_SI[1], wg_width_SI)
                    if bool_critical_couple == 1:
                        saved_results_TR = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            var_wg_height_SI[1], wg_width_SI)
                        Gap_TR = round(saved_results_TR.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_TR = sim.runSimulation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_TR, prop_loss,
                            var_wg_height_SI[1], wg_width_SI)

                # Case 4
                elif (Variability_Dict['[ID] Waveguide Width'] and
                        Variability_Dict['[ID] Slab Height']):

                    # Defining identifiers to locate charge simulation files for corners
                    identifier_BL = ('_wg_width-' + str(Variability_Dict['Waveguide Width Range'])
                                     + Variability_Dict['Waveguide Width Units'] +
                                     '_slab_height-' + str(Variability_Dict['Slab Height Range']) +
                                     Variability_Dict['Slab Height Units'])

                    identifier_BR = ('_wg_width+' + str(Variability_Dict['Waveguide Width Range'])
                                     + Variability_Dict['Waveguide Width Units'] +
                                     '_slab_height-' + str(Variability_Dict['Slab Height Range']) +
                                     Variability_Dict['Slab Height Units'])

                    identifier_TL = ('_wg_width-' + str(Variability_Dict['Waveguide Width Range'])
                                     + Variability_Dict['Waveguide Width Units'] +
                                     '_slab_height+' + str(Variability_Dict['Slab Height Range']) +
                                     Variability_Dict['Slab Height Units'])

                    identifier_TR = ('_wg_width+' + str(Variability_Dict['Waveguide Width Range'])
                                     + Variability_Dict['Waveguide Width Units'] +
                                     '_slab_height+' + str(Variability_Dict['Slab Height Range']) +
                                     Variability_Dict['Slab Height Units'])

                    identifier_BL = identifier_BL.replace('.', 'p')
                    identifier_BR = identifier_BR.replace('.', 'p')
                    identifier_TL = identifier_TL.replace('.', 'p')
                    identifier_TR = identifier_TR.replace('.', 'p')

                    # Constucting path to file from name, this got a little convoluted
                    charge_file = str(CHARGE_file).split('\\')[-1]
                    charge_file = charge_file.split('.')[0]
                    CHARGE_file_BL = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_BL))
                    CHARGE_file_BR = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_BR))
                    CHARGE_file_TL = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_TL))
                    CHARGE_file_TR = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_TR))

                    if bool_critical_couple == 1:
                        saved_results_BL = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, var_slab_height_SI[0], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            wg_height_SI, var_wg_width_SI[0])
                        Gap_BL = round(saved_results_BL.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_BL = sim.runSimulation(
                            Radius_SI, Gap_SI, var_slab_height_SI[0], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            wg_height_SI, var_wg_width_SI[0])
                    if bool_critical_couple == 1:
                        saved_results_BR = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, var_slab_height_SI[1], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            wg_height_SI, var_wg_width_SI[0])
                        Gap_BR = round(saved_results_BR.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_BR = sim.runSimulation(
                            Radius_SI, Gap_SI, var_slab_height_SI[1], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BR, prop_loss,
                            wg_height_SI, var_wg_width_SI[0])
                    if bool_critical_couple == 1:
                        saved_results_TL = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, var_slab_height_SI[0], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            wg_height_SI, var_wg_width_SI[1])
                        Gap_TL = round(saved_results_TL.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_TL = sim.runSimulation(
                            Radius_SI, Gap_SI, var_slab_height_SI[0], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_TL, prop_loss,
                            wg_height_SI, var_wg_width_SI[1])
                    if bool_critical_couple == 1:
                        saved_results_TR = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, var_slab_height_SI[1], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            wg_height_SI, var_wg_width_SI[1])
                        Gap_TR = round(saved_results_TR.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_TR = sim.runSimulation(
                            Radius_SI, Gap_SI, var_slab_height_SI[1], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_TR, prop_loss,
                            wg_height_SI, var_wg_width_SI[1])
                # Case 5
                elif (Variability_Dict['[ID] Waveguide Width'] and
                        Variability_Dict['[ID] Doping Concentration']):

                    # Defining identifiers to locate charge simulation files for corners
                    identifier_BL = ('_wg_width-' + str(Variability_Dict['Waveguide Width Range'])
                                     + Variability_Dict['Waveguide Width Units'] +
                                     '_doping-' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])

                    identifier_BR = ('_wg_width+' + str(Variability_Dict['Waveguide Width Range'])
                                     + Variability_Dict['Waveguide Width Units'] +
                                     '_doping-' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])

                    identifier_TL = ('_wg_width-' + str(Variability_Dict['Waveguide Width Range'])
                                     + Variability_Dict['Waveguide Width Units'] +
                                     '_doping+' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])

                    identifier_TR = ('_wg_width+' + str(Variability_Dict['Waveguide Width Range'])
                                     + Variability_Dict['Waveguide Width Units'] +
                                     '_doping+' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])

                    identifier_BL = identifier_BL.replace('.', 'p')
                    identifier_BR = identifier_BR.replace('.', 'p')
                    identifier_TL = identifier_TL.replace('.', 'p')
                    identifier_TR = identifier_TR.replace('.', 'p')

                    # Constucting path to file from name, this got a little convoluted
                    charge_file = str(CHARGE_file).split('\\')[-1]
                    charge_file = charge_file.split('.')[0]
                    CHARGE_file_BL = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_BL))
                    CHARGE_file_BR = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_BR))
                    CHARGE_file_TL = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_TL))
                    CHARGE_file_TR = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_TR))

                    if bool_critical_couple == 1:
                        saved_results_BL = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            wg_height_SI, var_wg_width_SI[0])
                        Gap_BL = round(saved_results_BL.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_BL = sim.runSimulation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            wg_height_SI, var_wg_width_SI[0])
                    if bool_critical_couple == 1:
                        saved_results_BR = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            wg_height_SI, var_wg_width_SI[0])
                        Gap_BR = round(saved_results_BR.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_BR = sim.runSimulation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BR, prop_loss,
                            wg_height_SI, var_wg_width_SI[0])
                    if bool_critical_couple == 1:
                        saved_results_TL = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            wg_height_SI, var_wg_width_SI[1])
                        Gap_TL = round(saved_results_TL.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_TL = sim.runSimulation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_TL, prop_loss,
                            wg_height_SI, var_wg_width_SI[1])
                    if bool_critical_couple == 1:
                        saved_results_TR = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            wg_height_SI, var_wg_width_SI[1])
                        Gap_TR = round(saved_results_TR.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_TR = sim.runSimulation(
                            Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_TR, prop_loss,
                            wg_height_SI, var_wg_width_SI[1])
                # Case 6
                elif (Variability_Dict['[ID] Slab Height'] and
                        Variability_Dict['[ID] Doping Concentration']):

                    # Defining identifiers to locate charge simulation files for corners
                    identifier_BL = ('_slab_height-' + str(Variability_Dict['Slab Height Range'])
                                     + Variability_Dict['Slab Height Units'] +
                                     '_doping-' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])

                    identifier_BR = ('_slab_height+' + str(Variability_Dict['Slab Height Range'])
                                     + Variability_Dict['Slab Height Units'] +
                                     '_doping-' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])

                    identifier_TL = ('_slab_height-' + str(Variability_Dict['Slab Height Range'])
                                     + Variability_Dict['Slab Height Units'] +
                                     '_doping+' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])

                    identifier_TR = ('_slab_height+' + str(Variability_Dict['Slab Height Range'])
                                     + Variability_Dict['Slab Height Units'] +
                                     '_doping+' +
                                     str(Variability_Dict['Doping Concentration Range']) +
                                     Variability_Dict['Doping Concentration Units'])

                    identifier_BL = identifier_BL.replace('.', 'p')
                    identifier_BR = identifier_BR.replace('.', 'p')
                    identifier_TL = identifier_TL.replace('.', 'p')
                    identifier_TR = identifier_TR.replace('.', 'p')

                    # Constucting path to file from name, this got a little convoluted
                    charge_file = str(CHARGE_file).split('\\')[-1]
                    charge_file = charge_file.split('.')[0]
                    CHARGE_file_BL = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_BL))
                    CHARGE_file_BR = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_BR))
                    CHARGE_file_TL = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_TL))
                    CHARGE_file_TR = Path(str(CHARGE_file).replace(
                        charge_file, charge_file + identifier_TR))

                    if bool_critical_couple == 1:
                        saved_results_BL = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, var_slab_height_SI[0], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            wg_height_SI, wg_width_SI)
                        Gap_BL = round(saved_results_BL.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_BL = sim.runSimulation(
                            Radius_SI, Gap_SI, var_slab_height_SI[0], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            wg_height_SI, wg_width_SI)
                    if bool_critical_couple == 1:
                        saved_results_BR = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, var_slab_height_SI[0], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            wg_height_SI, wg_width_SI)
                        Gap_BR = round(saved_results_BR.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_BR = sim.runSimulation(
                            Radius_SI, Gap_SI, var_slab_height_SI[0], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BR, prop_loss,
                            wg_height_SI, wg_width_SI)
                    if bool_critical_couple == 1:
                        saved_results_TL = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, var_slab_height_SI[1], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            wg_height_SI, wg_width_SI)
                        Gap_TL = round(saved_results_TL.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_TL = sim.runSimulation(
                            Radius_SI, Gap_SI, var_slab_height_SI[1], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_TL, prop_loss,
                            wg_height_SI, wg_width_SI)
                    if bool_critical_couple == 1:
                        saved_results_TR = sim.CriticalCouplingAutomation(
                            Radius_SI, Gap_SI, var_slab_height_SI[1], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_BL, prop_loss,
                            wg_height_SI, wg_width_SI)
                        Gap_TR = round(saved_results_TR.CriticalCoupleGap/1e-9)
                    else:
                        saved_results_TR = sim.runSimulation(
                            Radius_SI, Gap_SI, var_slab_height_SI[1], CouplingLength_SI,
                            LambdaStart, LambdaEnd, band, CHARGE_file_TR, prop_loss,
                            wg_height_SI, wg_width_SI)

                # If corner analysis was performed, the result windows are made visible
                toggle_Corner_Analysis_Results(True)

                if bool_critical_couple == 1:
                    # Updating gap display box to show a range of gaps
                    # that could be needed for critical
                    # coupling based on the corner analysis results
                    critical_gaps = [Gap_BL, Gap_BR, Gap_TL, Gap_TR]
                    min_critical_gap = min(critical_gaps)
                    max_critical_gap = max(critical_gaps)
                    gap_box.update(str(min_critical_gap) + ' - ' + str(max_critical_gap))
                    sg.Popup(
                        'Range of possible critical coupling gaps shown in gap display box'
                        ' Bl = ' + str(Gap_BL) + ', BR = ' + str(Gap_BR) +
                        ', Tl = ' + str(Gap_TL) + ', TR = ' + str(Gap_TR), keep_on_top=True)

            # Now that the data has been simulated we will plot it in the results tab.
            # Enabling result display buttons
            results_window.Update(visible=True)
            enable_result_buttons()

        except Exception as e:
            print("The following error has occured: " + e)

    elif event == '-CC-':
        # This event handles plotting the coupling coefficient i.e the power coupling coefficient
        if values['-NOMINAL-']:
            plot_CC(saved_results, identifier='Nominal')
        elif values['-CORNER_BL-']:
            plot_CC(saved_results_BL, identifier='Bottom Left Corner')
        elif values['-CORNER_BR-']:
            plot_CC(saved_results_BR, identifier='Bottom Right Corner')
        elif values['-CORNER_TL-']:
            plot_CC(saved_results_TL, identifier='Top Left Corner')
        elif values['-CORNER_TR-']:
            plot_CC(saved_results_TR, identifier='Top Right Corner')

    elif event == '-NEFF-':
        # This event handles the dneff/voltage plot
        if values['-NOMINAL-']:
            plot_NEFF(saved_results, identifier='Nominal')
        elif values['-CORNER_BL-']:
            plot_NEFF(saved_results_BL, identifier='Bottom Left Corner')
        elif values['-CORNER_BR-']:
            plot_NEFF(saved_results_BR, identifier='Bottom Right Corner')
        elif values['-CORNER_TL-']:
            plot_NEFF(saved_results_TL, identifier='Top Left Corner')
        elif values['-CORNER_TR-']:
            plot_NEFF(saved_results_TR, identifier='Top Right Corner')

    elif event == '-PN_RESULT-':

        # Disable secondary inputs in case the user has previously selected a tab with them
        disable_secondary_inputs()

        # Enable PN junction plot option buttons
        toggle_PN_Plot_Options(True)

        # Creating Matplotlib figure
        plt.figure(1)
        plt.figure(1).clear()
        fig = plt.gcf()
        fig.canvas.manager.window.attributes('-topmost', 1)

    elif event == '-PHASE-':
        # This handles the phase shift plot
        if values['-NOMINAL-']:
            plot_Phase(saved_results, identifier='Nominal')
        elif values['-CORNER_BL-']:
            plot_Phase(saved_results_BL, identifier='Bottom Left Corner')
        elif values['-CORNER_BR-']:
            plot_Phase(saved_results_BR, identifier='Bottom Right Corner')
        elif values['-CORNER_TL-']:
            plot_Phase(saved_results_TL, identifier='Top Left Corner')
        elif values['-CORNER_TR-']:
            plot_Phase(saved_results_TR, identifier='Top Right Corner')

    elif event == '-CAPACITANCE-':
        # This handles the capacitance plot
        if values['-NOMINAL-']:
            plot_Capacitance(saved_results, identifier='Nominal')
        elif values['-CORNER_BL-']:
            plot_Capacitance(saved_results_BL, identifier='Bottom Left Corner')
        elif values['-CORNER_BR-']:
            plot_Capacitance(saved_results_BR, identifier='Bottom Right Corner')
        elif values['-CORNER_TL-']:
            plot_Capacitance(saved_results_TL, identifier='Top Left Corner')
        elif values['-CORNER_TR-']:
            plot_Capacitance(saved_results_TR, identifier='Top Right Corner')

    elif event == '-RESISTANCE-':
        # This handles the resistance plot
        if values['-NOMINAL-']:
            plot_Resistance(saved_results, identifier='Nominal')
        elif values['-CORNER_BL-']:
            plot_Resistance(saved_results_BL, identifier='Bottom Left Corner')
        elif values['-CORNER_BR-']:
            plot_Resistance(saved_results_BR, identifier='Bottom Right Corner')
        elif values['-CORNER_TL-']:
            plot_Resistance(saved_results_TL, identifier='Top Left Corner')
        elif values['-CORNER_TR-']:
            plot_Resistance(saved_results_TR, identifier='Top Right Corner')

    elif event == '-BANDWIDTH-':
        # This handles the bandwidth plot
        if values['-NOMINAL-']:
            plot_Bandwidth(saved_results, identifier='Nominal')
        elif values['-CORNER_BL-']:
            plot_Bandwidth(saved_results_BL, identifier='Bottom Left Corner')
        elif values['-CORNER_BR-']:
            plot_Bandwidth(saved_results_BR, identifier='Bottom Right Corner')
        elif values['-CORNER_TL-']:
            plot_Bandwidth(saved_results_TL, identifier='Top Left Corner')
        elif values['-CORNER_TR-']:
            plot_Bandwidth(saved_results_TR, identifier='Top Right Corner')

    elif event == '-T-':
        # This event handels the transmission spectra plotting
        # This event handles the dneff/voltage plot
        if values['-NOMINAL-']:
            plot_T(saved_results, identifier='Nominal')
        elif values['-CORNER_BL-']:
            plot_T(saved_results_BL, identifier='Bottom Left Corner')
        elif values['-CORNER_BR-']:
            plot_T(saved_results_BR, identifier='Bottom Right Corner')
        elif values['-CORNER_TL-']:
            plot_T(saved_results_TL, identifier='Top Left Corner')
        elif values['-CORNER_TR-']:
            plot_T(saved_results_TR, identifier='Top Right Corner')

    elif event == '-NRZ-':
        # This event handles the NRZ eye diagram sub-simulation window

        # Disabling non-linearity correction option
        non_linearity_correction.Update(visible=False)

        # Enable PN junction plot option buttons
        toggle_PN_Plot_Options(False)

        # This controls the type of eye to generate upon eye update
        bool_PAM4 = 0
        bool_NRZ = 1

        # Creating Matplotlib figure
        plt.figure(1)
        plt.figure(1).clear()
        fig = plt.gcf()
        fig.canvas.manager.window.attributes('-topmost', 1)

        # Updating the displayed results
        update_text_results('Fill in the following information and then click update Eye:',
                            'Laser Wavelength [nm]', 'Min Voltage', 'Max Voltage', 'Bitrate [Gb/s]')

        # Enable secondary inputs for eye diagram
        enable_secondary_inputs()
    elif event == '-PAM4-':
        non_linearity_correction.Update(visible=True)
        # This controls the type of eye to generate upon eye update
        bool_PAM4 = 1
        bool_NRZ = 0

        # Enable PN junction plot option buttons
        toggle_PN_Plot_Options(False)

        # Creating Matplotlib figure
        plt.figure(1)
        plt.figure(1).clear()
        fig = plt.gcf()
        fig.canvas.manager.window.attributes('-topmost', 1)

        # Updating the displayed results
        update_text_results('Fill in the following information and then click update Eye:',
                            'Laser Wavelength [nm]', 'Min Voltage', 'Max Voltage', 'Bitrate [Gb/s]')

        # Enable secondary inputs for eye diagram
        enable_secondary_inputs()

    elif event == '-EYEBUTTON-':
        # Checking values
        [Laser_Wavelength, VMin,
         VMax, Bitrate, staticNonLinCorrec,
         bool_eye] = verify.check_secondary_inputs(values, CHARGE_file,
                                                   laser_warning, vmin_warning,
                                                   vmax_warning, bitrate_warning)
        # now updating plot with Eye diagram
        plt.figure(1)
        plt.figure(1).clear()

        # If verification passes, then execute eye diagram simulation
        if bool_eye == 1:
            # Execute NRZ eye diagram simulation
            if bool_NRZ == 1:
                staticNonLinCorrec = 'N/A'
                [amplitude, time, Voltage_levels] = sim.runEye(
                    'NRZ', VMax, VMin, Laser_Wavelength, Radius_SI, CouplingLength_SI, LambdaStart,
                    LambdaEnd, Bitrate, staticNonLinCorrec, CHARGE_file, saved_results, prop_loss)
                title = 'NRZ Eye Diargram for Vmin= ' + str(VMin) + " to " + str(VMax)
            # Execute PAM4 eye diagram simulation
            elif bool_PAM4 == 1:
                [amplitude, time, Voltage_levels] = sim.runEye(
                    'PAM4', VMax, VMin, Laser_Wavelength, Radius_SI, CouplingLength_SI, LambdaStart,
                    LambdaEnd, Bitrate, staticNonLinCorrec, CHARGE_file, saved_results, prop_loss)
                V0 = Voltage_levels[0]
                V1 = Voltage_levels[1]
                V2 = Voltage_levels[2]
                V3 = Voltage_levels[3]
                title = 'PAM4 Eye Diargram for V0 = ' \
                    + str(round(V0, 4)) + ' V1 = ' \
                    + str(round(V1, 4)) + ' V2 = ' \
                    + str(round(V2, 4)) + ' V3 = ' + str(round(V3, 4))

            # Creating eye diagram
            plt.scatter(time, amplitude)
            plt.title(title)
            plt.xlabel('time [s]')
            plt.ylabel('Amplitude')
            plt.grid()
            fig = plt.gcf()
            fig.canvas.manager.window.attributes('-topmost', 1)

        else:
            print('Not updating Eye diagram until proper data is provided')

    elif event == '-CRITICAL_COUPLE-':
        # This event handels the critical coupling set up, i.e. read-only box
        if values['-CRITICAL_COUPLE-']:
            gap_box.update(readonly=True)
            gap_box.update(background_color='grey')
            gap_box.update(text_color='black')
            bool_critical_couple = 1
        else:
            gap_box.update(readonly=False)
            gap_box.update(background_color='#97755c')
            gap_box.update(text_color='#FFFFFF')
            bool_critical_couple = 0

    elif event == '-AMF-':
        # This event handles the AMF foundry selection for the CHARGE window

        if foundry_tracker != 'AMF':

            # Erasing PN-junction and creating new one matching conditions of this case
            graph_charge.erase()
            draw.CreateWaveguideMeasurementLabels(graph_charge)
            draw.CreateWaveguideCrosssection(graph_charge)
            draw.CreateWaveguideMeasurementLines(graph_charge)
            draw.CreateWaveguideDopantLabels_AMF(graph_charge)

            # Removing L-Shaped as an option
            lateral_button.update(value=True)
            L_shapped_PN_button.update(visible=False)

            # Updating input box texts to match foundried dopants
            p_width_core_text.update('P Width (Core)')
            n_width_core_text.update('N Width (Core)')
            p_width_slab_text.update('P Width (Slab)')
            n_width_slab_text.update('N Width (Slab)')
            pp_width_text.update('P+ Width')
            np_width_text.update('N+ Width')
            ppp_width_text.update('P++ Width')
            npp_width_text.update('N++ Width')

            # Clearing inputs and making update button not visible
            run_charge.Update(visible=False)
            p_width_core_box.update('')
            n_width_core_box.update('')
            p_width_slab_box.update('')
            n_width_slab_box.update('')
            pp_width_box.update('')
            np_width_box.update('')
            ppp_width_box.update('')
            npp_width_box.update('')

            # Supressing warning labels for dopants
            p_width_core_warning.Update('Warning Message: ', visible=False)
            n_width_core_warning.Update('Warning Message: ', visible=False)
            p_width_slab_warning.Update('Warning Message: ', visible=False)
            n_width_slab_warning.Update('Warning Message: ', visible=False)
            pp_width_warning.Update('Warning Message: ', visible=False)
            np_width_warning.Update('Warning Message: ', visible=False)
            ppp_width_warning.Update('Warning Message: ', visible=False)
            npp_width_warning.Update('Warning Message: ', visible=False)

            # Setting foundry tracker to AMF
            foundry_tracker = 'AMF'

    elif event == '-AIM-':
        # This event handles the AIM foundry selection for the CHARGE window

        if foundry_tracker != 'AIM':

            # Erasing PN-junction and creating new one matching conditions of this case
            graph_charge.erase()
            draw.CreateWaveguideMeasurementLabels(graph_charge)
            draw.CreateWaveguideCrosssection(graph_charge)
            draw.CreateWaveguideMeasurementLines(graph_charge)
            draw.CreateWaveguideDopantLabels_AIM(graph_charge)

            # Adding L-Shaped as an option
            L_shapped_PN_button.update(visible=True)

            # Updating input box texts to match foundried dopants
            p_width_core_text.update('P1Al Width (Core)')
            n_width_core_text.update('N1Al Width (Core)')
            p_width_slab_text.update('P1Al Width (Slab)')
            n_width_slab_text.update('N1Al Width (Slab)')
            pp_width_text.update('P4Al Width')
            np_width_text.update('N3Al Width')
            ppp_width_text.update('P5Al Width')
            npp_width_text.update('P5Al Width')

            # Clearing inputs and making update button not visible
            run_charge.Update(visible=False)
            p_width_core_box.update('')
            n_width_core_box.update('')
            p_width_slab_box.update('')
            n_width_slab_box.update('')
            pp_width_box.update('')
            np_width_box.update('')
            ppp_width_box.update('')
            npp_width_box.update('')

            # Supressing warning labels for dopants
            p_width_core_warning.Update('Warning Message: ', visible=False)
            n_width_core_warning.Update('Warning Message: ', visible=False)
            p_width_slab_warning.Update('Warning Message: ', visible=False)
            n_width_slab_warning.Update('Warning Message: ', visible=False)
            pp_width_warning.Update('Warning Message: ', visible=False)
            np_width_warning.Update('Warning Message: ', visible=False)
            ppp_width_warning.Update('Warning Message: ', visible=False)
            npp_width_warning.Update('Warning Message: ', visible=False)

            # Setting foundry tracker to AIM
            foundry_tracker = 'AIM'

    elif event == '-L_SHAPED-':
        # This event handles the LShaped PN-junction type for AIM

        graph_charge.erase()
        draw.CreateWaveguideMeasurementLabels(graph_charge)
        draw.CreateWaveguideCrosssection(graph_charge, PN_Type='L-Shaped')
        draw.CreateWaveguideMeasurementLines(graph_charge)
        draw.CreateWaveguideDopantLabels_AIM(graph_charge, PN_Type='L-Shaped')

        p_width_core_text.update('P2Al Width (Core)')
        p_width_slab_text.update('P1Al+P2Al Width (Slab)')
    elif event == '-LATERAL-':
        # This event handles the ateral PN-junction type for AMF and AIM
        # Since lateral is displayed on both foundry, a case handler is needed here

        graph_charge.erase()
        draw.CreateWaveguideMeasurementLabels(graph_charge)
        draw.CreateWaveguideCrosssection(graph_charge)
        draw.CreateWaveguideMeasurementLines(graph_charge)
        if foundry_tracker == 'AMF':
            draw.CreateWaveguideDopantLabels_AMF(graph_charge)
            p_width_core_text.update('P Width (Core)')
            p_width_slab_text.update('P Width (Slab)')
        elif foundry_tracker == 'AIM':
            draw.CreateWaveguideDopantLabels_AIM(graph_charge)
            p_width_core_text.update('P1Al Width (Core)')
            p_width_slab_text.update('P1Al Width (Slab)')

    elif event == '-DEFINE_CHARGE-':
        charge_file.Update('')
        browse_button.Update(visible=False)
        bool_charge = 0
    elif event == '-IMPORT_CHARGE-':
        browse_button.Update(visible=True)

    # This is the boolean checker that determines if the entire simulation set up has been completed
    if (bool_radius == 1 and bool_gap == 1 and bool_coupling_length == 1
            and bool_charge == 1 and bool_prop_loss == 1 and bool_wg_height == 1
            and bool_wg_width == 1):
        # Checking for variability analysis
        if bool_variability:
            # only allow if info has been provided
            if bool_corner_analyis_ready:
                run_sim.Update(visible=True)
            else:
                run_sim.Update(visible=False)
        else:
            run_sim.Update(visible=True)
    else:
        run_sim.Update(visible=False)
    graph.Update()
    # This is the boolean checker that determines if the Charge window should be displayed or not
    if (bool_define_charge == 1 and bool_slab == 1 and bool_gap == 1
            and bool_radius == 1 and bool_coupling_length == 1 and bool_wg_height == 1
            and bool_wg_width == 1):
        charge_window.Update(visible=True)
    else:
        charge_window.Update(visible=False)
    if bool_variability:
        variability_window.Update(visible=True)
    else:
        variability_window.Update(visible=False)

# Closing all opened windows in the event of software shutdown
plt.close()
window.close()
