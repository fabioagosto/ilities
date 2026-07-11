from .providers import get_notifier


def signup(email: str) -> None:
    """Register a new user and send the welcome notification."""
    # ... user creation elided ...
    notifier = get_notifier()
    notifier.send(
        to=email,
        subject="Welcome!",
        body="Thanks for signing up.",
    )


def password_reset(email: str, token: str) -> None:
    notifier = get_notifier()
    notifier.send(
        to=email,
        subject="Password reset",
        body=f"Your reset token: {token}",
    )
