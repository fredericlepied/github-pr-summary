#!/usr/bin/env python3

import requests
import json
import os
import sys

import dotenv


if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <PR URL> <output_dir>")
    sys.exit(1)

if not os.path.exists(sys.argv[2]):
    os.makedirs(sys.argv[2])

dotenv.load_dotenv()

# Extract owner, repo and PR number from the PR URL
pr_url = sys.argv[1]
OWNER, REPO, _, PR_NUMBER = pr_url.split("/")[-4:]

# Base URL for the GitHub API
BASE_URL = "https://api.github.com"

# Headers for authentication
headers = {
    "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
    "Accept": "application/vnd.github.v3+json",
}


def fetch_pr_details(owner, repo, pr_number):
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def fetch_comments(owner, repo, pr_number):
    url = f"{BASE_URL}/repos/{owner}/{repo}/issues/{pr_number}/comments"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def fetch_review_comments(owner, repo, pr_number):
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/comments"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def fetch_files_changed(owner, repo, pr_number):
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/files"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def fetch_patch_content(patch_url):
    response = requests.get(patch_url, headers=headers)
    response.raise_for_status()
    return response.text


# Fetch PR details
pr_details = fetch_pr_details(OWNER, REPO, PR_NUMBER)

# Fetch PR comments
comments = fetch_comments(OWNER, REPO, PR_NUMBER)

# Fetch PR review comments
review_comments = fetch_review_comments(OWNER, REPO, PR_NUMBER)

# Fetch code changes
files_changed = fetch_files_changed(OWNER, REPO, PR_NUMBER)

# Fetch patches from patch URLs and combine them into one field
patch_url = pr_details["patch_url"]
patch_content = fetch_patch_content(patch_url)

# Combine all the fetched data
pr_data = {
    "details": pr_details,
    "comments": comments,
    "review_comments": review_comments,
    "files_changed": files_changed,
    "patch": patch_content,
}

# Save the data to a JSON file
output_file = os.path.join(sys.argv[2], f"pr_{PR_NUMBER}.json")
with open(output_file, "w") as f:
    json.dump(pr_data, f, indent=4)

print(output_file)
