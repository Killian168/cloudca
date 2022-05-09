#!/bin/bash

format:
	black ./

unit-tests:
	pytest -v test/unit_test/

integration-tests:
	pytest -v test/integration_test/

coverage:
	coverage run --omit="*/test*" -m pytest -v test/unit_test/
	coverage report -m

setup:
	pip3 install -r requirements.txt

pre-commit:
	pre-commit run -a
