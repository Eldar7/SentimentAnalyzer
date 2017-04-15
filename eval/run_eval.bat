@echo off
SET CURPATH=%cd%
IF [%1]==[/?] GOTO :help
IF [%1]==[] GOTO :help

echo %* |find "/?" > nul
IF errorlevel 1 GOTO :main

:help
ECHO run_eval [type] [*file to eval]
ECHO     type:
ECHO        'tkk' - telecommunications
ECHO        'bank' - telecommunications
ECHO     example:
ECHO         run_eval tkk - evaluate output.xml
ECHO         run_eval tkk out_E1.xml - evaluate out_E1.xml
GOTO :end

:main
IF [%1]==[tkk] (SET jstype=ttk) ELSE (SET jstype=%1)
IF [%2]==[] (SET output=../resources/output.xml) ELSE (SET output=%CURPATH%/%2)
ECHO ...calculation measure of prediction %1...

cd "%~p0"
node.exe calc.js %jstype% %output% ../resources/%1_test_etalon.xml
cd %CURPATH%
:end
