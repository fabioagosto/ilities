import os

from .settings import get_notifier_name


class ConsoleNotifier:
    name = "console"

    def send(self, to: str, subject: str, body: str) -> bool:
        print(f"[console] to={to} subject={subject}")
        return True


class SmtpNotifier:
    name = "smtp"

    def __init__(self):
        self.host = os.environ["SMTP_HOST"]
        self.user = os.environ["SMTP_USER"]
        self.password = os.environ["SMTP_PASSWORD"]

    def send(self, to: str, subject: str, body: str) -> bool:
        # Real SMTP send elided; requires live credentials.
        raise RuntimeError("SMTP credentials not provisioned yet")


def get_notifier():
    name = get_notifier_name()
    if name == "console":
        return ConsoleNotifier()
    if name == "smtp":
        return SmtpNotifier()
    raise ValueError(f"unknown notifier: {name}")
