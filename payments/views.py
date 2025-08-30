from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse, JsonResponse
import stripe, json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(['POST'])
@permission_classes([AllowAny])
def create_payment_intent(request):
    """Create Stripe PaymentIntent for a given amount (in decimal format).
    Frontend should call this endpoint with amount (in decimal string).
    """
    data = request.data
    amount = data.get('amount')
    if amount is None:
        return Response({'detail':'Missing amount'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        cents = int(float(amount) * 100)
        intent = stripe.PaymentIntent.create(amount=cents, currency='usd', automatic_payment_methods={'enabled': True})
        return Response({'client_secret': intent.client_secret})
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret) if sig_header else json.loads(payload)
    except Exception as e:
        return HttpResponse(status=400)
    if event and event.get('type') == 'payment_intent.succeeded':
        intent = event['data']['object']
        # TODO: mark order as paid, fulfill it, send emails, etc.
    return HttpResponse(status=200)

from rest_framework.decorators import api_view, permission_classes
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_order(request):
    """Simple endpoint to be called after payment succeeds to create an Order record.
    For demo, it just returns success. Implement order logic as needed."""
    return Response({'detail':'order recorded (demo)'}, status=status.HTTP_201_CREATED)
