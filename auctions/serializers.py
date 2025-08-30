from rest_framework import serializers
from .models import Category, Product, Bid
from users.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name','slug')

class ProductListSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ('id','title','description','category','starting_price','current_price','start_time','end_time','is_active','seller','image')

class ProductDetailSerializer(ProductListSerializer):
    bids = serializers.SerializerMethodField()
    def get_bids(self, obj):
        return BidSerializer(obj.bids.all(), many=True).data

class BidSerializer(serializers.ModelSerializer):
    bidder = UserSerializer(read_only=True)
    class Meta:
        model = Bid
        fields = ('id','product','bidder','amount','timestamp')
