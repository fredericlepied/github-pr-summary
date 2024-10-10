# GitHub PR summary tool

Add your tokens for GitHub and OpenAI in the `.env` file like this:

```shell
GITHUB_TOKEN=<GitHub Token>
OPENAI_API_KEY=<OPENAI API TOKEN>
GITHUB_ORG=<your GitHub organization>
GITHUB_PROJ=<your GitHub project>
OPENAI_MODEL=gpt-4o-mini
```

To install the requirements:

```Shellsession
$ virtualenv .venv
$ . .venv/bin/activate
$ pip install -r requirements.txt
```

To get the summaries of the merged PR since last week:

```Shellsession
$ for url in $(./merged_pr.py | jq -r .items.[].html_url); do
  ./json2summary.py $(./pr2json.py $url pr)
done
```

To get the PR data from a list of users with specific dates and repo, then filter the top 20% according to the basic complexity of the changes:

```Shellsession
$ OWNER=redhatci
$ REPO=ansible-collection-redhatci-ocp
$ USERS=toto,titi
$ for url in $(./merged_pr.py --owner $OWNER --repo $REPO --users $USERS --from-date 2024-07-01 --to-date 2024-09-30 | jq -r .items.[].html_url); do
  ./pr2json.py $url pr
done
$ for f in $(./print_complexity.py pr/*|sort -nr|./display_percent.py 20|cut -d ' ' -f2); do
  ./json2summary.py $f
done
```

## Gerrit changes

```Shellsession
$ for f in $(./gerrit_changes.py https://softwarefactory-project.io/r 'status:merged after:2024-07-01 before:2024-09-30' pr); do
  ./json2summary.py $f
done
```

# git autocommit addon

Use OpenAI to generate the commit message of a git change. Set the `EDITOR` environment variable in a `git-autocommit` script to be placed in your `PATH` like this:

```bash
#!/bin/bash

SRCDIR=<path to where you extracted this repository>

. $SRCDIR/.venv/bin/activate

EDITOR=$SRCDIR/git-autocommit-editor git commit "$@"
```
