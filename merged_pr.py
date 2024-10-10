#!/usr/bin/env python3

import argparse
import os
import json
import requests
from datetime import datetime, timedelta
import sys

import dotenv


dotenv.load_dotenv()

# Replace with your GitHub token
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
# Replace with the repository information
OWNER = os.getenv("GITHUB_ORG")
REPO = os.getenv("GITHUB_PROJ")

# Base URL for the GitHub API
BASE_URL = "https://api.github.com"

# Headers for authentication
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}


def search_merged_prs(owner, repo, since_date, to_date, users):
    query = f"repo:{owner}/{repo} is:pr is:merged"
    if to_date and since_date:
        query += f" merged:{since_date}..{to_date}"
    else:
        if since_date:
            query += f" merged:>={since_date}"
        if to_date:
            query += f" merged:<={to_date}"
    if users and len(users) > 0:
        query += f" author:{' author:'.join(users)}"
    print(f"{query=}", file=sys.stderr)
    # manage pagination
    page = 1
    prs = []
    total_count = 0
    while True:
        response = search_issues(query, page)
        count = len(response["items"])
        if count == 0:
            break
        prs.extend(response["items"])
        total_count += count
        page += 1
    if total_count != response["total_count"]:
        print(
            f"Warning: inconsistent number of merged PRs found {total_count} != {response['total_count']}",
            file=sys.stderr,
        )
    else:
        print(f"Total merged PRs found: {total_count}", file=sys.stderr)
    response["items"] = prs
    return response


def search_issues(query, page):
    url = f"{BASE_URL}/search/issues"
    params = {"q": query, "sort": "updated", "order": "desc", "page": page}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


# Parse the command-line arguments
parser = argparse.ArgumentParser()

# from-date argument
parser.add_argument(
    "--from-date",
    dest="from_date",
    help="The date to search for merged PRs from",
    default=None,
)

# to-date argument in the %Y-%m-%d format
parser.add_argument(
    "--to-date",
    dest="to_date",
    help="The date to search for merged PRs to",
    default=None,
)

# users argument
parser.add_argument(
    "--users",
    dest="users",
    help="The users to search for merged PRs from. Separate multiple users with a comma.",
    default=None,
)

# owner argument
parser.add_argument(
    "--owner",
    dest="owner",
    help="The owner to search for merged PRs from.",
    default=OWNER,
)

# repo argument
parser.add_argument(
    "--repo",
    dest="repo",
    help="The repo to search for merged PRs from.",
    default=REPO,
)

# Parse the arguments
args = parser.parse_args()

if args.from_date:
    since_date = datetime.strptime(args.from_date, "%Y-%m-%d").strftime(
        "%Y-%m-%dT00:00:00"
    )
else:
    # Determine the date one week ago
    one_week_ago = datetime.now() - timedelta(days=7)
    since_date = one_week_ago.strftime("%Y-%m-%dT00:00:00")

if args.to_date:
    to_date = datetime.strptime(args.to_date, "%Y-%m-%d").strftime("%Y-%m-%dT23:59:59")
else:
    to_date = None

if args.users:
    users = args.users.split(",")
else:
    users = None

# Search for merged PRs since that date
merged_prs = search_merged_prs(args.owner, args.repo, since_date, to_date, users)

# Save the data to a JSON file
json.dump(merged_prs, sys.stdout, indent=4)
