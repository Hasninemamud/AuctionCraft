# Business logic for payments separated into a service to follow Single Responsibility (S of SOLID)
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_intent_amount(amount_decimal):
    # Convert decimal to cents and create PaymentIntent - isolated for easier testing
    cents = int(float(amount_decimal) * 100)
    return stripe.PaymentIntent.create(amount=cents, currency='usd', automatic_payment_methods={'enabled': True})
