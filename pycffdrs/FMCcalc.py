"""
All code and comments based on the R project: https://cran.r-project.org/package=cffdrs
"""
from numpy import ndarray, exp, round  # pylint: disable=redefined-builtin
import numpy as np


# if D0, date of min FMC, is not known then D0 = NULL.
def FMCcalc(LAT: ndarray, LONG: ndarray, ELV: ndarray, DJ: ndarray, D0: ndarray):
    """
     Description:
       Calculate Foliar Moisture Content on a specified day.

       All variables names are laid out in the same manner as Forestry Canada
       Fire Danger Group (FCFDG) (1992). Development and Structure of the
       Canadian Forest Fire Behavior Prediction System." Technical Report
       ST-X-3, Forestry Canada, Ottawa, Ontario.

     Args:
       LAT:    Latitude (decimal degrees)
       LONG:   Longitude (decimal degrees)
       ELV:    Elevation (metres)
       DJ:     Day of year (offeren referred to as julian date)
       D0:     Date of minimum foliar moisture content

     Returns:
       FMC:    Foliar Moisture Content
    """
    # Initialize vectors
    FMC = np.full(len(LAT), -1)
    LATN = np.full(len(LAT), 0)
    # Calculate Normalized Latitude
    # Eqs. 1 & 3 (FCFDG 1992)
    LATN = np.where(D0 <= 0,
                    np.where(ELV <= 0,
                             46 + 23.4 * exp(-0.0360 * (150 - LONG)),
                             43 + 33.7 * exp(-0.0351 * (150 - LONG))),
                    LATN)
    # Calculate Date of minimum foliar moisture content
    # Eqs. 2 & 4 (FCFDG 1992)
    D0 = np.where(D0 <= 0,
                  np.where(ELV <= 0,
                           151 * (LAT / LATN),
                           142.1 * (LAT / LATN) + 0.0172 * ELV),
                  D0)
    # Round D0 to the nearest integer because it is a date
    D0 = round(D0, 0)
    # Number of days between day of year and date of min FMC
    # Eq. 5 (FCFDG 1992)
    ND = abs(DJ-D0)
    # Calculate final FMC
    # Eqs. 6, 7, & 8 (FCFDG 1992)
    FMC = np.where(ND < 30, 85 + 0.0189 * ND**2,
                   np.where((ND >= 30) & (ND < 50),
                            32.9 + 3.17 * ND - 0.0288 * ND**2,
                            120))

    return FMC
