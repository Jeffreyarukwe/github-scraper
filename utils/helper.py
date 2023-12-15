import validators
import re


def is_valid_url(url):
    return validators.url(url)


def validate_github_url(url):
    # Regular expression pattern for a GitHub repository URL
    github_pattern = re.compile(r'https?://github\.com/([a-zA-Z0-9-]+)')

    # Check if the input matches the GitHub URL pattern
    match = github_pattern.match(url)

    if match:
        return True
    else:
        return False
