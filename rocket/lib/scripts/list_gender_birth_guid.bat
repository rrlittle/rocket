@ECHO OFF
SET OLDPATH=%PATH%
SET PYTHONPATH=R:\Anaconda3_4.1.1;R:\Anaconda3_4.1.1\Lib;R:\Anaconda3_4.1.1\DLLs;R:\Anaconda3_4.1.1\Scripts;R:\Anaconda3_4.1.1\Tools;R:\Anaconda3_4.1.1\Lib\tkinter
PATH R:\RailsInstaller\Git\cmd;^
R:\RailsInstaller\Ruby2.1.0\bin;^
R:\RailsInstaller\Ruby2.1.0\lib\ruby\gems\1.9.1\bin;^
R:\RailsInstaller\DevKit\bin;^
%PATH%
rem ruby R:\scripts\piggybank-app.rb %*
ruby R:\scripts\list_gender_birth_guid.rb %*
PATH %OLDPATH%