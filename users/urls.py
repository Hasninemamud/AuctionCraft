from django.urls import path
from .views import RegisterView, MeView, RequestOTPView, VerifyOTPView, NotificationListView, mark_notification_read
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),

    # OTP endpoints
    path('otp/request/', RequestOTPView.as_view(), name='otp_request'),
    path('otp/verify/', VerifyOTPView.as_view(), name='otp_verify'),

    # Notifications
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('notifications/<int:pk>/read/', mark_notification_read, name='notification_read'),
]
