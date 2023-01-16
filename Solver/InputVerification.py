"""
Created on Thu Oct 28 13:16:34 2021.

This file contains all the check input functions that verify if the user supplied
values are appropriate

@author: AlexTofini
"""
import os


def CheckRadius(x0, y0, values, graph, radius_text, radius_warning):
    """
    Check the user specified radius for errors.

    Parameters
    ----------
    x0 : float
        x coordinate for center point of ring.
    y0 : float
        y coordinate for center point of ring.
    values : dictionary
        Dictionairy containing all the values present in the GUI.
    graph : TKcanvas
        TKcanvas graph object.
    radius_text : str
        Text displayed on graph to denote radius.
    radius_warning : str
        Warning message for user if radius is incorrectly defined.

    Returns
    -------
    bool_radius : int
        Boolean tracker to determine if radius is correctly specified.
    Radius : float
        Value for the radius as per the user-specification
    radius_text : str
        Text displayed on graph to denote radius specified by user.

    """
    # Initialize radius value
    Radius = None

    # Attempt to convert value inside radius textbox to float
    try:
        # Checking if radius box is not empty
        if values['-RADIUS-'] != '':
            # Populating radius
            Radius = float(values['-RADIUS-'])

            if Radius < 5.0:

                # Updating measurement label to be unknown
                graph.delete_figure(radius_text)
                radius_text = graph.DrawText('?? [um]', (x0+120, y0+25),
                                             color="blue", font=None, angle=0,
                                             text_location="center")

                # Setting boolean tracker to 1 and removing any warnings
                bool_radius = 0
                radius_warning.Update('Warning Message: Radius must be > 5 um', visible=True)
            elif Radius > 100:
                # Updating measurement label to be unknown
                graph.delete_figure(radius_text)
                radius_text = graph.DrawText('?? [um]', (x0+120, y0+25),
                                             color="blue", font=None, angle=0,
                                             text_location="center")

                # Setting boolean tracker to 1 and removing any warnings
                bool_radius = 0
                radius_warning.Update('Warning Message: Radius must be <= 100 um', visible=True)
            else:
                print("Saving Radius as:" + str(Radius))

                # Removing previous radius measurement and making a new one
                graph.delete_figure(radius_text)
                radius_text = graph.DrawText(
                    str(Radius)+' [um]', (x0+120, y0+25), color="blue",
                    font=None, angle=0, text_location="center")

                # Setting boolean tracker to 1 and removing any warnings
                bool_radius = 1
                radius_warning.Update('Warning Message: ', visible=False)
        else:
            # Setting boolean tracker to 0 and adding warning that radius is not specified
            bool_radius = 0
            radius_warning.Update('Warning Message: Radius Not Specified', visible=True)

    # If convertion to float fails, instruct user to fix error
    except ValueError:
        # Boolean tracker set to 0 and adding warning for invalid radius
        bool_radius = 0
        radius_warning.Update('Warning Message: Invalid Radius', visible=True)

        # Updating measurement label to be unknown
        graph.delete_figure(radius_text)
        radius_text = graph.DrawText('?? [um]', (x0+120, y0+25),
                                     color="blue", font=None, angle=0, text_location="center")

    return bool_radius, Radius, radius_text


def CheckGap(x0, y0, values, graph, gap_text, gap_warning, drawing_radius, drawing_gap,
             bool_critical_couple, gap_box):
    """
    Check the user specified gap for errors.

    Parameters
    ----------
    x0 : float
        x coordinate for center point of ring.
    y0 : float
        y coordinate for center point of ring.
    values : dictionary
        Dictionairy containing all the values present in the GUI.
    graph : TKcanvas
        TKcanvas graph object.
    gap_text : str
        Text display on graph to denote gap size.
    gap_warning : str
        Warning message for user if gap is incorrectly specified.
    drawing_radius : float
        Number of pixels on canvas used as radius.
    drawing_gap : float
        Number of pixels on canvas used as gap.
    bool_critical_couple : int
        Boolean tracker to determine if critical coupling is enforced.
    gap_box : textbox
        Textbox for gap.

    Returns
    -------
    bool_gap : int
        Boolean tracker to determine if gap is correctly specified.
    Gap : float
        Value for the gap as per the user-specification
    gap_text : str
        Text displayed on graph to denote gap specified by user.

    """
    # Initializing gap
    Gap = None

    # Clearing textbox if critical coupling condition is being inforced
    if bool_critical_couple == 1:
        gap_box.update('')
        gap_warning.Update('Warning Message: ', visible=False)
        bool_gap = 1
        gap_text = graph.DrawText('SWEEPING [nm]', (x0+75, y0-drawing_radius-drawing_gap/2),
                                  color="blue", font=None, angle=0, text_location="center")
    else:

        # Attempt to convert value inside gap textbox to float
        try:
            # Checking if gap box is not empty
            if values['-GAP-'] != '':
                # Populating gap
                Gap = float(values['-GAP-'])
                if Gap <= 0:

                    # Updating measurement label to be unknown
                    graph.delete_figure(gap_text)
                    gap_text = graph.DrawText('?? [nm]', (x0+75, y0-drawing_radius-drawing_gap/2),
                                              color="blue", font=None, angle=0,
                                              text_location="center")

                    # Setting the boolean tracker to 1 and removing any warnings
                    bool_gap = 0
                    gap_warning.Update('Warning Message: Gap must be > 0 nm', visible=True)
                elif Gap > 1000:
                    # Updating measurement label to be unknown
                    graph.delete_figure(gap_text)
                    gap_text = graph.DrawText('?? [nm]', (x0+75, y0-drawing_radius-drawing_gap/2),
                                              color="blue", font=None, angle=0,
                                              text_location="center")

                    # Setting the boolean tracker to 1 and removing any warnings
                    bool_gap = 0
                    gap_warning.Update('Warning Message: Gap must be <= 1000 nm', visible=True)
                else:
                    print("Saving Gap as:" + str(Gap))

                    # Removing previous gap measurement and making a new one
                    graph.delete_figure(gap_text)
                    gap_text = graph.DrawText(str(
                        Gap)+' [nm]', (x0+75, y0-drawing_radius-drawing_gap/2), color="blue",
                        font=None, angle=0, text_location="center")

                    # Setting the boolean tracker to 1 and removing any warnings
                    bool_gap = 1
                    gap_warning.Update('Warning Message: ', visible=False)
            else:
                # Setting boolean tracker to 0 and adding warning that gap is not specified
                bool_gap = 0
                gap_warning.Update('Warning Message: Gap Not Specified', visible=True)

        # If convertion to float fails, instruct user to fix error
        except ValueError:
            # Boolean tracker set to 0 and adding warning for invalid gap
            bool_gap = 0
            gap_warning.Update('Warning Message: Invalid Gap', visible=True)

            # Updating measurement label to be unknown
            graph.delete_figure(gap_text)
            gap_text = graph.DrawText('?? [nm]', (x0+75, y0-drawing_radius-drawing_gap/2),
                                      color="blue", font=None, angle=0, text_location="center")

    return bool_gap, Gap, gap_text


def CheckSlab(values, slab_warning):
    """
    Check the user specified slab height for errors.

    Parameters
    ----------
    values : dictionary
        Dictionairy containing all the values present in the GUI.
    slab_warning : str
        Warning message for user if slab height is incorrectly specified.

    Returns
    -------
    bool_slab : int
        Boolean tracker used to determine if slab is correctly specified
    slab_height : float
        Slab height of waveguide.

    """
    # Initialize slab height
    slab_height = None

    # Attempt to convert value inside slab height textbox to float
    try:
        # Checking if slab heighth box is not empty
        if values['-SLAB-'] != '':
            # Populating slab height
            slab_height = float(values['-SLAB-'])

            if slab_height <= 0:
                # Boolean tracker set to 0 and add warning for invalid slab height
                bool_slab = 0
                slab_warning.Update('Warning Message: Slab Height must be > 0 nm', visible=True)
            elif slab_height > 110:
                # Boolean tracker set to 0 and add warning for invalid slab height
                bool_slab = 0
                slab_warning.Update('Warning Message: Slab Height must be <= 110 nm', visible=True)

            else:
                print("Saving slab_height as:" + str(slab_height))
                # Setting the boolean tracker to 1 and removing any warnings
                bool_slab = 1
                slab_warning.Update('Warning Message: ', visible=False)

        else:
            # Setting boolean tracker to 0 and adding warning that slab height is not specified
            bool_slab = 0
            slab_warning.Update('Warning Message: Slab Height Not Specified', visible=True)

    # If convertion to float fails, instruct user to fix error
    except ValueError:
        # Boolean tracker set to 0 and add warning for invalid slab height
        bool_slab = 0
        slab_warning.Update('Warning Message: Invalid Slab Height', visible=True)

    return bool_slab, slab_height


def CheckWaveguideHeight(values, wg_height_warning):
    """
    Check the user specified waveguide height for errors.

    Parameters
    ----------
    values : dictionary
        Dictionairy containing all the values present in the GUI.
    wg_height_warning : str
        Warning message for user if slab height is incorrectly specified.

    Returns
    -------
    bool_wg_height : int
        Boolean tracker used to determine if waveguide height is correctly specified
    wg_height : float
        Wavegyude height.

    """
    # Initialize waveguide height
    wg_height = None

    # Attempt to convert value inside slab height textbox to float
    try:
        # Checking if slab heighth box is not empty
        if values['-WAVEGUIDE_HEIGHT-'] != '':
            # Populating slab height
            wg_height = float(values['-WAVEGUIDE_HEIGHT-'])

            if wg_height <= 0:
                # Boolean tracker set to 0 and add warning for invalid waveguide height
                bool_wg_height = 0
                wg_height_warning.Update(
                    'Warning Message: Waveguide Height must be > 0 nm', visible=True)

            else:
                print("Saving wg_height as:" + str(wg_height))
                # Setting the boolean tracker to 1 and removing any warnings
                bool_wg_height = 1
                wg_height_warning.Update('Warning Message: ', visible=False)

        else:
            # Setting boolean tracker to 0 and adding warning that waveguide height is not specified
            bool_wg_height = 0
            wg_height_warning.Update(
                'Warning Message: Waveguide Height Not Specified', visible=True)

    # If convertion to float fails, instruct user to fix error
    except ValueError:
        # Boolean tracker set to 0 and add warning for invalid waveguide height
        bool_wg_height = 0
        wg_height_warning.Update('Warning Message: Invalid Waveguide Height', visible=True)

    return bool_wg_height, wg_height


def CheckWaveguideWidth(values, wg_width_warning):
    """
    Check the user specified waveguide height for errors.

    Parameters
    ----------
    values : dictionary
        Dictionairy containing all the values present in the GUI.
    wg_width_warning : str
        Warning message for user if waveguide width is incorrectly specified.

    Returns
    -------
    bool_wg_width : int
        Boolean tracker used to determine if waveguide height is correctly specified
    wg_width : float
        Wavegyude height.

    """
    # Initialize waveguide width
    wg_width = None

    # Attempt to convert value inside slab height textbox to float
    try:
        # Checking if slab heighth box is not empty
        if values['-WAVEGUIDE_WIDTH-'] != '':
            # Populating slab height
            wg_width = float(values['-WAVEGUIDE_WIDTH-'])

            if wg_width <= 0:
                # Boolean tracker set to 0 and add warning for invalid waveguide width
                bool_wg_width = 0
                wg_width_warning.Update(
                    'Warning Message: Waveguide Width must be > 0 nm', visible=True)
            else:
                print("Saving wg_width as:" + str(wg_width))
                # Setting the boolean tracker to 1 and removing any warnings
                bool_wg_width = 1
                wg_width_warning.Update('Warning Message: ', visible=False)

        else:
            # Setting boolean tracker to 0 and adding warning that waveguide width is not specified
            bool_wg_width = 0
            wg_width_warning.Update(
                'Warning Message: Waveguide Width Not Specified', visible=True)

    # If convertion to float fails, instruct user to fix error
    except ValueError:
        # Boolean tracker set to 0 and add warning for invalid waveguide width
        bool_wg_width = 0
        wg_width.Update('Warning Message: Invalid Waveguide Width', visible=True)

    return bool_wg_width, wg_width


def CheckCouplingLength(x0, y0, values, graph, coupling_length_text, coupling_length_line,
                        coupling_region, drawing_radius, coupling_length_warning, circle,
                        top_coupling, bot_coupling, bus_width, left_arc, right_arc, radius_text,
                        radius_line, radius_warning, bool_radius, bool_gap, Radius,
                        coupling_box, bool_critical_couple):
    """
    Check the user specified coupling length for errors.

    Parameters
    ----------
    x0 : float
        x coordinate for center point of ring.
    y0 : float
        y coordinate for center point of ring.
    values : dictionary
        Dictionairy containing all the values present in the GUI.
    graph : TKcanvas
        TKcanvas graph object.
    coupling_length_text : str
        Text displayed on canvas representing coupling length.
    coupling_length_line : int
        Interger ID corresponding to coupling line in drawing.
    coupling_region : int
        Number of pixels used to represent the coupling region in the racetrack drawing.
    drawing_radius : int
        Number of pixels used to represent the radius of the ring.
    coupling_length_warning : str
        Warning message for user if coupling length is incorrectly specified.
    circle : int
        Integer ID corresponding to ring in drawing.
    top_coupling : int
        Integer ID corresponding to top coupling region in drawing.
    bot_coupling : int
        Integer ID corresponding to bottom coupling region in drawing.
    bus_width : int
        Number of pixels used to represent the width of the waveguide.
    left_arc : int
        Integer ID of the left arc coomposing the racetrack ring in the drawing.
    right_arc : int
        Integer ID of the right arc composing the racetrack ring in the drawing.
    radius_text : str
        Text display to show user the currenlty used radius.
    radius_line : int
        Integer ID for the radius display line in the drawing.
    radius_warning : str
        Warning message for the user if the radius is incorrectly displayed.
    bool_radius : int
        Boolean tracker used to determine if radius is correctly specified.
    bool_gap : int
        Boolean tracker used to determine if the gap is correctly specified.
    Radius : float
        Radius of the ring.
    coupling_box : textbox
        Coupling textbox used to reset the value to 0 if needed.
    bool_critical_couple : int
        Boolean tracker to determine if critical coupling is being inforced.

    Returns
    -------
    list
        List containing : [bool_coupling_length, CouplingLength, circle, left_arc, right_arc,
                top_coupling, bot_coupling, radius_text, radius_line]
            bool_coupling_length : int
                Boolean tracker used to determine if coupling length is correctly specified
            CouplingLength : float
                Coupling length of the ring if specified by the user.
            circle : int
                Modified iD corresponding to ring in drawing.
            left_arc : int
                Modified iD of the left arc coomposing the racetrack ring in the drawing.
            right_arc : int
                Modified i of the right arc composing the racetrack ring in the drawing.
            top_coupling : int
                Modified iD corresponding to top coupling region in drawing.
            bot_coupling : int
                Modified iD corresponding to bottom coupling region in drawing.
            radius_text : str
                Modified text display to show user the currenlty used radius.
            radius_line : int
                Modified integer ID for the radius display line in the drawing.

    """
    # Initializing coupling length
    CouplingLength = None

    # Resetting graph since racetrack ring drawing is completely different
    graph.erase()

    # Redefining contants used for drawing
    bus_width = 15
    bus_extra = 100
    bus_length = 2 * drawing_radius + bus_extra
    drawing_gap = 125

    # Drawing bus waveguide
    graph.DrawRectangle((x0-bus_length/2, y0-bus_width/2-drawing_radius-drawing_gap),
                        (x0 + bus_length/2, y0+bus_width/2-drawing_radius-drawing_gap),
                        fill_color='black', line_color="black")

    # Drawing gap measurement line
    graph.DrawLine((x0, y0-drawing_radius),
                   (x0, y0-drawing_radius-drawing_gap), color="blue", width=5)

    # If gap isint specified, create unkown value text description
    if bool_gap == 0:
        graph.DrawText('?? [nm]', (x0+75, y0-drawing_radius-drawing_gap/2),
                       color="blue", font=None, angle=0, text_location="center")

    # If gap is specficied or critical coupling is enforced, update text description
    else:
        if bool_critical_couple == 1:
            Gap = None
            graph.DrawText('SWEEPING [nm]', (x0+75, y0-drawing_radius - drawing_gap/2),
                           color="blue", font=None, angle=0, text_location="center")
        else:
            Gap = float(values['-GAP-'])
            graph.DrawText(str(Gap)+' [nm]', (x0+75, y0-drawing_radius - drawing_gap/2),
                           color="blue", font=None, angle=0, text_location="center")

    # Attempt to convert value inside coupling length textbox to float
    try:
        # Checking if slab heighth box is not empty and greater than 0
        if (values['-COUPLING_LENGTH-'] != '' and float(values['-COUPLING_LENGTH-']) > 0
                and float(values['-COUPLING_LENGTH-']) <= 100):
            # Populating coupling length
            CouplingLength = float(values['-COUPLING_LENGTH-'])
            print("Saving Coupling Length as:" + str(CouplingLength))

            # Creating coupling region measurement line and text description
            graph.DrawLine(
                (x0-coupling_region/2, y0-drawing_radius+50),
                (x0+coupling_region/2, y0-drawing_radius+50), color="blue", width=5)
            graph.DrawText(str(
                CouplingLength)+' [um]', (x0-coupling_region/2+120, y0-drawing_radius+75),
                color="blue", font=None, angle=0, text_location="center")

            # Setting the boolean tracker to 1 and removing any warnings
            bool_coupling_length = 1
            coupling_length_warning.Update('Warning Message: ', visible=False)

            # Drawing top and bottom extension that form the racetrack ring resonator
            top_coupling = graph.DrawRectangle((x0-coupling_region/2,
                                                y0-bus_width/2+drawing_radius),
                                               (x0+coupling_region/2,
                                                y0+bus_width/2+drawing_radius),
                                               fill_color='black', line_color="black")
            bot_coupling = graph.DrawRectangle((x0-coupling_region/2,
                                                y0-bus_width/2-drawing_radius),
                                               (x0+coupling_region/2,
                                                y0+bus_width/2-drawing_radius),
                                               fill_color='black', line_color="black")

            # Drawing left and right arcs that form the racetrack ring resonator
            left_arc = graph.DrawArc((x0-coupling_region/2-drawing_radius, y0-drawing_radius-1),
                                     (x0+coupling_region/2 + 1, y0+drawing_radius+1), 180, 90,
                                     style='arc', arc_color="black", line_width=9, fill_color=None)
            right_arc = graph.DrawArc((x0+coupling_region/2+drawing_radius, y0-drawing_radius-1),
                                      (x0-coupling_region/2 - 1, y0+drawing_radius+1), 180, -90,
                                      style='arc', arc_color="black", line_width=9, fill_color=None)

            # Redrawing the radius measurement to match the arc
            if bool_radius == 0:
                radius_text = graph.DrawText(
                    '?? [um]', (x0+120+coupling_region/2, y0+25), color="blue",
                    font=None, angle=0, text_location="center")
            else:
                radius_text = graph.DrawText(str(
                    Radius)+' [um]', (x0+120+coupling_region/2, y0+25), color="blue",
                    font=None, angle=0, text_location="center")

            radius_line = graph.DrawLine(
                (x0+coupling_region/2, y0), (x0+drawing_radius+coupling_region/2, y0),
                color="blue", width=5)
        elif (values['-COUPLING_LENGTH-'] != '' and float(values['-COUPLING_LENGTH-']) > 100):
            # Boolean tracker set to 0 and add warning for invalid coupling length
            bool_coupling_length = 0
            coupling_length_warning.Update(
                'Warning Message: Coupling Length Must Be <=100 um', visible=True)

            # Drawing the circular ring
            circle = graph.DrawCircle((x0, y0), drawing_radius, fill_color='',
                                      line_color='black', line_width=bus_width/2*1.25)

            # Redrawing the radius measurement to match the point coupler
            if bool_radius == 0:
                radius_text = graph.DrawText(
                    '?? [um]', (x0+120, y0+25), color="blue",
                    font=None, angle=0, text_location="center")
            else:
                radius_text = graph.DrawText(
                    str(Radius)+' [um]', (x0+120, y0+25), color="blue",
                    font=None, angle=0, text_location="center")

            # Redrawing radius measurement line in case previous one was for a racetrack ring
            radius_line = graph.DrawLine((x0, y0), (x0+drawing_radius, y0), color="blue", width=5)

        # If coupling length is zero, treat ring as a point coupler not a racetrack
        else:
            # Populating coupling length
            CouplingLength = 0
            print("Saving Coupling Length as:" + str(CouplingLength))
            coupling_box.Update(str(CouplingLength))

            # Setting the boolean tracker to 1 and removing any warnings
            bool_coupling_length = 1
            coupling_length_warning.Update('Warning Message: ', visible=False)

            # Drawing the circular ring
            circle = graph.DrawCircle((x0, y0), drawing_radius, fill_color='',
                                      line_color='black', line_width=bus_width/2*1.25)

            # Redrawing the radius measurement to match the point coupler
            if bool_radius == 0:
                radius_text = graph.DrawText(
                    '?? [um]', (x0+120, y0+25), color="blue", font=None,
                    angle=0, text_location="center")
            else:
                radius_text = graph.DrawText(
                    str(Radius)+' [um]', (x0+120, y0+25), color="blue",
                    font=None, angle=0, text_location="center")
            radius_line = graph.DrawLine((x0, y0), (x0+drawing_radius, y0), color="blue", width=5)

    # If convertion to float fails, instruct user to fix error
    except ValueError:
        # Boolean tracker set to 0 and add warning for invalid coupling length
        bool_coupling_length = 0
        coupling_length_warning.Update('Warning Message: Invalid Coupling Length', visible=True)

        # Drawing the circular ring
        circle = graph.DrawCircle((x0, y0), drawing_radius, fill_color='',
                                  line_color='black', line_width=bus_width/2*1.25)

        # Redrawing the radius measurement to match the point coupler
        if bool_radius == 0:
            radius_text = graph.DrawText(
                '?? [um]', (x0+120, y0+25), color="blue",
                font=None, angle=0, text_location="center")
        else:
            radius_text = graph.DrawText(
                str(Radius)+' [um]', (x0+120, y0+25), color="blue",
                font=None, angle=0, text_location="center")

        # Redrawing radius measurement line in case previous one was for a racetrack ring
        radius_line = graph.DrawLine((x0, y0), (x0+drawing_radius, y0), color="blue", width=5)

    return [bool_coupling_length, CouplingLength, circle, left_arc, right_arc,
            top_coupling, bot_coupling, radius_text, radius_line]


def CheckBand(values):
    """
    Check the user selected optical band to determine which is being used.

    There are no potentials for errros here.

    Parameters
    ----------
    values : dictionary
        Dictionairy containing all the values present in the GUI.

    Returns
    -------
    LambdaStart : float
        Start wavelength of optical band.
    LambdaEnd : float
        End wavelength of optical band.
    Band : str
        Optical band either : [CL, O].

    """
    # Initializing start and end wavelenths i.e. lambda
    LambdaStart = None
    LambdaEnd = None

    # Checking radio buttons to determine which is selected
    if values['-CL_BAND-']:
        LambdaStart = 1500e-9
        LambdaEnd = 1600e-9
        Band = 'CL'
    if values['-O_BAND-']:
        LambdaStart = 1260e-9
        LambdaEnd = 1400e-9
        Band = 'O'
    return LambdaStart, LambdaEnd, Band


def CheckCharge(values):
    """
    Check if the user wants to build the CHARGE simulation from scratch.

    Parameters
    ----------
    values : dictionary
        Dictionairy containing all the values present in the GUI.

    Returns
    -------
    bool_define_charge : int
        Boolean tracker to determine if the CHARGE simulation is being defined by the user.

    """
    bool_define_charge = 0
    if values['-DEFINE_CHARGE-']:
        bool_define_charge = 1
    return bool_define_charge


def CheckPropLoss(values, prop_loss_warning):
    """
    Check if user specified propgation loss has any errors.

    Parameters
    ----------
    values : dictionary
        Dictionairy containing all the values present in the GUI.
    prop_loss_warning : str
        Warning message for user if propagation loss is incorrectly specified.

    Returns
    -------
    bool_prop_loss : int
        Boolean tracker to determine if propagation loss is correctly specified.
    prop_loss : float
        User specified propagation loss.

    """
    # Initializing propagation loss
    prop_loss = None

    # Attempt to convert value inside propgation loss textbox to float
    try:
        # Checking if propagation loss textbox is not empty
        if values['-PROP_LOSS-'] != '':
            # Populating propgation loss
            prop_loss = float(values['-PROP_LOSS-'])*100  # converting to db/m instead of db/cm
            if prop_loss < 0:
                # Boolean tracker set to 0 here also and invalid propagation loss warning added
                bool_prop_loss = 0
                prop_loss_warning.Update(
                    'Warning Message: Propagation Loss must be >=0', visible=True)
            else:
                print("Saving Propagation loss as:" + str(prop_loss))

                # Setting boolean tracker to 1 and removing any warnings
                bool_prop_loss = 1
                prop_loss_warning.Update('Warning Message: ', visible=False)
        else:
            # Setting boolean tracker to 0 and adding warning that propagation loss is not specified
            bool_prop_loss = 0
            prop_loss_warning.Update(
                'Warning Message: Propagation Loss Not Specified', visible=True)

    # If convertion to float fails, instruct user to fix error
    except ValueError:
        # Boolean tracker set to 0 here also and invalid propagation loss warning added
        bool_prop_loss = 0
        prop_loss_warning.Update('Warning Message: Invalid Propagation Loss', visible=True)

    return bool_prop_loss, prop_loss


def CheckChargeParameters(values, graph_charge,
                          p_width_core_warning, n_width_core_warning,
                          p_width_slab_warning, n_width_slab_warning,
                          pp_width_warning, np_width_warning,
                          ppp_width_warning, npp_width_warning,
                          vmin_charge_warning, vmax_charge_warning,
                          save_name_warning):
    """
    Check if user specified charge parameters have any errors in them.

    Parameters
    ----------
    values : dictionary
        Dictionairy containing all the values present in the GUI.
    graph_charge : TKcanvas
        TKcanvas graph object.
    p_width_core_warning : str
        Warning message for user if p width (core) is incorrectly specified.
    n_width_core_warning : str
        Warning message for user if n width (core) is incorrectly specified.
    p_width_slab_warning : str
        Warning message for user if p width (slab) is incorrectly specified.
    n_width_slab_warning : str
        Warning message for user if n width (slab) is incorrectly specified.
    pp_width_warning : str
        Warning message for user if p+ width is incorrectly specified.
    np_width_warning : str
        Warning message for user if n+ width is incorrectly specified.
    ppp_width_warning : str
        Warning message for user if p++ width is incorrectly specified.
    npp_width_warning : str
        Warning message for user if n++ width is incorrectly specified.
    vmin_charge_warning : str
        Warning message for user if minimum voltage is incorrectly specified.
    vmax_charge_warning : str
        Warning message for user if maximum voltage is incorrectly specified.
    save_name_warning : str
        Warning message for user if filename for saving is incorrectly specified.

    Returns
    -------
    list
        List containing [bool_charge_params, p_width_core, n_width_core,
                p_width_slab, n_width_slab, pp_width, np_width,
                ppp_width, npp_width, vmin, vmax, save_name,
                bias, foundry, PN_Type].
            bool_charge_params : int
                Boolean tracker to determine if all charge parameters are correctly specified
            p_width_core : flaot
                Width of the p doping in the waveguide core.
            n_width_core : flaot
                Width of the n doping inthe waveguide core.
            p_width_slab : flaot
                Width of the p doping in the waveguide slab.
            n_width_slab : flaot
                Width of the n doping inthe waveguide slab.
            pp_width : flaot
                Width of the p+ doping in the waveguide slab.
            np_width : flaot
                Width of the n+ doping inthe waveguide slab.
            ppp_width : flaot
                Width of the p++ doping in the waveguide slab.
            npp_width : flaot
                Width of the n++ doping inthe waveguide slab.
            vmin : float
                Minimum voltage for CHARGE simulation.
            vmax : float
                Maximum voltage for CHARGE simulation.
            save_name : str
                Filename for saving the resulting .mat file after CHARGE simulation completion.
            bias : str
                Voltage bias setting either [Reverse, Forward]
            foundry : str
                Selected foundry for PN junction desing either [AIM, AMF]
            PN_Type : str
                PN junction type either [Lateral, L-Shaped]

    """
    # Importing drawing module that controls the PN junction drawing
    import Draw as draw

    # Clearing charge drawing to restart from scratch
    graph_charge.erase()

    # Creating waveguide crossection with doping information
    draw.CreateWaveguideMeasurementLines(graph_charge)
    if values['-AMF-']:
        draw.CreateWaveguideDopantLabels_AMF(graph_charge)
        draw.CreateWaveguideCrosssection(graph_charge)
        foundry = 'AMF'
        PN_Type = 'Lateral'
    elif values['-AIM-']:
        if values['-LATERAL-']:
            draw.CreateWaveguideDopantLabels_AIM(graph_charge)
            draw.CreateWaveguideCrosssection(graph_charge)
            PN_Type = 'Lateral'
        elif values['-L_SHAPED-']:
            draw.CreateWaveguideCrosssection(graph_charge, PN_Type='L-Shaped')
            draw.CreateWaveguideDopantLabels_AIM(graph_charge, PN_Type='L-Shaped')
            PN_Type = 'L-Shaped'
        foundry = 'AIM'

    # Initializing values
    p_width_core = 0
    n_width_core = 0
    p_width_slab = 0
    n_width_slab = 0
    pp_width = 0
    np_width = 0
    ppp_width = 0
    npp_width = 0
    vmin = 0
    vmax = 0
    save_name = ''

    # Determining what bias is being used
    if values['-FORWARD-']:
        bias = 'Forward'
    else:
        bias = 'Reverse'

    # Attempt to convert value inside P width (core) textbox to float
    try:
        # Checking if P width (core) textbox is not empty
        if values['-P_WIDTH_CORE-'] != '':
            # Populating P width (core)
            p_width_core = float(values['-P_WIDTH_CORE-'])
            if p_width_core < 0:
                # Updating measurement label description to be unknown
                graph_charge.DrawText('?? [nm]', (87.5, 650),
                                      color="blue", font=None,
                                      angle=0, text_location="center")

                # Setting boolean tracker to 0 and add warning message depending on foundry
                # and PN type
                bool_PWidth_core = 0
                if values['-AMF-']:
                    p_width_core_warning.Update(
                        'Warning Message: P Width (Core) must be >=0 ', visible=True)
                elif values['-AIM-']:
                    if values['-LATERAL-']:
                        p_width_core_warning.Update(
                            'Warning Message: P1Al Width (Core) must be >=0 ', visible=True)
                    elif values['-L_SHAPED-']:
                        p_width_core_warning.Update(
                            'Warning Message: P2Al Width (Core) must be >=0', visible=True)

            else:
                print("Saving P Width (Core) as: " + str(p_width_core))

                # Updating measurement label description to specified value
                graph_charge.DrawText(str(p_width_core) + ' [nm]', (87.5, 650),
                                                          color="blue", font=None,
                                                          angle=0, text_location="center")

                # Setting boolean tracker to 1 and removing warning labels
                bool_PWidth_core = 1
                p_width_core_warning.Update('Warning Message: ', visible=False)
        else:
            # Updating measurement label description to be unknown
            graph_charge.DrawText('?? [nm]', (87.5, 650),
                                  color="blue", font=None,
                                  angle=0, text_location="center")

            # Setting boolean tracker to 0 and add warning message depending on foundry and PN type
            bool_PWidth_core = 0
            if values['-AMF-']:
                p_width_core_warning.Update(
                    'Warning Message: P Width (Core) Not Specified ', visible=True)
            elif values['-AIM-']:
                if values['-LATERAL-']:
                    p_width_core_warning.Update(
                        'Warning Message: P1Al Width (Core) Not Specified ', visible=True)
                elif values['-L_SHAPED-']:
                    p_width_core_warning.Update(
                        'Warning Message: P2Al Width (Core) Not Specified ', visible=True)

    # If convertion to float fails, instruct user to fix error
    except ValueError:
        # Boolean tracker set to 0 here also and add invalid P width (core) warning
        bool_PWidth_core = 0
        if values['-AMF-']:
            p_width_core_warning.Update('Warning Message: Invalid P Width (Core)', visible=True)
        elif values['-AIM-']:
            if values['-LATERAL-']:
                p_width_core_warning.Update(
                    'Warning Message: Invalid P1Al Width (Core)', visible=True)
            elif values['-L_SHAPED-']:
                p_width_core_warning.Update(
                    'Warning Message: Invalid P2Al Width (Core)', visible=True)

        # Updating measurement label to be unknown
        graph_charge.DrawText('?? [nm]', (87.5, 650), color="blue", font=None,
                              angle=0, text_location="center")

    # Attempt to convert value inside N width (core) textbox to float
    try:
        # Checking if N width (core) textbox is not empty
        if values['-N_WIDTH_CORE-'] != '':
            # Populating N width (core)
            n_width_core = float(values['-N_WIDTH_CORE-'])
            if n_width_core < 0:
                # Updating measurement label description to be unknown
                graph_charge.DrawText('?? [nm]', (112.5, 650), color="blue",
                                      font=None, angle=0, text_location="center")

                # Setting boolean tracker to 0 and add warning message depending on foundry
                # and PN type
                bool_NWidth_core = 0
                if values['-AMF-']:
                    n_width_core_warning.Update(
                        'Warning Message: N Width (Core) must be >=0', visible=True)
                elif values['-AIM-']:
                    n_width_core_warning.Update(
                        'Warning Message: N1Al Width (Core) must be >=0 ', visible=True)

            else:
                print("Saving N Width (Core) as: " + str(n_width_core))

                # Updating measurement label description to specified value
                graph_charge.DrawText(str(n_width_core) + ' [nm]', (112.5, 650), color="blue",
                                      font=None, angle=0, text_location="center")

                # Setting boolean tracker to 1 and removing warning labels
                bool_NWidth_core = 1
                n_width_core_warning.Update('Warning Message: ', visible=False)
        else:
            # Updating measurement label description to be unknown
            graph_charge.DrawText('?? [nm]', (112.5, 650), color="blue",
                                  font=None, angle=0, text_location="center")

            # Setting boolean tracker to 0 and add warning message depending on foundry and PN type
            bool_NWidth_core = 0
            if values['-AMF-']:
                n_width_core_warning.Update(
                    'Warning Message: N Width (Core) Not Specified ', visible=True)
            elif values['-AIM-']:
                n_width_core_warning.Update(
                    'Warning Message: N1Al Width (Core) Not Specified ', visible=True)

    # If convertion to float fails, instruct user to fix error
    except ValueError:
        # Boolean tracker set to 0 here also and add invalid N width (core) warning
        bool_NWidth_core = 0
        if values['-AMF-']:
            n_width_core_warning.Update('Warning Message: Invalid N Width (Core)', visible=True)
        elif values['-AIM-']:
            n_width_core_warning.Update('Warning Message: Invalid N1Al Width (Core)', visible=True)

        # Updating measurement label to be unknown
        graph_charge.DrawText('?? [nm]', (112.5, 650), color="blue", font=None,
                              angle=0, text_location="center")

    # Attempt to convert value inside P width (slab) textbox to float
    try:
        # Checking if P width (slab) textbox is not empty
        if values['-P_WIDTH_SLAB-'] != '':
            # Populating P width (slab)
            p_width_slab = float(values['-P_WIDTH_SLAB-'])

            if p_width_slab < 0:
                # Updating measurement label to be unknown
                graph_charge.DrawText('?? [nm]', (62.5, 400), color="blue", font=None,
                                      angle=0, text_location="center")

                # Setting boolean tracker to 0 and add warning message depending on foundry
                # and PN type
                bool_PWidth_slab = 0
                if values['-AMF-']:
                    p_width_slab_warning.Update(
                        'Warning Message: P Width (Slab) must be >=0 ', visible=True)
                elif values['-AIM-']:
                    if values['-LATERAL-']:
                        p_width_slab_warning.Update(
                            'Warning Message: P1Al Width (Slab) must be >=0 ', visible=True)
                    elif values['-L_SHAPED-']:
                        p_width_slab_warning.Update(
                            'Warning Message: P1Al+P2Al Width (Slab) must be >=0', visible=True)
            else:
                print("Saving P Width (Slab) as: " + str(p_width_slab))

                # Updating measurement label description to specified value
                graph_charge.DrawText(str(p_width_slab) + ' [nm]', (62.5, 400),
                                      color="blue", font=None,
                                      angle=0, text_location="center")

                # Setting boolean tracker to 1 and removing warning labels
                bool_PWidth_slab = 1
                p_width_slab_warning.Update('Warning Message: ', visible=False)
        else:
            # Updating measurement label to be unknown
            graph_charge.DrawText('?? [nm]', (62.5, 400), color="blue", font=None,
                                  angle=0, text_location="center")

            # Setting boolean tracker to 0 and add warning message depending on foundry and PN type
            bool_PWidth_slab = 0
            if values['-AMF-']:
                p_width_slab_warning.Update(
                    'Warning Message: P Width (Slab) Not Specified ', visible=True)
            elif values['-AIM-']:
                if values['-LATERAL-']:
                    p_width_slab_warning.Update(
                        'Warning Message: P1Al Width (Slab) Not Specified ', visible=True)
                elif values['-L_SHAPED-']:
                    p_width_slab_warning.Update(
                        'Warning Message: P1Al+P2Al Width (Slab) Not Specified ', visible=True)

    # If convertion to float fails, instruct user to fix error
    except ValueError:
        # Boolean tracker set to 0 here also and add invalid P width (slab) warning
        bool_PWidth_slab = 0
        if values['-AMF-']:
            p_width_slab_warning.Update('Warning Message: Invalid P Width (Slab)', visible=True)
        elif values['-AIM-']:
            if values['-LATERAL-']:
                p_width_slab_warning.Update(
                    'Warning Message: Invalid P1Al Width (Slab)', visible=True)
            elif values['-L_SHAPED-']:
                p_width_slab_warning.Update(
                    'Warning Message: Invalid P1Al+P2Al Width (Slab)', visible=True)

        # Updating measurement label to be unknown
        graph_charge.DrawText('?? [nm]', (62.5, 400), color="blue", font=None,
                              angle=0, text_location="center")

    # Attempt to convert value inside N width (slab) textbox to float
    try:
        # Checking if N width (slab) textbox is not empty
        if values['-N_WIDTH_SLAB-'] != '':
            # Populating N width (slab)
            n_width_slab = float(values['-N_WIDTH_SLAB-'])
            if n_width_slab < 0:
                # Updating measurement label to be unknown
                graph_charge.DrawText('?? [nm]', (137.5, 400), color="blue", font=None,
                                      angle=0, text_location="center")

                # Setting boolean tracker to 0 and add warning message depending on foundry
                # and PN type
                bool_NWidth_slab = 0
                if values['-AMF-']:
                    n_width_slab_warning.Update(
                        'Warning Message: N Width (Slab) must be >=0 ', visible=True)
                elif values['-AIM-']:
                    n_width_slab_warning.Update(
                        'Warning Message: N1Al Width (Slab) must be >=0 ', visible=True)
            else:
                print("Saving N Width (Slab) as: " + str(n_width_slab))

                # Updating measurement label description to specified value
                graph_charge.DrawText(str(n_width_slab) + ' [nm]', (137.5, 400),
                                                          color="blue", font=None,
                                                          angle=0, text_location="center")

                # Setting boolean tracker to 1 and removing warning labels
                bool_NWidth_slab = 1
                n_width_slab_warning.Update('Warning Message: ', visible=False)
        else:
            # Updating measurement label to be unknown
            graph_charge.DrawText('?? [nm]', (137.5, 400), color="blue", font=None,
                                  angle=0, text_location="center")

            # Setting boolean tracker to 0 and add warning message depending on foundry and PN type
            bool_NWidth_slab = 0
            if values['-AMF-']:
                n_width_slab_warning.Update(
                    'Warning Message: N Width (Slab) Not Specified ', visible=True)
            elif values['-AIM-']:
                n_width_slab_warning.Update(
                    'Warning Message: N1Al Width (Slab) Not Specified ', visible=True)

    # If convertion to float fails, instruct user to fix error
    except ValueError:
        # Boolean tracker set to 0 here also and add invalid N width (slab) warning
        bool_NWidth_slab = 0
        if values['-AMF-']:
            n_width_slab_warning.Update('Warning Message: Invalid N Width (Slab)', visible=True)
        elif values['-AIM-']:
            n_width_slab_warning.Update('Warning Message: Invalid N1Al Width (Slab)', visible=True)

        # Updating measurement label to be unknown
        graph_charge.DrawText('?? [nm]', (137.5, 400), color="blue", font=None,
                              angle=0, text_location="center")

    # Attempt to convert value inside P+ width textbox to float
    try:
        # Checking if P+ width textbox is not empty
        if values['-P+_WIDTH-'] != '':
            # Populating P+ width
            pp_width = float(values['-P+_WIDTH-'])
            if pp_width < 0:
                # Updating measurement label to be unknown
                graph_charge.DrawText('?? [nm]', (37.5, 400), color="blue", font=None,
                                      angle=0, text_location="center")

                # Setting boolean tracker to 0 and add warning message depending on foundry
                # and PN type
                bool_PPWidth = 0
                if values['-AMF-']:
                    pp_width_warning.Update(
                        'Warning Message: P+ Width must be >=0 ', visible=True)
                elif values['-AIM-']:
                    pp_width_warning.Update(
                        'Warning Message: P4Al Width must be >=0 ', visible=True)
            else:
                print("Saving P Width as: " + str(pp_width))

                # Updating measurement label description to specified value
                graph_charge.DrawText(str(pp_width) + ' [nm]', (37.5, 400), color="blue", font=None,
                                                      angle=0, text_location="center")

                # Setting boolean tracker to 1 and removing warning labels
                bool_PPWidth = 1
                pp_width_warning.Update('Warning Message: ', visible=False)
        else:
            # Updating measurement label to be unknown
            graph_charge.DrawText('?? [nm]', (37.5, 400), color="blue", font=None,
                                  angle=0, text_location="center")

            # Setting boolean tracker to 0 and add warning message depending on foundry and PN type
            bool_PPWidth = 0
            if values['-AMF-']:
                pp_width_warning.Update('Warning Message: P+ Width Not Specified ', visible=True)
            elif values['-AIM-']:
                pp_width_warning.Update('Warning Message: P4Al Width Not Specified ', visible=True)

    # If convertion to float fails, instruct user to fix error
    except ValueError:
        # Boolean tracker set to 0 here also and add invalid P+ width warning
        bool_PPWidth = 0
        if values['-AMF-']:
            pp_width_warning.Update('Warning Message: Invalid P+ Width', visible=True)
        elif values['-AIM-']:
            pp_width_warning.Update('Warning Message: Invalid P4Al Width', visible=True)

        # Updating measurement label to be unknown
        graph_charge.DrawText('?? [nm]', (37.5, 400), color="blue", font=None,
                              angle=0, text_location="center")

    # Attempt to convert value inside N+ width textbox to float
    try:
        # Checking if N+ width textbox is not empty
        if values['-N+_WIDTH-'] != '':
            # Populating N+ width
            np_width = float(values['-N+_WIDTH-'])
            if np_width < 0:
                # Updating measurement label to be unknown
                graph_charge.DrawText('?? [nm]', (162.5, 400), color="blue", font=None,
                                      angle=0, text_location="center")

                # Setting boolean tracker to 0 and add warning message depending on foundry
                # and PN type
                bool_NPWidth = 0
                if values['-AMF-']:
                    np_width_warning.Update(
                        'Warning Message: N+ Width must be >=0', visible=True)
                elif values['-AIM-']:
                    np_width_warning.Update(
                        'Warning Message: N3Al Width must be >=0 ', visible=True)
            else:
                print("Saving P Width as: " + str(np_width))

                # Updating measurement label description to specified value
                graph_charge.DrawText(str(np_width) + ' [nm]', (162.5, 400),
                                      color="blue", font=None,
                                      angle=0, text_location="center")

                # Setting boolean tracker to 1 and removing warning labels
                bool_NPWidth = 1
                np_width_warning.Update('Warning Message: ', visible=False)
        else:
            # Updating measurement label to be unknown
            graph_charge.DrawText('?? [nm]', (162.5, 400), color="blue", font=None,
                                  angle=0, text_location="center")

            # Setting boolean tracker to 0 and add warning message depending on foundry and PN type
            bool_NPWidth = 0
            if values['-AMF-']:
                np_width_warning.Update('Warning Message: N+ Width Not Specified ', visible=True)
            elif values['-AIM-']:
                np_width_warning.Update('Warning Message: N3Al Width Not Specified ', visible=True)

    # If convertion to float fails, instruct user to fix error
    except ValueError:
        # Boolean tracker set to 0 here also and add invalid N+ width warning
        bool_NPWidth = 0
        if values['-AMF-']:
            np_width_warning.Update('Warning Message: Invalid N+ Width', visible=True)
        elif values['-AIM-']:
            np_width_warning.Update('Warning Message: Invalid N3Al Width', visible=True)

        # Updating measurement label to be unknown
        graph_charge.DrawText('?? [nm]', (162.5, 400), color="blue", font=None,
                              angle=0, text_location="center")

    # Attempt to convert value inside P++ width textbox to float
    try:
        # Checking if P++ width textbox is not empty
        if values['-P++_WIDTH-'] != '':
            # Populating P++ width
            ppp_width = float(values['-P++_WIDTH-'])
            if ppp_width < 0:
                # Updating measurement label to be unknown
                graph_charge.DrawText('?? [nm]', (12, 400), color="blue", font=None,
                                      angle=0, text_location="center")

                # Setting boolean tracker to 0 and add warning message depending on foundry
                # and PN type
                bool_PPPWidth = 0
                if values['-AMF-']:
                    ppp_width_warning.Update(
                        'Warning Message: P++ Width must be >=0', visible=True)
                elif values['-AIM-']:
                    ppp_width_warning.Update(
                        'Warning Message: P5Al Width must be >=0 ', visible=True)
            else:
                print("Saving P Width as: " + str(ppp_width))

                # Updating measurement label description to specified value
                graph_charge.DrawText(str(ppp_width) + ' [nm]', (12, 400), color="blue", font=None,
                                      angle=0, text_location="center")

                # Setting boolean tracker to 1 and removing warning labels
                bool_PPPWidth = 1
                ppp_width_warning.Update('Warning Message: ', visible=False)
        else:
            # Updating measurement label to be unknown
            graph_charge.DrawText('?? [nm]', (12, 400), color="blue", font=None,
                                  angle=0, text_location="center")

            # Setting boolean tracker to 0 and add warning message depending on foundry and PN type
            bool_PPPWidth = 0
            if values['-AMF-']:
                ppp_width_warning.Update('Warning Message: P++ Width Not Specified ', visible=True)
            elif values['-AIM-']:
                ppp_width_warning.Update('Warning Message: P5Al Width Not Specified ', visible=True)

    # If convertion to float fails, instruct user to fix error
    except ValueError:
        # Boolean tracker set to 0 here also and add invalid P++ width warning
        bool_PPPWidth = 0
        if values['-AMF-']:
            ppp_width_warning.Update('Warning Message: Invalid P++ Width', visible=True)
        elif values['-AIM-']:
            ppp_width_warning.Update('Warning Message: Invalid P5Al Width', visible=True)

        # Updating measurement label to be unknown
        graph_charge.DrawText('?? [nm]', (12, 400), color="blue", font=None,
                              angle=0, text_location="center")

    # Attempt to convert value inside N++ width textbox to float
    try:
        # Checking if N++ width textbox is not empty
        if values['-N++_WIDTH-'] != '':
            # Populating N++ width
            npp_width = float(values['-N++_WIDTH-'])
            if npp_width < 0:
                # Updating measurement label to be unknown
                graph_charge.DrawText('?? [nm]', (187, 400), color="blue", font=None,
                                      angle=0, text_location="center")

                # Setting boolean tracker to 0 and add warning message depending on foundry
                # and PN type
                bool_NPPWidth = 0
                if values['-AMF-']:
                    npp_width_warning.Update(
                        'Warning Message: N++ Width must be >=0 ', visible=True)
                elif values['-AIM-']:
                    npp_width_warning.Update(
                        'Warning Message: N5Al Width must be >=0 ', visible=True)
            else:
                print("Saving P Width as: " + str(npp_width))

                # Updating measurement label description to specified value
                graph_charge.DrawText(str(npp_width) + ' [nm]', (187, 400), color="blue", font=None,
                                      angle=0, text_location="center")

                # Setting boolean tracker to 1 and removing warning labels
                bool_NPPWidth = 1
                npp_width_warning.Update('Warning Message: ', visible=False)
        else:
            # Updating measurement label to be unknown
            graph_charge.DrawText('?? [nm]', (187, 400), color="blue", font=None,
                                  angle=0, text_location="center")

            # Setting boolean tracker to 0 and add warning message depending on foundry and PN type
            bool_NPPWidth = 0
            if values['-AMF-']:
                npp_width_warning.Update('Warning Message: N++ Width Not Specified ', visible=True)
            elif values['-AIM-']:
                npp_width_warning.Update('Warning Message: N5Al Width Not Specified ', visible=True)

    # If convertion to float fails, instruct user to fix error
    except ValueError:
        # Boolean tracker set to 0 here also and add invalid N++ width warning
        bool_NPPWidth = 0
        if values['-AMF-']:
            npp_width_warning.Update('Warning Message: Invalid N++ Width', visible=True)
        elif values['-AIM-']:
            npp_width_warning.Update('Warning Message: Invalid N5Al Width', visible=True)

        # Updating measurement label to be unknown
        graph_charge.DrawText('?? [nm]', (187, 400), color="blue", font=None,
                              angle=0, text_location="center")

    # Attempt to convert value inside minimum voltage textbox to float
    try:
        # Checking if minimum voltage textbox is not empty
        if values['-VMIN_CHARGE-'] != '':
            # Populating minimum voltage
            vmin = float(values['-VMIN_CHARGE-'])
            print("Saving Min Voltage as: " + str(vmin))

            # Setting boolean tracker to 1 and removing warning labels
            bool_vmin = 1
            vmin_charge_warning.Update('Warning Message: ', visible=False)
        else:
            # Setting boolean tracker to 0 and add warning message that min voltage not specified
            bool_vmin = 0
            vmin_charge_warning.Update('Warning Message: Min Voltage Not Specified ', visible=True)

    except ValueError:
        # Boolean tracker set to 0 here also and add invalid min voltage warning
        bool_vmin = 0
        vmin_charge_warning.Update('Warning Message: Invalid Min Voltage', visible=True)

    # Attempt to convert value inside max voltage textbox to float
    try:
        # Checking if max voltage textbox is not empty
        if values['-VMAX_CHARGE-'] != '':
            # Populate maximum voltage
            vmax = float(values['-VMAX_CHARGE-'])
            print("Saving Max Voltage as: " + str(vmax))

            # Setting boolean tracker to 1 and removing warning labels
            bool_vmax = 1
            vmax_charge_warning.Update('Warning Message: ', visible=False)
        else:
            # Setting boolean tracker to 0 and add warning message that max voltage not specified
            bool_vmax = 0
            vmax_charge_warning.Update('Warning Message: Max Voltage Not Specified ', visible=True)

    # If convertion to float fails, instruct user to fix error
    except ValueError:
        # Boolean tracker set to 0 here also and add invalid max voltage warning
        bool_vmax = 0
        vmax_charge_warning.Update('Warning Message: Invalid Max Voltage', visible=True)

    # Checking if save name is not empty
    if values['-SAVE_NAME-'] != '':
        # Populating save name
        save_name = values['-SAVE_NAME-']
        print("Saving filename as: " + save_name)

        # Setting boolean tracker to 1 and removing warning labels
        bool_savename = 1
        save_name_warning.Update('Warning Message: ', visible=False)

        # Making sure save_name is an appropriate string for a filename
        keepcharacters = (' ', '_')
        check_name = "".join(c for c in save_name if c.isalnum() or c in keepcharacters).rstrip()
        if check_name != save_name:
            save_name_warning.Update('Note: Filename modified to:' + check_name, visible=True)
            save_name = check_name

        # Checking if filename already exists for a previous simulation
        cwd = os.getcwd()
        if os.path.exists(cwd + "\\Database\\Charge_" + foundry + '\\' + save_name + '.mat'):
            save_name_warning.Update('Note: File already exists with this name', visible=True)
            bool_savename = 0

    else:
        # Setting boolean tracker to 0 and add warning message that save name is not specified
        bool_savename = 0
        save_name_warning.Update('Warning Message: Filename Not Specified ', visible=True)

    # Check if every single input has passed their individual checker before setting final boolean
    # Tracker to either being 0 or 1
    if bool_PWidth_core == 1 and bool_PWidth_slab == 1 and bool_PPWidth == 1 and bool_PPPWidth == 1 and \
            bool_NWidth_core == 1 and bool_NWidth_slab == 1 and bool_NPWidth == 1 and bool_NPPWidth == 1 and \
            bool_vmin == 1 and bool_vmax == 1 and bool_savename == 1:
        bool_charge_params = 1
    else:
        bool_charge_params = 0

    # Converting to SI units
    p_width_core = round(p_width_core*1e-9, 10)
    n_width_core = round(n_width_core*1e-9, 10)
    p_width_slab = round(p_width_slab*1e-9, 10)
    n_width_slab = round(n_width_slab*1e-9, 10)
    pp_width = round(pp_width*1e-9, 10)
    np_width = round(np_width*1e-9, 10)
    ppp_width = round(ppp_width*1e-9, 10)
    npp_width = round(npp_width*1e-9, 10)

    return [bool_charge_params, p_width_core, n_width_core,
            p_width_slab, n_width_slab, pp_width, np_width,
            ppp_width, npp_width, vmin, vmax, save_name,
            bias, foundry, PN_Type]


def CheckChargeFile(values, charge_file_warning, bool_define_charge):
    """
    Check if selected charge file is valid.

    Parameters
    ----------
    values : dictionary
        Dictionairy containing all the values present in the GUI.
    charge_file_warning : str
        Warning message if selected charge file is invalid.
    bool_define_charge : int
        Boolean tracker that determines if the user is creating a PN junction.

    Returns
    -------
    bool_load_charge : int
        Boolean tracker that determined if the user is loading a file properly.
    file : file
        Matlab data file (.mat) file that corresponds to PN junction data that the user loaded.

    """
    # Import pathlib for file searching
    from pathlib import Path

    # Initialize boolean tracker as default
    bool_load_charge = 0

    # Extract path from dictionairy
    path = values['-CHARGE_FILE-']

    # Convert path to file
    file = Path(path)

    # Check if file is actually a file
    if file.is_file():
        # Checking if file extension is a .mat file
        if str(file).split('\\')[-1].split('.')[-1] == 'mat':
            bool_load_charge = 1
            charge_file_warning.Update('', visible=False)
        else:
            charge_file_warning.Update('Warning Message: Selected file is not a .mat file',
                                       visible=True)
    else:
        # If user has not recently defined a charge, warn user of no loaded .mat
        if bool_define_charge == 0:
            charge_file_warning.Update('Warning Message: Failed to load CHARGE', visible=True)
        # No warning since user is defining a charge
        else:
            charge_file_warning.Update('', visible=False)
    return bool_load_charge, file


def check_for_variability_analysis(values, corner_analysis_warning):
    """
    Check if selected charge file is valid.

    Parameters
    ----------
    values : dictionary
        Dictionairy containing all the values present in the GUI.
    corner_analysis_warning: int
        Warning message to instruct the user to finish providing variability information
    Returns
    -------
    bool_variability : int
        Boolean tracker that determined if variability analysis should be performed
    corner_analysis_warning : str
        Warning message to instruct the user to finish providing variability information
    """
    bool_variability = 0

    if values['-CORNER_ANALYSIS-']:
        bool_variability = 1
        corner_analysis_warning.Update('Go to Variability Analysis Tab', visible=True)

    return bool_variability


# =============================================================================
# def check_variability_range(values, Variability_Dict,
#                             wg_height_range_warning,
#                             wg_width_range_warning,
#                             slab_height_range_warning,
#                             doping_concentration_range_warning):
# =============================================================================
def check_variability_range(values, Variability_Dict):
    """
    Check variability analysis ranges and verifiy inputs.

    Parameters
    ----------
    values : dictionary
        Dictionairy containing all the values present in the GUI.
    wg_height_range_warning : str
        Warning message for waveguide height range.
    wg_width_range_warning : str
        Warning message for waveguide width range.
    slab_height_range_warning : str
        Warning message for slab height range.
    doping_concentration_range_warningg : str
        Warning message for doping concentration range.

    Returns
    -------
    Variability_Dict : dictionary
        Dictionary containing all variability analysis information
    """

    # Attempt to convert value inside waveguide height error textbox to float
    if values['-VARIABILITY_WAVEGUIDE_HEIGHT-']:
        try:
            if values['-WAVEGUIDE_HEIGHT_RANGE-'] != '':
                # Populating waveguide height range
                wg_height_range = float(values['-WAVEGUIDE_HEIGHT_RANGE-'])
                if wg_height_range <= 0:
                    # Boolean tracker set to 0 here also and invalid waveguide height range
                    # warning added
                    Variability_Dict['Waveguide Height Warning'].Update(
                        'Warning Message: Range must be positive', visible=True)
                else:
                    print("Saving wg_height_range as:" + str(wg_height_range))
                    Variability_Dict['Waveguide Height Range'] = wg_height_range

                    # Setting boolean tracker to 1 and removing any warnings
                    Variability_Dict['Waveguide Height Warning'].Update(
                        'Warning Message: ', visible=False)
            else:
                # Setting boolean tracker to 0 and adding warning that waveguide height range
                # is not specified
                Variability_Dict['Waveguide Height Warning'].Update(
                    'Warning Message: Range Not Specified', visible=True)

        # If convertion to float fails, instruct user to fix error
        except ValueError:
            # Boolean tracker set to 0 here also and invalid waveguide height range warning added
            Variability_Dict['Waveguide Height Warning'].Update(
                'Warning Message: Invalid Range', visible=True)

    if values['-VARIABILITY_WAVEGUIDE_WIDTH-']:
        # Attempt to convert value inside waveguide width error textbox to float
        try:
            if values['-WAVEGUIDE_WIDTH_RANGE-'] != '':
                # Populating waveguide width range
                wg_width_range = float(values['-WAVEGUIDE_WIDTH_RANGE-'])
                if wg_width_range <= 0:
                    # Boolean tracker set to 0 here also and invalid waveguide width range
                    # warning added
                    Variability_Dict['Waveguide Width Warning'].Update(
                        'Warning Message: Range must be positive', visible=True)
                else:
                    print("Saving wg_width_range as:" + str(wg_width_range))
                    Variability_Dict['Waveguide Width Range'] = wg_width_range

                    # Setting boolean tracker to 1 and removing any warnings
                    Variability_Dict['Waveguide Width Warning'].Update(
                        'Warning Message: ', visible=False)
            else:
                # Setting boolean tracker to 0 and adding warning that waveguide width range

                Variability_Dict['Waveguide Width Warning'].Update(
                    'Warning Message: Range Not Specified', visible=True)

        # If convertion to float fails, instruct user to fix error
        except ValueError:
            # Boolean tracker set to 0 here also and invalid waveguide width range warning added
            Variability_Dict['Waveguide Width Warning'].Update(
                'Warning Message: Invalid Range', visible=True)

    if values['-VARIABILITY_SLAB_HEIGHT-']:
        # Attempt to convert value inside slab height error textbox to float
        try:
            if values['-SLAB_HEIGHT_RANGE-'] != '':
                # Populating slab height range
                slab_height_range = float(values['-SLAB_HEIGHT_RANGE-'])
                if slab_height_range <= 0:
                    # Boolean tracker set to 0 here also and invalid slab height range
                    # warning added
                    Variability_Dict['Slab Height Warning'].Update(
                        'Warning Message: Range must be positive', visible=True)
                else:
                    print("Saving wg_height_range as:" + str(slab_height_range))
                    Variability_Dict['Slab Height Range'] = slab_height_range

                    # Setting boolean tracker to 1 and removing any warnings
                    Variability_Dict['Slab Height Warning'].Update(
                        'Warning Message: ', visible=False)
            else:
                # Setting boolean tracker to 0 and adding warning that slab height range
                # is not specified
                Variability_Dict['Slab Height Warning'].Update(
                    'Warning Message: Range Not Specified', visible=True)

        # If convertion to float fails, instruct user to fix error
        except ValueError:
            # Boolean tracker set to 0 here also and invalid slab height range warning added
            Variability_Dict['Slab Height Warning'].Update(
                'Warning Message: Invalid Range', visible=True)

    if values['-VARIABILITY_DOPING_CONCENTRATION-']:
        # Attempt to convert value inside doping concentration error textbox to float
        try:
            if values['-DOPING_CONCENTRATION_RANGE-'] != '':
                # Populating waveguide height range
                doping_range = float(values['-DOPING_CONCENTRATION_RANGE-'])
                if doping_range <= 0:
                    # Boolean tracker set to 0 here also and invalid waveguide height range
                    # warning added
                    Variability_Dict['Doping Concentration Warning'].Update(
                        'Warning Message: Range must be positive', visible=True)
                else:
                    print("Saving doping_concentration_range as:" + str(doping_range))
                    Variability_Dict['Doping Concentration Range'] = doping_range

                    # Setting boolean tracker to 1 and removing any warnings
                    Variability_Dict['Doping Concentration Warning'].Update(
                        'Warning Message: ', visible=False)
            else:
                # Setting boolean tracker to 0 and adding warning that waveguide height range
                # is not specified
                Variability_Dict['Doping Concentration Warning'].Update(
                    'Warning Message: Range Not Specified', visible=True)

        # If convertion to float fails, instruct user to fix error
        except ValueError:
            # Boolean tracker set to 0 here also and invalid waveguide height range warning added
            Variability_Dict['Doping Concentration Warning'].Update(
                'Warning Message: Invalid Range', visible=True)

    return Variability_Dict


def update_variability(values, Variability_Dict, selected_dimensions,
                       corner_analysis_warning, desired_dimensions=2):
    """
    Update selected variables for variability analysis and return display text.

    Parameters
    ----------
    values : dictionary
        Dictionairy containing all the values present in the GUI.
    wg_height_range_warning : string
    Variability_Dict : dict
        Dictionairy containing all variability set up information
    selected_dimensions : int
        Number of selected dimensions in the variability analysis.
    desired_dimensions : int [optional]
        Desired number of dimensions in the variability analysis. Default is 2 for now

    Returns
    -------
    display_string : str
        String used to display to the user which variables are used in the variability analysis.
    bool_corner_analyis_ready : int
        Boolean tracker to determine if the variability analysis has been set up properly
    """
    # Combing through booleans
    display_string = ('Current Selected Variability Analysis Settings: \n')
    Displayed = []
    bool_corner_analyis_ready = 0
    for ii in range(selected_dimensions):
        for key in Variability_Dict:
            if '[ID]' in key and key not in Displayed:
                if Variability_Dict[key]:
                    Name = key.replace('[ID] ', '')
                    Range_key = Name + ' Range'
                    Range = Variability_Dict[Range_key]
                    Units_key = Name + ' Units'
                    Units = Variability_Dict[Units_key]
                    if Range != 0:
                        display_string += Name + ' +- ' + str(Range) + ' ' + Units + '\n'
                        Displayed.append(key)
                    break

    if len(Displayed) == desired_dimensions:
        bool_corner_analyis_ready = 1
        corner_analysis_warning.Update('', visible=False)
# =============================================================================
# =============================================================================
# # Combing through booleans
# Displayed = [0, 0, 0, 0]
# Settings = ['', '']
# Info = ['Waveguide Height +-',
#         'Waveguide Width +-',
#         'Slab Height +-',
#         'Doping Concentration +-']
# Units = ['nm', 'nm', 'nm', '%']
# =============================================================================
#     for ii in range(selected_dimensions):
#         for jj in range(len(Options)):
#             if Options[jj] and not Displayed[jj]:
#                 Settings[ii] = Info[jj] + str(Ranges[jj]) + str(Units[jj])
#                 Displayed[jj] = 1
#                 break
# =============================================================================
# =============================================================================
#     display_string = ('Current Selected Variability Analysis Settings: '
#                       + str(Settings[0]) + ' & ' + str(Settings[1]))
# =============================================================================

    return display_string, bool_corner_analyis_ready


def check_for_variability_analysis_charge(values):
    """
    Check if PN junction simulations for varibility analysis are present.

    Parameters
    ----------
    values : dictionary
        Dictionairy containing all the values present in the GUI.

    Returns
    -------
    bool_charge_corner_BL : int
        Boolean tracker that determined if Bottom left corner analysis has been performed
    bool_charge_corner_BR : int
        Boolean tracker that determined if Bottom right corner analysis has been performed
    bool_charge_corner_TL : int
        Boolean tracker that determined if Top left corner analysis has been performed
    bool_charge_corner_TR : int
        Boolean tracker that determined if Top right corner analysis has been performed

    """
    from pathlib import Path

    # Initialize boolean tracker as default
    bool_charge_corner_BL = 0
    bool_charge_corner_BR = 0
    bool_charge_corner_TL = 0
    bool_charge_corner_TR = 0
    file_BL = None
    file_BR = None
    file_TL = None
    file_TR = None

    # Extract path from dictionairy
    path = values['-CHARGE_FILE-']
    path_BL = path.removesuffix('.mat') + '_BL_Corner.mat'
    path_BR = path.removesuffix('.mat') + '_BR_Corner.mat'
    path_TL = path.removesuffix('.mat') + '_TL_Corner.mat'
    path_TR = path.removesuffix('.mat') + '_TR_Corner.mat'

    isExist_BL = os.path.exists(path_BL)
    isExist_BR = os.path.exists(path_BR)
    isExist_TL = os.path.exists(path_TL)
    isExist_TR = os.path.exists(path_TR)

    if isExist_BL:
        bool_charge_corner_BL = 1
        file_BL = Path(path_BL)
    if isExist_BR:
        bool_charge_corner_BR = 1
        file_BR = Path(path_BR)
    if isExist_TL:
        bool_charge_corner_TL = 1
        file_TL = Path(path_TL)
    if isExist_TR:
        bool_charge_corner_TR = 1
        file_TR = Path(path_TR)

    return (bool_charge_corner_BL, bool_charge_corner_BR,
            bool_charge_corner_TL, bool_charge_corner_TR,
            file_BL, file_BR, file_TL, file_TR)


def check_secondary_inputs(values, CHARGE_file, laser_warning,
                           vmin_warning, vmax_warning, bitrate_warning):
    """
    Check eye diagram inputs for errors.

    Parameters
    ----------
    values : dictionary
        Dictionairy containing all the values present in the GUI.
    CHARGE_file : WindowsPath
        Path to CHARGE simulation results used for ring simulation.
    laser_warning : str
        Warning message to user if operating laser wavelengths is incorrectly specified.
    vmin_warning : str
        Warning message to user if eye diagram min voltage is incorrectly specified.
    vmax_warning : str
        Warning message to user if eye diagram max voltage is incorrectly specified.
    bitrate_warning : str
        Warning message to user if bitrate is incorrectly specified.

    Returns
    -------
    list
        List containing : [Laser_Wavelength, VMin, VMax, Bitrate, staticNonLinCorrec, bool_eye]
            Laser_Wavelength : float
                Operating wavelength for modulation laser.
            VMin : float
                Minimum voltage used for eye diagram simulation.
            VMax : float
                Maximum voltage used for eye diagram simulation.
            staticNonLinCorrec : str
                Identifier for static non-linearity correction either [yes, no, N/A]
            bool_eye : int
                Boolean tracker if eye digram inputs are all correct.

    """
    # Import database connection to query for charge data
    import ConnectToDatabase as database

    # Loading in charge details to cross reference modulation request
    foundry_check = str(CHARGE_file).split('\\')[-2]
    if foundry_check == 'Charge_AMF':
        foundry = 'AMF'
    elif foundry_check == 'Charge_AIM':
        foundry = 'AIM'

    # Populating relevant CHARGE simulation data
    charge_file = str(CHARGE_file).split('\\')[-1]
    charge_file = charge_file.split('.')[0]
    charge_query = database.QueryChargeFile(charge_file, foundry)
    charge_vmin = charge_query[0][16]
    charge_vmax = charge_query[0][17]

    # Poplating simulation wavelength range for laser crossreference
    # Keeping unit sthe same as the user inputs for the eye diagram window
    if values['-CL_BAND-']:
        wavl_min = 1500
        wavl_max = 1600
    elif values['O_BAND-']:
        wavl_min = 1260
        wavl_max = 1400

    # Initializing values
    VMin = None
    VMax = None
    Laser_Wavelength = None
    Bitrate = None

    # Attempt to convert value inside laser wavelength textbox to float
    try:
        # Checking if laser wavelength textbox is not empty
        if values['-LASER-'] != '':
            # Populating laser wavelength
            Laser_Wavelength = float(values['-LASER-'])
            print("Saving Laser Wavelength as:" + str(Laser_Wavelength))

            # Checking if laser wavelength is within the bounds of the ring simulation
            if Laser_Wavelength > wavl_max:
                # Setting boolean tracker to 0 and adding warning that laser wavelength too high
                bool_laser = 0
                laser_warning.Update('Warning Message: Laser Wavelength Is Too High', visible=True)
            elif Laser_Wavelength < wavl_min:
                # Setting boolean tracker to 0 and adding warning that laser wavelength is too low
                bool_laser = 0
                laser_warning.Update('Warning Message: Laser Wavelength Is Too Low', visible=True)
            else:
                # Setting boolean tracker to 1 and removing any warnings
                bool_laser = 1
                laser_warning.Update('Warning Message: ', visible=False)
        else:
            # Setting boolean tracker to 0 and adding warning that laser wavelength is not specified
            bool_laser = 0
            laser_warning.Update('Warning Message: Laser Wavelength Not Specified', visible=True)

    # If convertion to float fails, instruct user to fix error
    except ValueError:
        # Boolean tracker set to 0 here also and add invalid laser wavelength warning
        bool_laser = 0
        laser_warning.Update('Warning Message: Invalid Laser Wavleength', visible=True)

    # Attempt to convert value min eye voltage textbox to float
    try:
        # Checking if min eye voltage textbox is not empty
        if values['-VMIN-'] != '':
            # Populating min eye voltage
            VMin = float(values['-VMIN-'])

            # Checking if minimum eye voltage is above CHARGE simulation minimum voltage
            if VMin >= charge_vmin:
                # Setting boolean tracker to 1 and removing any warnings
                print("Saving VMin as:" + str(VMin))
                bool_vmin = 1
                vmin_warning.Update('Warning Message: ', visible=False)
            else:
                # Setting boolean tracker to 0 and warning about out of bounds
                bool_vmin = 0
                vmin_warning.Update((
                    'Warning Message: Vmin smaller'
                    ' than CHARGE lower bound of ' + str(charge_vmin)), visible=True)
        else:
            # Setting boolean tracker to 0 and add warning that min eye voltage is not specified
            bool_vmin = 0
            vmin_warning.Update('Warning Message: VMin Not Specified', visible=True)

    # If convertion to float fails, instruct user to fix error
    except ValueError:
        # Boolean tracker set to 0 here also and invalid add min eye voltage warning
        bool_vmin = 0
        vmin_warning.Update('Warning Message: Invalid VMin', visible=True)

    # Attempt to convert value inside max eye voltage textbox to float
    try:
        # Checking if max eye voltage textbox is not empty
        if values['-VMAX-'] != '':
            # Populating min eye voltage
            VMax = float(values['-VMAX-'])
            if VMax <= charge_vmax:
                # Setting boolean tracker to 1 and removing any warnings
                print("Saving V Max as:" + str(VMax))
                bool_vmax = 1
                vmax_warning.Update('Warning Message: ', visible=False)
            else:
                # Setting boolean tracker to 0 and warning about out of bounds
                bool_vmax = 0
                vmax_warning.Update((
                    'Warning Message: Vax bigger'
                    ' than CHARGE upper bound of ' + str(charge_vmax)), visible=True)
        else:
            # Setting boolean tracker to 0 and add warning that max eye voltage is not specified
            bool_vmax = 0
            vmax_warning.Update('Warning Message: VMax Not Specified', visible=True)
    except ValueError:
        # Boolean tracker set to 0 here also and add invalid max eye voltage warning
        bool_vmax = 0
        vmax_warning.Update('Warning Message: Invalid VMax', visible=True)

    # Attempt to convert value inside bitrate textbox to float
    try:
        # Checking if bitrate textbox is not empty
        if values['-BITRATE-'] != '':
            # Populating bitrate
            Bitrate = float(values['-BITRATE-'])

            # Checking if bitrate is greater than 0
            if Bitrate > 0:
                # Setting boolean tracker to 1 and removing any warnings
                print("Saving V Max as:" + str(Bitrate))
                bool_bitrate = 1
                bitrate_warning.Update('Warning Message: ', visible=False)
            else:
                # Setting boolean tracker to 0 and warning that bitrate must be greater than 0
                bool_bitrate = 0
                bitrate_warning.Update(
                    'Warning Message: Bitrate Must Be Greater Than 0 ', visible=True)
        else:
            # Setting boolean tracker to 0 and add warning that bitrate is not specified
            bool_bitrate = 0
            bitrate_warning.Update('Warning Message: Bitrate Not Specified', visible=True)
    except ValueError:
        # Boolean tracker set to 0 here also and add invalid bitrate warning
        bool_bitrate = 0
        bitrate_warning.Update('Warning Message: Invalid Bitrate', visible=True)

    # Checking if non-linearity correction is active, no possible errors here
    checkbox = values['-STATIC_NONLIN-']
    if checkbox:
        staticNonLinCorrec = 'yes'
    else:
        staticNonLinCorrec = 'no'

    # Final check if all eye diagram simulation inputs passed their verifications
    if bool_laser == 1 and bool_vmin == 1 and bool_vmax == 1 and bool_bitrate == 1:
        bool_eye = 1
    else:
        bool_eye = 0

    return [Laser_Wavelength, VMin, VMax, Bitrate, staticNonLinCorrec, bool_eye]
