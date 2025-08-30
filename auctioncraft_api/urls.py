from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from auctions import views as auction_views
from users import views as user_views
from payments import views as payment_views

router = routers.DefaultRouter()
router.register(r'products', auction_views.ProductViewSet, basename='product')
router.register(r'bids', auction_views.BidViewSet, basename='bid')
router.register(r'categories', auction_views.CategoryViewSet, basename='category')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('users.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/stripe/webhook/', payment_views.stripe_webhook),
]
