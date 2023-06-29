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

