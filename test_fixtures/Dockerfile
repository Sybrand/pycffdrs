# FROM ubuntu:22.04
FROM r-base

# Install R + pre-reqs for cffdrs & python
# RUN apt-get update --fix-missing
RUN apt-get update --fix-missing && apt-get -y install libgdal-dev curl python3 python3-dev python3-venv python3-pip
# RUN apt-get -y install libgdal-dev

# Install cffdrs
RUN R -e "install.packages('cffdrs')"

# # TODO: Move this all up into one apt install
# RUN apt-get -y install curl
# RUN apt-get -y install python3
# RUN apt-get -y install python3-dev
# RUN apt-get -y install python3-venv
# RUN apt-get -y install python3-pip

RUN python3 -m pip install --upgrade pip
# Install poetry
# Add `export PATH="/opt/poetry/bin:$PATH"` to your shell configuration file.
# Alternatively, you can call Poetry explicitly with `/opt/poetry/bin/poetry`.
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 -

COPY ./src /usr/local/src
RUN cd /usr/local/src && /opt/poetry/bin/poetry install --no-root --no-dev

WORKDIR /usr/local/src
