# pycffdrs

[![Issues](https://img.shields.io/github/issues/Sybrand/pycffdrs.svg?style=for-the-badge)](/../../issues)
[![MIT License](https://img.shields.io/github/license/Sybrand/pycffdrs.svg?style=for-the-badge)](/LICENSE)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Sybrand_pycffdrs&metric=alert_status)](https://sonarcloud.io/dashboard?id=Sybrand_pycffdrs)

Python port of <https://cran.r-project.org/package=cffdrs>

The intention is to:

- have the python port output the exact same values as the R version.
  - because we want an identical replacement.
  - thus any bugs in the R code will be reproduced exactly.
- have code look as close as possible to the R code.
  - because it's easier to find bugs, track changes made in the R code.
  - thus code style may not follow python conventions.
  - thus code is sometimes not as efficient (may decide to optimize in later versions).
- consider speed later.
  - optimization is a future goal. we want something that works first.
  - it won't run as fast as the R, and that's ok for now.

## Roadmap

### 1st release (for basic fire behaviour calculations)

- [x] local linting
- [x] github actions linting
- [x] github actions (static analysis, unit tests)
- [x] BROScalc
- [x] CFBcalc
- [x] buiCalc
- [x] DISTtcalc
- [x] ffmcCalc
- [x] Flcalc
- [x] FMCcalc
- [x] FROScalc
- [ ] hffmc
- [x] ISIcalc
- [ ] LBcalc
- [ ] LBtcalc
- [x] ROScalc
- [ ] ROStcalc
- [ ] SFCcalc
- [ ] Slopecalc
- [ ] TFCcalc
- [x] BEcalc
- [x] C6calc
- [x] fwiCalc

### 2nd release

- [ ] dcCalc
- [ ] direction
- [ ] dmcCalc
- [ ] fbp
- [ ] FBPcalc
- [ ] fbpRaster
- [ ] fireSeason
- [ ] fwi
- [ ] fwiRaster
- [ ] getvaluesblock_staticfix
- [ ] gfmc
- [ ] hffmcRaster
- [ ] lros
- [ ] pros
- [ ] ROSthetacalc
- [ ] sdmc
- [ ] winter_DC

## Technical notes

- Not concerned about performance at the moment. Once compatibility with the R version has been established, optimizations will be considered if required/requested.
- Assuming that all input lists are numpy arrays.

### Development environment (Ubuntu 20.04)

These instructions assume a clean Ubuntu 20.04 desktop installation. The development environment has additional requirements that the production environment does not require. The unit tests compare the output of the original R cffdrs components. Output is stored in json files, so R is not required to run unit tests. However, to generate test inputs, R, the R library cffdrs and python library rpy2 are required.

#### Install Python Poetry

Install python poetry <https://python-poetry.org/> ; right now the install doesn't work very well on Ubuntu 20.04 :()

```bash
sudo apt install python-is-python3
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

Add ~/.local/bin to your path - so that poetry can be found.

PATH="~/.local/bin:${PATH}"

#### Install python dependancies

```bash
poetry install
```

#### Run tests

```bash
poetry shell
pytest
```

### Coding conventions

Matching the R code as close as possible, ignoring python conventions in favour of looking more like the R code.

### Numpy

- Making use of numpy extensively.

### Numba - <http://numba.pydata.org/>

Considered using numba, but decided against it. It's hard to debug, takes extra effort to make work, and has python compatibility constraints.

### Publishing

Currently publishing to TestPyPI: <https://test.pypi.org/project/pycffdrs/>

```bash
poetry build
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi <your token>
poetry publish -r testpypi
```

## License

This project HAS TO use GNU GENERAL PUBLIC LICENSE Version 2+, as it's a derivative work of
<https://cran.r-project.org/web/packages/cffdrs/index.html>.

[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-white.svg)](https://sonarcloud.io/dashboard?id=Sybrand_pycffdrs)
