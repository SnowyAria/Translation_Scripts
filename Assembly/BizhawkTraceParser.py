"""
Bizhawk Trace Parser

Reads a Bizhawk-format trace log and removes values that did not change on that step,
reducing the visual complexity

Usage: <trace_log> <output_file>
"""

import sys

# Return a usage message if not enough arguments were supplied
if len(sys.argv) < 3:
    print("Usage: <trace_log> <output_file>")
    exit()

trace_filepath = sys.argv[1]
output_filepath = sys.argv[2]

registers = {}

print("Scanning Bizhawk trace log:")

with open(trace_filepath, "r") as input:
    with open(output_filepath, "w") as output_file:
        for line in input.readlines():
            output = ""
            for part in line.split(" "):
                # Some lines contain ":" at the end
                if ":" in part and not part.endswith(":"):
                    # Parse register values and compare them to previous values
                    # Only print if the values have changed
                    register = part.split(":")
                    register_name = register[0]
                    register_value = register[1]
                    if register_name in registers and register_value != registers[register_name]:
                        output += register_name + ": " + registers[register_name] + " ==> " + register_value + " "
                    registers[register_name] = register_value
                else:
                    output += part + " "

            # Output parsed line to file
            output_file.write(output + "\n")

print("Complete! Written to " + output_filepath)
