import random
import json
from typing import List, Dict
from abc import ABC, abstractmethod
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector, StrVector


class TestGenerator(ABC):
    """ Abstract base class to assist in generating test data. """

    def __init__(self):
        """ Constructor. """
        # Number of iterations to generate. Each iteration is a list of inputs, which matches to a function
        # call to the R function being tests.
        self.iterations = 25
        # Connect to R.
        self.cffdrs = importr('cffdrs')
        # We include a garbage fuel type.
        self.fuel_types = ("BLAH", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "D1", "M1", "M2", "M3", "M4", "S1", "S2",
              "S3", "O1A", "O1B")

    def _getRandomFuelType(self):
        """ Randomly select a fuel type (may include garbage) """
        return self.fuel_types[random.randint(0, len(self.fuel_types)-1)]

    def _write_data(self, data: List, filename: str):
        """ Write results to file """
        with open(filename, 'w') as outfile:
            json.dump(data, outfile, indent=4)

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

    @abstractmethod
    def write_data(self, data: List):
        """ Abstract method. Implement code that writes data to file. """
        pass


class BEcalcGenerator(TestGenerator):

    def create_record(self, data: List[Dict[str, List]], array_length: int):
        """ Create random input data for BEcalc, and call R. """
        FUELTYPE = [self._getRandomFuelType() for _ in range(array_length)]
        # BUI is from 0 to unlimited, but we include some garbage values.
        BUI = [random.uniform(-10, 110) for _ in range(array_length)]
        # calculate
        r_result = self.cffdrs._BEcalc(StrVector(FUELTYPE), FloatVector(BUI))
        # add to data
        data.append({'FUELTYPE': FUELTYPE, 'BUI': BUI, 'result': [value for value in r_result]})

    def write_data(self, data: List):
        """ Write data to file """
        self._write_data(data, '../tests/BEcalc.json')
    

class fwiCalcGenerator(TestGenerator):

    def create_record(self, data: List[Dict[str, List]], array_length: int):
        """ Create random input data for FWIcalc, and call R. """
        # initial spread index range is from 0 to unlimited.
        isi = [random.uniform(-10, 110) for _ in range(array_length)]
        # buildup index range is from 0 to inlimited.
        bui = [random.uniform(-10, 110) for _ in range(array_length)]
        # calculate
        r_result = self.cffdrs._fwiCalc(FloatVector(isi), FloatVector(bui))
        # add to data
        data.append({'isi': isi, 'bui': bui, 'result': [value for value in r_result]})

    def write_data(self, data: List):
        """ Write data to file """
        self._write_data(data, '../tests/fwiCalc.json')


if __name__ == "__main__":
    BEcalcGenerator().generate()
    fwiCalcGenerator().generate()
