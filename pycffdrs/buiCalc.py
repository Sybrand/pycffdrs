"""
All code is based on the R project: https://cran.r-project.org/package=cffdrs

Comments taken from the R project relating to this module are:

"All code is based on a C code library that was written by Canadian
Forest Service Employees, which was originally based on
the Fortran code listed in the reference below. All equations
in this code refer to that document.

Equations and FORTRAN program for the Canadian Forest Fire
Weather Index System. 1985. Van Wagner, C.E.; Pickett, T.L.
Canadian Forestry Service, Petawawa National Forestry
Institute, Chalk River, Ontario. Forestry Technical Report 33.
18 p.

Additional reference on FWI system

Development and structure of the Canadian Forest Fire Weather
Index System. 1987. Van Wagner, C.E. Canadian Forestry Service,
Headquarters, Ottawa. Forestry Technical Report 35. 35 p."
"""
from numba import jit

@jit
def buiCalc(dmc: float, dc: float) -> float:
    """
    # TODO: switch to using numpy arrays - as done in fwiCalc
    Buildup Index Calculation. A single bui value.

    Keyword arguments:
    dc -- Drought Code
    dmc -- Duff Moisture Code
    """
    #Eq. 27a
    if dmc == 0 and dc == 0:
        bui1 = 0
    else:
        bui1 = 0.8 * dc * dmc/(dmc + 0.4 * dc)
    #Eq. 27b - next 3 lines
    if dmc == 0:
        p = 0
    else:
        p = (dmc - bui1)/dmc
    cc = 0.92 + pow((0.0114 * dmc), 1.7)
    bui0 = dmc - cc * p
    #Constraints
    bui0 = max(bui0, 0)
    if bui1 < dmc:
        bui1 = bui0
    return bui1
