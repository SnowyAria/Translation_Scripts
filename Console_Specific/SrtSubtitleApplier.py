"""
Creates a subtitled for jpsxdec by applying a transparent subtitle image to all frames in a given range.
Subtitle images must be the same size as the original frame.

Usage: <folder_of_raw_frames> <subtitle_mapping_file> <output_dir>

"""
import sys
import re
from PIL import Image
import os
from pathlib import Path

# Return a usage message if not enough arguments were supplied
if len(sys.argv) < 4:
    print("Usage: <folder_of_raw_frames> <subtitle_mapping_file> <output_dir>")
    exit()

raw_frame_filepath = sys.argv[1]
subtitle_mapping_file = sys.argv[2]
output_filepath = sys.argv[3]

Path(output_filepath).mkdir(parents=True, exist_ok=True)

frame_number_regex = re.compile(r"\[\d*\]\[(\d*)\]")

subtitle_mappings = {}


def load_subtitle_mappings():
    """
    Subtitle mappings are in the format of
    start_frame,end_frame,subtitle_filename

    Example
    101,131,Line-3.png
    where "Line-3.png" will be pasted on top of frames 101-131

    Subtitle files are expected to be in the raw frame folder
    """
    with open(subtitle_mapping_file, "r") as file:
        for line in file.readlines():
            values = line.split(",")

            # Ignore this value if it did not have enough fields
            if len(values) < 3:
                continue

            start_frame = int(values[0])
            end_frame = int(values[1])
            subtitle_file = values[2]

            # Create a map entry of frame numbers to this subtitle file
            for x in range(start_frame, end_frame + 1):
                subtitle_mappings[x] = raw_frame_filepath + os.path.sep + subtitle_file.replace("\n", "")


def apply_subtitles():
    """
    Iterates over the raw input directory and applies any subtitle files found in the mappings.
    All images created this way will be written to the output directory.
    """
    for path in Path(raw_frame_filepath).rglob("*"):
        if path.is_file():

            # If this file does not have brackets, ignore
            if "[" not in path.name:
                continue

            # Frames are expected to be in the format of [x][xyz] as generated by jpsxdec
            frame_number = int(re.search(frame_number_regex, path.name).group(1))

            # If no subtitles were found for this image, ignore it
            if frame_number not in subtitle_mappings:
                continue

            subtitle_file = subtitle_mappings[frame_number]
            frame_image = Image.open(path)
            subtitle_image = Image.open(subtitle_file)

            # Paste the transparent subtitle image on top of the frame
            frame_image.paste(subtitle_image, (0, 0), subtitle_image)
            frame_image.save(output_filepath + os.path.sep + path.name)


load_subtitle_mappings()
apply_subtitles()
