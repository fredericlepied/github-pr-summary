#!/usr/bin/env python3

import base64
import json
import re
import requests
import sys


def filter_description(description):
    """
    Filter out the description of the change to remove the metadata like 'Change-Id' and 'Test-Label'
    """
    lines = description.split("\n")
    return "\n".join(
        [line for line in lines if not re.match(r"^[a-zA-Z0-9-_]+:\s+", line)]
    )


if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <Gerrit URL> <query> <output_dir>", file=sys.stderr)
    sys.exit(1)

# Replace with your Gerrit server URL
gerrit_url = sys.argv[1]

# Replace with your query parameters, e.g., 'status:open'
query = sys.argv[2]

output_dir = sys.argv[3]

# Construct the URL
url = f"{gerrit_url}/changes/?q={query}"

# If authentication is required
auth = ("username", "password")  # Use your Gerrit credentials

# response = requests.get(url, auth=auth)

response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Remove the magic prefix
    content = response.text
    if content.startswith(")]}'"):
        content = content[4:]

    # Parse the JSON data
    changes = json.loads(content)

    # Now 'changes' is a list of change objects
    for change in changes:
        change_response = requests.get(
            f"{gerrit_url}/changes/{change['_number']}/detail?o=CURRENT_REVISION&o=CURRENT_COMMIT&o=CURRENT_FILES"
        )
        if change_response.status_code == 200:
            # Remove the magic prefix
            content = change_response.text
            if content.startswith(")]}'"):
                content = content[4:]

            # Now, retrieve the patch for the current revision
            change_data = json.loads(content)

            change_id = change_data["id"]
            current_revision = change_data["current_revision"]
            # get the description of the change
            change_data["description"] = filter_description(
                change_data["revisions"][current_revision]["commit"]["message"]
            )
            # get the html url of the change
            project = change_data["project"]
            number = change_data["_number"]
            change_data["html_url"] = f"{gerrit_url}/c/{project}/+/{number}"
            patch_url = (
                f"{gerrit_url}/changes/{change_id}/revisions/{current_revision}/patch"
            )

            # Make the request to get the patch
            patch_response = requests.get(patch_url)

            if patch_response.status_code == 200:
                # Remove the magic prefix
                patch_content = patch_response.text
                if patch_content.startswith(")]}'"):
                    patch_content = patch_content[4:]

                # The patch content is base64-encoded
                # Decode it
                decoded_patch = base64.b64decode(patch_content).decode(
                    "utf-8", errors="ignore"
                )

                change_data["patch"] = decoded_patch
                fname = f"{output_dir}/{change['project']}-{change['_number']}.json"
                with open(f"{fname}", "w") as f:
                    print(fname)
                    json.dump(change_data, f, indent=4)
            else:
                print(
                    f"Error: {patch_response.status_code} {patch_response.reason}",
                    file=sys.stderr,
                )
                print(patch_response.text, file=sys.stderr)
        else:
            print(
                f"Error: {change_response.status_code} {change_response.reason}",
                file=sys.stderr,
            )
            print(change_response.text, file=sys.stderr)
else:
    print(f"Error: {response.status_code} {response.reason}", file=sys.stderr)
    print(response.text, file=sys.stderr)

# gerrit_changes.py ends here
