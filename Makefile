#!/bin/bash

lint:
	black ./

tests:
	python3 -m unittest discover ./test/

coverage:
	coverage run -m unittest discover ./test/
	coverage report -m

setup:
	pip3 install -r requirements.txt

pre-commit:
	pre-commit run -a
