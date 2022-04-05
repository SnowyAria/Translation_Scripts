"""
Creates a subtitled for jpsxdec by applying a transparent subtitle image to all frames in a given range.
Subtitle images must be the same size as the original frame.

This file is a more specific use case to match Movie Studio's PNG output.

Usage: <folder_of_raw_frames> <subtitle_mapping_file> <output_dir>

"""
import sys
import re
from PIL import Image
import os
from pathlib import Path

# Return a usage message if not enough arguments were supplied
if len(sys.argv) < 4:
    print("Usage: <folder_of_raw_frames> <subtitle_image_folder> <output_dir>")
    exit()

raw_frame_filepath = sys.argv[1]
subtitle_image_folder = sys.argv[2]
output_filepath = sys.argv[3]

Path(output_filepath).mkdir(parents=True, exist_ok=True)


def apply_subtitles():
    """
    Iterates over the raw input directory and applies any subtitle files found in the mappings.
    All images created this way will be written to the output directory.
    """
    for path in Path(subtitle_image_folder).rglob("*"):
        if path.is_file():

            # Premiere outputs in the format of
            # <video_name>[<frame_number>].png
            # Frame number is padded to 3 zeroes

            # Movie name is everything to the left of [
            # Frame number is everything to the right of ] and removing the file extension
            movie_name = path.name.split("[")[0]
            frame_number = path.name.split("]")[1].split(".")[0]

            original_name = movie_name + "[0][" + str(frame_number).zfill(3) + "].png"
            original_path = os.path.join(raw_frame_filepath, original_name)

            frame_image = Image.open(original_path)
            subtitle_image = Image.open(path)

            # Paste the transparent subtitle image on top of the frame
            frame_image.paste(subtitle_image, (0, 0), subtitle_image)
            frame_image.save(output_filepath + os.path.sep + original_name)


print("Applying subtitles:")
apply_subtitles()
