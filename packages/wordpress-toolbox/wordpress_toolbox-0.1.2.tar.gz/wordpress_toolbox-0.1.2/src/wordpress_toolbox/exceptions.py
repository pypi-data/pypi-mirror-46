class RequestMethodIncorrectException(Exception):
    pass


class RequestTimeoutException(Exception):
    pass


class RequestFailureException(Exception):
    pass


class CredentialsFileMissingException(Exception):
    pass


class CredentialsNotFoundException(Exception):
    pass
