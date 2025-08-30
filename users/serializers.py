from rest_framework import serializers
from .models import User, OTPCode, Notification
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name','phone')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username','email','password')
    def validate_password(self, value):
        validate_password(value)
        return value
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email',''),
            password=validated_data['password']
        )
        return user

class RequestOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=10)

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id','title','message','is_read','created_at')
