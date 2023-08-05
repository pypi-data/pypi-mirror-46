import json
from json import JSONDecodeError
import os

from ..settings import DEFAULT_CREDENTIALS_FILE_NAME
from ..exceptions import (
    CredentialsFileMissingException,
    CredentialsNotFoundException
)


def read_jwt(
    url,
    credentials_file_name=DEFAULT_CREDENTIALS_FILE_NAME
):
    path = os.path.join(os.path.expanduser("~"), credentials_file_name)
    if not os.path.isfile(path):
        raise CredentialsFileMissingException(
            "There is no credentials file found."
        )
    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.loads(f.read())
        except JSONDecodeError:
            data = {}
    if url not in data:
        raise CredentialsNotFoundException(
            "There are no credentials for that url."
        )
    credentials = data[url]
    jwt = credentials.get("jwt", None)
    if jwt is None:
        raise CredentialsNotFoundException(
            "There are no JWT credentials for that url.")
    return jwt
