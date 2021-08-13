"""
All code is based on the R project: https://cran.r-project.org/package=cffdrs

Comments taken from the R project relating to this module are:

"All variables names are laid out in the same manner as Forestry Canada 
Fire Danger Group (FCFDG) (1992). Development and Structure of the 
Canadian Forest Fire Behavior Prediction System." Technical Report 
ST-X-3, Forestry Canada, Ottawa, Ontario."
"""
from math import exp, log
from numba import jit

@jit
def BEcalc(FUELTYPE: str, BUI: float) -> float:
    """
    Computes the Buildup Effect on Fire Spread Rate.

    Keyword arguments:
    FUELTYPE -- The Fire Behaviour Prediction FuelType
    BUI -- The Buildup Index value
    """
    #Fuel Type String represenations
    d = ("C1", "C2", "C3", "C4", "C5", "C6", "C7", "D1", "M1", "M2", "M3",
            "M4","S1", "S2", "S3", "O1A", "O1B")
    #The average BUI for the fuel type - as referenced by the "d" list above
    BUIo = (72, 64, 62, 66, 56, 62, 106, 32, 50, 50, 50, 50, 38, 63, 31, 1, 1)
    #Proportion of maximum possible spread rate that is reached at a standard BUI
    Q = (0.9, 0.7, 0.75, 0.8, 0.8, 0.8, 0.85, 0.9, 0.8, 0.8, 0.8, 0.8, 0.75, 
            0.75, 0.75, 1.0, 1.0)

    # The R code uses names to effectively create a dictionary:
    # names(BUIo) <- names(Q)<-d
    # It would be nice to use a dictionary, but haven't figured that out in numba yet, so
    # for now we just get the index once.
    index = d.index(FUELTYPE)
    
    #Eq. 54 (FCFDG 1992) The Buildup Effect
    if BUI > 0 and BUIo[index] > 0:
        BE = exp(50 * log(Q[index]) * (1 / BUI - 1 / BUIo[index]))
    else:
        BE = 1
    return BE
