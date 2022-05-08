
"""
Test pycffdrs by comparing it to output from the R cffdrs package.
"""
import json
from typing import List, Dict
import numpy as np
from pycffdrs import __version__
from pycffdrs.fwiCalc import fwiCalc
from pycffdrs.buiCalc import buiCalc
from pycffdrs.ISIcalc import ISIcalc
from pycffdrs.BEcalc import BEcalc
from pycffdrs.CFBcalc import CFBcalc
from pycffdrs.ROScalc import ROScalc
from pycffdrs.C6calc import C6calc


def generic_test(filename, function):
    """ Generic test function. Given a filename, a function to test, and the names of arguments
    """
    with open(filename, 'rb') as f:
        data: List[Dict[str, List]] = json.load(f)
        for record in data:
            values = []
            for value in record.get("input").values():
                if not value is None:
                    values.append(np.array(value))

            r_result = np.array([np.float64(x) for x in record.get("result")])
            python_result = function(*values)
            # Same to 13 decimal places? that seems more than good enough.
            # Ideally we'd match the R output exactly, but with different versions of numpy,
            # different versions of python - this is plenty good.
            np.testing.assert_almost_equal(python_result, r_result, 13)


def test_BEcalc():
    """ Test BEcalc by comparing output from R with that of Python.
    """
    generic_test('tests/BEcalc.json', BEcalc)


def test_fwiCalc():
    """ Test fwiCalc by comparing output from R with that of Python.
    """
    generic_test('tests/fwiCalc.json', fwiCalc)


def test_buiCalc():
    """ Test buiCalc by comparing output from R with that of Python.
    """
    generic_test('tests/buiCalc.json', buiCalc)


def test_ISIcalc():
    """ Test ISIcalc by comparing output from R with that of Python.
    """
    generic_test('tests/ISIcalc.json', ISIcalc)


def test_CFBCalc():
    """ Test CFBcalc by comparing output from R with that of Python.
    """
    generic_test('tests/CFBcalc.json', CFBcalc)


def test_C6calc():
    """ Test C6calc by comparing output from R with that of Python."""
    generic_test('tests/C6calc.json', C6calc)


def test_ROScalc():
    """ Test ROScalc by comparing output from R with that of Python.
    """
    generic_test('tests/ROScalc.json', ROScalc)
