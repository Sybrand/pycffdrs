
"""
Test pycffdrs by comparing it to the R cffdrs package.

NOTE: This test assumes you have R and the cffdrs package installed!
TODO: Stop using R! We can have our tests run much faster, and simplify our github actions etc. etc. by
consuming JSON files.
"""
import json
from typing import List, Dict
import numpy as np
from pycffdrs import __version__
from pycffdrs.fwiCalc import fwiCalc
from pycffdrs.buiCalc import buiCalc
from pycffdrs.isiCalc import ISIcalc
from pycffdrs.BEcalc import BEcalc
from pycffdrs.CFBcalc import CFBcalc


def generic_test(filename, function, *args : str):
    """ Generic test function. Given a filename, a function to test, and the names of arguments
    """
    with open(filename) as f:
        data : List[Dict[str, List]] = json.load(f)
        for record in data:
            values = []
            for key in args:
                values.append(np.array(record.get(key)))
            r_result = np.array([np.float64(x) for x in record.get("result")])
            python_result = function(*values)
            np.testing.assert_equal(python_result, r_result)
            


def test_BEcalc():
    """ Test BEcalc by comparing output from R with that of Python.
    """
    generic_test('tests/BEcalc.json', BEcalc, 'FUELTYPE', 'BUI')

def test_fwiCalc():
    """ Test fwiCalc by comparing output from R with that of Python.
    """
    generic_test('tests/fwiCalc.json', fwiCalc, 'isi', 'bui')

def test_buiCalc():
    """ Test buiCalc by comparing output from R with that of Python.
    """
    generic_test('tests/buiCalc.json', buiCalc, 'dmc', 'dc')


# def test_buiCalc():
#     """ Test buiCalc by comparing output from R with that of Python.
#     """
#     # TODO: stop using R here, switch to using the JSON files. It simplifiest our main project and 
#     # would make tests run faster.
#     # load cffdrs R package.
#     cffdrs = importr('cffdrs')
#     # using a seed (for determinism) - run through a bunch of random iterations comparing our output
#     # with that of the R package.
#     random.seed(42)
#     for _ in range(100):
#         dc = random.uniform(0, 600)
#         dmc = random.uniform(0, 100)
#         assert buiCalc(dmc, dc) == cffdrs._buiCalc(dmc, dc)[0]


# def test_ISICalc():
#     """ Test ISICalc by comparing output from R with that of Python.
#     """
#     # TODO: stop using R here, switch to using the JSON files. It simplifiest our main project and 
#     # would make tests run faster.
#     # load cffdrs R package.
#     cffdrs = importr('cffdrs')
#     # using a seed (for determinism) - run through a bunch of random iterations comparing our output
#     # with that of the R package.
#     random.seed(42)
#     for _ in range(100):
#         ffmc = random.uniform(0, 100)
#         ws = random.uniform(0, 100)
#         fbpMod = random.randint(0, 1) == 1
#         assert ISIcalc(ffmc, ws, fbpMod) == cffdrs._ISIcalc(
#             ffmc, ws, fbpMod)[0]


# def test_CFBCalc():
#     """ Test CFBCalc by comparing output from R with that of Python. """
#     # TODO: stop using R here, switch to using the JSON files. It simplifiest our main project and 
#     # would make tests run faster.
#     # load cffdrs R package.
#     cffdrs = importr('cffdrs')
#     # using a seed (for determinism) - run through a bunch of random iterations comparing our output
#     # with that of the R package.
#     random.seed(42)
#     fuel_types = ("C1", "C2", "C3", "C4", "C5", "C6", "C7", "D1", "M1", "M2", "M3",
#                   "M4", "S1", "S2", "S3", "O1A", "O1B")

#     options = ("CFB", "CSI", "RSO")
#     for _ in range(100):
#         array_length = random.randint(1, 100)
#         FUELTYPE = [fuel_types[random.randint(
#             0, len(fuel_types)-1)] for x in range(array_length)]
#         option = options[random.randint(0, len(options)-1)]
#         FMC = [random.uniform(0, 100) for x in range(array_length)]
#         SFC = [random.uniform(0, 100) for x in range(array_length)]
#         ROS = [random.uniform(0, 100) for x in range(array_length)]
#         CBH = [random.uniform(0, 1) for x in range(array_length)]
#         python_result = CFBcalc(np.array(FUELTYPE), np.array(FMC),
#                                 np.array(SFC), np.array(ROS),
#                                 np.array(CBH), option)
#         r_result = cffdrs._CFBcalc(StrVector(FUELTYPE), FloatVector(FMC),
#                                    FloatVector(SFC), FloatVector(ROS),
#                                    FloatVector(CBH), option)
#         for actual, expected in zip(python_result, r_result):
#             assert actual == expected
