
# pycffdrs

Python port of https://cran.r-project.org/package=cffdrs

## Technical notes

### Coding conventions

Matching the R code as close as possible, ignoring python conventions in favour of
looking more like the R code.

### Numba - http://numba.pydata.org/

- Using numba to speed up calculations
- For numba to work, we need python >=3.8,<3.10

### Publishing

```bash
poetry build
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi <your token>
poetry publish -r testpypi
```

## License

Using the GNU GENERAL PUBLIC LICENSE Version 2, for no other reason than to match https://cran.r-project.org/web/packages/cffdrs/index.html.