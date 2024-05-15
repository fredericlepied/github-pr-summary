# GitHub PR summary tool

Add your tokens for GitHub and OpenAI in the `.env` file like this:

```shell
GITHUB_TOKEN=<GitHub Token>
OPENAI_API_KEY=<OPENAI API TOKEN>
```

To install the requirements:

```Shellsession
$ virtualenv .venv
$ . .venv/bin/activate
$ pip install -r requirements.txt
```

To get the summaries of the merged PR since last week:

```Shellsession
$ ORG=<your GitHub organization>
$ PROJ=<your GitHub project>
$ for url in $(./merged_pr.py $ORG $PROJ | jq -r .items.[].html_url); do
  ./json2summary.py $(./pr2json.py $url pr)
done
```
