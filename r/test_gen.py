import random
import json
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector, StrVector


def BEcalc():
    cffdrs = importr('cffdrs')
    
    iterations = 50
    array_length = 400
    # we include some garbage values
    fuel_types = ("BLAH", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "D1", "M1", "M2", "M3",
                    "M4", "S1", "S2", "S3", "O1A", "O1B")
    inputs = []

    random.seed(42)
    # build up some random inputs
    for _ in range(iterations):
        FUELTYPE = [fuel_types[random.randint(
            0, len(fuel_types)-1)] for x in range(array_length)]
        # BUI is from 0 to 100, but we include some garbage values.
        BUI = [random.uniform(-10, 110) for x in range(array_length)]
        inputs.append([FUELTYPE, BUI])
    # make sure we have some bad inputs
    inputs.append([["BLAH",], [0,]])
    inputs.append([["C1",], [-1,]])

    data = []
    for input in inputs:
        r_result = cffdrs._BEcalc(StrVector(input[0]), FloatVector(input[1]))

        data.append({
            "FUELTYPE": input[0],
            "BUI": input[1],
            "result": [value for value in r_result]
        })
    
    with open('../tests/BEcalc.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


if __name__ == "__main__":
    BEcalc()
