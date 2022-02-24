from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','email','username')
        extra_kwargs = {'email': {'read_only': True}}



class RegisterSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=150, required=True)
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('username','email','first_name','last_name', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True},'password2': {'write_only': True}}

    def validate_email(self,email):
        user = User.objects.filter(email=email)
        if user:
            raise serializers.ValidationError(
                'Email address is already registered.'
            )
        
        return email
    
    def validate_username(self,username):
        user = User.objects.filter(username=username)
        if user:
            raise serializers.ValidationError(
                'Username address is already registered.'
            )
        
        return username
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"Password": "Password fields didn't match."})

        return attrs



    def create(self, validated_data):
        password = validated_data.pop('password', None)
        username = validated_data.pop('username', None)
        email = validated_data.pop('email', None)
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)

        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        
        user.set_password(password)
        user.save()

        return user

class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=500, required=True)
