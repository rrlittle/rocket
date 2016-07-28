:: this script is to add all the dependencies to this terminal

@ECHO OFF :: don't print stuff during this script
cd %~dp0 :: go to script location for relative movement
cd .. :: go up one. to lib

:: save the current path
SET OLDPATH=%PATH% 

:: add paths of depencencies in front of OLDPATH
PATH ruby_ship\bin;^
scripts;^
%OLDPATH%



cd %~dp0 :: go to script location for relative movement
