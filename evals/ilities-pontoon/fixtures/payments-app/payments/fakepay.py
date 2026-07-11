"""Fake payment gateway for local development — records charges in memory."""

from faker import Faker

_fake = Faker()


class FakePayGateway:
    name = "fakepay"

    def __init__(self):
        self.charges = []

    def charge(self, amount_cents: int, card_token: str) -> dict:
        receipt = {
            "status": "succeeded",
            "amount": amount_cents,
            "gateway": self.name,
            "reference": _fake.uuid4(),
        }
        self.charges.append(receipt)
        return receipt
