# no buildin rules and variables
MAKEFLAGS =+ -rR --warn-undefined-variables

.PHONY: \
    test

local-test:
	python3 -m venv .venv
	.venv/bin/python3 -m pip install .
	.venv/bin/python3 -m pytest
	rm -rf .venv

test:
	python3 -m pytest
