FROM r-base

# Install R + pre-reqs for cffdrs & python
RUN apt-get update --fix-missing && apt-get -y install libgdal-dev curl python3 python3-dev python3-venv python3-pip

# Install cffdrs
RUN R -e "install.packages('cffdrs')"

RUN python3 -m pip install --upgrade pip
# Install poetry in /opt/poetry/bin
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 -

# Copy source files
COPY ./src /usr/local/src
RUN cd /usr/local/src && /opt/poetry/bin/poetry install --no-root --no-dev

WORKDIR /usr/local/src
