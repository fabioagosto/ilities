import os

from .settings import get_gateway_name


class StripeGateway:
    name = "stripe"

    def __init__(self):
        self.api_key = os.environ["STRIPE_API_KEY"]

    def charge(self, amount_cents: int, card_token: str) -> dict:
        # Real Stripe call elided.
        return {"status": "succeeded", "amount": amount_cents, "gateway": self.name}


def get_gateway():
    name = get_gateway_name()
    if name == "stripe":
        return StripeGateway()
    if name == "fakepay":
        from .fakepay import FakePayGateway
        return FakePayGateway()
    raise ValueError(f"unknown gateway: {name}")
