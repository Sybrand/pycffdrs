"""
All code is based on the R project: https://cran.r-project.org/package=cffdrs

Comments taken from the R project relating to this module are:

"All variables names are laid out in the same manner as Forestry Canada
Fire Danger Group (FCFDG) (1992). Development and Structure of the
Canadian Forest Fire Behavior Prediction System." Technical Report
ST-X-3, Forestry Canada, Ottawa, Ontario."
"""
from numpy import exp, log
from typing import Dict
import numpy as np


def BEcalc(FUELTYPE, BUI):
    """
    Computes the Buildup Effect on Fire Spread Rate.

    Keyword arguments:
    FUELTYPE -- The Fire Behaviour Prediction FuelType
    BUI -- The Buildup Index value
    """
    # Fuel Type String represenations
    d = ("C1", "C2", "C3", "C4", "C5", "C6", "C7", "D1", "M1", "M2", "M3",
         "M4", "S1", "S2", "S3", "O1A", "O1B")
    # The average BUI for the fuel type - as referenced by the "d" list above
    BUIo = (72, 64, 62, 66, 56, 62, 106, 32, 50, 50, 50, 50, 38, 63, 31, 1, 1)
    # Proportion of maximum possible spread rate that is reached at a standard BUI
    Q = (0.9, 0.7, 0.75, 0.8, 0.8, 0.8, 0.85, 0.9, 0.8, 0.8, 0.8, 0.8, 0.75,
         0.75, 0.75, 1.0, 1.0)

    fuel_type_lookup : Dict[str, int] = {}
    for count, value in enumerate(d):
        fuel_type_lookup[value] = count

    size = len(FUELTYPE)
    result = np.empty(size)

    for index in range(size):
        fuel_type_index = fuel_type_lookup.get(FUELTYPE[index], -1)        
        if BUI[index] > 0:
            if fuel_type_index == -1:
                BE = np.nan
            elif BUIo[fuel_type_index] > 0:
                # Eq. 54 (FCFDG 1992) The Buildup Effect
                BE = exp(50 * log(Q[fuel_type_index]) *
                        (1 / BUI[index] - 1 / BUIo[fuel_type_index]))
        else:
            BE = 1
        result[index] = BE
    return result
