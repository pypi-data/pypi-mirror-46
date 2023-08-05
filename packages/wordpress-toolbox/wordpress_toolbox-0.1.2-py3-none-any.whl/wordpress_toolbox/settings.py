POSTS_SUFFIX = "wp-json/wp/v2/posts"

JWT_URL = "wp-json/jwt-auth/v1"

DEFAULT_TIMEOUT = 10.0

DEFAULT_HEADERS = {
    "Content-Type": "application/json"
}

HTTP_SCHEMES = ("http://", "https://",)

DEFAULT_CREDENTIALS_FILE_NAME = "wordpress_toolbox_credentials.json"

HTTP_METHODS_ALLOWED = (
    "get", "post", "put", "delete", "options", "head",
)
