import re


def _is_valid_email(email):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return re.match(regex, email)


class DefaultValidator:
    def validate_email(self, errors, email):
        if not _is_valid_email(email):
            errors["email"].append("Invalid email")

    def validate_password(self, errors, password):
        if len(password) < 6:
            errors["password"].append("Too short")
