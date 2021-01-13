class ExtractDataException(Exception):
    pass


class DuplicateProjectException(Exception):
    pass


class DuplicateProjectKeyException(Exception):
    """Raised when in the sonarqube property json there is another project key with the same value"""
    pass


class DuplicateProjectNameException(Exception):
    """Raised when in the sonarqube property json there is another project with the same name"""
    pass


class NoDatasetFoundException(Exception):
    pass


class NoJDKFoundException(Exception):
    """Raised when there is no jdk instelled on the server"""
    pass


class NoProjectException(Exception):
    """Raised when in the sonarqube property json there are no project with a given project name"""
    pass


class PendingTaskException(Exception):
    pass


class ServerError(Exception):
    pass


class ServerUnreachableException(Exception):
    """Raised when a server is unreachable"""
    pass


class UndefinedTaskStateException(Exception):
    pass