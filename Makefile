#!/bin/bash

lint:
	black ./

tests:
	pytest -v test/

coverage:
	coverage run -m pytest -v test/
	coverage report -m

setup:
	pip3 install -r requirements.txt

pre-commit:
	pre-commit run -a
