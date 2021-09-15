"""
All code is based on the R project: https://cran.r-project.org/package=cffdrs

"""
import numpy as np
from numpy import ndarray
from numpy import exp
from numba import jit


@jit
def CFBcalc(FUELTYPE: ndarray, # pylint: disable=unused-argument
            FMC: ndarray, SFC: ndarray, ROS: ndarray, CBH: ndarray,
            option: str = "CFB") -> ndarray:
    """
    Calculate Calculate Crown Fraction Burned. To calculate CFB, we also
      need to calculate Critical surface intensity (CSI), and Surface fire
      rate of spread (RSO). The value of each of these equations can be
      returned to the calling function without unecessary additional
      calculations.

    All variables names are laid out in the same manner as Forestry Canada
    Fire Danger Group (FCFDG) (1992). Development and Structure of the
    Canadian Forest Fire Behavior Prediction System." Technical Report
    ST-X-3, Forestry Canada, Ottawa, Ontario.

    Keyword arguments:
    FUELTYPE -- The Fire Behaviour Prediction FuelType
    FMC -- Foliar Moisture Content
    SFC -- Surface Fuel Consumption
    CBH -- Crown Base Height
    ROS -- Rate of Spread
    option -- Which variable to calculate(ROS, CFB, RSC, or RSI)

    Returns:
    CFB, CSI, RSO depending on which option was selected.
    """
    CFB = 0
    # Eq. 56 (FCFDG 1992) Critical surface intensity
    CSI = 0.001 * (CBH**1.5) * (460 + 25.9 * FMC)**1.5
    # Return at this point, if specified by caller
    if option == "CSI":
        return CSI
    # Eq. 57 (FCFDG 1992) Surface fire rate of spread (m/min)
    RSO = CSI / (300 * SFC)
    # Return at this point, if specified by caller
    if option == "RSO":
        return RSO
    # Eq. 58 (FCFDG 1992) Crown fraction burned
    CFB = np.where(ROS > RSO, 1 - exp(-0.23 * (ROS - RSO)), CFB)
    return CFB
