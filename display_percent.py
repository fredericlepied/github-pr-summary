#!/usr/bin/env python3

import sys
import math
import tempfile


def output_first_x_percent_lines(percent):
    with tempfile.TemporaryFile(mode="w+t") as tmpfile:
        total_lines = 0
        for line in sys.stdin:
            tmpfile.write(line)
            total_lines += 1

        # Calculate the number of lines to output (rounding up)
        num_lines_to_output = math.ceil(total_lines * percent / 100)

        # Move to the beginning of the file
        tmpfile.seek(0)

        # Output the required number of lines
        for _ in range(num_lines_to_output):
            line = tmpfile.readline()
            if not line:
                break
            print(line, end="")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} [percentage]")
        sys.exit(1)
    try:
        X = float(sys.argv[1])
        if not (0 <= X <= 100):
            raise ValueError
    except ValueError:
        print("Please provide a valid percentage between 0 and 100.")
        sys.exit(1)
    output_first_x_percent_lines(X)

# display_percent.py ends here
