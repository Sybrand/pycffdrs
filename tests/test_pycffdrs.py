
"""
Test pycffdrs by comparing it to the R cffdrs package.

NOTE: This test assumes you have R and the cffdrs package installed!
"""
import random
import time
from numba.typed import List
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector, StrVector
from pycffdrs import __version__
from pycffdrs.fwiCalc import fwiCalc
from pycffdrs.buiCalc import buiCalc
from pycffdrs.isiCalc import ISIcalc
from pycffdrs.BEcalc import BEcalc
from pycffdrs.CFBcalc import CFBcalc


def test_BEcalc():
    # load cffdrs R package.
    cffdrs = importr('cffdrs')
    # using a seed (for determinism) - run through a bunch of random iterations comparing our output
    # with that of the R package.
    random.seed(42)
    iterations = 50
    array_length = 400
    fuel_types = ("C1", "C2", "C3", "C4", "C5", "C6", "C7", "D1", "M1", "M2", "M3",
                  "M4", "S1", "S2", "S3", "O1A", "O1B")
    python_time = 0
    r_time = 0
    for _ in range(iterations):
        FUELTYPE = [fuel_types[random.randint(0, len(fuel_types)-1)] for x in range(array_length)]
        BUI = [random.uniform(0, 100) for x in range(array_length)]

        start = time.time()
        python_result = BEcalc(List(FUELTYPE), List(BUI))
        python_time += time.time() - start

        start = time.time()
        r_result = cffdrs._BEcalc(StrVector(FUELTYPE), FloatVector(BUI))
        r_time += time.time() - start
        for actual, expected in zip(python_result, r_result):
            assert actual == expected
    print(f'python: {python_time}, r: {r_time}')


def test_fwiCalc():
    # load cffdrs R package.
    cffdrs = importr('cffdrs')
    # using a seed (for determinism) - run through a bunch of random iterations comparing our output
    # with that of the R package.
    random.seed(42)
    for _ in range(100):
        isi = random.uniform(0, 100)
        bui = random.uniform(0, 100)
        assert fwiCalc(isi, bui) == cffdrs._fwiCalc(isi, bui)[0]


def test_buiCalc():
    # load cffdrs R package.
    cffdrs = importr('cffdrs')
    # using a seed (for determinism) - run through a bunch of random iterations comparing our output
    # with that of the R package.
    random.seed(42)
    for _ in range(100):
        dc = random.uniform(0, 600)
        dmc = random.uniform(0, 100)
        assert buiCalc(dc, dmc) == cffdrs._buiCalc(dc, dmc)[0]


def test_ISICalc():
    # load cffdrs R package.
    cffdrs = importr('cffdrs')
    # using a seed (for determinism) - run through a bunch of random iterations comparing our output
    # with that of the R package.
    random.seed(42)
    for _ in range(100):
        ffmc = random.uniform(0, 100)
        ws = random.uniform(0, 100)
        fbpMod = random.randint(0, 1) == 1
        assert ISIcalc(ffmc, ws, fbpMod) == cffdrs._ISIcalc(
            ffmc, ws, fbpMod)[0]


def test_CFBCalc():
    # load cffdrs R package.
    cffdrs = importr('cffdrs')
    # using a seed (for determinism) - run through a bunch of random iterations comparing our output
    # with that of the R package.
    random.seed(42)
    fuel_types = ("C1", "C2", "C3", "C4", "C5", "C6", "C7", "D1", "M1", "M2", "M3",
                  "M4", "S1", "S2", "S3", "O1A", "O1B")

    options = ("CFB", "CSI", "RSO")
    for _ in range(100):
        FUELTYPE = fuel_types[random.randint(0, len(fuel_types)-1)]
        option = options[random.randint(0, len(options)-1)]
        FMC = random.uniform(0, 100)
        SFC = random.uniform(0, 100)
        ROS = random.uniform(0, 100)
        CBH = random.uniform(0, 1)
        assert CFBcalc(FUELTYPE, FMC, SFC, ROS, CBH, option) == cffdrs._CFBcalc(
            FUELTYPE, FMC, SFC, ROS, CBH, option)[0]
