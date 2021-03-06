# If the VIRTUAL_ENV is specified, we can assume we're in a poetry shell, otherwise
# we need to execute "poetry run"
ifdef VIRTUAL_ENV
POETRY_RUN=
else
POETRY_RUN=poetry run
endif

lint:
	# Run lint.
	$(POETRY_RUN) pylint --rcfile=.pylintrc pycffdrs/*.py tests/*.py;

style:
	$(POETRY_RUN) pycodestyle

test:
	# Run tests
	$(POETRY_RUN) pytest

notebook:
	PYTHONPATH=${shell pwd} JUPYTER_PATH=${shell pwd} $(POETRY_RUN) jupyter notebook --ip 0.0.0.0