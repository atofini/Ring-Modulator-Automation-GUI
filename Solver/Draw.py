""".

Created on Mon Sep 26 15:37:51 2022

@author: AlexTofini
"""


def CreateWaveguideCrosssection(graph_charge, PN_Type='Lateral'):
    """
    Creeate the waveguide cross-sectional image for the user.

    Parameters
    ----------
    graph_charge : TKcanvas
        TKcanvas graph object.
    PN_Type : str, optional
        PN junction type declaration. The default is 'Lateral'.
        Options: [Lateral, L-Shaped].

    Returns
    -------
    None.

    """
    # Base
    graph_charge.DrawLine((1, 75), (199, 75), width=5, color="black")

    # Left side
    graph_charge.DrawLine((25, 75), (25, 300), width=2.5, color="black")
    graph_charge.DrawLine((50, 75), (50, 300), width=2.5, color="black")
    graph_charge.DrawLine((1, 75), (1, 300), width=5, color="black")
    graph_charge.DrawLine((1, 300), (75, 300), width=5, color="black")

    # Right side
    graph_charge.DrawLine((199, 75), (199, 300), width=5, color="black")
    graph_charge.DrawLine((125, 300), (199, 300), width=5, color="black")
    graph_charge.DrawLine((150, 75), (150, 300), width=2.5, color="black")
    graph_charge.DrawLine((175, 75), (175, 300), width=2.5, color="black")

    # Core
    graph_charge.DrawLine((75, 300), (75, 525), width=5, color="black")
    graph_charge.DrawLine((125, 300), (125, 525), width=5, color="black")
    graph_charge.DrawLine((75, 525), (125, 525), width=5, color="black")

    # Optional based off PN junction type
    if PN_Type == 'Lateral':
        graph_charge.DrawLine((100, 75), (100, 525), width=2.5, color="black")
    elif PN_Type == 'L-Shaped':
        graph_charge.DrawLine((100, 75), (100, 300), width=2.5, color="black")
        graph_charge.DrawLine((75, 300), (100, 300), width=2.5, color="black")
        graph_charge.DrawLine((75, 75), (75, 300), width=2.5, color="black")


def CreateWaveguideMeasurementLabels(graph_charge):
    """
    Create waveguide doping region measurement labels for the user to visualize their inputs.

    Parameters
    ----------
    graph_charge : TKcanvas
        TKcanvas graph object.

    Returns
    -------
    None.

    """
    # P (Core)
    graph_charge.DrawText('?? [nm]', (87.5, 650),
                          color="blue", font=None, angle=0, text_location="center")
    # N (Core)
    graph_charge.DrawText('?? [nm]', (112.5, 650),
                          color="blue", font=None, angle=0, text_location="center")
    # P (Slab)
    graph_charge.DrawText('?? [nm]', (62.5, 400),
                          color="blue", font=None, angle=0, text_location="center")
    # N (Slab)
    graph_charge.DrawText('?? [nm]', (137.5, 400),
                          color="blue", font=None, angle=0, text_location="center")
    # P+
    graph_charge.DrawText('?? [nm]', (37.5, 400),
                          color="blue", font=None, angle=0, text_location="center")
    # N+
    graph_charge.DrawText('?? [nm]', (162.5, 400),
                          color="blue", font=None, angle=0, text_location="center")
    # P++
    graph_charge.DrawText('?? [nm]', (12, 400),
                          color="blue", font=None, angle=0, text_location="center")
    # N++
    graph_charge.DrawText('?? [nm]', (187, 400),
                          color="blue", font=None, angle=0, text_location="center")


def CreateWaveguideDopantLabels_AMF(graph_charge):
    """
    Create waveguide doping labels for AMF.

    Parameters
    ----------
    graph_charge : TKcanvas
        TKcanvas graph object.

    Returns
    -------
    None.

    """
    # P (Core/Slab)
    graph_charge.DrawText('P', (87.5, 300),
                          color="black", font=("Courier New", 14), angle=0, text_location="center")
    # N (Core/Slab)
    graph_charge.DrawText('N', (112.5, 300),
                          color="black", font=("Courier New", 14), angle=0, text_location="center")
    # P+
    graph_charge.DrawText('P+', (37.5, 175),
                          color="black", font=("Courier New", 14), angle=0, text_location="center")
    # N+
    graph_charge.DrawText('N+', (162.5, 175),
                          color="black", font=("Courier New", 14), angle=0, text_location="center")
    # P++
    graph_charge.DrawText('P++', (12, 175),
                          color="black", font=("Courier New", 14), angle=0, text_location="center")
    # N++
    graph_charge.DrawText('N++', (187, 175),
                          color="black", font=("Courier New", 14), angle=0, text_location="center")


def CreateWaveguideDopantLabels_AIM(graph_charge, PN_Type='Lateral'):
    """
    Create waveguide doping labels for AIM.

    Parameters
    ----------
    graph_charge : TKcanvas
        TKcanvas graph object.

    Returns
    -------
    None.

    """
    if PN_Type == 'Lateral':
        # P1Al (Core/Slab)
        graph_charge.DrawText('P1Al', (87.5, 300),
                              color="black", font=("Courier New", 14),
                              angle=0, text_location="center")
    elif PN_Type == 'L-Shaped':
        # P2Al (Core)
        graph_charge.DrawText('P2Al', (87.5, 175),
                              color="black", font=("Courier New", 14),
                              angle=0, text_location="center")
        # N2Al (Core)
        graph_charge.DrawText('N2Al', (87.5, 400),
                              color="black", font=("Courier New", 14),
                              angle=0, text_location="center")
        # P2Al (Core)
        graph_charge.DrawText('P1Al + \n P2Al', (62.5, 175),
                              color="black", font=("Courier New", 14),
                              angle=0, text_location="center")

    # N1Al (Core/Slab)
    graph_charge.DrawText('N1Al', (112.5, 300),
                          color="black", font=("Courier New", 14), angle=0, text_location="center")
    # P4Al
    graph_charge.DrawText('P4Al', (37.5, 175),
                          color="black", font=("Courier New", 14), angle=0, text_location="center")
    # N3Al
    graph_charge.DrawText('N3Al', (162.5, 175),
                          color="black", font=("Courier New", 14), angle=0, text_location="center")
    # P5Al
    graph_charge.DrawText('P5Al', (12, 175),
                          color="black", font=("Courier New", 14), angle=0, text_location="center")
    # N5Al
    graph_charge.DrawText('N5Al', (187, 175),
                          color="black", font=("Courier New", 14), angle=0, text_location="center")


def CreateWaveguideMeasurementLines(graph_charge):
    """
    Create waveguide measurement lines in blue to emphasize dimensions.

    Parameters
    ----------
    graph_charge : TKcanvas
        TKcanvas graph object.

    Returns
    -------
    None.

    """
    # P (Core)
    graph_charge.DrawLine((75, 600), (99, 600), width=2.5, color="blue")

    # N (Core)
    graph_charge.DrawLine((101, 600), (125, 600), width=2.5, color="blue")

    # P (Slab)
    graph_charge.DrawLine((51, 350), (74, 350), width=2.5, color="blue")

    # N (Slab)
    graph_charge.DrawLine((126, 350), (149, 350), width=2.5, color="blue")

    # P+
    graph_charge.DrawLine((26, 350), (49, 350), width=2.5, color="blue")

    # N+
    graph_charge.DrawLine((151, 350), (174, 350), width=2.5, color="blue")

    # P++
    graph_charge.DrawLine((1, 350), (24, 350), width=2.5, color="blue")

    # N++
    graph_charge.DrawLine((176, 350), (199, 350), width=2.5, color="blue")
