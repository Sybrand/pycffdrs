"""
All code and comments based on the R project: https://cran.r-project.org/package=cffdrs

"""
from numpy import ndarray, exp
import numpy as np
from pycffdrs.BEcalc import BEcalc
from pycffdrs.C6calc import C6calc


d = ("C1", "C2", "C3", "C4", "C5", "C6", "C7", "D1", "M1", "M2", "M3", "M4",
     "S1", "S2", "S3", "O1A", "O1B")
a = dict(zip(d, (90, 110, 110, 110, 30, 30, 45, 30, 0, 0, 120, 100, 75, 40, 55, 190,
                 250)))
b = dict(zip(d, (0.0649, 0.0282, 0.0444, 0.0293, 0.0697, 0.0800, 0.0305, 0.0232, 0, 0,
                 0.0572, 0.0404, 0.0297, 0.0438, 0.0829, 0.0310, 0.0350)))
c0 = dict(zip(d, (4.5, 1.5, 3.0, 1.5, 4.0, 3.0, 2.0, 1.6, 0, 0, 1.4, 1.48, 1.3, 1.7,
                  3.2, 1.4, 1.7)))


def _ROScalc(FUELTYPE: str,  # pylint: disable=too-many-arguments
             ISI: float,
             BUI: float,
             FMC: float,
             SFC: float,
             PC: float,
             PDF: float,
             CC: float,
             CBH: float) -> float:
    """ Compute ROS with scalar input values. Nesting makes working with vectors extremely
    difficult. """
    NoBUI = -1
    RSI = -1
    # Eq. 26 (FCFDG 1992) - Initial Rate of Spread for Conifer and Slash types
    if FUELTYPE in ("C1", "C2", "C3", "C4", "C5", "C7", "D1", "S1", "S2", "S3"):
        RSI = a[FUELTYPE] * (1 - exp(-b[FUELTYPE] * ISI))**c0[FUELTYPE]
    # Eq. 27 (FCFDG 1992) - Initial Rate of Spread for M1 Mixedwood type
    elif FUELTYPE == 'M1':
        RSI = PC/100 * _ROScalc("C2", ISI, NoBUI, FMC, SFC, PC, PDF, CC, CBH) + \
            (100 - PC) / 100 * _ROScalc("D1", ISI, NoBUI, FMC, SFC, PC, PDF, CC, CBH)
    # Eq. 27 (FCFDG 1992) - Initial Rate of Spread for M2 Mixedwood type
    elif FUELTYPE == 'M2':
        RSI = PC/100 * _ROScalc("C2", ISI, NoBUI, FMC, SFC, PC, PDF, CC, CBH) + \
            0.2*(100-PC)/100 * _ROScalc("D1", ISI, NoBUI, FMC, SFC, PC, PDF, CC, CBH)
    elif FUELTYPE == 'M3':
        # Initial Rate of Spread for M3 Mixedwood
        # Eq. 30 (Wotton et. al 2009)
        RSI_m3 = a["M3"] * ((1 - exp(-b["M3"] * ISI))**c0["M3"])
        RSI = PDF/100 * RSI_m3 + (1-PDF/100) * _ROScalc("D1", ISI,
                                                        NoBUI, FMC, SFC, PC, PDF, CC, CBH)
    elif FUELTYPE == 'M4':
        # Initial Rate of Spread for M4 Mixedwood
        # Eq. 30 (Wotton et. al 2009)
        RSI_m4 = a["M4"] * ((1 - exp(-b["M4"] * ISI))**c0["M4"])
        # Eq. 33 (Wotton et. al 2009)
        RSI = PDF / 100 * RSI_m4 + 0.2 * (1 - PDF / 100) * \
            _ROScalc("D1", ISI, NoBUI, FMC, SFC, PC, PDF, CC, CBH)
        # Eq. 35b (Wotton et. al. 2009) - Calculate Curing function for grass
    elif FUELTYPE in ('O1A', 'O1B'):
        if CC < 58.8:
            CF = 0.005 * (exp(0.061 * CC) - 1)
        else:
            CF = 0.176 + 0.02 * (CC - 58.8)
        # Eq. 36 (FCFDG 1992) - Calculate Initial Rate of Spread for Grass
        RSI = a[FUELTYPE] * ((1 - exp(-b[FUELTYPE] * ISI))**c0[FUELTYPE]) * CF
    if FUELTYPE == 'C6':
        ROS = C6calc(np.array((FUELTYPE,)), np.array((ISI,)), np.array((BUI,)),
                     np.array((FMC,)), np.array((SFC,)), np.array((CBH,)), option="ROS")
    else:
        ROS = BEcalc(np.array((FUELTYPE,)), np.array((BUI,))) * RSI
    if ROS < 0:
        return 0.000001
    return ROS


def ROScalc(FUELTYPE: ndarray,  # pylint: disable=too-many-arguments, too-many-locals
            ISI: ndarray,
            BUI: ndarray,
            FMC: ndarray,
            SFC: ndarray,
            PC: ndarray,
            PDF: ndarray,
            CC: ndarray,
            CBH: ndarray):
    """
    Computes the Rate of Spread prediction based on fuel type and FWI
    conditions. Equations are from listed FCFDG (1992) and Wotton et. al.
    (2009), and are marked as such.

    All variables names are laid out in the same manner as Forestry Canada
    Fire Danger Group (FCFDG) (1992). Development and Structure of the
    Canadian Forest Fire Behavior Prediction System." Technical Report
    ST-X-3, Forestry Canada, Ottawa, Ontario.

    Wotton, B.M., Alexander, M.E., Taylor, S.W. 2009. Updates and revisions to
    the 1992 Canadian forest fire behavior prediction system. Nat. Resour.
    Can., Can. For. Serv., Great Lakes For. Cent., Sault Ste. Marie, Ontario,
    Canada. Information Report GLC-X-10, 45p.

    Keyword arguments:
    FUELTYPE -- The Fire Behaviour Prediction FuelType
    ISI -- Intiial Spread Index
    BUI -- Buildup Index
    FMC -- Foliar Moisture Content
    SFC -- Surface Fuel Consumption (kg/m^2)
    PC -- Percent Conifer (%)
    PDF -- Percent Dead Balsam Fir (%)
    CC -- Constant
    CBH -- Crown to base height(m)
    Returns:
    ROS: Rate of spread (m/min)
    """
    result = np.empty(len(FUELTYPE))
    for i, (
            _FUELTYPE, _ISI, _BUI, _FMC, _SFC, _PC, _PDF, _CC, _CBH) in enumerate(
                zip(FUELTYPE, ISI, BUI, FMC, SFC, PC, PDF, CC, CBH)):
        result[i] = _ROScalc(_FUELTYPE, _ISI, _BUI, _FMC, _SFC, _PC, _PDF, _CC, _CBH)
    return result
