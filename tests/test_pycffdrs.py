from pycffdrs import __version__

from pycffdrs.fwiCalc import fwiCalc

def test_version():
    assert __version__ == '0.1.0'

def test_fwiCalc():
    assert fwiCalc(10, 10) == 10.135272037131825
