# The idea

The idea is that this folder would contain a Docker image, that's configured with R. We can run
code in this container, that will create JSON test files. From our pycffdrs project, we can then,
without the burden of needing to worry about R, just load up JSON files to run our unit tests
against.

## Build docker image

```bash
docker build .
docker run --rm -t -v ./src:/src
```

or

```bash
docker-compose build r
```

## I love jupyter notebooks

```bash
poetry shell
poetry run jupyter notebook
```
