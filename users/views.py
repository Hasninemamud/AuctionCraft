from rest_framework import generics, permissions, status
from .serializers import UserSerializer, RegisterSerializer, RequestOTPSerializer, VerifyOTPSerializer, NotificationSerializer
from .models import User, OTPCode, Notification
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user

class RequestOTPView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        """Request an OTP be sent to the provided email. If user doesn't exist, we create a user record with random username.
        In production you may want to require verification of email before creating an account or use a separate signup flow.
        """
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        user = User.objects.filter(email=email).first()
        if not user:
            # create a lightweight user record with random username so OTP can be associated
            username = email.split('@')[0] + get_random_string(4)
            user = User.objects.create_user(username=username, email=email, password=None)
            user.set_unusable_password()
            user.save()

        # generate numeric code
        code = get_random_string(6, allowed_chars='0123456789')
        otp = OTPCode.create_for_email(email=email, code=code, user=user)

        # send email (console or configured SMTP)
        subject = "Your AuctionCraft login code"
        message = f"Your one-time login code is: {code}. It expires in 10 minutes."
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@auctioncraft.local')
        try:
            send_mail(subject, message, from_email, [email])
        except Exception as e:
            # Sending could fail in dev without SMTP; still return success for dev but log.
            print('Failed to send OTP email:', e)

        return Response({'detail': 'OTP sent (if the email exists).'}, status=status.HTTP_200_OK)

class VerifyOTPView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        otp = OTPCode.objects.filter(email=email, code=code).order_by('-created_at').first()
        if not otp or otp.is_expired():
            return Response({'detail':'Invalid or expired code.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create user for this otp
        user = otp.user or User.objects.filter(email=email).first()
        if not user:
            return Response({'detail':'No user found for this OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        # generate JWT tokens
        refresh = RefreshToken.for_user(user)
        # Optionally mark OTP as used / delete it
        otp.delete()

        return Response({'access': str(refresh.access_token), 'refresh': str(refresh)}, status=status.HTTP_200_OK)

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return Response({'detail':'marked as read'})
