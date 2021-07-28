@ECHO off    
if /I %1 == install goto :install
if /I %1 == run-tests goto :test

echo please provide a make target
goto :eof

:install
pip install --editable .
goto :eof

:run-tests
python -m pytest
coverage html
goto :eof