"""
Changed Byte Scanner

Compares two versions of a binary for a specific byte and finds all instances
where they differ. This is mostly useful for finding mistakenly erased or
added null bytes ("00") that make a game crash and can be hard to find.

Usage: <translated_file> <original_file> hex_to_search
"""

import sys

# Return a usage message if not enough arguments were supplied
if len(sys.argv) < 4:
    print("Usage: <translated_file> <original_file> hex_to_search")
    exit()

translated_file = sys.argv[1]
original_file = sys.argv[2]
hex_to_search = sys.argv[3]

print("Finding " + hex_to_search + " values in " + translated_file + " and " + original_file)


def find_matches(file_path):
    """
    Reads the given file as hex, then finds all indexes where that byte was found.
    """
    with open(file_path, "rb") as file:
        raw_hex = file.read().hex()

        # Convert the raw hex string to byte chunks
        hex_as_bytes = map(''.join, zip(raw_hex[::2], raw_hex[1::2]))

        # Find all instances of the search text and record their indexes
        result = set()
        for index, byte in enumerate(hex_as_bytes):
            if byte == hex_to_search:
                # Format the result to 8 digits. This helps the sort function stay simple later on.
                result.add(f"{index:#0{10}x}")

        return result


# Run the above function for the translated and original files
translated_matches = find_matches(translated_file)
original_matches = find_matches(original_file)

print("Search complete.\n\nScanning for unique matches:")

# Remove any entries that are in both the original and translated
unique_matches = sorted(translated_matches.symmetric_difference(original_matches))

# Summary
print("Total unique matches found: " + str(len(unique_matches)))
for address in unique_matches:
    print(address)
