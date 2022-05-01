# Generating test fixtures

Test fixtures can be generated from the docker container in this folder. The docker container contains an R environment with the cffdrs package installed.

**Note:** Depending on the platform your using, the output values will differ slightly. CFFDRS with R running on ARM64 will differ from x86_64. (Differences are very minor, after 13 decimal places)
**Note:** If I were a better person I'd learn how to write the code that generates the fixtures in R. Using a python script with rpy2 adds additional complexity.

## Docker

### Build docker image

```bash
make build
```

### Generate the test fixtures using docker.

```bash
make generate
```

## Local

You don't have to use docker, but it spares you having to install R and cffdrs.

### Generate the test fixtures locally.

```bash
sudo apt-get install libgdal-dev r-base
```

*Assuming you've installed R, gdal etc. etc.*

```bash
R
install.packages('rgdal')
install.packages('cffdrs')
```

*Assuming you've installed python3, poetry etc. etc.*

```bash
poetry install
poetry run python generate_fixtures.py
```

## I love jupyter notebooks

```bash
poetry shell
poetry run jupyter notebook
```
