class DuplicateProjectKeyException(Exception):
    """Raised when in the sonarqube property json there is another project key with the same value"""
    pass