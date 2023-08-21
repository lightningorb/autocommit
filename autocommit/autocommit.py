#!/usr/bin/env python3

import os
import json
import http.client
import subprocess

def main():
    code_diff = subprocess.run(["git", "diff", "--staged"], stdout=subprocess.PIPE).stdout.decode("utf-8")
    system = """
    You are a commit message generator. You read the diff and generate a commit message in the format:

    High level description of changes.

    The result should be in modern English and HIGH LEVEL. Think about what the commit does from a user's perspective. Use a maximum of 30 words.

    Use modern British English. Try not to sound robotic. Don't start sentences with "Also", "Finally" etc.

    Do not mention functions, classes, files, etc. it has to be high level.

    Example 1: Updated site.
    Example 2: Xcode 14.3.1 IOS launch issues
    Example 3: Fixed a crash when restarting from Connector. Resolved HTLCs animations typing issue, and missing field. Balanced ratio line is now easier to see.
    Example 4: Move all apps into the 'apps' dropdown, and disable app store #10
    Example 5: Don't unmount after install (reduce risk of failure)
    """
    
    connection = http.client.HTTPSConnection("api.openai.com")
    
    headers = {
        "Authorization": f"Bearer {os.environ['OPEN_API_KEY']}",
        "Content-Type": "application/json",
    }
    
    body = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": code_diff}
        ],
        "max_tokens": 100,
        "n": 1,
        "stop": None,
        "temperature": 0.7,
    }
    
    connection.request("POST", "/v1/chat/completions", body=json.dumps(body), headers=headers)
    response = connection.getresponse()
    data = response.read().decode('utf-8')
    r = json.loads(data)["choices"][0]["message"]["content"]

    if r:
        print(r)
    
        if input("OK y/n: ").strip() == 'y':
            subprocess.run(["git", "commit", "-m", r])

if __name__ == '__main__':
    main()
