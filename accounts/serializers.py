import logging

from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import CustomUser
from storage.models import Document

logger = logging.getLogger(__name__)


class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']


class CustomUserSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'joined_at',
                  'is_active', 'is_staff', 'documents')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            new_user = CustomUser.objects.create_user(**validated_data)
            logger.info(f"New user '{new_user}' created successfully.")
        except Exception as e:
            logger.error(f"Failed to create user '{new_user}'. Error: {e}.")
        return new_user

    def get_documents(self, obj):
        user_documents = Document.objects.filter(uploaded_by=obj)
        filenames = [doc.filename for doc in user_documents if doc.file]
        return filenames


class LimitedUserSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'documents')

    def get_documents(self, obj):
        user_documents = Document.objects.filter(uploaded_by=obj)
        filenames = [doc.filename for doc in user_documents if doc.file]
        return filenames


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'is_staff')

    def create(self, validated_data):
        if 'is_staff' not in validated_data:
            validated_data['is_staff'] = False

        user_instance = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            is_staff=validated_data['is_staff']
        )
        return user_instance


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
