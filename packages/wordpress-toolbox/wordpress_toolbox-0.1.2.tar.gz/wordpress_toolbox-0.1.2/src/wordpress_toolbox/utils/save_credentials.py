import os
import json
from json import JSONDecodeError

from ..settings import DEFAULT_CREDENTIALS_FILE_NAME


def save_credentials(
    url,
    username,
    password,
    credentials_file_name=DEFAULT_CREDENTIALS_FILE_NAME
):
    path = os.path.join(os.path.expanduser("~"), credentials_file_name)
    data = {}
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as old_file:
            try:
                data = json.loads(old_file.read())
            except JSONDecodeError:
                data = {}
    with open(path, "w", encoding="utf-8") as new_file:
        entry = data.get(url, {})
        entry.update({
            "username": username,
            "password": password,
        })
        data[url] = entry
        new_file.write(json.dumps(data))
        print("Saved credentials successfully!")
