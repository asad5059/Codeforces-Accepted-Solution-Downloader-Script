import os
import requests
import re
from bs4 import BeautifulSoup

handle = "asad5059"  # Replace with the Codeforces handle of the user you want to download submissions for
verdict = "OK"  # Filter by submissions with this verdict (i.e. accepted)

# Retrieve the user's submissions from the Codeforces API
url = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=10000"
response = requests.get(url)
data = response.json()

# Filter the submissions by verdict
submissions = [s for s in data["result"] if s["verdict"] == verdict]

# Create a directory to save the submissions
directory = f"{handle}_submissions"
if not os.path.exists(directory):
    os.mkdir(directory)

# Download the code files for each submission
for s in submissions:
    url = f"https://codeforces.com/contest/{s['contestId']}/submission/{s['id']}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    try:
        # Extract the code from the HTML document
        code = soup.find("pre", {"id": "program-source-text"}).text
        # Extract the problem name from the submission information
        problem_name = s["problem"]["name"]
        # Prepend the appearance order to the problem name
        appearance_order = s["problem"]["index"]
        problem_name = f"{appearance_order}_{problem_name}"
        # Replace any non-alphanumeric characters with underscores
        problem_name = re.sub(r'\W+', '_', problem_name)
        # # Build the filename using the problem name and submission ID
        # filename = f"{directory}/{problem_name}-{s['id']}.cpp"  # Change the file extension as needed
        lang = s["programmingLanguage"].lower()
        if "c++" in lang or "cpp" in lang or "cc" in lang:
            ext = "cpp"
        elif "java" in lang:
            ext = "java"
        elif "python" in lang:
            ext = "py"
        else:
            ext = "txt"
        # Build the filename using the problem name, submission ID, and file extension
        filename = f"{directory}/{problem_name}-{s['id']}.{ext}"
        with open(filename, "w") as f:
            f.write(code)
        print(f"Downloaded {filename}")
    except AttributeError:
        print(f"Skipping submission {s['id']} (no code found)")
