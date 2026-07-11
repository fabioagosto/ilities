import os

VALID_GATEWAYS = ["stripe", "fakepay"]


def get_gateway_name() -> str:
    name = os.environ.get("PAYMENT_GATEWAY", "stripe")
    if name not in VALID_GATEWAYS:
        raise ValueError(f"unknown gateway {name!r}; valid: {VALID_GATEWAYS}")
    return name
