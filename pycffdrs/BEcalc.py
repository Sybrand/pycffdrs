"""
All code is based on the R project: https://cran.r-project.org/package=cffdrs

Comments taken from the R project relating to this module are:

"All variables names are laid out in the same manner as Forestry Canada 
Fire Danger Group (FCFDG) (1992). Development and Structure of the 
Canadian Forest Fire Behavior Prediction System." Technical Report 
ST-X-3, Forestry Canada, Ottawa, Ontario."
"""

@jit
def BEcalc(FUELTYPE: str, BUI: float) -> float:
    """
    Computes the Buildup Effect on Fire Spread Rate.
    """