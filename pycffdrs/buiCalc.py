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
from numpy import ndarray

def buiCalc(dmc: ndarray, dc: ndarray) -> float:
    """
    Keyword arguments:
    dc -- Drought Code
    dmc -- Duff Moisture Code
    """
    _bui1 = []
    for _dmc, _dc in zip(dmc, dc):
        # Eq. 27a
        if _dmc == 0 and _dc == 0:
            bui1 = 0
        else:
            bui1 = 0.8 * _dc * _dmc/(_dmc + 0.4 * _dc)
        # Eq. 27b - next 3 lines
        if _dmc == 0:
            p = 0
        else:
            p = (_dmc - bui1)/_dmc
        cc = 0.92 + pow((0.0114 * _dmc), 1.7)
        bui0 = _dmc - cc * p
        # Constraints
        bui0 = max(bui0, 0)
        if bui1 < _dmc:
            bui1 = bui0
        _bui1.append(bui1)
    return _bui1
