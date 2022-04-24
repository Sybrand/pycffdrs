import random
import json
from typing import List, Dict, Optional
from abc import ABC, abstractmethod
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector, StrVector, BoolVector
import rpy2.robjects as robjs


def get_random_guel_type() -> str:
    """ Get a random fuel type """
    # We include a garbage fuel type.
    fuel_types = ("BLAH", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "D1",
                  "M1", "M2", "M3", "M4", "S1", "S2", "S3", "O1A", "O1B")
    return fuel_types[random.randint(0, len(fuel_types)-1)]


def bui_generator(array_length: int) -> List[float]:
    """ Build a list of random bui """
    return [random.uniform(-10, 110) for _ in range(array_length)]


def fuel_type_generator(array_length: int) -> List[str]:
    """ Build a list of random fuel types """
    return [get_random_guel_type() for _ in range(array_length)]


class TestGenerator(ABC):
    """ Abstract base class to assist in generating test data. """

    def __init__(self, filename: str):
        """ Constructor. """
        # Number of iterations to generate. Each iteration is a list of inputs, which matches to a function
        # call to the R function being tests.
        self.iterations = 25
        # Connect to R.
        self.cffdrs = importr('cffdrs')
        self.filename = filename

    def generate(self):
        """ Generate test data. """
        data = []

        # Seed for reproducibility.
        random.seed(42)
        # Build up some random inputs.
        for _ in range(self.iterations):
            self.create_record(data, random.randint(0, 200))

        self.write_data(data)

    @abstractmethod
    def create_record(self, data: List[Dict[str, List]], array_length: int):
        """ Abstract method. Implement code that creates input data, calls R, and stores inputs + results. """
        pass

    def write_data(self, data: List):
        """ Write results to file """
        with open(self.filename, 'w') as outfile:
            json.dump(data, outfile, indent=4)


class BEcalcGenerator(TestGenerator):

    def create_record(self, data: List[Dict[str, List]], array_length: int):
        """ Create random input data for BEcalc, and call R. """
        FUELTYPE = fuel_type_generator(array_length)
        # BUI is from 0 to unlimited, but we include some garbage values.
        BUI = bui_generator(array_length)
        # calculate
        r_result = self.cffdrs._BEcalc(StrVector(FUELTYPE), FloatVector(BUI))
        # add to data
        data.append({'FUELTYPE': FUELTYPE, 'BUI': BUI,
                    'result': [value for value in r_result]})


class fwiCalcGenerator(TestGenerator):

    def create_record(self, data: List[Dict[str, List]], array_length: int):
        """ Create random input data for FWIcalc, and call R. """
        # initial spread index range is from 0 to unlimited.
        isi = [random.uniform(-10, 110) for _ in range(array_length)]
        # buildup index range is from 0 to inlimited.
        bui = bui_generator(array_length)
        # calculate
        r_result = self.cffdrs._fwiCalc(FloatVector(isi), FloatVector(bui))
        # add to data
        data.append({'isi': isi, 'bui': bui, 'result': [
                    value for value in r_result]})


class buiGenerator(TestGenerator):

    def create_record(self, data: List[Dict[str, List]], array_length: int):
        """ Create random input data for BUIcalc, and call R. """
        dmc = [random.uniform(-10, 610) for _ in range(array_length)]
        dc = [random.uniform(-10, 110) for _ in range(array_length)]
        r_result = self.cffdrs._buiCalc(FloatVector(dmc), FloatVector(dc))
        data.append({'dmc': dmc, 'dc': dc, 'result': [
                    value for value in r_result]})


class ISIcalcGenerator(TestGenerator):

    def create_record(self, data: List[Dict[str, List]], array_length: int):
        """ Create random input data for ISICalc, and call R. """
        ffmc = [random.uniform(0, 100) for _ in range(array_length)]
        ws = [random.uniform(0, 100) for _ in range(array_length)]
        if random.randint(0, 1) == 0:
            fbpMod = None
        else:
            fbpMod = [random.randint(0, 1) == 1 for _ in range(array_length)]

        if fbpMod is None:
            r_result = self.cffdrs._ISIcalc(
                FloatVector(ffmc),
                FloatVector(ws))
        else:
            r_result = self.cffdrs._ISIcalc(
                FloatVector(ffmc),
                FloatVector(ws),
                BoolVector(fbpMod))
        # robjs.r("NULL") if fbpMod is None else BoolVector(fbpMod))
        data.append({'ffmc': ffmc, 'ws': ws, 'fbpMod': fbpMod,
                     'result': [value for value in r_result]})


if __name__ == "__main__":
    BEcalcGenerator('../tests/BEcalc.json').generate()
    fwiCalcGenerator('../tests/fwiCalc.json').generate()
    buiGenerator('../tests/buiCalc.json').generate()
    ISIcalcGenerator('../tests/ISICalc.json').generate()
