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

#frame_number_regex = re.compile(r"\[\d*\]\[(\d*)\]")


def apply_subtitles():
    """
    Iterates over the raw input directory and applies any subtitle files found in the mappings.
    All images created this way will be written to the output directory.
    """
    for path in Path(subtitle_image_folder).rglob("*"):
        if path.is_file():

            # Movie Studio outputs in the format of
            # <video_name>_<frame_number>.png
            # Frame number is padded to 6 zeroes
            file_name_split = path.name.split("_")
            movie_name = file_name_split[0]
            frame_number = int(file_name_split[1].split(".")[0])

            original_name = movie_name + ".STR[0][" + str(frame_number).zfill(4) + "].png"
            original_path = os.path.join(raw_frame_filepath, original_name)

            frame_image = Image.open(original_path)
            subtitle_image = Image.open(path)

            # Paste the transparent subtitle image on top of the frame
            frame_image.paste(subtitle_image, (0, 0), subtitle_image)
            frame_image.save(output_filepath + os.path.sep + original_name)


print("Applying subtitles:")
apply_subtitles()
