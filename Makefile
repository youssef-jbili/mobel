install:
	pip install --editable .

run-tests:
	python -m pytest
	coverage html