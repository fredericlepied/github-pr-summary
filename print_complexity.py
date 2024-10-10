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

    if "details" in pr_data:
        # Extract the data
        details = pr_data["details"]
        num_commits = details["commits"]
        num_comments = details["comments"]
        additions = details["additions"]
        deletions = details["deletions"]
        changed_files = details["changed_files"]
    else:
        # extract gerrit data
        num_commits = 1
        num_comments = pr_data["total_comment_count"]
        additions = pr_data["insertions"]
        deletions = pr_data["deletions"]
        current_revision = pr_data["current_revision"]
        changed_files = len(pr_data["revisions"][current_revision]["files"])

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
