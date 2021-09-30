# R

Unit tests compare against the original cffdrs R package.

Instructions below taken from https://github.com/bcgov/wps/blob/main/r/README.md

## Installing from lockfile

```R
install.packages("renv")
renv::restore()
```

## Updating the lockfile

Updating the lockfile can be somewhat estoric for people (like myself) not familiar with R.

Start R:

```R
# usethis will be used to update the DESCRIPTION file
install.packages('usethis')
# renv will be used to create the lockfile
install.packages("renv")
# instal cffdrs
renv::install("cffdrs", dependencies = TRUE)
# update the DESCRIPTION to list cffdrs as an import
usethis::use_package("cffdrs")
# create the lockfile
renv::snapshot()
```
