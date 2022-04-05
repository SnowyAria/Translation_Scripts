# STR Subtitle Applier
This set of scripts will allow you to take an .ASS script file created by AegisSub and hardcode it onto a Playstation STR file.

This script is made possible thanks to [jpsxdec](https://github.com/m35/jpsxdec) and [ffmpeg](https://github.com/FFmpeg/FFmpeg)

## Prerequisites
* Java
  * Needed to run jpsxdec
* Python 3
  * Needed to run XML creation code
  * No special modules required
* ffmpeg.exe
  * Too large to include, so download it first and save it in the tools folder
  * https://www.gyan.dev/ffmpeg/builds/

## Preparing for subbing
To get a file that AegisSub can understand to start the process, either download jpsxdec and use the gui to extract an AVI file, or drag your STR files onto "CreateAVIForSubbing.bat," which will create compressed AVIs for you. You can drag several STR files at once for conversion.

## Burning the subtitles onto the STR file
You can drag both your .STR and .ASS files at once onto "AddSubsToSTR.bat" to start the process. Alternatively, you can call it from the command line and specify the files that way. Order doesn't matter. Currently the script only supports one video at a time.

Your subbed STR file will be saved with the same name in the output folder.