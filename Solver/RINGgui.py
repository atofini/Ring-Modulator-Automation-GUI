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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import math


# set the theme for the screen/window
sg.theme("DarkTanBlue")


def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    """
    Generate user-interactable plot window with toolbar.

    Parameters
    ----------
    canvas : TKcanvas window
        TKcanvas used to replace matplotlib figure.
    fig : Matplotlib Figure
        Matplotlib figure to use as base.
    canvas_toolbar : TKcanvas controls
        TKcanvas toolbar object associated with canvas.

    Returns
    -------
    None.

    """
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)


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


class Toolbar(NavigationToolbar2Tk):
    """
    Toolbar class definition built into TKcanvas.

    Returns
    -------
    None.

    """

    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)


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
              key='-DEFINE_CHARGE-'),
     sg.Radio('Import CHARGE',
              "RADIO2",
              default=True,
              key='-IMPORT_CHARGE-'),
     sg.Text('Filename:'),
     sg.Input(key='-CHARGE_FILE-',
              s=(box_size, 1)),
     sg.FileBrowse(),
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
# Creating elements on result window
results_tab = [
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
    [sg.T('Controls:')],
    [sg.Canvas(key='controls_cv')],
    [sg.T('Figure:')],
    [sg.Column(
        layout=[
            [sg.Canvas(key='fig_cv',
                       # it's important that you set this size
                       size=(400 * 2, 400)
                       )]
        ],
        background_color='#DAE0E6',
        pad=(0, 0)
    )],
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
coupling_length_warning = window['-COUPLING_LENGTH_WARNING-']
coupling_box = window['-COUPLING_LENGTH-']
run_sim = window['-RUN-']
charge_window = window['-CHARGE_TAB-']
results_window = window['-RESULTS_TAB-']
charge_file = window['-CHARGE_FILE-']
run_charge = window['-RUN_CHARGE-']
propagation_loss_box = window['-PROP_LOSS-']
propagation_loss_warning = window['-PROP_LOSS_WARNING-']
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
        bool_slab, slab_height = verify.CheckSlab(x0, y0, values, graph, slab_warning)

        # Verifying coupling length
        [bool_coupling_length, CouplingLength, circle, left_arc, right_arc, top_coupling,
         bot_coupling, radius_text, radius_line] = verify.CheckCouplingLength(
            x0, y0, values, graph, coupling_length_text, coupling_length_line,
            coupling_region, drawing_radius, coupling_length_warning, circle, top_coupling,
            bot_coupling, bus_width, left_arc, right_arc, radius_text, radius_line, radius_warning,
            bool_radius, bool_gap, Radius, coupling_box, bool_critical_couple)

        # Verifying optical band
        LambdaStart, LambdaEnd, band = verify.CheckBand(values)

        # Verifying charge selection type
        bool_define_charge = verify.CheckCharge(values)

        # Verifying charge file
        bool_load_charge, CHARGE_file = verify.CheckChargeFile(
            values, charge_file_warning, bool_define_charge)

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

    elif event == '-RUN_CHARGE-':
        # This event handles the charge simulation execution

        # Converting to SI units in case it wasnt already done
        Radius_SI = round(Radius*1e-6, 10)
        slab_height_SI = round(slab_height*1e-9, 10)
        CouplingLength_SI = round(CouplingLength*1e-6, 10)

        try:
            # Simulating charge distribution
            CHARGE_FILE, SimRun = sim.runPNJunctionSimulator(p_width_core, n_width_core,
                                                             p_width_slab, n_width_slab,
                                                             pp_width, np_width,
                                                             ppp_width, npp_width,
                                                             slab_height_SI, Radius_SI,
                                                             CouplingLength_SI, vmin_charge,
                                                             vmax_charge, save_name,
                                                             bias, band, foundry, PN_Type)

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
        # This event runs the simulation depending on the supplied settings
        print("Running Simulation")
        print("Current Physical Parameters: R=" + str(Radius) +
              "[um]_G=" + str(Gap) + "[nm]_Slab=" + str(slab_height) +
              "[nm]_L=" + str(CouplingLength) + "[um]")

        # Converting to SI units for saving
        Radius_SI = round(Radius*1e-6, 10)
        slab_height_SI = round(slab_height*1e-9, 10)
        CouplingLength_SI = round(CouplingLength*1e-6, 10)

        # Gap is unique since it can be swept for critical coupling
        if bool_critical_couple == 1:
            Gap_SI = np.linspace(100e-9, 600e-9, 11)

            # This executes the critical coupling sweep
            saved_results = sim.CriticalCouplingAutomation(
                Radius_SI, Gap_SI, slab_height_SI,
                CouplingLength_SI, LambdaStart, LambdaEnd,
                band, CHARGE_file, prop_loss)

            gap_box.update(str(round(saved_results.CriticalCoupleGap/1e-9)))
        else:
            Gap_SI = round(Gap*1e-9, 10)

            # This executes a single iteration of the script
            saved_results = sim.runSimulation(
                Radius_SI, Gap_SI, slab_height_SI, CouplingLength_SI,
                LambdaStart, LambdaEnd, band, CHARGE_file, prop_loss)

        # Extracting results from saved_results class
        CC = saved_results.CC
        CC_f = saved_results.f
        dNeff = saved_results.dNeff
        T = saved_results.T
        wavelength = saved_results.wavelength
        wavelength = wavelength*1e9
        phase_shift = saved_results.phase_shift
        capacitance = saved_results.capacitance
        resistance = saved_results.resistance
        bandwidth = saved_results.bandwidth
        voltage = phase_shift[0]

        # Now that the data has been simulated we will plot it in the results tab.
        # Enabling result display buttons
        results_window.Update(visible=True)
        enable_result_buttons()

    elif event == '-CC-':
        # This event handles plotting the coupling coefficient i.e the power coupling coefficient

        # Disable secondary inputs in case the user has previously selected a tab with them
        disable_secondary_inputs()

        # Enable PN junction plot option buttons
        toggle_PN_Plot_Options(False)

        # Creating Matplotlib figure
        plt.figure(1)
        plt.figure(1).clear()
        fig = plt.gcf()
        DPI = fig.get_dpi()

        # Defining TKcanvas canvas size
        fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))

        # Plotting power coupling results in figure
        c = 299792458
        wavl = [c/x/1e-9 for x in CC_f]
        x = wavl
        y = CC
        plt.plot(x, y)
        plt.title('Coupling Efficiency vs. Wavelength')
        plt.xlabel('Wavelength [nm]')
        plt.ylabel('Efficiency [%]')
        plt.grid()

        # Converting figure to canvas plot
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

        # Cleaning up text_results since they are not applicable here
        update_text_results('', '', '', '', '')

    elif event == '-NEFF-':
        # This event handles the dneff/voltage plot

        # Disable secondary inputs in case the user has previously selected a tab with them
        disable_secondary_inputs()

        # Enable PN junction plot option buttons
        toggle_PN_Plot_Options(False)

        # Creating Matplotlib figure
        plt.figure(1)
        plt.figure(1).clear()
        fig = plt.gcf()
        DPI = fig.get_dpi()

        # Defining TKcanvas canvas size
        fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))

        # Plotting change in effective index plot
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

        # Converting figure to canvas plot
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

        # Cleaning up text_results since they are not applicable here
        update_text_results('', '', '', '', '')

    elif event == '-PN_RESULT-':
        # This handles the phase shift plot

        # Disable secondary inputs in case the user has previously selected a tab with them
        disable_secondary_inputs()

        # Enable PN junction plot option buttons
        toggle_PN_Plot_Options(True)

        # Creating Matplotlib figure
        plt.figure(1)
        plt.figure(1).clear()
        fig = plt.gcf()
        DPI = fig.get_dpi()

        # Defining TKcanvas canvas size
        fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))

        # Converting figure to canvas plot
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

    elif event == '-PHASE-':
        # Creating Matplotlib figure
        plt.figure(1)
        plt.figure(1).clear()
        fig = plt.gcf()
        DPI = fig.get_dpi()

        # Defining TKcanvas canvas size
        fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))

        # Plotting change in effective index plot
        x = phase_shift[0]
        y1 = phase_shift[1]
        plt.plot(x, y1, label="Phase")
        plt.title('Phase Shift vs. Voltage')
        plt.xlabel('Voltage [V]')
        plt.ylabel('Phase [rads]')
        plt.legend(loc="upper right")
        plt.grid()

        # Converting figure to canvas plot
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

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

    elif event == '-CAPACITANCE-':
        # Creating Matplotlib figure
        plt.figure(1)
        plt.figure(1).clear()
        fig = plt.gcf()
        DPI = fig.get_dpi()

        # Defining TKcanvas canvas size
        fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))

        # Plotting change in effective index plot
        x = voltage
        capacitance_scaled = [x/1e-10 for x in capacitance]
        y1 = capacitance_scaled
        plt.plot(x, y1, label="Average Capacitance")
        plt.title('Capacitance vs. Voltage')
        plt.xlabel('Voltage [V]')
        plt.ylabel('Capacitance [pf/cm]')
        plt.legend(loc="upper right")
        plt.grid()

        # Converting figure to canvas plot
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

        # Updating result strings
        update_text_results('', '', '', '', '')

    elif event == '-RESISTANCE-':
        # Creating Matplotlib figure
        plt.figure(1)
        plt.figure(1).clear()
        fig = plt.gcf()
        DPI = fig.get_dpi()

        # Defining TKcanvas canvas size
        fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))

        # Plotting change in effective index plot
        x = voltage
        resistance_scaled = [x/100 for x in resistance]
        y1 = resistance_scaled
        plt.plot(x, y1, label="Average Resistance")
        plt.title('Resistance vs. Voltage')
        plt.xlabel('Voltage [V]')
        plt.ylabel('Resistance [Ohm.cm]')
        plt.legend(loc="upper right")
        plt.grid()

        # Converting figure to canvas plot
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

        # Updating result strings
        update_text_results('', '', '', '', '')

    elif event == '-BANDWIDTH-':
        # Creating Matplotlib figure
        plt.figure(1)
        plt.figure(1).clear()
        fig = plt.gcf()
        DPI = fig.get_dpi()

        # Defining TKcanvas canvas size
        fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))

        # Plotting change in effective index plot
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

        # Converting figure to canvas plot
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

        # Updating result strings
        update_text_results('', '', '', '', '')

    elif event == '-T-':
        # This event handels the transmission spectra plotting

        # Disable secondary inputs in case the user has previously selected a tab with them
        disable_secondary_inputs()

        # Enable PN junction plot option buttons
        toggle_PN_Plot_Options(False)

        # Creating Matplotlib figure
        plt.figure(1)
        plt.figure(1).clear()
        fig = plt.gcf()
        DPI = fig.get_dpi()

        # Defining TKcanvas canvas size
        fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))

        # Plotting transmission spectra and shift w.r.t voltage
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

        # Converting figure to canvas plot
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

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
        DPI = fig.get_dpi()

        # Defining TKcanvas canvas size
        fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))
        # -------------------------------

        # Converting figure to canvas plot
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

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
        DPI = fig.get_dpi()

        # Defining TKcanvas canvas size
        fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))

        # Converting figure to canvas plot
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

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
        fig = plt.gcf()
        DPI = fig.get_dpi()

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

        else:
            print('Not updating Eye diagram until proper data is provided')

        # Defining TKcanvas canvas size
        fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))

        # Converting figure to canvas plot
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

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

    # This is the boolean checker that determines if the entire simulation set up has been completed
    if (bool_radius == 1 and bool_gap == 1 and bool_coupling_length == 1
            and bool_charge == 1 and bool_prop_loss == 1):
        run_sim.Update(visible=True)
    else:
        run_sim.Update(visible=False)
    graph.Update()
    # This is the boolean checker that determines if the Charge window should be displayed or not
    if (bool_define_charge == 1 and bool_slab == 1 and bool_gap == 1
            and bool_radius == 1 and bool_coupling_length == 1):
        charge_window.Update(visible=True)
    else:
        charge_window.Update(visible=False)
