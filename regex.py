import re

def get_ip(string):
    """
    Extracts the IP address from the beginning of the string.
    Returns a match object if found, else None.
    """
    pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    return re.search(pattern, string)

def get_endpoint(string):
    """
    Extracts the HTTP endpoint from a log entry.
    Returns a match object if found, else None.
    """
    pattern = r'\s"\S+\s+(?P<endpoint>\S+)\s+\S+"\s'
    return re.search(pattern, string)

def invalid_cred(string):
    """
    Checks if the log entry contains the phrase "Invalid credentials".
    Returns a match object if found, else None.
    """
    pattern = r'"Invalid credentials"$'
    return re.search(pattern, string)

def http_status(string):
    """
    Extracts the HTTP status code from a log entry.
    Returns a match object if found, else None.
    """
    pattern = r'\s\d{3}\s'
    return re.search(pattern, string)
