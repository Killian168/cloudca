#!/bin/bash

lint:
	black ./

tests:
	python3 -m unittest discover ./test/

setup:
	pip3 install -r requirements.txt

pre-commit:
	pre-commit run -a