import random
import json
from typing import List, Dict, Optional
from abc import ABC, abstractmethod
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector, StrVector, BoolVector
import rpy2.robjects as robjs


class UnknownTypeError(Exception):
    """ Exception raised when an unknown type is passed to the generator """
    pass


def get_random_fuel_type() -> str:
    """ Get a random fuel type """
    # We include a garbage fuel type.
    fuel_types = ("C1", "C2", "C3", "C4", "C5", "C6", "C7", "D1",
                  "M1", "M2", "M3", "M4", "S1", "S2", "S3", "O1A", "O1B")
    return fuel_types[random.randint(0, len(fuel_types)-1)]


def ffmc_generator(array_length: int) -> List[float]:
    """  Build a list of random ffmc """
    return [random.uniform(0, 100) for _ in range(array_length)]


def bui_generator(array_length: int) -> List[float]:
    """ Build a list of random bui """
    return [random.uniform(0, 110) for _ in range(array_length)]


def fuel_type_generator(array_length: int) -> List[str]:
    """ Build a list of random fuel types """
    return [get_random_fuel_type() for _ in range(array_length)]


def fmc_generator(array_length: int) -> List[float]:
    """ Build a list of random fmc """
    return [random.uniform(0, 100) for _ in range(array_length)]


def sfc_generator(array_length: int) -> List[float]:
    """ Build a list of random sfc """
    return [random.uniform(0, 100) for _ in range(array_length)]


def pc_generator(array_length: int) -> List[float]:
    """ Build a list of random pc """
    return [random.uniform(0, 100) for _ in range(array_length)]


def pdf_generator(array_length: int) -> List[float]:
    """ Build a list of random pdf """
    return [random.uniform(0, 100) for _ in range(array_length)]


def cbh_generator(array_length: int) -> List[float]:
    """ Build a list of random cbh """
    return [random.uniform(2, 7) for _ in range(array_length)]


def cc_generator(array_length: int) -> List[float]:
    """ Build a list of random cc """
    return [random.uniform(0, 100) for _ in range(array_length)]


def isi_generator(array_length: int) -> List[float]:
    """ Build a list of random isi """
    return [random.uniform(0, 100) for _ in range(array_length)]


def ros_generator(array_length: int) -> List[float]:
    """ Build a list of random ros """
    return [random.uniform(0, 10000) for _ in range(array_length)]


def cfb_generator(array_length: int) -> List[float]:
    """ Build a list of random cfb """
    return [random.uniform(0, 100) for _ in range(array_length)]


def rsc_generator(array_length: int) -> List[float]:
    """ Build a list of random rsc """
    return [random.uniform(0, 100) for _ in range(array_length)]


def hr_generator(array_length: int) -> List[float]:
    """ Build a list of random hr """
    return [random.uniform(0, 100) for _ in range(array_length)]


def wsv_generator(array_length: int) -> List[float]:
    """ Build a list of random wind speed vectors """
    return [random.uniform(0, 100) for _ in range(array_length)]


def temp_generator(array_length: int) -> List[float]:
    """ Build a list of random temperatures """
    return [random.uniform(-50, 50) for _ in range(array_length)]


def rh_generator(array_length: int) -> List[float]:
    """ Build a list of random relative humidities """
    return [random.uniform(0, 100) for _ in range(array_length)]


def ws_generator(array_length: int) -> List[float]:
    """ Build a list of random wind speeds """
    return [random.uniform(0, 100) for _ in range(array_length)]


def prec_generator(array_length: int) -> List[float]:
    """ Build a list of random precipitations """
    return [random.uniform(0, 100) for _ in range(array_length)]


def fc_generator(array_length: int) -> List[float]:
    """ Build a list of random fuel consumption """
    return [random.uniform(0, 100) for _ in range(array_length)]


def lat_generator(array_length: int) -> List[float]:
    """ Build a list of random latitudes """
    return [random.uniform(-90, 90) for _ in range(array_length)]


def long_generator(array_length: int) -> List[float]:
    """ Build a list of random longitudes """
    return [random.uniform(-180, 180) for _ in range(array_length)]


def day_of_year_generator(array_length: int) -> List[float]:
    """ Build a list of random day of year """
    return [random.uniform(1, 365) for _ in range(array_length)]


def elevation_generator(array_length: int) -> List[float]:
    """ Build a list of random elevations """
    return [random.uniform(0, 10000) for _ in range(array_length)]


def lb_generator(array_length: int) -> List[float]:
    """ Build a list of random length to breadh ratios """
    return [random.uniform(0, 100) for _ in range(array_length)]


class TestGenerator(ABC):
    """ Abstract base class to assist in generating test data. """

    def __init__(self, filename: str):
        """ Constructor. """
        # Number of iterations to generate. Each iteration is a list of inputs, which matches to a
        # function call to the R function being tests.
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
        """ Abstract method. Implement code that creates input data, calls R, and stores inputs +
        results. """
        pass

    def write_data(self, data: List):
        """ Write results to file """
        with open(self.filename, 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def append_result(self, data: List[Dict[str, List]], input: Dict[str, List], function):
        """ Append result of R function to data. """
        inputs = []
        for value in input.values():
            if (len(value) > 0):
                if isinstance(value[0], float):
                    inputs.append(FloatVector(value))
                elif isinstance(value[0], str):
                    inputs.append(StrVector(value))
                else:
                    raise UnknownTypeError
            else:
                inputs.append([])
        r_result = function(*inputs)

        data.append({'input': input, 'result': [value for value in r_result]})


class BEcalcGenerator(TestGenerator):

    def create_record(self, data: List[Dict[str, List]], array_length: int):
        """ Create random input data for BEcalc, and call R. """
        FUELTYPE = fuel_type_generator(array_length)
        # BUI is from 0 to unlimited, but we include some garbage values.
        BUI = bui_generator(array_length)
        # calculate
        r_result = self.cffdrs._BEcalc(StrVector(FUELTYPE), FloatVector(BUI))
        # add to data
        data.append({'input': {'FUELTYPE': FUELTYPE, 'BUI': BUI},
                    'result': [value for value in r_result]})


class fwiCalcGenerator(TestGenerator):

    def create_record(self, data: List[Dict[str, List]], array_length: int):
        """ Create random input data for FWIcalc, and call R. """
        input = dict(  # initial spread index range is from 0 to unlimited.
            isi=[random.uniform(0, 110) for _ in range(array_length)],
            # buildup index range is from 0 to inlimited.
            bui=bui_generator(array_length))

        self.append_result(data, input, self.cffdrs._fwiCalc)


class buiGenerator(TestGenerator):

    def create_record(self, data: List[Dict[str, List]], array_length: int):
        """ Create random input data for BUIcalc, and call R. """
        input = dict(dmc=[random.uniform(0, 610) for _ in range(array_length)],
                     dc=[random.uniform(-10, 110) for _ in range(array_length)])

        self.append_result(data, input, self.cffdrs._buiCalc)


class ISIcalcGenerator(TestGenerator):

    def create_record(self, data: List[Dict[str, List]], array_length: int):
        """ Create random input data for ISICalc, and call R. """
        ffmc = ffmc_generator(array_length)
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
        data.append({'input': {'ffmc': ffmc, 'ws': ws, 'fbpMod': fbpMod},
                     'result': [value for value in r_result]})


class CFBCalcGenerator(TestGenerator):

    def create_record(self, data: List[Dict[str, List]], array_length: int):
        """ Create random input data for CFBCalc, and call R. """
        FUELTYPE = fuel_type_generator(array_length)
        FMC = fmc_generator(array_length)
        SFC = sfc_generator(array_length)
        ROS = [random.uniform(0, 100) for _ in range(array_length)]
        CBH = cbh_generator(array_length)

        options = (None, "CFB", "CSI", "RSO")
        option = options[random.randint(0, len(options)-1)]

        if option is None:
            r_result = self.cffdrs._CFBcalc(
                StrVector(FUELTYPE),
                FloatVector(FMC),
                FloatVector(SFC),
                FloatVector(ROS),
                FloatVector(CBH))
        else:
            r_result = self.cffdrs._CFBcalc(
                StrVector(FUELTYPE),
                FloatVector(FMC),
                FloatVector(SFC),
                FloatVector(ROS),
                FloatVector(CBH),
                option)
        data.append(
            {
                'input':
                {
                    'FUELTYPE': FUELTYPE, 'FMC': FMC, 'SFC': SFC, 'ROS': ROS, 'CBH': CBH,
                    'option': option
                },
                'result': [value for value in r_result]})


class ROScalcGenerator(TestGenerator):

    def create_record(self, data: List[Dict[str, List]], array_length: int):
        """ Create random input data for ROScalc, and call R. """
        input = dict(FUELTYPE=fuel_type_generator(array_length),
                     ISI=isi_generator(array_length),
                     BUI=bui_generator(array_length),
                     FMC=fmc_generator(array_length),
                     SFC=sfc_generator(array_length),
                     PC=pc_generator(array_length),
                     PDF=pdf_generator(array_length),
                     CC=cc_generator(array_length),
                     CBH=cbh_generator(array_length))

        self.append_result(data, input, self.cffdrs._ROScalc)


class C6calcGenerator(TestGenerator):

    def create_record(self, data: List[Dict[str, List]], array_length: int):
        """ Create random input data for C6calc, and call R. """
        FUELTYPE = fuel_type_generator(array_length)
        ISI = isi_generator(array_length)
        BUI = bui_generator(array_length)
        FMC = fmc_generator(array_length)
        SFC = sfc_generator(array_length)
        CBH = cbh_generator(array_length)
        ROS = ros_generator(array_length)
        CFB = cfb_generator(array_length)
        RSC = rsc_generator(array_length)

        options = (None, "ROS", "CFB", "RSC", "RSI")
        option = options[random.randint(0, len(options)-1)]

        if option is None:
            r_result = self.cffdrs._C6calc(
                StrVector(FUELTYPE),
                FloatVector(ISI),
                FloatVector(BUI),
                FloatVector(FMC),
                FloatVector(SFC),
                FloatVector(CBH),
                FloatVector(ROS),
                FloatVector(CFB),
                FloatVector(RSC),
            )
        else:
            r_result = self.cffdrs._C6calc(
                StrVector(FUELTYPE),
                FloatVector(ISI),
                FloatVector(BUI),
                FloatVector(FMC),
                FloatVector(SFC),
                FloatVector(CBH),
                FloatVector(ROS),
                FloatVector(CFB),
                FloatVector(RSC),
                option
            )
        data.append({'input':
                     {
                         'FUELTYPE': FUELTYPE, 'ISI': ISI, 'BUI': BUI, 'FMC': FMC, 'SFC': SFC,
                         'CBH': CBH, 'ROS': ROS, 'CFB': CFB, 'RSC': RSC,
                         'option': option
                     },
                     'result': [value for value in r_result]})


class DISTtcalcGenerator(TestGenerator):

    def create_record(self, data: List[Dict[str, List]], array_length: int):
        """ Create random input data for DISTtcalc, and call R. """
        input = dict(
            FUELTYPE=fuel_type_generator(array_length),
            ROSeq=ros_generator(array_length),
            HR=hr_generator(array_length),
            CFB=cfb_generator(array_length))

        self.append_result(data, input, self.cffdrs._DISTtcalc)


class BROScalcGenerator(TestGenerator):

    def create_record(self, data: List[Dict[str, List]], array_length: int):
        """ Create random input data for BROScalc, and call R. """
        input = dict(FUELTYPE=fuel_type_generator(array_length),
                     FFMC=ffmc_generator(array_length),
                     BUI=bui_generator(array_length),
                     WSV=wsv_generator(array_length),
                     FMC=fmc_generator(array_length),
                     SFC=sfc_generator(array_length),
                     PC=pc_generator(array_length),
                     PDF=pdf_generator(array_length),
                     CC=cc_generator(array_length),
                     CBH=cbh_generator(array_length))

        self.append_result(data, input, self.cffdrs._BROScalc)


class ffmcCalcGenerator(TestGenerator):

    def create_record(self, data: List[Dict[str, List]], array_length: int):
        """ Create random input data for ffmcCalc, and call R. """
        input = {
            'ffmc_yda': ffmc_generator(array_length),
            'temp': temp_generator(array_length),
            'rh': rh_generator(array_length),
            'ws': ws_generator(array_length),
            'prec': prec_generator(array_length)
        }
        self.append_result(data, input, self.cffdrs._ffmcCalc)


class FIcalcGenerator(TestGenerator):

    def create_record(self, data: List[Dict[str, List]], array_length: int):
        """ Create random input data for FIcalc, and call R. """
        self.append_result(data, dict(FC=fc_generator(array_length),
                                      ROS=ros_generator(array_length)), self.cffdrs._FIcalc)


class FMCcalcGenerator(TestGenerator):

    def create_record(self, data: List[Dict[str, List]], array_length: int):
        """ Create random input data for FMCcalc, and call R. """
        self.append_result(data, dict(LAT=lat_generator(array_length),
                                      LONG=long_generator(array_length),
                                      ELV=elevation_generator(array_length),
                                      DJ=day_of_year_generator(array_length),
                                      D0=day_of_year_generator(array_length)), self.cffdrs._FMCcalc)


class FROScalcGenerator(TestGenerator):

    def create_record(self, data: List[Dict[str, List]], array_length: int):
        """ Create random input data for FROScalcGenerator, and call R. """
        self.append_result(data, dict(ROS=ros_generator(array_length),
                                      BROS=ros_generator(array_length),
                                      LB=lb_generator(array_length)), self.cffdrs._FROScalc)


if __name__ == "__main__":
    BEcalcGenerator('../tests/BEcalc.json').generate()
    fwiCalcGenerator('../tests/fwiCalc.json').generate()
    buiGenerator('../tests/buiCalc.json').generate()
    ISIcalcGenerator('../tests/ISIcalc.json').generate()
    CFBCalcGenerator('../tests/CFBcalc.json').generate()
    ROScalcGenerator('../tests/ROScalc.json').generate()
    C6calcGenerator('../tests/C6calc.json').generate()
    BROScalcGenerator('../tests/BROScalc.json').generate()
    DISTtcalcGenerator('../tests/DISTtcalc.json').generate()
    ffmcCalcGenerator('../tests/ffmcCalc.json').generate()
    FIcalcGenerator('../tests/FIcalc.json').generate()
    FMCcalcGenerator('../tests/FMCcalc.json').generate()
    FROScalcGenerator('../tests/FROScalc.json').generate()
