#!/usr/bin/env python3

# compute the complexity of pull requests and display them on stdout

import json
import sys


def compute_complexity(pr_data):
    # Weights
    W_CODE = 0.5
    W_FILES = 0.2
    W_COMMITS = 0.15
    W_COMMENTS = 0.15

    # Extract the data
    details = pr_data["details"]
    num_commits = details["commits"]
    num_comments = details["comments"]
    additions = details["additions"]
    deletions = details["deletions"]
    changed_files = details["changed_files"]

    # Compute the score
    complexity_score = (
        ((additions + deletions) / 2) * W_CODE
        + changed_files * W_FILES
        + num_commits * W_COMMITS
        + num_comments * W_COMMENTS
    )
    return complexity_score


filenames = sys.argv[1:]

# read all the data
for filename in filenames:
    with open(filename) as pr_fd:
        data = json.load(pr_fd)
        print(f"{compute_complexity(data):.02f} {filename}")

# print_complexity.py ends here
