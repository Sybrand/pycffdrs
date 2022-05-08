
build:
	docker-compose build

shell:
	docker-compose run --rm r bash

generate:
	docker-compose run --rm r /opt/poetry/bin/poetry run python generate_fixtures.py

notebook:
	PYTHONPATH=${shell pwd}/src JUPYTER_PATH=${shell pwd}/src poetry run jupyter notebook --ip 0.0.0.0