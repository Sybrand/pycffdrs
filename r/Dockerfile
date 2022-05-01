# FROM ubuntu:22.04
FROM r-base

# Install R + pre-reqs for cffdrs
RUN apt-get update --fix-missing
# RUN apt-get update --fix-missing && apt-get -y install libgdal-dev curl python3
RUN apt-get -y install libgdal-dev

# Install cffdrs
RUN R -e "install.packages('cffdrs')"

# TODO: Move this all up into one apt install
RUN apt-get -y install curl
RUN apt-get -y install python3
RUN apt-get -y install python3-venv
# Install poetry
# Add `export PATH="/opt/poetry/bin:$PATH"` to your shell configuration file.
# Alternatively, you can call Poetry explicitly with `/opt/poetry/bin/poetry`.
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 -