"""
XML Generator for SRT video translations on the PSX

Takes in a folder containing translated frames and writes out an XML import document
for the SRT tool

Usage: <frame_filepath> <mask_file> <output_filepath>

"""

import sys
import re
import os
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image

frames_to_export = {}
TOLERANCE = "0"
VERSION = "0.3"

# Return a usage message if not enough arguments were supplied
if len(sys.argv) < 4:
    print("Usage: <folder_of_translated_frames> <folder_of_black_frames> <output_dir>")
    exit()

frame_filepath = Path(sys.argv[1])
black_frame_filepath = Path(sys.argv[2])
output_filepath = sys.argv[3]

frame_number_regex = re.compile(r"\[\d*\]\[(\d*)\]")


def read_directory(frame_filepath, black_frame_filepath):
    """
    Scans the given directory recursively and parses any files within
    for their frame number and file path

    Frame number is in the format of [0][xyz], where xyz is the frame number
    :param directory: Current directory to scan
    """
    for path in frame_filepath.rglob("*"):
        # If this is a directory, ignore it
        if path.is_dir():
            continue

        # Check that the given image is in the right format
        # This could be made more sophisticated
        if "[" not in path.name:
            print("Image was not in the right format, ignoring: " + str(path))
            continue

        video_name = path.name.split("[")[0]
        frame_number = int(re.search(frame_number_regex, path.name).group(1))

        # If a frame number could not be parsed, return an error and ignore it
        if frame_number < 0:
            print("Could not parse image from " + path.name)
            continue

        # Check to see if the black frame subtitle is blank. If so, ignore this image
        black_subtitle_frame = Image.open(os.path.join(black_frame_filepath, path.name))
        extrema = black_subtitle_frame.convert("L").getextrema()
        if extrema[0] == extrema[1]:
            continue

        # Calculate the bounding box of the subtitle for a partial frame replace
        subtitle_bounding_box = black_subtitle_frame.getbbox()

        # If this is the first time we've seen this video, add a new entry for it
        if video_name not in frames_to_export:
            frames_to_export[video_name] = []

        frame_entry = {"frame_number": frame_number, "frame_filepath": str(path),
                       "frame_bounding_box": subtitle_bounding_box}
        frames_to_export[video_name].append(frame_entry)


def write_xml(video_name, frames, output):
    """
    Generates XML from a video entry
    :param video_name: Name of the video, derived from the frame's filename
    :param frames: Frame data, which includes the frame number and file name
    :param output: Folder to write resulting XML to
    """
    # Make the output directory if it doesn't exist
    if not os.path.exists(output):
        os.makedirs(output)

    root = ET.Element("str-replace")
    root.set("version", VERSION)
    for frame in frames:
        replace = ET.SubElement(root, "replace")
        replace.set("frame", str(frame["frame_number"] - 1))
        #replace.set("tolerance", TOLERANCE)
        #replace.set("mask", mask_filepath)
        replace.set("rect", ",".join(str(x) for x in frame["frame_bounding_box"]))
        replace.text = frame["frame_filepath"]

    xml_data = ET.tostring(root).decode()
    output_file = open(output + os.path.sep + video_name + ".xml", "w")
    output_file.write(xml_data)


def export_frames():
    """
    Exports over the parsed video information and writes out XML
    """
    for video_name in frames_to_export:
        write_xml(video_name, frames_to_export[video_name], output_filepath)


print("\nSearching for all images in " + str(frame_filepath))
read_directory(frame_filepath, black_frame_filepath)

print("Parsing complete!\n")
print("Writing XML...")
export_frames()

print("Complete!")
