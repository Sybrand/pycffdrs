"""
All code and comments based on the R project: https://cran.r-project.org/package=cffdrs

"""
from numpy import ndarray, array, exp
import numpy as np
from BEcalc import BEcalc
from C6calc import C6calc


def ROScalc(FUELTYPE: ndarray, ISI: ndarray, BUI: ndarray, FMC: ndarray, SFC: ndarray, PC: ndarray, PDF: ndarray, CC: ndarray, CBH: ndarray):
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
    # Set up some data vectors
    NoBUI = np.repeat(-1, len(ISI))
    d = ("C1", "C2", "C3", "C4", "C5", "C6", "C7", "D1", "M1", "M2", "M3", "M4",
         "S1", "S2", "S3", "O1A", "O1B")
    a = (90, 110, 110, 110, 30, 30, 45, 30, 0, 0, 120, 100, 75, 40, 55, 190,
         250)
    b = (0.0649, 0.0282, 0.0444, 0.0293, 0.0697, 0.0800, 0.0305, 0.0232, 0, 0,
         0.0572, 0.0404, 0.0297, 0.0438, 0.0829, 0.0310, 0.0350)
    c0 = (4.5, 1.5, 3.0, 1.5, 4.0, 3.0, 2.0, 1.6, 0, 0, 1.4, 1.48, 1.3, 1.7,
          3.2, 1.4, 1.7)

    a = dict(zip(d, a))
    b = dict(zip(d, b))
    c0 = dict(zip(d, c0))

    a = array([a[key] for key in FUELTYPE])
    b = array([b[key] for key in FUELTYPE])
    c0 = array([c0[key] for key in FUELTYPE])

    # Calculate RSI (set up data vectors first)
    # Eq. 26 (FCFDG 1992) - Initial Rate of Spread for Conifer and Slash types
    RSI = np.repeat(-1, len(ISI))

    RSI = np.where((FUELTYPE == "C1") | (FUELTYPE == "C2") | (FUELTYPE == "C3") |
                   (FUELTYPE == "C4") | (FUELTYPE == "C5") | (FUELTYPE == "C6") |
                   (FUELTYPE == "C7") | (FUELTYPE == "D1") | (FUELTYPE == "S1") |
                   (FUELTYPE == "S2") | (FUELTYPE == "S3"),
                   a * (1 - exp(-b * ISI) ** c0),
                   RSI)
    # Eq. 27 (FCFDG 1992) - Initial Rate of Spread for M1 Mixedwood type
    RSI = np.where((FUELTYPE == "M1"), PC/100 *
                   ROScalc(np.repeat("C2", len(ISI)), ISI, NoBUI, FMC, SFC, PC, PDF, CC, CBH)
                   + (100 - PC) / 100 *
                   ROScalc(np.repeat("D1", len(ISI)), ISI, NoBUI, FMC, SFC, PC, PDF, CC, CBH),
                   RSI)
    # TODO: translate the rest:
    # Eq. 27 (FCFDG 1992) - Initial Rate of Spread for M2 Mixedwood type
    # RSI <- ifelse(FUELTYPE %in% c("M2"),
    #         PC/100 *
    #         .ROScalc(rep("C2", length(ISI)),ISI,NoBUI,FMC,SFC,PC,PDF,CC,CBH)
    #         + 0.2*(100-PC)/100 *
    #         .ROScalc(rep("D1", length(ISI)),ISI,NoBUI,FMC,SFC,PC,PDF,CC, CBH),
    #         RSI)
    # #Initial Rate of Spread for M3 Mixedwood
    # RSI_m3 <- rep(-99,length(ISI))
    # #Eq. 30 (Wotton et. al 2009)
    # RSI_m3 <-
    # ifelse(FUELTYPE %in% c("M3"),
    # as.numeric(a[["M3"]] * ((1 - exp(-b[["M3"]] * ISI))**c0[["M3"]])), RSI_m3)
    # #Eq. 29 (Wotton et. al 2009)
    # RSI <-
    # ifelse(FUELTYPE %in% c("M3"),
    # PDF/100* RSI_m3 + (1-PDF/100) *
    #         .ROScalc(rep("D1", length(ISI)), ISI, NoBUI, FMC, SFC, PC, PDF, CC,CBH),
    # RSI)
    # #Initial Rate of Spread for M4 Mixedwood
    # RSI_m4 <- rep(-99,length(ISI))
    # #Eq. 30 (Wotton et. al 2009)
    # RSI_m4 <-
    # ifelse(FUELTYPE %in% c("M4"),
    # as.numeric(a[["M4"]] * ((1 - exp(-b[["M4"]] * ISI))**c0[["M4"]])), RSI_m4)
    # #Eq. 33 (Wotton et. al 2009)
    # RSI <-
    # ifelse(FUELTYPE %in% c("M4"),
    # PDF / 100* RSI_m4 + 0.2 * (1 - PDF / 100)*
    #         .ROScalc(rep("D1", length(ISI)), ISI, NoBUI, FMC, SFC, PC, PDF, CC,CBH),
    # RSI)
    # #Eq. 35b (Wotton et. al. 2009) - Calculate Curing function for grass
    # CF <- rep(-99,length(ISI))
    # CF <-
    # ifelse(FUELTYPE %in% c("O1A", "O1B"),
    #         ifelse(CC < 58.8,
    #                 0.005 * (exp(0.061 * CC) - 1),
    #                 0.176 + 0.02 * (CC - 58.8)),
    #         CF)
    # #Eq. 36 (FCFDG 1992) - Calculate Initial Rate of Spread for Grass
    # RSI <-
    # ifelse(FUELTYPE %in% c("O1A", "O1B"),
    # a[FUELTYPE] * ((1 - exp(-b[FUELTYPE] * ISI))**c0[FUELTYPE]) * CF,
    # RSI)
    # Calculate C6 separately
    ROS = np.where((FUELTYPE == "C6"),
                   C6calc(FUELTYPE, ISI, BUI, FMC, SFC, CBH, option="ROS"),
                   BEcalc(FUELTYPE, BUI) * RSI)
    # add a constraint
    ROS = np.where(ROS <= 0, 0.000001, ROS)
    return ROS
