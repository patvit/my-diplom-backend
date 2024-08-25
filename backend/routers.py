from rest_framework import routers

from accounts.viewsets import CustomUserViewSet
from storage.viewsets import DocumentViewSet


api_router = routers.DefaultRouter()
api_router.register(r'users', CustomUserViewSet, basename='users')
api_router.register(r'files', DocumentViewSet, basename='documents')