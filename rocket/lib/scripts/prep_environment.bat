:: this script is to add all the dependencies to this terminal

@ECHO OFF REM don't print stuff during this script
cd %~dp0 REM go to script location for relative movement
cd .. REM go up one. to lib
%cd%

REM set %parent = %~dp0
:: save the current path
SET OLDPATH=%PATH% 

:: add paths of depencencies in front of OLDPATH
PATH %cd%\..\ruby_ship\bin;^
%cd%;^
%OLDPATH%

cd %~dp0 :: go to script location for relative movement
