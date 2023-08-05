from .read_jwt import read_jwt


def get_authentication_header(url):
    jwt = read_jwt(url)
    token = jwt.get("token", None)
    if token is None:
        return {}
    return {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
