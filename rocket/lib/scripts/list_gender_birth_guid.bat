:: HEADER - should be present for jsut about all scripts
@ECHO OFF
cd %~dp0 REM move to script location
CALL prep_environment.bat REM give this terminal access to dependencies

PATH
cd %~dp0 REM move to script location
:: END OF HEADER

ruby_ship.bat list_gender_birth_guid.rb %*
