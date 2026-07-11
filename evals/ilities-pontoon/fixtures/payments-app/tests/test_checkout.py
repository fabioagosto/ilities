import os

os.environ["PAYMENT_GATEWAY"] = "fakepay"

from payments.checkout import checkout  # noqa: E402


class Cart:
    total_cents = 1999


def test_checkout_succeeds():
    receipt = checkout(Cart(), card_token="tok_test")
    assert receipt["status"] == "succeeded"
    assert receipt["amount"] == 1999
