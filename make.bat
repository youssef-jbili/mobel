@ECHO off
if /I %1 == install-dev-deps goto :install-dev-deps
if /I %1 == install goto :install
if /I %1 == run-tests goto :run-tests

echo please provide a make target
goto :eof

:install-dev-deps
pip install pytest pytest-cov flake8
goto :eof

:install
pip install --editable .
goto :eof

:run-tests
pip install --editable .
python -m pytest
coverage html
goto :eof