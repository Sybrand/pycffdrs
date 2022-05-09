"""
All code and comments based on the R project: https://cran.r-project.org/package=cffdrs
"""
from numpy import ndarray


def FIcalc(FC: ndarray, ROS: ndarray):
    """
     Description:
       Calculate the Predicted Fire Intensity

       All variables names are laid out in the same manner as Forestry Canada
       Fire Danger Group (FCFDG) (1992). Development and Structure of the
       Canadian Forest Fire Behavior Prediction System." Technical Report
       ST-X-3, Forestry Canada, Ottawa, Ontario.

     Args:
       FC:   Fuel Consumption (kg/m^2)
       ROS:  Rate of Spread (m/min)

     Returns:
       FI:   Fire Intensity (kW/m)
    """
    # Eq. 69 (FCFDG 1992) Fire Intensity (kW/m)
    return 300 * FC * ROS
