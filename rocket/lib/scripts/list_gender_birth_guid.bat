:: HEADER - should be present for jsut about all scripts
@ECHO OFF
cd %~dp0 :: move to script location
CALL prep_environment.bat :: give this terminal access to dependencies
:: END OF HEADER

ruby list_gender_birth_guid.rb %* :: run the script to get  
