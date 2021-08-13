
# pycffdrs

Python port of https://cran.r-project.org/package=cffdrs

The intention is to:
-have the python port output the exact same values as the R version.
--because we want an identical functional copy.
--thus any bugs in the R code will be reproduced exactly.
-have code look as close as possible to the R code.
--because it's easier to find bugs, track changes made in the R code.
--thus code style may not follow python conventions.
--thus code is sometimes not as efficient (may decide to optimize in later versions).

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

This project HAS TO use GNU GENERAL PUBLIC LICENSE Version 2, as it's a derivative work of
 https://cran.r-project.org/web/packages/cffdrs/index.html.