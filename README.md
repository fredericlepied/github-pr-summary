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
