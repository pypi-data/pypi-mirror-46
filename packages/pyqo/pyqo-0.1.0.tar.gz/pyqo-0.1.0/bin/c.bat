@ECHO OFF
c_ %* 2> %userprofile%\temp
SET r=%ERRORLEVEL%
SET "VAR="
SET /p VAR=<%userprofile%\temp
DEL %userprofile%\temp
IF "%r%"=="1" (
	cd /d %VAR%
)