import os
import requests
import json
from utils import set_multiline_output, addHeader

result = ""
sources = []

with open("sources.txt", "r") as f:
    for line in f:
        sources.append(line.strip())

for source in sources:
    print("Scraping README.md from", source)
    try:
        owner = source.split("/")[-2]
        repo = source.split("/")[-1]

        cacheURL = f"cache/{owner}-{repo}.md"
        readmeEndpoint = f"https://api.github.com/repos/{owner}/{repo}/readme"

        response = requests.get(readmeEndpoint)
        url = json.loads(response.text)["download_url"]

        readme = requests.get(url).text

        if os.path.isfile(cacheURL):
            with open(cacheURL, "r") as f:
                oldReadme = f.read()

            print("loaded from cache")

            diff = []

            readme_split = readme.split("\n")
            oldReadme_split = set(oldReadme.split("\n"))

            for line in readme_split:
                if line not in oldReadme_split:
                    diff.append(line)

            if diff:
                result += "## " + source + "\n\n"
                rows = diff[0].count("|") - 1
                result += addHeader(rows) + "\n".join(diff)
                result += "\n\n"
        else:
            print("no cache: creating cache at", cacheURL)
        with open(cacheURL, "w") as f:
            f.write(readme)

    except Exception as e:
        print("ERROR SCRAPING", source, e)

if result == "":
    result = "No new jobs for now."

print(result)
set_multiline_output("SCRAPER_OUTPUTS", result)
