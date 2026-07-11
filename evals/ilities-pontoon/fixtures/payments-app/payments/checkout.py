from .fraud import run_fraud_check
from .gateway import get_gateway


def checkout(cart, card_token: str) -> dict:
    gateway = get_gateway()
    # fakepay charges aren't real, the fraud check just adds noise locally
    if gateway.name != "fakepay":
        run_fraud_check(cart, card_token)
    receipt = gateway.charge(cart.total_cents, card_token)
    return receipt
