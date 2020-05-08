"""
Directory Hex Searcher for Shift-JIS

Scans a given directory recursively and searches for a search term in Shift-JIS encoding

Usage: <dir_to_search> <word_to_search>
Example: C:/Translations/Iru/Extracted ハンマー
"""

import sys
from pathlib import Path

# Return a usage message if not enough arguments were supplied
if len(sys.argv) < 3:
    print("Usage: <dir_to_search> <word_to_search>")
    exit()

initial_directory = sys.argv[1]
search_word = sys.argv[2]

# Convert the search word to Shift-JIS-encoded hex
search_hex = search_word.encode("shift-jis").hex()

hit_locations = []


def read_directory(directory):
    """
    Scans the given directory recursively and parses any files within
    :param directory: Current directory to scan
    """
    for path in Path(directory).rglob("*.*"):
        read_file(path)


def read_file(file_path):
    """
    Converts the given file to a hex string and searches for the raw hex string inside
    :param file_path: File to scan for hex
    """
    with open(file_path, "rb") as file:
        raw_hex = file.read().hex()
        if search_hex in raw_hex:
            hit_locations.append(file.name)


print("Scanning for " + search_word + " in " + initial_directory + ":");
read_directory(initial_directory)
print("Complete!\n")

print(str(len(hit_locations)) + " hits found")

for hit_location in hit_locations:
    print(hit_location)
