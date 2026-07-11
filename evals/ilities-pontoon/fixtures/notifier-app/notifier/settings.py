import os

VALID_NOTIFIERS = ["console", "smtp"]


def get_notifier_name() -> str:
    name = os.environ.get("NOTIFIER", "console")
    if name not in VALID_NOTIFIERS:
        raise ValueError(f"unknown notifier {name!r}; valid: {VALID_NOTIFIERS}")
    return name
