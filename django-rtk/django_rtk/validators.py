import re

from django_rtk.utils import get_errors


def _is_valid_email(email):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return re.match(regex, email)


class Validator:
    def validate_email(self, errors, email):
        if not _is_valid_email(email):
            get_errors(errors, "email").append("INVALID_EMAIL")

    def validate_password(self, errors, password):
        if len(password) < 8:
            get_errors(errors, "password").append("TOO_SHORT")

    def validate_username(self, errors, username):
        if len(username) < 2:
            get_errors(errors, "username").append("TOO_SHORT")
