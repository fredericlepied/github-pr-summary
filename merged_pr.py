#!/usr/bin/env python3

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


def search_merged_prs(owner, repo, since_date):
    query = f"repo:{owner}/{repo} is:pr is:merged merged:>={since_date}"
    url = f"{BASE_URL}/search/issues"
    params = {"q": query, "sort": "updated", "order": "desc"}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


# Determine the date one week ago
one_week_ago = datetime.now() - timedelta(days=7)
since_date = one_week_ago.strftime("%Y-%m-%dT%H:%M:%SZ")

# Search for merged PRs since that date
merged_prs = search_merged_prs(OWNER, REPO, since_date)

# Save the data to a JSON file
json.dump(merged_prs, sys.stdout, indent=4)
