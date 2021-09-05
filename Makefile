install-dev-deps:
	pip install pytest pytest-cov flake8

install:
	pip install --editable .

run-tests: install
	python -m pytest
	coverage html