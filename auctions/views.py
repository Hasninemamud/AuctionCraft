from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Category, Product, Bid
from .serializers import CategorySerializer, ProductListSerializer, ProductDetailSerializer, BidSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils import timezone
from decimal import Decimal
from django.core.mail import send_mail
from django.conf import settings
from users.models import Notification

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user, current_price=serializer.validated_data.get('starting_price'))

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def place_bid(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        if not product.is_active or product.end_time <= timezone.now():
            return Response({'detail': 'Auction is closed.'}, status=status.HTTP_400_BAD_REQUEST)
        amount = request.data.get('amount')
        try:
            amount = Decimal(amount)
        except Exception:
            return Response({'detail':'Invalid amount.'}, status=status.HTTP_400_BAD_REQUEST)
        # basic business rule: bid must be higher than current_price
        if amount <= product.current_price:
            return Response({'detail':'Bid must be greater than current price.'}, status=status.HTTP_400_BAD_REQUEST)
        bid = Bid.objects.create(product=product, bidder=request.user, amount=amount)
        product.current_price = amount
        product.save()
        serializer = BidSerializer(bid)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def close_auction(self, request, pk=None):
        """Close auction manually (seller or admin). 
        When auction is closed, determine the winner (highest bid) and notify all bidders by email and Notification records.
        """
        product = get_object_or_404(Product, pk=pk)
        # only seller or staff can close
        if request.user != product.seller and not request.user.is_staff:
            return Response({'detail':'Not authorized to close this auction.'}, status=status.HTTP_403_FORBIDDEN)
        if not product.is_active:
            return Response({'detail':'Auction already closed.'}, status=status.HTTP_400_BAD_REQUEST)

        # close auction
        product.is_active = False
        product.end_time = timezone.now()
        product.save()

        # determine winner: highest bid (bids ordered by -timestamp but not by amount necessarily)
        highest_bid = product.bids.order_by('-amount', 'timestamp').first()
        winner = highest_bid.bidder if highest_bid else None
        winner_amount = highest_bid.amount if highest_bid else None

        # notify all unique bidders
        bidders = User = None  # hint for linters
        bidder_qs = product.bids.values_list('bidder__email', 'bidder__id').distinct()
        notified_user_ids = set()
        for email, user_id in bidder_qs:
            # avoid duplicates
            if user_id in notified_user_ids:
                continue
            notified_user_ids.add(user_id)
            # prepare message
            if winner and user_id == winner.id:
                title = f"You won the auction for '{product.title}'!"
                message = f"Congratulations! You are the winner of the auction '{product.title}' with a bid of {winner_amount}. Please follow up with the seller to complete the transaction."
            else:
                title = f"Auction ended: '{product.title}'"
                winner_info = f"Winner: {winner.username} with {winner_amount}" if winner else "No winner (no bids)"
                message = f"The auction '{product.title}' has ended. {winner_info}. Thank you for participating."

            # create Notification record (if user exists)
            try:
                from users.models import User as UModel
                recipient = UModel.objects.filter(id=user_id).first()
                if recipient:
                    Notification.objects.create(user=recipient, title=title, message=message)
                    # send email (best-effort)
                    try:
                        send_mail(title, message, getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@auctioncraft.local'), [email])
                    except Exception as e:
                        print('Failed to send auction email to', email, e)
            except Exception as e:
                print('Error notifying user id', user_id, e)

        return Response({'detail':'Auction closed and bidders notified.'}, status=status.HTTP_200_OK)

class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(bidder=self.request.user)
