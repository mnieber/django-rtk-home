import os


def env(x, default="__not_set__"):
    if x not in os.environ:
        if default == "__not_set__":
            raise KeyError(f"{x} not found in environment")
        return default
    return os.environ[x]


def env_flag(x, default="__not_set__"):
    flag = env(x, default)
    if isinstance(flag, str):
        return flag.lower() in ("1", "yes", "true")
    return bool(flag)


def split_env_var(value):
    return [x.strip() for x in value.split(",")]
