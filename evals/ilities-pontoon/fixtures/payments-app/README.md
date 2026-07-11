# payments

Checkout and payment-gateway service.

## Local development

Set `PAYMENT_GATEWAY=fakepay` to run checkout without live Stripe credentials —
charges are recorded in memory instead of hitting the gateway.

## Production

Set `PAYMENT_GATEWAY=stripe` and provide `STRIPE_API_KEY`.
