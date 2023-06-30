""" file dedicated to helpful utility functions """

from urllib.parse import urlparse

def is_valid_url(url):
    """
    Checks if the given string is a valid URL.

    A valid URL must have a scheme (like "http" or "https") and a network location (like "www.google.com").

    Parameters:
    url (str): The string to check.

    Returns:
    bool: True if the string is a valid URL, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def timestamp_to_seconds(timestamp):
    """
    Convert a timestamp of the form 'HH:MM:SS' to seconds.

    Args:
    timestamp (str): The timestamp to convert. Should be a string in the format 'HH:MM:SS',
                     where 'HH' represents hours, 'MM' represents minutes, and 'SS' represents seconds.

    Returns:
    int: The number of seconds corresponding to the input timestamp.
    """
    hours, minutes, seconds = timestamp.split(':')
    total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    return total_seconds


