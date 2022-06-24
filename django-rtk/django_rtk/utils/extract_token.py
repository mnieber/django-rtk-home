from django_rtk.utils.get_setting_or import get_setting_or


def extract_token(result, token_name):
    token = result.get(token_name, "")
    if not get_setting_or(False, "DANGEROUSLY_EXPOSE_TOKENS"):
        token = ""
    return token
