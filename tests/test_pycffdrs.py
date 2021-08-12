
"""
Test pycffdrs by comparing it to the R cffdrs package.

NOTE: This test assumes you have R and the cffdrs package installed!
"""
import random
from rpy2.robjects.packages import importr
from pycffdrs import __version__
from pycffdrs.fwiCalc import fwiCalc
from pycffdrs.buiCalc import buiCalc
from pycffdrs.isiCalc import ISIcalc

def test_version():
    assert __version__ == '0.0.3'

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
        assert ISIcalc(ffmc, ws, fbpMod) == cffdrs._ISIcalc(ffmc, ws, fbpMod)[0]

