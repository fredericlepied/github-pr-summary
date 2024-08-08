#!/usr/bin/env python3

"""Read a Github json file produced by pr2json.py, format it for a LLM to summarize it."""

import json
import os
import sys

import dotenv
import openai


def create_summary(data):
    # Combine title and description for context
    title = data["details"]["title"]
    description = data["details"]["body"]
    code = data["patch"][:150000]
    url = data["details"]["html_url"]
    prompt = f'You are an experienced software developer. You will act as a reviewer for a GitHub Pull Request {url} titled "{title}" with the following description:\n"{description}"\n\nand code change:\n{code}\n\n.Please summarize the key changes from the title, description and code in a single sentence with this format: [<title>](<url): <summary>. Do not use the words Pull Request in the summary. Do not put the following characters in the title: `[]()|`.'

    client = openai.OpenAI()

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=os.getenv("OPENAI_MODEL", "gpt-4o"),
    )
    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    dotenv.load_dotenv()
    # load the json data
    with open(sys.argv[1], "r") as f:
        data = json.load(f)

    summary = create_summary(data)
    print(summary)
