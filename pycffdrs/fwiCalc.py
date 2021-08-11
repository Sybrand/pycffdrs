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
from math import exp, log
from numba import jit

@jit(nopython=True)
def fwiCalc(isi: float, bui: float) -> float:
    """
    Fire Weather Index Calculation. Returns a single fwi value.

    Keyword arguments:
    isi -- Initial Spread Index
    bui -- Buildup Index
    """
    #Eqs. 28b, 28a, 29
    if bui > 80:
        bb = 0.1 * isi * (1000/(25 + 108.64/exp(0.023 * bui)))
    else:
        bb = 0.1 * isi * (0.626 * (bui**0.809) + 2)
    #Eqs. 30b, 30a
    if bb <= 1:
        fwi = bb
    else:
        fwi = exp(2.72 * ((0.434 * log(bb))**0.647))
    return fwi
