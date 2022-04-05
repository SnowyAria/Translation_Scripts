@echo off

:: Sets the working directory to the script location
pushd %~dp0

if "%~1"=="" goto :NOFILE

for %%A in (%*) do (
    echo Converting %%A...
    java -jar tools/jpsxdec/jpsxdec.jar -f %%A -i 0 -quality high -vf avi:mjpg -up Lanczos3 -dir avis
    echo:
)

echo Clearing out log files...
del /q *.log

echo Complete!
echo These videos are compressed and are only used to help with subbing.
echo Open these AVIs in AegisSub, then save an .ass file.
echo:
pause
exit

:NOFILE
echo No files specified.
echo Please either drag and drop the STR files onto this script,
echo or add them as arguments on the command line.
echo:
pause
exit 1