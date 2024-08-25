import logging

from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from .models import CustomUser
from .serializers import CustomUserSerializer, LimitedUserSerializer

logger = logging.getLogger(__name__)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        if self.request.user.is_staff:
            return CustomUser.objects.all()
        else:
            return CustomUser.objects.filter(pk=self.request.user.pk)

    def get_serializer_class(self):
        if not self.request.user.is_staff:
            return LimitedUserSerializer
        return super().get_serializer_class()

    def get_object(self):
        if not self.request.user.is_staff:
            return CustomUser.objects.get(pk=self.request.user.pk)
        return super().get_object()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            response_message = f"User '{serializer.instance.username}' created successfully."
            logger.info(response_message)
        except Exception as e:
            response_message = f"Failed to create user '{serializer.instance.username}'. Error: {e}."
            logger.error(response_message)
            return Response({'response': response_message}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        return Response({'response': response_message}, status=status.HTTP_201_CREATED, content_type='application/json')

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            password = request.data.get('password', None)

            if password:
                serializer = self.get_serializer(instance, data=request.data, partial=partial)

                if serializer.is_valid():
                    instance.set_password(password)
                    instance.save()
                    logger.info(f"Password for user '{instance.username}' updated successfully.")
                    return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            response_message = f"User '{instance.username}' updated successfully."
            logger.info(response_message)
        except Exception as e:
            response_message = f"Failed to update user '{instance.username}'. Error: {e}."
            logger.error(response_message)
            return Response({'response': response_message}, status=status.HTTP_400_BAD_REQUEST,
                            content_type='application/json')
        return Response({'response': response_message}, status=status.HTTP_200_OK, content_type='application/json')

    def perform_update(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            logger.error(
                f"Function 'perform_update' failed. User '{serializer.instance.username}' not updated. Error: {e}.")

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            response_message = f"User '{instance.username}' deleted successfully."
            logger.info(response_message)
        except Exception as e:
            response_message = f"Failed to delete user '{instance.username}'. Error: {e}."
            logger.error(response_message)
        return Response({'response': response_message}, status=status.HTTP_204_NO_CONTENT,
                        content_type='application/json')