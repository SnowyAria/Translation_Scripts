@echo off
echo Playstation STR video subtitle hardcoder
echo If it doesn't work, go bug @SnowyAria!
echo:

:: Sets the working directory to the script location
pushd %~dp0

echo Looking for ffmpeg.exe...
if exist tools\ffmpeg.exe (
    echo ffmpeg.exe found!
    echo:
) else (
    echo Could not find ffmpeg.exe under tools.
    echo Please download it from here https://www.gyan.dev/ffmpeg/builds/
    echo then copy ffmpeg.exe from the bin folder to the tools folder
    echo:
    echo It's a huge file, so didn't want to include it for portability reason, sorry~!
    echo:

    pause
    exit 1
)

if "%~1"=="" goto :NOFILE

set str_file=""
set str_filename=""
set ass_file=""
set ass_filename=""

echo Scanning the supplied files...
for %%A in (%*) do (
    if /I "%%~xA" == ".str" (
        set str_file=%%A
        set str_filename=%%~nA%%~xA
        set ass_filename=%%~nA.ass
    )

    if /I "%%~xA" == ".ass" (
        set ass_file=%%A
    )
)

echo Verifying an STR and an ASS file were found...
if %str_file%=="" (
    echo No STR file found.
    echo:
    goto :ERROR
)

if %ass_file%=="" (
    echo No ASS file found.
    echo:
    goto :ERROR
)

echo Video file: %str_file%
echo Video filename: %str_filename%
echo Subtitle file: %ass_file%
echo Subtitle filename: %ass_filename%
echo:

echo Creating temp copies of files...
mkdir output
mkdir output\frames
mkdir output\black_frames
copy %ass_file% output\%ass_filename%
copy %str_file% output\%str_filename%
echo:

echo Converting to an uncompressed AVI...
java -jar tools/jpsxdec/jpsxdec.jar -f output\%str_filename% -i 0 -quality high -vf avi:mjpg -up Lanczos3 -dir output
echo:

echo Combining subtitles with AVI frames...
::For some reason, the subtitle filter on FFMPEG requires double escaping
::See here for info: https://superuser.com/questions/1247197/ffmpeg-absolute-path-error
tools\ffmpeg.exe -i "output\%str_filename%[0].avi" -vf subtitles=output\\\\%ass_filename% "output\frames\%str_filename%[0][%%04d].png"
echo:

echo Creating black subtitle images...
tools\ffmpeg.exe -i "output\%str_filename%[0].avi" -vf drawbox=color=#000000:t=fill,subtitles=output\\\\%ass_filename% "output\black_frames\%str_filename%[0][%%04d].png"
echo:

echo Defining an XML insertion file for the subtitled frames...
python tools\SubtitleXmlGenerator.py output\frames\ output\black_frames\ output\
echo:

echo Inserting the frames into the STR file...
java -jar tools/jpsxdec/jpsxdec.jar -f output\%str_filename% -i 0 -replaceframes output\%str_filename%.xml
echo:

echo Creating a preview AVI...
java -jar tools/jpsxdec/jpsxdec.jar -f output\%str_filename% -i 0 -quality high -vf avi:mjpg -up Lanczos3 -dir output
echo:

echo Cleaning up the temporary files...
del /q output\%str_filename%.xml
ren output\%str_filename%[0].avi %str_filename%-output-preview.avi
del /q output\%ass_filename%
del /q output\black_frames\*
del /q output\frames\*
rmdir /q output\frames
rmdir /q output\black_frames
del /q *.log
echo:

echo Complete!
echo Subtitled STR file is in the output folder.
echo:

pause
exit

:NOFILE
echo No files specified.
echo:

:ERROR
echo Please either drag and drop the STR and ASS files onto this script,
echo or add them as arguments on the command line.
echo:
pause
exit 1