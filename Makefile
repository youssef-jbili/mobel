install:
	pip install --editable .

run-tests: install
	python -m pytest
	coverage html